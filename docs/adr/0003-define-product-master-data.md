# ADR-0003: 상품 기초 데이터의 필드와 규칙을 정의한다

- 상태: Draft
- 작성일: 2026-11-10
- 결정자: 프로젝트 소유자
- 상위 기획 문서: 미작성. 아래 `배경과 문제 정의`의 현장 장면은 Product Brief 작성 전의 가설이다.
- 관련 ADR: [ADR-0001](./0001-use-kotlin-as-primary-language.md), [ADR-0002](./0002-use-spring-boot-as-application-platform.md), [ADR-0004](./0004-record-outbound-product-attribute-candidates.md)
- 대체한 ADR: 없음
- 대체된 ADR: 없음
- 검토 예정일: 입고 검수 또는 포장 시나리오를 처음 구현할 때

> 이 문서는 상품 기초 데이터(상품 마스터)를 도메인 코드로 처음 표현하기 전에 필드와 규칙을 확정하기 위한 초안이다.
> 상위 Product Brief와 PRD가 연결되기 전에는 `Proposed`로 전환하지 않는다.

## 한 문장 결정

> 창고 현장이 상품 정보를 믿고 입고 검수, 적치, 피킹, 포장을 할 수 있어야 하는 상황에서,
> 실물에 없는 값이나 임시 값이 데이터에 들어가지 않게 하기 위해
> 낱개·인박스·아웃박스 3단계 고정 구조와 등록 시점의 규격 필수 입력, LOT·시리얼·유통기한 3단계 관리 정책을 선택한다.
> 측정 전 상태 허용, 임시 값 입력, 범용 포장 단위 계층은 채택하지 않는다.
> 그 대가로 규격을 모르는 상품은 등록할 수 없고, 팔레트나 4단계 이상 포장은 이후 구조 변경이 필요하다.

## 배경과 문제 정의

mini-WMS의 주 사용자는 창고 현장이다. 현장 작업은 상품 정보가 실물과 맞는다는 전제 위에서 이루어진다.
상품 정보가 틀리거나 비어 있을 때 현장이 막히는 장면은 다음 두 가지로 정리했다.
두 장면 모두 프로젝트 소유자가 제시한 문제 인식이며, 인터뷰나 운영 데이터로 확인하지는 않았다(`가설`).

1. **입고·출고 검수와 내품 검수 장면**: 작업자가 상품을 스캔했는데 등록된 SKU나 바코드가 실물과 다르다.
   그러면 맞는 물건이 맞는 수량만큼 들어왔는지 또는 나가는지 시스템으로 확인할 수 없고, 작업자는 육안이나 수기 확인으로 돌아간다.
   박스를 열어 안에 든 상품과 수량이 등록 정보와 맞는지 확인하는 내품 검수도 같은 문제를 겪는다. 바코드뿐 아니라 인박스·아웃박스 입수량이 틀려도 내품 검수 결과를 믿을 수 없다.
2. **적치·포장 장면**: 상품의 크기·무게나 인박스·아웃박스 구성이 비어 있거나 틀리다.
   그러면 어느 로케이션에 들어가는지, 어떤 포장 박스를 써야 하는지 시스템이 판단할 수 없고, 현장이 감으로 결정한다.

두 장면의 공통 원인은 상품 기초 데이터가 실물을 정확하게 표현하지 못하는 것이다.
이번 결정은 그 데이터를 어떤 필드와 규칙으로 표현할지 정한다.

이 결정이 해결하지 않는 문제:

- 등록된 값이 실제로 실물과 맞는지 확인하는 일. 이 일은 검수·실측 프로세스의 몫이다.
- 입고 검수, 적치 추천, 포장 박스 추천 같은 작업 자체

## 상위 제품 근거

| 항목 | 내용 | 상위 문서 근거 |
| --- | --- | --- |
| 타깃 오디언스 | 창고 현장 작업자와 현장 관리자 | Product Brief 미작성. 프로젝트 소유자 진술 |
| 북극성 시나리오 | 미작성 | Product Brief 미작성 |
| 첫 마일스톤의 사용자 결과 | 미작성 | PRD 미작성 |
| 관련 기능 요구사항 | 위 두 현장 장면(검수, 적치·포장) | `가설` |
| 관련 비기능 요구사항 | 미작성 | PRD 미작성 |

## 범위와 비범위

### 범위

- 상품 기초 데이터의 필드 목록, 필수 여부와 값 규칙(불변식)
- 포장 단계(낱개·인박스·아웃박스)의 표현 방식
- LOT·시리얼·유통기한 관리 정책의 의미
- 이 규칙을 순수 도메인 코드와 단위 테스트로 표현하는 것

### 비범위

- 영속성(DB 스키마, JPA/JDBC 선택), API, 화면
- SKU 중복 검사. 유일성 규칙은 이 문서에서 정하지만, 실제 검사는 저장소가 생길 때 구현한다.
- 입고 검수, 적치, 피킹, 보충, 포장 박스 추천(카토나이제이션) 로직
- 팔레트 단계(팔레트당 아웃박스 적재 수량)
- 상품당 바코드 여러 개, 포장 단계별 바코드
- 아웃박스 무게
- 출고불가 기준일, 입고 허용 잔여 유통기한, 제조일 기준 유통기한 계산
- X12, UN/ECE, SAP 같은 외부 단위 코드와의 변환
- 재고가 있는 상품의 입수량 변경 제한(아래 `열린 질문` 참고)
- 바코드 형식 검증(GTIN 체크 디지트 등)
- 송장 발급, 채널 출고(FBA, FBT), 해외 통관에 필요한 상품 속성(아웃박스 무게, 채널 바코드, HS코드, 원산지, 위험물, 보관 온도 등). 후보로만 [ADR-0004](./0004-record-outbound-product-attribute-candidates.md)에 기록한다.

## 제약과 전제

| 구분 | 내용 | 근거 또는 확인 방법 |
| --- | --- | --- |
| 제약 | 주 사용자는 창고 현장이며, 현장 작업은 등록된 상품 정보에 의존한다. | 프로젝트 소유자 진술 |
| 제약 | 구현 언어와 플랫폼은 Kotlin과 Spring Boot다. 이번 범위는 프레임워크에 의존하지 않는 도메인 코드다. | ADR-0001, ADR-0002 |
| 제약 | 지금 시나리오가 요구하는 가장 좁은 설계를 우선한다. | `AGENTS.md` 기획 문서 작성 규칙 |
| 전제 | 상품을 등록하는 시점에 낱개와 박스 규격을 실측할 수 있다. | `가설`. 첫 도그푸딩에서 확인 |
| 가설 | 낱개·인박스·아웃박스 3단계면 초기 대상 상품을 표현할 수 있다. | 첫 상품 데이터 입력 시 확인 |
| 가설 | 포장 단위 4종(`EACH`, `PACK`, `BOX`, `CARTON`)으로 현장이 실물을 구분할 수 있다. | 도그푸딩 마찰 로그 |

## 결정 기준

| 우선순위 | 결정 기준 | 프로젝트에서 중요한 이유 | 검증 방법 |
| --- | --- | --- | --- |
| 1 | 현장 작업에 필요한 실물 정보가 등록 시점에 확보된다 | 규격과 입수량이 없으면 검수 수량 환산, 적치, 포장 판단을 할 수 없다. | 필수 값이 빠진 상품을 만들 수 없음을 단위 테스트로 확인 |
| 2 | 실물에 없는 값이나 임시 값이 데이터에 들어가지 않는다 | 임시 값은 진짜 값과 구분되지 않아 데이터 문제를 시스템이 감지할 수 없다. 존재하지 않는 박스를 지시하면 현장이 혼란스러워진다. | 인박스 `없음`과 측정값을 타입으로 구분 |
| 3 | 현재 시나리오에 필요한 가장 좁은 모델이다 | 미래 요구를 미리 일반화하면 변경 비용과 학습 비용이 늘어난다. | 리뷰에서 사용되지 않는 필드·추상화가 없는지 확인 |
| 4 | 기존 WMS 관행과 대응할 수 있다 | 이후 외부 연동이나 학습 자료와 비교할 때 개념을 맞출 수 있어야 한다. | 아래 `근거 비교`의 대응 관계 |

## 검토한 선택지

결정은 여섯 가지 쟁점으로 나뉜다.

### D1. 규격(크기·무게)을 언제 받는가

- A. 등록할 때 반드시 실측값을 받는다 (**채택**)
- B. 등록 후 `미측정` 상태를 허용하고 첫 입고 때 실측한다
- C. 형식상 필수로 두고 모르면 `1` 같은 임시 값을 넣는다

### D2. 인박스가 없는 상품을 어떻게 표현하는가

- A. 인박스를 `없음`으로 명시할 수 있게 한다 (**채택**)
- B. 인박스를 항상 두고, 없으면 낱개 값(입수량 1, 낱개 규격)을 복사한다
- C. CJ대한통운의 `단수여부`처럼 별도 플래그로 구분한다

### D3. LOT·시리얼·유통기한 관리 여부를 몇 단계로 두는가

- A. 필수 / 선택 / 비허용 3단계 (**채택**)
- B. 사용 / 미사용 2단계

### D4. 포장 단계를 어떻게 모델링하는가

- A. 낱개·인박스·아웃박스 고정 3단계 (**채택**)
- B. 단계 수를 자유롭게 늘릴 수 있는 범용 단위 계층(SAP EWM의 대체 단위, 포장 명세 방식)

### D5. 포장 단위 코드를 어떻게 정하는가

- A. 고정 목록 `EACH`, `PACK`, `BOX`, `CARTON` (**채택**)
- B. 고정 목록 `EACH`, `PACK`, `CARTON`
- C. 자유 입력

### D6. 바코드를 몇 개 두는가

- A. 상품당 1개 (**채택**)
- B. 대표 바코드 1개와 추가 바코드 여러 개, 또는 포장 단계별 바코드

## 근거 비교

| 쟁점 | 선택지 | 확인된 사실 | 프로젝트에 대한 해석 | 출처 |
| --- | --- | --- | --- | --- |
| D1 | C | CJ대한통운은 부피·가로·세로·높이·중량을 모두 1로 입력하게 하고, 초도 입고 때 센터가 실측해 등록한다. Extensiv도 해당 없으면 규격에 1을 넣게 한다. | 임시 값은 진짜 값과 구분되지 않아, "규격이 제대로 안 되어 있다"는 문제를 시스템이 감지할 수 없게 만든다. | [CJ대한통운 품목 등록](https://docs.channel.io/cjlogistics/ko/articles/%ED%92%88%EB%AA%A9-%EB%93%B1%EB%A1%9D-dd38cbb0), [Extensiv Import Items](https://3w.extensiv.com/presentationtier/help/en/wms_items_importitems.htm) |
| D1 | A, B | Oracle WMS는 낱개 길이·너비·높이·무게·부피가 cubing, 적치, 보충 같은 기능에 필요하다고 설명한다. | 규격 없이는 현장 판단 기능을 쓸 수 없다. 현장이 주 사용자이므로 등록 시점에 받는 A를 택한다. | [Oracle WMS Description of Item fields](https://docs.oracle.com/en/cloud/saas/warehouse-management/24a/owmol/additional-fields-item-details.html) |
| D2 | A | Oracle WMS는 `std_pack_qty`·`std_case_qty`가 없으면 해당 포장 단위를 정의할 수 없다. 사방넷은 인박스 항목이 없고 카톤 규격도 선택이다. | 실물에 없는 단계는 데이터에서도 없음으로 둔다. | [Oracle WMS Input Interface](https://docs.oracle.com/en/cloud/saas/warehouse-management/22d/owmim/input-interface.html), [사방넷 상품 매뉴얼](https://www.sbfulfillment.co.kr/manual/product) |
| D2 | B | SPS Commerce는 인박스가 없으면 인박스 규격을 낱개 규격과 같게 넣게 한다. Extensiv는 해당 없으면 기본 단위를 다시 넣게 한다. | 존재하지 않는 박스가 데이터에 생겨 "인박스 2개 피킹" 같은 잘못된 지시로 이어질 수 있다. | [SPS Commerce Item packaging](https://help.fulfillment.spscommerce.com/en/articles/12038407-item-packaging-and-dimensions) |
| D2 | C | CJ대한통운은 `단수여부`가 N이면 입수 수량이 필수이고, Y이면 박스 바코드를 품목 바코드로 쓴다. | 낱개가 곧 박스인 경우는 아웃박스 입수량 1, 포장 단위 `EACH`로 표현할 수 있어서 별도 플래그가 필요 없다. | 위 CJ대한통운 문서 |
| D3 | A | Extensiv는 LOT·시리얼·유통기한마다 `Track`과 `Required` 플래그를 따로 둔다(시리얼은 `Must Be Unique`도 있다). Infor WMS는 입고 시 유통기한 입력을 필수로 할지 설정할 수 있다. | 추적 안 함 = 비허용, 추적만 함 = 선택, 둘 다 켬 = 필수와 같다. 3단계는 플래그 두 개를 하나의 값으로 합친 표현이다. | [Extensiv Import Items](https://3w.extensiv.com/presentationtier/help/en/wms_items_importitems.htm), [Infor Distribution A+ WMS](https://docs.infor.com/aplus/10.03.00/en-us/useradminlist/Infor%20Distribution%20A%20Warehouse%20Management%20v10.03.00_55740.pdf) |
| D3 | B | Odoo는 추적 방식(LOT/시리얼)과 유통기한 사용 여부를 켜기·끄기로 둔다. 사방넷도 유통기한 사용을 체크로 둔다. | "기록하면 좋지만 없어도 입고를 막지 않는" 경우를 표현할 수 없다. | [Odoo Expiration dates](https://www.odoo.com/documentation/master/applications/inventory_and_mrp/inventory/product_management/product_tracking/expiration_dates.html) |
| D4 | A | 일반적인 포장 계층은 낱개 → 이너팩 → 케이스 → 팔레트이고, 아래 단계와의 환산 계수를 명시한다. 아웃박스는 주로 입고 단위, 인박스는 주로 보충 단위로 쓰인다. | 인박스·아웃박스가 현재 장면에 필요한 단계다. 팔레트는 이후로 미룬다. | [Racklify UOM hierarchy](https://racklify.com/encyclopedia/what-is-uom-hierarchy-definition-components-and-why-it-matters/), [Racklify Pack size vs case pack vs inner pack](https://racklify.com/encyclopedia/pack-size-versus-case-pack-versus-inner-pack-what-warehouses-need-to-know/) |
| D4 | B | SAP EWM은 대체 단위와 포장 명세로 포장 단계를 자유롭게 정의한다. | 지금 필요하지 않은 일반화이며, `AGENTS.md`의 가장 좁은 설계 원칙과 맞지 않는다. | [SAP EWM alternative unit of measure](https://blogs.sap.com/2022/03/11/ewm-alternative-unit-of-measure/) |
| D5 | 공통 | 단위 코드는 표준이 하나가 아니다. X12는 `CA`(Case)·`CT`(Carton)·`BX`·`PK`·`PL`, UN/ECE Rec 21은 `CT`(Carton)·`CS`(Case), SAP는 `PC`·`CAR`·`PAL`, TraceLink는 `PK`를 inner pack/bundle로 정의한다. X12의 Case와 Carton 차이를 정의한 공식 자료는 찾지 못했다. | 외부 코드를 그대로 쓰지 않고 내부 고정 목록을 정의한 뒤, 연동할 때 변환한다. | [Infor Trading partner-specific UOM](https://docs.infor.com/ifsm/2025.x/en-us/ifsmolh/ifsmediug/ibq1484185321259.html), [UK trade tariff kind of packages codes](https://gov.uk/government/publications/uk-trade-tariff-kind-of-packages-codes/uk-trade-tariff-kind-of-packages-codes), [TraceLink UOM](https://opus.tracelink.com/documentation/2024.6/en-US/pie/Content/back_matter/UOM.htm) |
| D5 | B | `BOX`가 없으면 작은 종이 상자 인박스를 `PACK` 또는 `CARTON`으로 등록해야 한다. | 작업자가 비닐 묶음이나 골판지 외박스를 찾게 되어 포장 단위의 역할(실물 식별)을 해친다. | 프로젝트 소유자와의 논의 |
| D6 | B | 사방넷은 대표 바코드 1개와 추가 바코드 여러 개를 두고, 카톤 바코드에는 입수를 함께 적는다. 포장 단계마다 GTIN이 따로 있는 경우가 흔하다. | 이후에 필요해질 가능성이 높지만, 지금 장면은 상품당 1개로 충분하다. 이후 재검토한다. | [사방넷 상품 매뉴얼](https://www.sbfulfillment.co.kr/manual/product), [Racklify packaging hierarchy](https://racklify.com/encyclopedia/how-to-build-a-packaging-hierarchy-for-your-warehouse/) |

출처 대부분은 WMS 솔루션 회사의 제품 문서나 블로그다. 업계의 공통 관행이라기보다 여러 제품이 이렇게 설계했다는 참고로 사용한다.
국내 WMS의 실무 용어(박스입수, 팔레트 적재수량 등)를 정리한 자료는 확인하지 못했다(`미확인`).

## 결정

### 필드

| 필드 | 필수 여부 | 규칙 | 쓰이는 현장 작업 |
| --- | --- | --- | --- |
| SKU | 필수 | 빈 값 불가. 시스템 전체에서 유일하다(검사는 비범위). | 모든 작업의 상품 식별 |
| 상품명 | 필수 | 빈 값 불가 | 화면·라벨에서 사람이 상품을 알아봄 |
| 바코드 | 필수 | 빈 값 불가. 상품당 1개 | 입고·피킹·출고 검수와 내품 검수 스캔 |
| 규격 단위 체계 | 필수 | `METRIC` 또는 `IMPERIAL`. 상품의 모든 길이·무게 값에 공통 적용 | 규격 값 해석 |
| 낱개 길이·너비·높이 | 필수 | 0보다 큰 수 | 적치 가능 여부, 포장 박스 선택 |
| 낱개 무게 | 필수 | 0보다 큰 수 | 적재 하중, 포장 박스 무게 한도, 운임 |
| 유통기한 관리 정책 | 필수 | `REQUIRED` / `OPTIONAL` / `NOT_ALLOWED` | 입고 시 유통기한 입력, 출고 시 할당 순서 |
| 유통기한 경고일수 | 선택 | 정책이 `REQUIRED` 또는 `OPTIONAL`일 때만 입력할 수 있고, 입력하면 1 이상의 정수. `NOT_ALLOWED`이면 입력할 수 없다. | 만료 N일 전 임박 재고 경고 |
| LOT 관리 정책 | 필수 | `REQUIRED` / `OPTIONAL` / `NOT_ALLOWED` | 입고 시 LOT 기록, 출고 할당, 리콜 추적 |
| 시리얼 관리 정책 | 필수 | `REQUIRED` / `OPTIONAL` / `NOT_ALLOWED` | 낱개별 고유 번호 기록과 추적 |
| 인박스 | 선택 | `없음` 또는 아래 인박스 정보 전체 | 보충·피킹 단위 |
| 인박스 포장 단위 | 인박스가 있으면 필수 | `PACK` / `BOX` / `CARTON`. `EACH`는 쓸 수 없다. | 작업자의 실물 식별 |
| 인박스 입수량 | 인박스가 있으면 필수 | 낱개 기준 2 이상의 정수 | 수량 환산, 내품 검수 기준 수량 |
| 인박스 가로·세로·높이 | 인박스가 있으면 필수 | 0보다 큰 수 | 적치·보충 판단 |
| 아웃박스 포장 단위 | 필수 | `EACH` / `PACK` / `BOX` / `CARTON` | 작업자의 실물 식별 |
| 아웃박스 입수량 | 필수 | 낱개 기준 1 이상의 정수 | 입고 수량 환산, 내품 검수 기준 수량 |
| 아웃박스 가로·세로·높이 | 필수 | 0보다 큰 수 | 입고·적치 판단 |

### 정책 값의 의미

정책 값이 실제 작업에서 무엇을 뜻하는지는 입고·출고 기능이 없어서 아직 검증하지 않았다(`가설`).

| 값 | 의미 |
| --- | --- |
| `REQUIRED` | 해당 값(유통기한, LOT 번호, 시리얼 번호)이 없으면 작업을 진행할 수 없다. |
| `OPTIONAL` | 값이 있으면 기록하고, 없어도 작업을 막지 않는다. |
| `NOT_ALLOWED` | 해당 값을 받지 않는다. |

### 포장 단위 정의

| 값 | 정의 | 예시 |
| --- | --- | --- |
| `EACH` | 낱개 그 자체. 아웃박스가 곧 낱개일 때만 쓴다. | TV 1대가 든 박스 |
| `PACK` | 비닐, 수축필름, 띠지 등으로 묶은 형태가 단단하지 않은 포장 | 6캔 묶음, 라면 5입 멀티팩 |
| `BOX` | 형태가 있는 소형 상자 | 화장품 10개가 든 단상자 |
| `CARTON` | 운송용 골판지 외박스 | 제조사 출하 박스, 마스터 카톤 |

### 규격 단위

| 단위 체계 | 길이 | 무게 |
| --- | --- | --- |
| `METRIC` | mm | g |
| `IMPERIAL` | inch | lb |

규격 값은 소수를 허용한다. 인치법 값은 보통 소수로 표현되기 때문이다.

### 불변식

1. 필수 필드가 하나라도 빠지면 상품을 만들 수 없다. 측정 전 상태나 임시 값은 없다.
2. 모든 길이·무게 값은 0보다 크다.
3. 입수량은 항상 낱개 기준으로 센다.
4. 인박스가 있으면 인박스 입수량은 2 이상이고, 아웃박스 입수량은 인박스 입수량의 배수다.
5. 아웃박스 포장 단위가 `EACH`이면 아웃박스 입수량은 1이다. 인박스는 `EACH`를 쓸 수 없다.
6. 유통기한 경고일수는 유통기한 정책이 `NOT_ALLOWED`일 때 존재할 수 없다. 그 외에는 비워 둘 수 있으며, 값이 없으면 해당 상품은 임박 재고 경고를 하지 않는다.
7. 상품의 모든 규격 값은 하나의 단위 체계로 해석한다.

### 예시

| 상품 | 인박스 | 아웃박스 |
| --- | --- | --- |
| 음료 캔 | `PACK`, 입수량 6 | `CARTON`, 입수량 24 |
| 화장품 | `BOX`, 입수량 10 | `CARTON`, 입수량 100 |
| 의류 | 없음 | `CARTON`, 입수량 50 |
| TV | 없음 | `EACH`, 입수량 1, 규격은 낱개와 같다 |

## 결과와 영향

### 긍정적 결과

- 등록된 모든 상품은 현장 작업에 필요한 규격과 입수량을 갖는다.
- 인박스 `없음`이 명시적이라, 존재하지 않는 박스를 지시하는 일이 생기지 않는다.
- 3단계 관리 정책 덕분에 "기록하면 좋지만 막지는 않는" 운영을 표현할 수 있다.

### 부정적 결과와 감수한 비용

- 규격을 실측하지 못한 상품은 등록할 수 없다. 첫 입고 때 실측하는 운영(CJ대한통운 방식)은 지원하지 않는다.
- 팔레트 단계, 포장 단계별 바코드, 4단계 이상 포장이 필요해지면 모델 구조를 바꿔야 한다.
- 아웃박스 무게가 없어서 박스 단위 적재 하중은 낱개 무게와 입수량으로 추정해야 한다.

### 중립적 결과

- 외부 시스템과 연동할 때 내부 포장 단위 코드와 단위 체계를 외부 코드로 바꾸는 변환 계층이 필요하다.
- SKU 유일성 검사, 재고가 있는 상품의 입수량 변경 제한 같은 규칙은 영속성 계층을 설계할 때 결정해야 한다.

## 열린 질문

- 재고가 남아 있는 상품의 입수량·규격 변경을 허용할 것인가? CJ대한통운은 재고가 있으면 입수 수량을 바꿀 수 없게 한다(`미확인`: mini-WMS에서의 필요성).
- 출고불가 기준일이나 입고 허용 잔여 유통기한이 필요해지는 시점은 언제인가? 사방넷은 임박재고 전환일과 출고불가 기준일을, CJ대한통운은 입고·출고 허용 오차를 둔다.
- SKU와 바코드의 형식(길이, 허용 문자)을 제한할 것인가?
- 시리얼 관리 상품에서 시리얼 번호의 유일성 범위(상품 내, 시스템 전체)는 어떻게 정하는가?

## 재검토 조건

- 입고 검수, 적치, 포장 중 하나를 처음 구현할 때 이 필드로 충분한지 확인한다.
- 실측할 수 없는 상품 때문에 등록이 막히는 사례가 도그푸딩에서 나오면 D1을 재검토한다.
- 박스 바코드 스캔이 필요한 시나리오가 생기면 D6을 재검토한다.
- 팔레트 단위 입고나 적재가 시나리오에 들어오면 D4를 재검토한다.

## 참고 자료

- [WMS의 주요 특징 – LOT 관리 기반](../../books/wms-원리와-이해/01-wms-개요/3-WMS의-주요-특징.md)
- [사방넷 풀필먼트 – 상품 매뉴얼](https://www.sbfulfillment.co.kr/manual/product)
- [CJ대한통운 풀필먼트 – 품목 등록](https://docs.channel.io/cjlogistics/ko/articles/%ED%92%88%EB%AA%A9-%EB%93%B1%EB%A1%9D-dd38cbb0)
- [Extensiv 3PL Warehouse Manager – Import Items](https://3w.extensiv.com/presentationtier/help/en/wms_items_importitems.htm)
- [Oracle WMS Cloud – Item Master Setup](https://docs.oracle.com/en/cloud/saas/warehouse-management/22c/owmim/item-master-setup.html)
- [Oracle WMS Cloud – Description of Item fields](https://docs.oracle.com/en/cloud/saas/warehouse-management/24a/owmol/additional-fields-item-details.html)
- [Oracle WMS Cloud – Input Interface](https://docs.oracle.com/en/cloud/saas/warehouse-management/22d/owmim/input-interface.html)
- [Infor Distribution A+ Warehouse Management](https://docs.infor.com/aplus/10.03.00/en-us/useradminlist/Infor%20Distribution%20A%20Warehouse%20Management%20v10.03.00_55740.pdf)
- [Infor WMS – Configuring Shelf Life Validation](https://docs.infor.com/wms/2022.x/en-us/useradminlib/sceconfigug/our1612893584270.html)
- [Odoo – Expiration dates](https://www.odoo.com/documentation/master/applications/inventory_and_mrp/inventory/product_management/product_tracking/expiration_dates.html)
- [SPS Commerce – Item packaging and dimensions](https://help.fulfillment.spscommerce.com/en/articles/12038407-item-packaging-and-dimensions)
- [SAP EWM – Alternative unit of measure](https://blogs.sap.com/2022/03/11/ewm-alternative-unit-of-measure/)
- [Racklify – UOM hierarchy](https://racklify.com/encyclopedia/what-is-uom-hierarchy-definition-components-and-why-it-matters/)
- [Racklify – Pack size vs case pack vs inner pack](https://racklify.com/encyclopedia/pack-size-versus-case-pack-versus-inner-pack-what-warehouses-need-to-know/)
- [Racklify – How to build a packaging hierarchy](https://racklify.com/encyclopedia/how-to-build-a-packaging-hierarchy-for-your-warehouse/)
- [FCBCO – Accurate weights and dimensions](https://www.fcbco.com/blog/dimensioning-sku-inventory)
- [Infor – Trading partner-specific UOM](https://docs.infor.com/ifsm/2025.x/en-us/ifsmolh/ifsmediug/ibq1484185321259.html)
- [UK trade tariff – Kind of packages codes](https://gov.uk/government/publications/uk-trade-tariff-kind-of-packages-codes/uk-trade-tariff-kind-of-packages-codes)
- [TraceLink – UOM](https://opus.tracelink.com/documentation/2024.6/en-US/pie/Content/back_matter/UOM.htm)
