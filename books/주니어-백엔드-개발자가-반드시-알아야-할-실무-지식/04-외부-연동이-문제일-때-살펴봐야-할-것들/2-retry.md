# Retry

> [외부 연동이 문제일 때 살펴봐야 할 것들](./README.md)

> [!WARNING]
> **Retry는 실패한 의존성의 부하를 증폭할 수 있습니다**
>
> 멱등성, backoff·jitter, 횟수와 retry budget을 함께 정하고 전체 deadline 안에서만 재시도해야 합니다.

## 빠른 복습

- Retry는 일시 실패를 회복하지만 이미 느린 dependency에 추가 부하를 보낸다.
- 조회 또는 멱등한 변경처럼 중복 실행이 안전한 경우에만 수행한다.
- 적은 횟수, exponential backoff, jitter와 전체 retry deadline을 둔다.
- 여러 계층이 각각 retry해 호출 수가 곱셈으로 늘어나지 않도록 책임을 한곳에 둔다.
- Timeout과 재시도 비교로 증폭을 확인한다.
- Lab의 `스레드 유지`와 `다시 예약`을 비교해 backoff가 blocking thread 점유에 주는 차이도 확인한다.

네트워크에는 일시적인 연결 실패, connection reset, 429와 일시적 5xx가 발생할 수 있다. retry는 이런 순간 실패를 성공으로 바꿀 수 있지만, 실패한 시스템에 추가 부하를 보내는 행위이기도 하다.

## 무엇을 Retry할 수 있는가

재시도 가능 여부는 HTTP method 이름만이 아니라 실제 business effect와 실패 단계로 판단한다.

| 상황 | 기본 판단 | 조건 |
| --- | --- | --- |
| 단순 조회 | retry 가능 | 조회가 실제로 상태를 변경하지 않아야 함 |
| 연결 수립 실패 | 비교적 안전 | 요청이 전달되지 않았음을 확실히 판단할 수 있어야 함 |
| 읽기 timeout·응답 유실 | 결과 불명 | 조회이거나 idempotency key·상태 확인 수단이 있을 때만 |
| `400`, validation 실패 | retry하지 않음 | 같은 입력이면 반복 실패 |
| `401`, `403` | 보통 retry하지 않음 | token 갱신처럼 명확한 복구 동작이 있을 때만 |
| `408`, `429` | 제한적으로 retry | `Retry-After`, 전체 deadline과 rate limit 준수 |
| 일시적 `5xx` | 제한적으로 retry | retry budget과 downstream 상태 고려 |

“Connect timeout이면 서버에 도착하지 않았으므로 항상 안전하다”고 단정하면 위험하다. proxy·load balancer와 연결 재사용이 개입하고 어느 단계에서 실패했는지 client가 명확히 알지 못하는 경우가 있다. 상태 변경 호출은 전송 단계와 관계없이 멱등성을 갖추는 편이 안전하다.

HTTP 표준에서 `PUT`, `DELETE`와 safe method는 의미상 멱등이지만 실제 API 구현의 부수 효과까지 자동으로 보장하지는 않는다. `POST`도 idempotency key와 서버의 중복 요청 저장으로 멱등하게 만들 수 있다.

## 횟수, 간격과 Retry Budget

retry는 보통 적은 횟수로 제한한다. `1초 → 2초`처럼 exponential backoff를 적용하고 여러 client가 동시에 다시 요청하지 않도록 jitter를 추가한다.

```mermaid
flowchart LR
    A["0초<br/>최초 요청 실패"] --> B["약 1초 + jitter<br/>1차 retry"]
    B --> C["약 2초 + jitter<br/>2차 retry"]
    C --> D["전체 deadline·retry budget 종료"]
```

호출 경로가 여러 계층이면 각 계층이 세 번씩 재시도해 요청이 곱셈으로 늘어날 수 있다. 한 계층에서 retry 책임을 지도록 하고, 전체 호출 중 retry가 차지할 수 있는 비율인 retry budget을 둔다.

```text
원 요청 1개
× API Gateway 3회
× 서비스 A 3회
× 서비스 B 3회
= 최악의 경우 downstream 호출 27회
```

다음 조건을 함께 설정한다.

- 초기 호출을 포함한 최대 attempt 수
- attempt별 timeout과 전체 call deadline
- exponential backoff의 최대 간격과 jitter
- retry할 exception·status code의 명시적 목록
- `Retry-After`와 공급자의 rate-limit header 준수
- 사용자 요청과 background job의 서로 다른 retry 정책
- 전체 retry 비율과 성공 회복률 모니터링

## 참고 자료

- [RFC 9110: HTTP Semantics와 Idempotency](https://www.rfc-editor.org/rfc/rfc9110.html)
- [Resilience4j Retry](https://resilience4j.readme.io/docs/retry)
- [AWS Builders' Library: Timeouts, Retries and Backoff](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
