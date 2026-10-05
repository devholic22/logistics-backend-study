# ADR-0001: 주 개발 언어로 Kotlin을 사용한다

- 상태: Proposed
- 작성일: 2026-10-05
- 결정자: 프로젝트 소유자
- 상위 기획 문서: 미작성 — 첫 Product Brief와 PRD 작성 후 연결
- 관련 ADR: ADR-0002
- 대체한 ADR: 없음
- 대체된 ADR: 없음
- 검토 예정일: 첫 번째 도메인 모델과 영속성 실험 완료 후

## 한 문장 결정

> 재고와 작업 상태가 자주 바뀌는 mini-WMS를 장기간 발전시키는 상황에서,
> 업무 개념과 유효한 상태를 타입으로 명확히 표현하고 WMS의 정합성 문제에 학습을 집중하기 위해
> Kotlin을 주 개발 언어로 선택하고 TypeScript, Go, Rust를 첫 구현 언어로 채택하지 않는다.
> 그 대가로 JVM 운영 비용과 Kotlin-Spring/JPA 연동 규칙을 학습하고 관리한다.

## 배경과 문제 정의

mini-WMS는 물류 화면이나 CRUD API를 빠르게 시연하고 종료하는 프로젝트가 아니다.
입고, 재고, 할당, 피킹, 출고처럼 서로 연결된 업무 상태를 구현하고,
동시 요청과 실패 상황에서 재고 정합성이 어떻게 깨지는지 관찰하며,
약 1년 동안 설계와 운영 방식을 점진적으로 개선하는 프로젝트다.

따라서 언어 선택에서 중요한 문제는 문법 선호나 단순 처리 성능이 아니다.

- `SKU`, `LocationId`, `OrderId`처럼 원시 타입은 같지만 의미가 다른 값을 구분할 수 있어야 한다.
- 미할당, 부분 할당, 할당 완료, 취소처럼 가능한 상태 집합과 전이를 명시적으로 표현해야 한다.
- 존재하지 않음과 아직 입력되지 않음을 무분별한 `null`로 섞지 않아야 한다.
- DB 트랜잭션, 락, 멱등성, 대사와 장애 복구가 주요 학습 주제로 남아야 한다.
- 언어 런타임 자체를 익히는 일이 WMS 도메인 학습을 압도하지 않아야 한다.
- 이후 선택할 JVM 기반 애플리케이션 플랫폼과 안정적으로 통합되어야 한다.

이번 결정은 Kotlin이 모든 백엔드 시스템에 더 우월하다는 주장이 아니다.
현재 mini-WMS의 문제와 검증 계획에 가장 적합한 언어를 고르는 결정이다.

## 범위와 비범위

### 범위

- mini-WMS 애플리케이션의 주 개발 언어
- 도메인 모델, 애플리케이션 서비스, 어댑터와 테스트에 사용하는 언어
- 언어 선택으로 새로 생기는 제약과 검증 계획

### 비범위

- Spring Boot 선택 근거: ADR-0002에서 다룬다.
- JPA와 JDBC 중 어떤 데이터 접근 방식을 사용할지
- API 요청·응답 필드와 외부 계약
- 코루틴이나 리액티브 프로그래밍 도입 여부
- Go 또는 Rust로 별도 컴포넌트를 구현할 가능성

## 제약과 전제

| 구분 | 내용 | 근거 또는 확인 방법 |
| --- | --- | --- |
| 제약 | 한 명이 시작하여 장기간 발전시키는 학습·포트폴리오 프로젝트다. | 프로젝트 계획 |
| 제약 | 초기 저장소에는 검증된 초저지연, 극저메모리, 네이티브 실행 요구가 없다. | 성능 요구사항이 아직 정의되지 않음 |
| 제약 | 핵심 데이터는 PostgreSQL 같은 외부 저장소에서 여러 요청이 공유하게 된다. | WMS 재고 정합성 문제의 성격 |
| 전제 | 상태 전이와 값의 의미를 코드에서 분명히 표현하는 것이 변경 비용을 낮춘다. | 첫 도메인 모델에서 검증 |
| 전제 | JVM 생태계와의 상호 운용성이 이후 프레임워크 선택의 폭을 넓힌다. | Kotlin 공식 Java 상호 운용 문서 |
| 가설 | Kotlin의 타입 기능이 WMS 상태 모델에서 실수 방지와 설명 가능성에 실질적인 이점을 준다. | 도메인 모델 및 테스트 리뷰 |

## 결정 기준

| 우선순위 | 결정 기준 | 프로젝트에서 중요한 이유 | 검증 방법 |
| --- | --- | --- | --- |
| 1 | 업무 개념과 유효한 상태를 타입으로 표현 | 잘못된 ID 혼용과 누락된 상태 처리가 재고 오류로 이어질 수 있다. | 첫 도메인 모델 코드 리뷰와 컴파일 실패 사례 |
| 2 | `null` 가능성을 경계에서 드러냄 | 미확정·미존재·오류를 한 값으로 섞지 않아야 한다. | Kotlin 타입, Java 경계 설정과 정적 분석 |
| 3 | WMS·DB 문제에 학습을 집중 | 언어 런타임 학습이 트랜잭션과 도메인 학습을 압도하지 않아야 한다. | 작업 기록에서 언어 문제 해결 비중 관찰 |
| 4 | 선택할 애플리케이션 플랫폼과의 통합 | 트랜잭션, 배치, 관측성 실험을 하나의 기반에서 이어가야 한다. | ADR-0002와 부트스트랩 검증 |
| 5 | 장기간 변경 가능한 코드 | 1년 동안 상태와 경계가 바뀌어도 변경 영향을 추적할 수 있어야 한다. | 변경 PR과 테스트 유지 비용 기록 |
| 6 | 성능 요구가 생겼을 때 측정 가능 | 성능 우위를 추측으로 주장하지 않고 실제 병목을 측정해야 한다. | 부하 테스트와 프로파일링 |

## 검토한 선택지

- Kotlin/JVM
- TypeScript/Node.js
- Go
- Rust

## 근거 비교

| 결정 기준 | 선택지 | 공식 문서에서 확인된 사실 | 프로젝트에 대한 해석 | 출처 |
| --- | --- | --- | --- | --- |
| 상태 모델 | Kotlin | sealed class/interface의 직접 하위 타입은 컴파일 시 알려지고 `when`이 모든 경우를 다뤘는지 검사할 수 있다. | 유한한 작업 상태와 오류 유형을 닫힌 집합으로 표현하기 적합하다. | https://kotlinlang.org/docs/sealed-classes.html |
| 의미 있는 값 | Kotlin | value class는 기반 타입과 대입 호환되지 않는 별도 타입을 만들 수 있다. 공식 idiom은 서로 다른 ID를 혼용하면 컴파일 오류가 나는 예를 든다. | `SKU`와 `LocationId`가 모두 문자열이어도 실수로 바꾸어 전달하는 일을 줄일 수 있다. | https://kotlinlang.org/docs/inline-classes.html, https://kotlinlang.org/docs/idioms.html#use-inline-value-classes-for-type-safe-values |
| null 처리 | Kotlin | nullable과 non-null 타입을 구분하고 잠재적인 null 문제를 컴파일 단계에서 확인한다. Java 연동의 platform type은 예외다. | 내부 도메인에서는 부재를 명시할 수 있지만 Java 경계에는 별도 규칙이 필요하다. | https://kotlinlang.org/docs/null-safety.html, https://kotlinlang.org/docs/java-interop.html#null-safety-and-platform-types |
| 생태계 통합 | Kotlin | Kotlin은 Java 코드와 상호 운용되며 Java 기반 프레임워크를 사용할 수 있다. | JVM의 데이터 접근과 운영 생태계를 사용하면서 언어 수준의 상태 표현을 얻을 수 있다. | https://kotlinlang.org/docs/java-interop.html, https://kotlinlang.org/docs/server-overview.html |
| 런타임 타입 | TypeScript | TypeScript 타입은 컴파일 후 지워지고 결과 JavaScript에는 타입 정보가 남지 않는다. 런타임 동작은 JavaScript와 같다. | 외부 입력과 영속화 경계에서 런타임 검증이 별도로 필요하다. 이는 결함이 아니라 의도된 설계지만, 이번 프로젝트에서는 관리할 경계가 하나 더 생긴다. | https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html#erased-types |
| 타입 호환성 | TypeScript | TypeScript는 구조적 타입을 사용하며 공식 문서는 의도적으로 허용한 비건전한 동작이 있음을 명시한다. | DTO와 도메인 타입을 구분하려면 브랜드 타입, 스키마와 변환 규칙 같은 프로젝트 관례가 중요해진다. | https://www.typescriptlang.org/docs/handbook/type-compatibility |
| 실행 모델 | Node.js | Node.js는 event loop와 worker pool을 사용하며, 높은 처리량을 유지하려면 각 callback과 task가 오래 실행되어 이를 막지 않게 해야 한다. | I/O 중심 연동에는 장점이 있지만 작업 분류와 event loop 지연을 별도의 운영 관심사로 다뤄야 한다. | https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop |
| 동시성 | Go | Go는 goroutine과 channel을 통한 동시성 구성을 강조하며, 공식 문서는 모든 병렬화 문제가 이 모델에 맞는 것은 아니라고 설명한다. | 프로세스 내부 작업 분배에는 강점이 있지만 여러 인스턴스가 같은 DB 재고를 갱신하는 문제는 별도의 DB 동시성 설계가 필요하다. | https://go.dev/doc/effective_go#concurrency |
| 타입 정의 | Go | Go는 기반 타입과 다른 defined type, struct, method와 interface를 제공한다. | WMS 값 객체를 만들 수 있다. 다만 닫힌 상태 집합과 모든 분기 처리는 Kotlin의 sealed hierarchy보다 명시적인 관례와 테스트에 더 의존한다. | https://go.dev/ref/spec#Type_declarations |
| 오류 처리 | Go | Go는 정상 반환값과 함께 `error`를 명시적으로 반환하는 관례를 사용한다. | 오류 흐름이 분명해지는 장점이 있지만, 이번 프로젝트에서는 각 계층의 오류 전달 코드가 도메인 상태 실험보다 큰 비중을 차지하는지 검증이 필요하다. | https://go.dev/doc/effective_go#errors |
| 메모리·동시성 안전 | Rust | Rust의 ownership과 타입 시스템은 많은 메모리·동시성 오류를 컴파일 오류로 바꾼다. | 프로세스 내부 안전성에는 강력하지만 DB 행, 분산 트랜잭션, 중복 메시지의 정합성을 대신 해결하지 않는다. | https://doc.rust-lang.org/book/ch16-00-concurrency.html |
| 오류 모델 | Rust | 복구 가능한 오류는 `Result<T, E>`, 복구 불가능한 오류는 `panic!`으로 구분한다. | 명시적인 오류 모델은 장점이지만 ownership과 함께 Rust 자체가 별도의 큰 학습 주제가 된다. | https://doc.rust-lang.org/stable/book/ch09-00-error-handling.html |
| 비동기 실행 | Rust | Rust 표준 라이브러리는 async runtime을 제공하지 않으며 요구에 맞는 runtime을 선택한다. | 웹·DB 스택 선택과 runtime 호환성 검토가 WMS 도메인 외의 주요 결정으로 추가된다. | https://rust-lang.github.io/async-book/part-guide/async-await.html |

## 선택지별 트레이드오프

### Kotlin/JVM

#### 얻는 것

- sealed hierarchy와 exhaustive `when`으로 닫힌 상태 집합을 표현할 수 있다.
- value class로 같은 원시 타입을 가진 업무 식별자를 구분할 수 있다.
- nullability를 내부 타입 계약에 포함할 수 있다.
- Java/JVM 라이브러리와 상호 운용할 수 있다.

#### 치르는 비용과 위험

- Java에서 들어오는 platform type은 Kotlin의 null-safety를 약화시킬 수 있다.
- Kotlin 클래스는 기본적으로 `final`이므로 프록시를 사용하는 Spring과 결합할 때 compiler plugin 동작을 이해해야 한다.
- JPA를 선택한다면 생성자, 프록시, 지연 로딩과 엔티티 설계 규칙을 별도로 검증해야 한다.
- JVM 시작 시간과 메모리 사용량이 문제가 되는지는 운영 측정으로 확인해야 한다.

#### 이 선택지가 더 적합해지는 조건

- 복잡한 상태와 값 객체가 실제 코드의 중심이 될 때
- JVM 기반 트랜잭션·배치·관측성 생태계를 함께 사용할 때

### TypeScript/Node.js

#### 얻는 것

- TypeScript의 union과 narrowing으로 상태별 로직을 표현할 수 있다.
- 프론트엔드와 언어 및 일부 스키마 도구를 공유할 가능성이 있다.
- Node.js의 비동기 I/O 모델로 많은 네트워크 연결을 효율적으로 다룰 수 있다.

#### 치르는 비용과 위험

- 컴파일 타입은 런타임에 지워지므로 입력과 영속화 경계에 런타임 스키마 검증이 필수다.
- 구조적 타입의 유연성 때문에 업무상 다른 값의 구분을 위한 별도 관례가 필요하다.
- event loop를 막지 않는 작업 분할과 CPU 작업 격리가 운영 설계의 주요 관심사가 된다.

#### 이 선택지가 더 적합해지는 조건

- 프론트엔드와 계약·도구 공유가 핵심 요구가 될 때
- 외부 I/O 연동과 데이터 파이프라인이 재고 트랜잭션보다 프로젝트의 중심이 될 때

### Go

#### 얻는 것

- defined type과 명시적 오류 반환으로 계약을 분명히 표현할 수 있다.
- goroutine과 channel로 프로세스 내부 동시 작업을 간결하게 구성할 수 있다.
- 작은 서비스와 worker 중심으로 시스템을 분할하는 실험에 적합하다.

#### 치르는 비용과 위험

- WMS의 유한 상태와 모든 분기를 빠짐없이 처리하는 규칙을 프로젝트 관례와 테스트로 더 많이 보완해야 한다.
- 통합 애플리케이션 플랫폼보다 필요한 라이브러리와 운영 구성을 직접 조합하는 일이 학습의 큰 부분이 될 수 있다.
- goroutine은 여러 서버 인스턴스가 공유 DB를 변경할 때의 정합성을 해결하지 않는다.

#### 이 선택지가 더 적합해지는 조건

- 경량 배포, 빠른 시작, 낮은 메모리 사용이 측정 가능한 핵심 요구가 될 때
- WCS adapter, event consumer 같은 작은 독립 서비스가 필요할 때

### Rust

#### 얻는 것

- ownership과 타입 시스템을 통해 메모리 및 프로세스 내부 동시성 오류를 강하게 제한한다.
- `Result`와 `Option`으로 실패와 부재를 명시적으로 모델링한다.
- 런타임 자원 제어와 예측 가능한 성능이 중요한 컴포넌트에 적합하다.

#### 치르는 비용과 위험

- ownership, lifetime, async runtime과 라이브러리 호환성이 별도의 핵심 학습 주제가 된다.
- 현재 프로젝트에는 그 비용을 정당화할 네이티브 성능·메모리 안전 요구가 확인되지 않았다.
- 언어가 보장하는 프로세스 내부 안전성과 WMS가 요구하는 DB·분산 정합성을 혼동할 위험이 있다.

#### 이 선택지가 더 적합해지는 조건

- WCS 장비 agent, edge process처럼 자원 제어와 네이티브 실행이 핵심일 때
- 프로파일링으로 JVM runtime이 실제 병목임이 확인됐을 때

## 결정

mini-WMS의 주 개발 언어로 Kotlin을 선택한다.

Kotlin을 선택하는 핵심 이유는 코드가 짧기 때문이 아니다.
현재 가장 중요한 실패 ㅈ가능성인 잘못된 업무 상태와 값의 혼용을 타입 수준에서 드러내고,
이후 DB 트랜잭션·동시성·장애 복구 실험을 JVM 생태계 안에서 이어갈 수 있기 때문이다.

TypeScript, Go와 Rust는 모두 실무 가능한 선택지다. 다만 현재 프로젝트에서는 각각
런타임 스키마와 event loop, 경량 동시 서비스 조합, ownership과 async runtime이라는
별도의 주요 학습 축을 추가한다. 이 프로젝트는 해당 런타임의 우열을 검증하는 대신
WMS의 업무 정합성과 장기간의 설계 변화에 학습 범위를 집중한다.

## 결과와 영향

### 긍정적 결과

- 업무 식별자와 수량을 원시 타입과 구분할 수 있다.
- 유한한 상태 집합과 상태별 처리를 컴파일러의 도움으로 점검할 수 있다.
- Java/JVM 생태계의 라이브러리를 사용할 수 있다.
- ADR-0002의 Spring Boot 선택과 자연스럽게 결합된다.

### 부정적 결과와 감수한 비용

- Kotlin과 Spring의 proxy·reflection·serialization 규칙을 이해해야 한다.
- platform type 경계에서는 null-safety를 자동으로 신뢰할 수 없다.
- Kotlin/JPA 조합을 선택할 경우 compiler plugin과 entity 규칙이 추가된다.
- Kotlin 경험 확보 자체가 목적처럼 보이지 않도록 실제 결함 예방과 변경 비용을 증거로 남겨야 한다.

### 중립적 결과

- 코루틴은 Kotlin 선택의 자동 결과가 아니다. 필요성이 검증될 때 별도로 결정한다.
- JPA 사용 여부도 Kotlin 선택의 자동 결과가 아니다. 별도 ADR에서 비교한다.

## 위험 완화책

| 위험 | 완화책 | 확인 시점 |
| --- | --- | --- |
| `!!`와 platform type으로 null-safety가 무력화됨 | 도메인 계층에서 `!!`를 금지하고 Java 경계에서 명시적으로 변환한다. | 코드 리뷰와 정적 분석 |
| value class를 장식적으로 남용 | 실제로 혼용 위험이 있는 식별자와 단위에만 사용한다. | 첫 도메인 모델 리뷰 |
| sealed class가 모든 상태 전이를 보장한다고 착각 | 허용 전이는 도메인 메서드와 상태 전이 테스트로 별도 검증한다. | 유스케이스 구현 시 |
| Spring proxy와 Kotlin final 충돌 | `kotlin-spring` plugin을 명시하고 proxy가 필요한 경계를 테스트한다. | 부트스트랩 및 트랜잭션 테스트 |
| JPA 제약이 도메인 모델을 오염 | 데이터 접근 방식은 별도 ADR로 결정하고 persistence model 분리를 검토한다. | 영속성 도입 전 |

## 검증 계획과 성공 기준

| 확인할 가설 | 실험 또는 관찰 | 성공 기준 | 증거 위치 |
| --- | --- | --- | --- |
| 의미가 다른 값을 혼용하는 문제를 컴파일 단계에서 방지할 수 있다. | `SKU`, `LocationId`를 value class로 만들고 교차 전달 사례를 확인한다. | 잘못된 전달이 컴파일되지 않는다. | 첫 도메인 PR |
| 상태 추가 시 누락된 처리를 발견할 수 있다. | sealed 상태에 새 값을 추가한다. | exhaustive `when`의 누락이 컴파일 오류로 드러난다. | 상태 모델 테스트/PR |
| null 경계를 통제할 수 있다. | Kotlin 타입과 Java 연동 nullability 설정, 경계 변환을 점검한다. | 도메인 계층에 platform type과 `!!`가 남지 않는다. | 빌드 설정과 정적 분석 |
| 언어 학습이 프로젝트를 압도하지 않는다. | 첫 두 마일스톤의 작업 기록을 분류한다. | 언어 문법·runtime 문제보다 WMS/DB 설계 기록이 중심이다. | 회고 문서 |

## 재검토 조건

- 메모리 사용량, 시작 시간 또는 네이티브 실행이 측정 가능한 핵심 제약이 되면 Go와 Rust를 다시 비교한다.
- 프로젝트의 중심이 외부 데이터 파이프라인과 프론트엔드 계약 공유로 이동하면 TypeScript/Node.js를 다시 비교한다.
- Kotlin-Spring/JPA 연동 비용이 반복적으로 도메인 구현 비용보다 커지면 Java 또는 다른 JVM 접근을 검토한다.
- 별도 WCS/edge component가 필요해지면 그 컴포넌트의 언어를 별도 ADR로 결정한다.

## 후속 작업

- [ ] ADR-0002에서 애플리케이션 플랫폼을 결정한다.
- [ ] Kotlin nullability 설정과 코드 규칙을 정한다.
- [ ] 첫 도메인 모델에서 value class와 sealed hierarchy 가설을 검증한다.
- [ ] 데이터 접근 방식은 별도 ADR로 비교한다.

## Outcome review

- 검토일: 미정
- 실제 결과: 구현 후 작성
- 측정값과 증거: 구현 후 작성
- 예상과 달랐던 점: 구현 후 작성
- 실패하거나 폐기한 시도: 구현 후 작성
- 새로 배운 점: 구현 후 작성
- 유지, 수정 또는 대체 결정: 구현 후 작성

## 참고 자료

### Kotlin 공식 문서

- Null safety: https://kotlinlang.org/docs/null-safety.html
- Sealed classes and interfaces: https://kotlinlang.org/docs/sealed-classes.html
- Inline value classes: https://kotlinlang.org/docs/inline-classes.html
- Java interoperability: https://kotlinlang.org/docs/java-interop.html
- Backend development with Kotlin: https://kotlinlang.org/docs/server-overview.html
- All-open compiler plugin: https://kotlinlang.org/docs/all-open-plugin.html

### TypeScript 공식 문서

- Erased types: https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html#erased-types
- Type compatibility and soundness: https://www.typescriptlang.org/docs/handbook/type-compatibility

### Node.js 공식 문서

- Don't block the event loop: https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop
- Worker threads: https://nodejs.org/api/worker_threads.html

### Go 공식 문서

- Language specification: https://go.dev/ref/spec
- Effective Go - concurrency and errors: https://go.dev/doc/effective_go

### Rust 공식 문서

- Ownership: https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html
- Concurrency: https://doc.rust-lang.org/book/ch16-00-concurrency.html
- Error handling: https://doc.rust-lang.org/stable/book/ch09-00-error-handling.html
- Async runtime: https://rust-lang.github.io/async-book/part-guide/async-await.html
