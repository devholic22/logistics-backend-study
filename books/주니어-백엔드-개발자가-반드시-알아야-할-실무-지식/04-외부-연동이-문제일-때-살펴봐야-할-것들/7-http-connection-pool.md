# HTTP Connection pool

> [외부 연동이 문제일 때 살펴봐야 할 것들](./README.md)

> [!IMPORTANT]
> **Pool 대기 시간도 전체 호출 시간에 포함됩니다**
>
> HTTP client를 재사용하고 전체·route별 연결 수와 획득 Timeout을 하위 서비스 용량에 맞춰 제한해야 합니다.

## 빠른 복습

- HTTP client를 재사용해야 TCP·TLS connection과 thread pool을 재사용할 수 있다.
- 전체·route별 pool 크기, 획득 대기, idle lifetime과 stale validation을 함께 본다.
- HTTP/2는 한 connection에서 여러 stream을 처리하므로 HTTP/1.1 계산을 그대로 적용할 수 없다.
- Pool을 무턱대고 키우면 downstream에 더 큰 burst를 전달할 수 있어 bulkhead·quota와 맞춰야 한다.

DB 연결처럼 HTTP 연결도 TCP·TLS 설정 비용이 있으므로 client를 재사용하고 connection pool을 활용하면 latency와 자원 사용을 줄일 수 있다. 요청마다 새 `OkHttpClient`나 HTTP client를 만들면 pool과 thread가 분리되어 재사용 효과가 사라진다.

Pool 크기·획득 대기·유휴 connection이라는 공통 원리는 [DB 커넥션 풀](../02-느려진-서비스-어디부터-봐야-할까/2-서버-성능-개선-기초.md#db-커넥션-풀)과 유사하지만, HTTP/2 multiplexing과 downstream quota라는 차이가 있다.

다음 설정을 함께 본다.

- 전체 최대 connection과 host·route별 최대 connection
- pool에서 connection을 빌릴 때까지의 timeout
- idle connection 수와 idle timeout
- connection 최대 lifetime과 stale connection 검사
- DNS 변경과 connection 재수립 정책
- HTTP/2의 connection 수, 동시 stream 수와 flow control
- 응답 body를 끝까지 소비하거나 명시적으로 닫아 pool에 반환하는지

Pool acquisition timeout을 1~5초 정도로 시작할 수 있지만 고정 정답은 아니다. 우리 API의 전체 deadline보다 충분히 짧아야 하며, 순간 트래픽을 조금 흡수할지 즉시 거절할지는 서비스 목표에 따라 결정한다.

HTTP/1.1은 기본적으로 persistent connection을 지원하지만 서버와 중간 proxy는 connection을 언제든 닫을 수 있다. 일부 구현은 `Keep-Alive` 정보로 유휴 유지 시간을 제안하지만 모든 환경에서 반드시 제공되거나 보장되는 것은 아니다. Client의 idle lifetime, connection validation과 실패 시 안전한 재연결을 함께 설정한다.

HTTP/2는 한 connection에서 여러 stream을 multiplex할 수 있으므로 “동시 요청 수만큼 TCP connection을 만든다”는 HTTP/1.1식 계산을 그대로 적용할 수 없다. 상대가 `SETTINGS_MAX_CONCURRENT_STREAMS`로 동시 stream을 제한할 수 있고 connection·stream flow control도 존재한다.

Pool 크기를 무턱대고 늘리면 우리 내부 대기는 줄어도 downstream에 순간적으로 더 많은 요청을 보내 장애를 악화시킬 수 있다. HTTP pool 크기, bulkhead와 rate limit을 같은 용량 계획 안에서 맞춘다.

## 참고 자료

- [OkHttpClient 공식 API 문서](https://lysine.dev/okhttp/5.x/okhttp/okhttp3/-ok-http-client/)
- [Apache HttpClient 5 RequestConfig](https://hc.apache.org/httpcomponents-client-5.6.x/current/httpclient5/apidocs/org/apache/hc/client5/http/config/RequestConfig.html)
- [RFC 9113: HTTP/2 Stream Concurrency](https://www.rfc-editor.org/rfc/rfc9113.html)
