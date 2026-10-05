# ADR-0002: 애플리케이션 플랫폼으로 Spring Boot를 사용한다

- 상태: Draft
- 작성일: 2026-10-05
- 결정자: 프로젝트 소유자
- 상위 기획 문서: 미작성 — 첫 Product Brief와 PRD 작성 후 연결
- 관련 ADR: ADR-0001
- 대체한 ADR: 없음
- 대체된 ADR: 없음
- 검토 예정일: 시스템 골격과 첫 트랜잭션 실험 완료 후

> 이 문서는 상위 Product Brief와 PRD 작성 전에 기술 가설을 비교하기 위한 초안이다.
> 사용자 시나리오와 기능·비기능 요구사항이 연결되기 전에는 `Proposed`로 전환하지 않는다.

## 한 문장 결정

> 재고 정합성, 재시작 가능한 작업과 운영 가시성을 장기간 검증해야 하는 mini-WMS에서
> 일관된 트랜잭션 모델과 점진적으로 확장할 운영 기반을 얻기 위해 Spring Boot를 선택하고,
> NestJS/Node.js 또는 Go·Rust 기반의 조합을 첫 애플리케이션 플랫폼으로 채택하지 않는다.
> 그 대가로 Spring의 proxy·자동 설정과 JVM 운영 모델을 명시적으로 학습하고 검증한다.

## 배경과 문제 정의

WMS는 HTTP 요청에 CRUD 응답만 반환하는 시스템이 아니다. 프로젝트가 발전하면 다음 실행 형태가 필요할 수 있다.

- 입고·재고·할당·출고 API
- 재고 대사와 장기 미완료 작업 탐지
- 대량 작업을 위한 batch
- 외부 OMS/WCS 연동
- 메시지 consumer와 재시도
- health, metrics, logging과 장애 분석

이 가운데 현재 가장 중요한 품질 속성은 다음과 같다.

1. 함께 성공하거나 실패해야 하는 DB 변경의 트랜잭션 경계를 명확히 할 수 있어야 한다.
2. 실패한 장기 작업을 식별하고 재시작하는 모델로 확장할 수 있어야 한다.
3. 운영 상태를 health와 metrics로 확인하고 이후 실험의 결과를 남길 수 있어야 한다.
4. 초기에는 단순하게 시작하되 필요가 확인된 기능만 점진적으로 추가할 수 있어야 한다.
5. 런타임이나 라이브러리 조합 자체보다 WMS 업무와 DB 정합성에 학습을 집중해야 한다.

이번 결정은 Spring Boot가 모든 서버에 더 적합하다는 주장이 아니다.
NestJS/Node.js, Go와 Rust는 서로 다른 문제에서 더 나은 선택일 수 있다.

## 범위와 비범위

### 범위

- mini-WMS의 기본 웹 애플리케이션 플랫폼
- 트랜잭션과 운영 상태 확인을 위한 기반
- 미래 batch·scheduler·messaging 확장 가능성을 평가하는 기준

### 비범위

- Spring Batch, Kafka, Redis를 지금 도입하는 결정
- JPA와 JDBC 중 하나를 선택하는 결정
- 동기 MVC, coroutine, reactive stack 중 하나를 선택하는 결정
- microservice 전환 결정
- API 계약과 데이터 모델

## 제약과 전제

| 구분 | 내용 | 근거 또는 확인 방법 |
| --- | --- | --- |
| 제약 | 초기에는 한 애플리케이션과 PostgreSQL로 시작한다. | 프로젝트 범위 |
| 제약 | 아직 대규모 트래픽과 초저지연 요구는 측정되지 않았다. | 성능 기준 미정 |
| 제약 | 장기간 운영과 변경 과정 자체를 학습 결과로 남겨야 한다. | 프로젝트 목표 |
| 전제 | 재고 관련 상태 변경은 DB 트랜잭션과 격리 수준의 영향을 크게 받는다. | 이후 동시성 실험으로 검증 |
| 전제 | 대사와 batch는 WMS가 성장하면 중요한 운영 기능이 될 가능성이 높다. | WMS 학습 기록과 시나리오 |
| 가설 | Spring의 통합된 트랜잭션·운영 모델이 기반 조립 비용을 줄여 WMS 문제에 집중하게 한다. | 첫 마일스톤 회고로 검증 |

## 결정 기준

| 우선순위 | 결정 기준 | 프로젝트에서 중요한 이유 | 검증 방법 |
| --- | --- | --- | --- |
| 1 | DB 트랜잭션을 일관되게 실험 | 재고 오류는 여러 변경의 원자성과 동시 실행에서 발생한다. | 실제 PostgreSQL 통합 테스트 |
| 2 | 운영 실패와 재시작을 다룰 확장 경로 | 대사·batch·consumer는 중단 후 재개와 실행 이력이 중요하다. | batch 도입 시 별도 실험 |
| 3 | health·metrics 기반 관찰 | 운영했다고 주장하려면 상태와 변화에 대한 증거가 필요하다. | Actuator와 metrics 검증 |
| 4 | 초기 단순성과 점진적 확장 | 필요하지 않은 인프라를 미리 도입하지 않아야 한다. | 의존성 목록과 ADR 리뷰 |
| 5 | Kotlin과 공식적으로 지원되는 결합 | 언어와 프레임워크 연결 비용을 통제해야 한다. | 공식 plugin과 부팅 테스트 |
| 6 | 런타임 특성에 대한 설명 가능성 | 자동 설정이나 event loop를 막연히 신뢰하지 않아야 한다. | 장애·성능 실험 기록 |

## 검토한 선택지

- Kotlin + Spring Boot
- TypeScript + NestJS + Node.js
- Go + 표준 라이브러리 및 필요한 구성요소 조합
- Rust + async runtime 및 웹·데이터 라이브러리 조합

Go와 Rust는 Spring Boot나 NestJS와 동일한 층위의 단일 프레임워크가 아니다.
따라서 언어의 우열이 아니라, 해당 언어로 이 프로젝트에 필요한 애플리케이션 플랫폼을 조합했을 때의 결정 부담까지 비교한다.

## 근거 비교

| 결정 기준 | 선택지 | 공식 문서에서 확인된 사실 | 프로젝트에 대한 해석 | 출처 |
| --- | --- | --- | --- | --- |
| 트랜잭션 | Spring | Spring은 JDBC, Hibernate, JPA 등 서로 다른 transaction API에 일관된 추상화와 선언적·프로그램 방식의 transaction 관리를 제공한다. | 데이터 접근 방식을 나중에 바꾸거나 비교해도 transaction 개념과 실험 방식을 일정하게 유지할 수 있다. | https://docs.spring.io/spring-framework/reference/data-access/transaction.html |
| 트랜잭션 경계 | Spring | 선언적 transaction은 메서드 단위로 동작을 지정할 수 있고 local JDBC/JPA/Hibernate transaction에 적용된다. 원격 호출로 transaction context를 전파하지 않는다. | 로컬 DB 원자성과 외부 시스템 연동을 구분하는 학습에 적합하다. `@Transactional`의 proxy 경계는 반드시 검증해야 한다. | https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative.html |
| 운영 가시성 | Spring Boot | Actuator는 health, metrics, auditing과 관리 endpoint 등 production-ready 기능을 제공한다. | 운영 실험을 시작할 최소 관측 기반을 작은 의존성 추가로 마련할 수 있다. | https://docs.spring.io/spring-boot/reference/actuator/index.html |
| batch | Spring Batch | Spring Batch는 Job, Step, JobRepository와 실행 metadata, restartability를 명시적인 domain model로 제공한다. | 대사와 대량 작업이 실제 요구가 됐을 때 실패·재시작을 직접 처음부터 발명하지 않고 검증된 모델로 확장할 수 있다. 현재 즉시 도입할 이유는 아니다. | https://docs.spring.io/spring-batch/reference/domain.html |
| Kotlin 결합 | Spring Boot | Spring Boot 공식 문서는 Kotlin 지원, `kotlin-spring` plugin, Kotlin JSON module과 null-safety 연동을 설명한다. | 언어와 프레임워크의 결합이 우연한 community 조합이 아니라 공식 지원 경로를 가진다. | https://docs.spring.io/spring-boot/reference/features/kotlin.html |
| 모듈·DI | NestJS | Nest는 module과 provider를 통해 기능 경계와 dependency injection을 제공하고 module의 exports를 public interface로 사용한다. | 모듈러 모놀리스 구조를 만드는 데 충분히 유효한 대안이다. NestJS를 단순 CRUD framework라서 제외할 수 없다. | https://docs.nestjs.com/modules, https://docs.nestjs.com/providers |
| 데이터 접근 | NestJS | Nest는 database-agnostic이며 TypeORM, Sequelize, MikroORM, Knex, Prisma 등 여러 통합 선택지를 제공한다. transaction 방식은 선택한 도구에 따라 달라진다. | 유연성이 장점이지만, 이번 프로젝트에서는 ORM·transaction 조합 선택이 별도의 핵심 설계 부담이 된다. | https://docs.nestjs.com/techniques/database |
| schedule·queue | NestJS | Nest는 schedule package와 Redis 기반 queue integration 등 background 작업 수단을 제공한다. | NestJS도 WMS의 비동기·예약 작업을 구현할 수 있다. 제외 이유는 기능 부재가 아니라 일관된 transaction/batch 학습 축의 차이다. | https://docs.nestjs.com/application/task-scheduling, https://docs.nestjs.com/techniques/queues |
| 실행 모델 | Node.js | Node.js는 event loop와 소수 thread로 많은 client를 처리하며, client별 작업을 작게 유지하고 event loop나 worker pool을 막지 않아야 한다. | I/O 중심 연동에는 강점이 있지만 event loop 공정성과 CPU 작업 격리가 별도의 핵심 운영 관심사가 된다. | https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop |
| CPU 작업 | Node.js | worker thread는 CPU-intensive JavaScript 작업에 유용하며 I/O-intensive 작업에는 내장 async I/O가 더 효율적이다. | runtime 특성에 따라 작업 분류와 offloading 정책을 설계해야 한다. 현재 WMS의 핵심 검증 대상은 DB transaction과 lock이다. | https://nodejs.org/api/worker_threads.html |
| 동시성 | Go | goroutine은 같은 address space에서 실행되고 channel을 통한 통신을 권장한다. | worker와 adapter에는 매력적이지만 여러 프로세스의 공유 DB 정합성 모델을 제공하는 것은 아니다. 필요한 transaction·batch·metrics 구성을 별도로 선택해야 한다. | https://go.dev/doc/effective_go#concurrency |
| 실행 모델 | Rust | async task를 실행하려면 runtime을 선택해야 하며 표준 라이브러리는 하나의 runtime을 제공하지 않는다. | 자원 제어가 중요한 서비스에는 선택권이 장점이지만, 이번 프로젝트에서는 runtime·웹·DB 생태계 조합이 추가 연구 주제가 된다. | https://rust-lang.github.io/async-book/part-guide/async-await.html |

## 선택지별 트레이드오프

### Kotlin + Spring Boot

#### 얻는 것

- JDBC/JPA/Hibernate에 걸친 일관된 transaction abstraction을 사용해 경계를 실험할 수 있다.
- Actuator로 health와 metrics를 초기 운영 기반에 포함할 수 있다.
- 요구가 생기면 restart metadata를 가진 batch model로 확장할 수 있다.
- Kotlin에 대한 공식 지원 경로가 있다.

#### 치르는 비용과 위험

- 선언적 transaction과 여러 Spring 기능이 proxy/AOP에 의존하므로 호출 경계를 이해하지 못하면 오작동할 수 있다.
- 자동 설정이 실제 생성한 bean과 기본값을 확인하지 않으면 시스템 동작을 잘못 이해할 수 있다.
- JVM과 framework의 기본 resource 사용량이 단순 Go/Rust executable보다 클 가능성이 있으므로 측정이 필요하다.
- Spring 기능이 많다는 이유로 batch, messaging, cache를 조기에 도입할 위험이 있다.

#### 이 선택지가 더 적합해지는 조건

- transaction, batch restart, 운영 관측이 핵심 학습과 운영 요구일 때
- 하나의 JVM application을 점진적으로 확장할 때

### TypeScript + NestJS + Node.js

#### 얻는 것

- module과 provider로 명확한 feature boundary와 DI 구조를 만들 수 있다.
- Express/Fastify, 여러 ORM과 database library를 선택할 수 있다.
- 외부 시스템과 대량 I/O를 연결하는 data pipeline에 Node.js의 비동기 I/O 특성을 활용할 수 있다.
- schedule과 queue 등 필요한 기능으로 확장할 수 있다.

#### 치르는 비용과 위험

- database-agnostic한 만큼 ORM과 transaction semantics를 선택하고 일관성을 직접 관리해야 한다.
- TypeScript 타입은 runtime에 남지 않아 API와 persistence 경계 검증 체계가 별도로 필요하다.
- event loop를 막는 작업, worker pool, CPU 작업 offloading이 운영 설계의 중요한 축이 된다.

#### 이 선택지가 더 적합해지는 조건

- 외부 데이터 정규화와 수많은 I/O integration이 중심일 때
- frontend와 언어·schema tooling 공유가 큰 가치일 때
- 팀이 Node runtime 운영 경험을 이미 가지고 있을 때

### Go 기반 조합

#### 얻는 것

- 작은 배포 단위와 명시적인 코드 구성을 만들기 좋다.
- goroutine과 channel로 consumer와 worker를 구성하기 좋다.
- framework magic을 줄이고 runtime 동작을 직접 파악할 수 있다.

#### 치르는 비용과 위험

- transaction, migration, validation, batch metadata, metrics 등 프로젝트 기반을 여러 선택지에서 직접 조합해야 한다.
- 기반 조합 과정이 WMS 도메인 학습보다 큰 비중을 차지할 수 있다.
- 프로세스 내부 concurrency와 DB concurrency를 별도로 설계해야 한다.

#### 이 선택지가 더 적합해지는 조건

- 여러 개의 작은 worker와 adapter로 분리하는 것이 실제 요구가 될 때
- memory footprint와 startup time이 측정 가능한 운영 제약이 될 때

### Rust 기반 조합

#### 얻는 것

- memory safety와 process 내부 concurrency safety를 강하게 확보할 수 있다.
- runtime overhead와 resource 사용을 세밀하게 제어할 수 있다.
- 장비 연동 agent나 고성능 component에 적합할 수 있다.

#### 치르는 비용과 위험

- async runtime, web framework, DB library의 compatibility와 운영 방식을 선택해야 한다.
- ownership과 lifetime이 프로젝트의 독립적인 주요 학습 축이 된다.
- 그 비용을 정당화할 native performance 요구가 아직 없다.

#### 이 선택지가 더 적합해지는 조건

- WCS/edge process 또는 CPU·memory profile이 중요한 component를 분리할 때
- JVM runtime이 실제 병목이라는 측정 결과가 있을 때

## 결정

mini-WMS의 애플리케이션 플랫폼으로 Spring Boot를 선택한다.

선택의 핵심은 Spring의 시장 점유율이나 일반적인 선호도가 아니다.
이 프로젝트의 첫 번째 학습 대상인 DB transaction과 향후 대사·batch·운영 관측을
하나의 일관된 programming model에서 점진적으로 검증할 수 있기 때문이다.

초기 범위에서는 Spring Boot Web, PostgreSQL 연결, migration, test와 Actuator만 사용한다.
Spring Batch, messaging, cache와 distributed lock은 구체적인 문제가 발생하고 별도 ADR이 승인되기 전에는 도입하지 않는다.

NestJS/Node.js는 기능이 부족해서 제외하지 않는다. 공식 문서상 module, DI, database integration,
scheduling과 queue를 제공하는 충분히 유효한 플랫폼이다. 다만 현재 mini-WMS에서는
database library별 transaction model과 Node event loop 운영을 함께 주요 학습 대상으로 삼는 것보다,
Spring의 transaction abstraction 위에서 WMS 정합성 문제를 먼저 깊게 다루는 편이 프로젝트 목적에 더 맞는다.

## 결과와 영향

### 긍정적 결과

- transaction 경계를 같은 모델로 반복 실험할 수 있다.
- health와 metrics를 프로젝트 초기부터 운영 증거로 남길 수 있다.
- 필요가 확인되면 batch restart와 execution metadata 모델로 확장할 수 있다.
- Kotlin과 Spring의 공식 integration을 사용할 수 있다.

### 부정적 결과와 감수한 비용

- proxy, AOP, auto-configuration과 transaction propagation을 이해해야 한다.
- framework annotation만 붙이고 실제 DB 동작을 검증하지 않는 잘못을 범할 수 있다.
- JVM resource 사용량과 build feedback time을 관리해야 한다.
- 익숙한 기업용 stack을 선택했다는 사실만으로 기술 판단이 정당화되지는 않는다.

### 중립적 결과

- Spring Boot 선택은 JPA, microservice, Kafka 또는 Kubernetes 선택을 의미하지 않는다.
- Spring Batch는 미래 선택지일 뿐 현재 의존성이 아니다.
- Node.js, Go와 Rust는 향후 독립 component의 요구에 따라 다시 선택할 수 있다.

## 위험 완화책

| 위험 | 완화책 | 확인 시점 |
| --- | --- | --- |
| `@Transactional`을 붙이면 정합성이 자동 보장된다고 오해 | 실제 PostgreSQL을 사용하는 integration test로 commit, rollback, isolation을 확인한다. | 첫 상태 변경 유스케이스 |
| auto-configuration을 이해하지 못함 | 주요 bean과 설정 근거를 README 또는 ADR에 기록하고 condition report를 활용한다. | 시스템 부트스트랩 |
| 의존성 과다 도입 | 새 starter·infrastructure는 문제, 대안, 측정 계획이 있는 경우에만 추가한다. | 모든 dependency PR |
| framework에 도메인 로직이 종속 | domain model에는 가능한 한 Spring annotation을 두지 않는다. | 구조 리뷰 |
| JVM 비용을 무시 | startup, memory, request latency와 DB pool을 측정하고 기록한다. | 운영 baseline 수립 시 |

## 검증 계획과 성공 기준

| 확인할 가설 | 실험 또는 관찰 | 성공 기준 | 증거 위치 |
| --- | --- | --- | --- |
| 실행 가능한 최소 시스템을 빠르게 구성할 수 있다. | application, PostgreSQL, migration, health와 CI를 구성한다. | README의 명령만으로 실행·test·health 확인이 가능하다. | bootstrap PR |
| transaction semantics를 재현할 수 있다. | 성공, exception rollback, 중복 요청과 concurrent update를 실제 DB에서 시험한다. | 예상한 commit/rollback 결과가 통합 테스트와 SQL 관찰로 확인된다. | transaction 실험 문서 |
| 운영 상태를 측정할 수 있다. | health와 기본 metrics를 노출하고 baseline을 기록한다. | 장애 주입 시 상태 변화가 관찰되고 원인 추적에 사용할 수 있다. | dashboard 또는 실험 보고서 |
| framework 학습이 WMS 학습을 압도하지 않는다. | 첫 두 마일스톤 작업을 framework, domain, database로 분류한다. | 기록의 중심이 domain/database 문제와 결과에 있다. | 마일스톤 회고 |

## 재검토 조건

- 외부 데이터 수집·정규화와 수많은 I/O integration이 핵심 제품으로 바뀌면 NestJS/Node.js를 다시 비교한다.
- 서비스가 작은 독립 worker 중심으로 분리되고 startup time과 memory가 핵심 제약이 되면 Go를 다시 비교한다.
- WCS/edge 또는 native resource control이 필요한 component가 생기면 Rust를 별도로 검토한다.
- Spring proxy와 auto-configuration으로 인한 결함이나 개발 비용이 반복적으로 프로젝트 가치를 넘어가면 플랫폼을 재검토한다.
- 측정 결과 JVM resource 비용이 목표를 충족하지 못하고 tuning으로 해결되지 않으면 대안을 검토한다.

## 후속 작업

- [ ] Spring Boot application과 Actuator health를 구성한다.
- [ ] PostgreSQL을 포함한 실제 DB integration test 기반을 만든다.
- [ ] Spring transaction proxy와 rollback 규칙을 검증하는 작은 실험을 남긴다.
- [ ] 데이터 접근 방식은 별도 ADR에서 비교한다.
- [ ] batch가 실제로 필요해질 때 Spring Batch와 단순 scheduler/SQL 방식을 별도 ADR에서 비교한다.

## Outcome review

- 검토일: 미정
- 실제 결과: 구현 후 작성
- 측정값과 증거: 구현 후 작성
- 예상과 달랐던 점: 구현 후 작성
- 실패하거나 폐기한 시도: 구현 후 작성
- 새로 배운 점: 구현 후 작성
- 유지, 수정 또는 대체 결정: 구현 후 작성

## 참고 자료

### Spring 공식 문서

- Transaction Management: https://docs.spring.io/spring-framework/reference/data-access/transaction.html
- Declarative Transaction Management: https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative.html
- Spring Boot Actuator: https://docs.spring.io/spring-boot/reference/actuator/index.html
- Spring Boot metrics: https://docs.spring.io/spring-boot/reference/actuator/metrics.html
- Spring Batch domain language: https://docs.spring.io/spring-batch/reference/domain.html
- Spring Boot Kotlin support: https://docs.spring.io/spring-boot/reference/features/kotlin.html
- Spring projects in Kotlin: https://docs.spring.io/spring-framework/reference/languages/kotlin/spring-projects-in.html

### NestJS·Node.js·TypeScript 공식 문서

- NestJS first steps and platforms: https://docs.nestjs.com/first-steps
- NestJS modules: https://docs.nestjs.com/modules
- NestJS providers: https://docs.nestjs.com/providers
- NestJS database integration: https://docs.nestjs.com/techniques/database
- NestJS task scheduling: https://docs.nestjs.com/application/task-scheduling
- NestJS queues: https://docs.nestjs.com/techniques/queues
- Node.js event loop and worker pool: https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop
- Node.js worker threads: https://nodejs.org/api/worker_threads.html
- TypeScript erased types: https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html#erased-types

### Go·Rust 공식 문서

- Effective Go - concurrency and errors: https://go.dev/doc/effective_go
- Go language specification: https://go.dev/ref/spec
- Rust concurrency: https://doc.rust-lang.org/book/ch16-00-concurrency.html
- Rust async runtime: https://rust-lang.github.io/async-book/part-guide/async-await.html
