# 실무 런북: Webhook 트래픽 급증과 ALB 504 진단

> [외부 연동이 문제일 때 살펴봐야 할 것들](./README.md) · [외부 연동 관측](./9-외부-연동-관측과-점검.md)

> [!NOTE]
> 이 문서는 외부 시스템 → 수신 API → 내부 이벤트 발행 구조를 가정한 **일반화된 장애 대응 예시**다. 특정 운영 사고의 원인이나 조치 결과를 확정한 사후 분석이 아니다. 메트릭 이름·경보 임계값·실제 설정은 환경별로 검증해야 한다.

## 장애를 정의하고 가설을 분리하기

예시 경로: 외부 WMS → 공개 Webhook API → 내부 서비스 → SQS 또는 EventBridge 발행 → HTTP 응답.

Webhook이 집중되는 순간 ALB에서 504가 발생했다는 사실만으로 **Node.js 이벤트 루프 지연** 또는 **ECS task 부족**을 원인으로 단정할 수 없다. ALB가 target에 연결하지 못한 경우, target이 제한 시간 내 응답하지 못한 경우, 네트워크 오류 등이 서로 다른 증거를 남긴다. 외부 공급자의 타임아웃, ALB의 타임아웃, 애플리케이션의 전체 deadline도 구분한다.

| 관측 | 우선 의심할 층 | 확인할 증거 | 단독으로는 결론낼 수 없는 것 |
| --- | --- | --- | --- |
| ALB 504 증가, target 연결 오류도 증가 | target 연결·가용성 | ALB access log의 error reason/시간 필드, target health, 배포·task 종료, SG/NACL, 포트 리스닝 | DB 또는 이벤트 루프가 직접 원인이라는 결론 |
| 연결은 됐지만 응답 지연 | 앱 처리·downstream | target 처리 시간, APM trace, 큐 전송·외부 API span | CPU 부족이라는 결론 |
| event loop delay가 증가 | Node.js 스케줄링 지연 | p95/p99 event loop delay, event loop utilization, CPU, 동기 작업·GC | 지연과 장애의 인과 관계 |
| CPU가 낮고 진행 중 요청·소켓 대기가 증가 | I/O 대기·리소스 포화 | socket/connection pool, SDK retry, network, downstream latency | task 수 증가만으로 해결된다는 결론 |
| 5xx와 retry 트래픽이 함께 증가 | retry 증폭 | 원 요청 수와 attempt 수, 중복 event ID, 공급자 재시도 정책 | 원 요청 자체가 급증했다는 결론 |
| ECS task 재시작 또는 unhealthy 시점과 일치 | 배포·헬스체크·용량 | ECS events, target 등록·해제, health-check reason, graceful shutdown | 재시작이 최초 원인이라는 결론 |

**진단 원칙:** 같은 시간대의 ALB access log, target health/ECS event, 애플리케이션 trace, 런타임 지표, downstream 지표를 함께 정렬한다. ALB의 HTTP 코드만으로 호출 체인에서 어디까지 요청이 도달했는지 알 수 없다.

## 사고 당시 10분 대응 순서

1. **영향 확인:** 504 건수·영향 라우트·발생 구간·성공률·요청 유입량을 기록한다. 504 외에 502·503 및 클라이언트 타임아웃도 함께 본다.
2. **요청이 target까지 도달했는지 구분:** ALB access log의 target 관련 시간과 상태, target health, 연결 오류를 검토한다. target 측 trace가 없다면 로그 샘플링·수집 손실 가능성도 확인한다.
3. **시간축을 정렬:** ECS 배포/scale event, target 등록·해제, Node.js event loop delay, CPU·메모리, downstream API/SQS/EventBridge 요청 지연을 동일 시간대에 배치한다.
4. **증폭 여부 확인:** 공급자의 webhook 재전송 건수와 내부 retry attempt를 원본 event ID 단위로 비교한다. 중복 수신을 곧바로 비즈니스 이벤트 중복 처리로 연결하지 않는다.
5. **피해 제한:** 원인이 밝혀지지 않은 상태에서 무제한 retry, 큐 크기 확대, 무조건적인 timeout 연장은 피한다. 안전하게 적용 가능한 동시성 상한·backpressure·운영 절차를 우선 검토한다.
6. **복구 검증:** 5xx와 p99가 정상화됐는지뿐 아니라 누락/중복 webhook, DLQ, 처리 지연, 재처리 대기 물량을 확인한다.

## 계층별 계측 계약

| 계층 | 최소 계측 항목 | 주의 |
| --- | --- | --- |
| ALB | request/target status, 요청 시간, target 처리 시간, target 연결 오류, target health | 집계 metric과 요청별 access log를 구분한다. 필드 가용성은 ALB 로그 형식에 따른다 |
| ECS | task 수, running/pending, CPU·메모리, 배포·stop reason | 서비스 평균은 hot task 또는 짧은 spike를 가릴 수 있다 |
| Node.js | event loop delay p95/p99, event loop utilization, heap/GC, in-flight request, socket 수 | 성능 계측 자체의 overhead와 aggregation window를 관리한다 |
| 다운스트림 | publish 지연·오류·throttle, SDK retry, pool 대기 | 단순 publish 요청 성공과 최종 비즈니스 처리 성공은 다르다 |
| 이벤트 처리 | event ID별 최초 수신·중복·enqueue·소비·실패·DLQ | 민감 정보 payload 전체를 로그에 남기지 않는다 |

### 타임아웃 관계 검토

다음은 숫자를 정하는 공식이 아니라 **검증해야 할 관계**다.

- 공급자가 응답을 기다리는 상한 안에서 우리 요청이 끝나야 하는지 계약을 확인한다.
- 애플리케이션의 다운스트림 호출 시간 + 예상 큐잉 + 응답 작성 시간을 요청 deadline 안에 배치한다.
- ALB idle timeout이 앱의 요청 중단을 보장하는 것은 아니다. 앱 내부 deadline과 취소/정리 정책을 별도로 둔다.
- 실패 응답/응답 유실 후 공급자가 같은 이벤트를 다시 전송할 수 있으므로, 전송의 적어도 한 번(at-least-once) 특성을 가정하고 멱등성 설계를 검토한다.

## 개선안의 가설과 반증 지표

| 제안 | 기대하는 효과 | 먼저 확인할 조건 | 반증 신호 |
| --- | --- | --- | --- |
| ECS task 증설 | task당 동시 요청 감소 | 실제 target 용량 포화, 분산 균형, downstream 여유 | 연결 오류·downstream throttle이 그대로이거나 증가 |
| Node.js 동기 작업 제거 | event loop 대기 감소 | 지연 구간에 동기 CPU·직렬화·GC spike 존재 | event loop delay 변화 없이 504 지속 |
| 이벤트 발행 비동기화/응답 경계 재설계 | webhook 응답시간 감소 | 수신 확인의 의미, 내구성 있는 저장 또는 큐잉 보장 | 응답은 성공하지만 이벤트가 유실 |
| 제한된 retry + jitter | 일시 실패 복구 | 멱등성, 전체 deadline, 공급자 quota | attempt 증가와 함께 원 요청 성공률 악화 |
| concurrency 상한/backpressure | 연쇄 포화 방지 | 의도한 초과 요청 처리 방식, 재전송·DLQ 운영 | 거절·유실이 증가하고 복구가 불가능 |

## 실험으로 원인 확인하기

운영 계정에 바로 장애를 주입하지 말고 격리된 환경에서 다음 경우를 재현한다.

- **연결 실패:** target 연결 불가 또는 등록/해제 전환 시 ALB 로그와 앱 trace가 어떻게 다른가?
- **응답 지연:** downstream publish를 지연시켜 target latency·event loop delay·in-flight 추이를 비교한다.
- **동기 블로킹:** CPU 동기 작업을 인위적으로 늘려 event loop delay와 timeout의 상관관계를 관측한다.
- **재시도 폭증:** 동일 event ID를 반복 전송하여 재시도·멱등성·중복 집계·DLQ를 검증한다.
- **장애 이후 복구:** downstream이 정상화된 뒤 백로그 처리, 누락 대사, 중복 반영 방지가 완료되는가?

각 실험에는 요청량, duration, timeout, retry 설정, 성공률, p95/p99, 누락·중복 개수를 함께 기록한다. 단일 메트릭 개선을 복구 완료로 간주하지 않는다.

## 종료 기준과 사후 분석 템플릿

- [ ] 실패율과 tail latency가 정상 범위로 복귀했다.
- [ ] target health·ECS·런타임·downstream 지표가 일관되게 회복됐다.
- [ ] 수신한 event ID와 최종 처리 기록을 대사하여 누락·중복 영향을 확인했다.
- [ ] 임시 제한/설정 변경에 담당자·만료일·되돌리기 조건이 있다.
- [ ] 관측 증거와 남아 있는 **미확정 가설**을 구분해 기록했다.

| 항목 | 기록할 내용 |
| --- | --- |
| 타임라인 | 최초 신호 → 영향 확대 → 완화 → 복구 확인 (시간대 명시) |
| 영향 | 사용자 과업, 실패 요청/이벤트 수, 처리 지연, 비즈니스 결과 |
| 증거 | ALB 로그·ECS event·APM·Node 메트릭·downstream metric의 링크 |
| 확정 원인 / 가설 | 재현 또는 충분한 증거로 뒷받침된 사실과 미검증 추정을 분리 |
| 완화 / 재발 방지 | 즉시 조치, 구조 개선, 경보, 실험, 담당자, 검증 일정 |

## 함께 읽기

- [Timeout](./1-timeout.md) — 계층별 timeout과 전체 deadline
- [Retry](./2-retry.md) — retry 증폭과 backoff
- [Rate limit과 동시 요청 제한](./3-rate-limit과-동시-요청-제한.md) — backpressure와 bulkhead
- [외부 연동 관측](./9-외부-연동-관측과-점검.md) — 장기 운영 계측 목록
- [실무 사례: 동기 외부 API와 계층별 Timeout](./10-실무-사례-동기-외부-api와-계층별-timeout.md) — timeout 조합 예시

## 참고 자료

- [AWS Application Load Balancer troubleshooting](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-troubleshooting.html)
- [AWS ALB access log entries](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html)
- [AWS ECS service events](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-event-messages.html)
- [Node.js perf_hooks](https://nodejs.org/api/perf_hooks.html)
- [AWS Builders' Library: Timeouts, retries and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
