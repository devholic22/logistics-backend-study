# 외부 WMS 연동 도식

본문에서는 SVG를 표시하고, HTML은 다운로드 후 브라우저에서 열어 탐색할 수 있다. JSON은 archify 재생성 원본이다. 본문·노드는 한글이며 뷰어의 고정 UI는 영어로 표시된다.

| 원본 | 유형 | 설명 |
| --- | --- | --- |
| `01-http-connection-boundaries.json` | architecture | 내부 요청 경로와 외부 요청 경로 |
| `02-alb-timeout-propagation.json` | sequence | ALB idle 종료 이후에도 외부 작업이 남는 상황 |
| `03-sync-async-structure.json` | architecture | 접수 응답과 Worker 실행의 분리 |

```bash
node "$ARCHIFY_ROOT/bin/archify.mjs" validate architecture 01-http-connection-boundaries.json --quality showcase --json
node "$ARCHIFY_ROOT/bin/archify.mjs" deliver architecture 01-http-connection-boundaries.json 01-http-connection-boundaries.html --quality showcase --json
```

다른 파일에도 대응하는 유형으로 같은 명령을 적용한다. SVG는 검증된 HTML의 SVG 및 관련 스타일을 추출하고 light 테마 색상을 고정한 정적 미리보기다. HTML의 탐색 메뉴와 하단 설명 카드는 SVG에 포함되지 않는다.

세 HTML 모두 showcase 9개 항목 통과, 오류 0건·경고 0건이다. SHA-256 및 상세 결과는 `validation-receipts.json`에 기록했다. 브라우저 부재로 HTML 화면·인터랙션 검증은 수행하지 못했으며, SVG는 한글 폰트로 실제 렌더링하여 시각 확인했다.

## 4장 나머지 도식 전환

기존 실무 사례 3개에 이어 Mermaid 9개를 workflow 7개·sequence 2개로 전환했습니다. 상태 도식은 자동으로 추가되는 전이 없이 모든 조건을 명시하기 위해 workflow로 표현했습니다. 설명은 한국어이며 고정 Viewer UI와 HTML lang은 영어입니다.

| 원본 | 유형 | 내용 |
| --- | --- | --- |
| `04-thread-saturation.json` | sequence | 느린 외부 호출이 요청 thread를 포화시키는 과정 |
| `05-http-call-stages.json` | workflow | HTTP 호출 단계와 Timeout 경계 |
| `06-payment-unknown.json` | workflow | 결제 결과 불명 상태와 최종 확인 |
| `07-retry-budget.json` | workflow | Backoff·jitter와 재시도 예산 |
| `08-dependency-bulkheads.json` | workflow | Dependency별 Bulkhead 격리 |
| `09-circuit-breaker-states.json` | workflow | Circuit Breaker의 차단과 복구 |
| `10-db-transaction-boundary.json` | workflow | 외부 호출과 DB Transaction 경계 |
| `11-socket-idle-vs-deadline.json` | sequence | Socket 무응답 제한과 전체 호출 시간 |
| `12-dependency-failure-propagation.json` | workflow | 외부 장애가 사용자 응답으로 전파되는 경로 |

새 도식의 검증 기록은 [chapter-04-validation.json](./chapter-04-validation.json)에 보관합니다. SVG는 검증된 HTML에서 밝은 테마의 계산된 스타일을 포함해 내보냈습니다. 화살표에 별도 문구가 없는 단계는 양 끝 노드에 적힌 처리 순서를 뜻합니다. 기존 3개의 검증 범위는 위 기록을 따릅니다.
