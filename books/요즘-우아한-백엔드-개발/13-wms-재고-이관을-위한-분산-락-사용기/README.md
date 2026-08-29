# WMS 재고 이관을 위한 분산 락 사용기

## 취소된 이관 요청서에 재고가 할당되어 있다

이 장은 **WMS에서 재고를 이관하는 과정에서 마주친 동시성 문제의 해결 과정**을 다룬다. 제보는 현장에서 왔다 — **취소된 이관 요청서에 재고가 할당되어 있다**는 DC 관리자의 문의였다.

원인은 하나였고, 그것을 고치는 방법은 세 번 바뀌었다. **분산 락을 거는 것만으로는 부족했고, 대기시켰더니 느려졌고, 마지막에 상태 키를 함께 쓰고서야 "막을 것은 막고 병렬로 할 것은 병렬로" 되었다.**

```mermaid
flowchart LR
    S0["문제<br/>취소에 락이 없다"]
    S1["1단계<br/>분산 락 추가"]
    S2["2단계<br/>분산 락 대기"]
    S3["3단계<br/>분산 락 + 상태 키"]

    S0 --> S1
    S1 -- "N개 SKU 중 첫 건만 성공" --> S2
    S2 -- "SKU가 늘수록 느려짐" --> S3

    %% lint-ok: DEAD-END  해결 방법이 바뀌어 간 순서를 보여주는 도식이므로 마지막 단계에서 나가는 흐름이 없다
    classDef core fill:#93ad70,stroke:#5f7a44,color:#121a08
    classDef sys fill:#e9e5a8,stroke:#a99f4d,color:#26240c
    classDef muted fill:#dcdcd2,stroke:#a8a89c,color:#3a3a30
    class S3 core
    class S1,S2 sys
    class S0 muted
```

*해결책이 두 번 바뀐 이유는 각 단계가 새 문제를 만들었기 때문이다*

## WMS가 하는 일과 재고 이관의 자리

**WMS(Warehouse Management System)는 물류센터에서 반복되는 수기 작업을 시스템화하여 안정적으로 운영되게 한다.**

- **발주 상품 입고 및 검수/검품**(수량, 품질, 소비기한)
- **실시간 재고 정보 관리**
- **고객 주문 정보에 따른 신속하고 정확한 상품 출고**

```mermaid
flowchart LR
    SUP["공급업체"]
    DC["DC<br/>중앙물류기지"]
    PPC["PPC<br/>피킹패킹센터"]
    CUST["고객"]

    SUP -- "입고" --> DC
    DC -- "재고 이관" --> PPC
    PPC -- "주문 출고" --> CUST

    %% lint-ok: DEAD-END  물류 흐름의 종착점이 고객이므로 나가는 흐름이 없다
    %% lint-ok: NO-INBOUND  공급업체는 흐름의 출발점이므로 들어오는 흐름이 없다
    classDef core fill:#93ad70,stroke:#5f7a44,color:#121a08
    classDef sys fill:#e9e5a8,stroke:#a99f4d,color:#26240c
    classDef muted fill:#dcdcd2,stroke:#a8a89c,color:#3a3a30
    class DC,PPC core
    class SUP sys
    class CUST muted
```

*이 장이 다루는 구간은 가운데 — **DC에서 PPC로의 재고 이관**이다*

창고 안에서의 단계는 이렇게 이어진다.

```mermaid
flowchart LR
    A["상품 입고"]
    B["적재"]
    C["재고 관리"]
    D["분배 · 배치"]
    E["재고 보충"]
    F["상품 피킹"]
    G["상품 패킹"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G

    %% lint-ok: DEAD-END  작업 순서를 나열한 도식이므로 마지막 단계에서 나가는 흐름이 없다
    %% lint-ok: NO-INBOUND  상품 입고가 순서의 출발점이므로 들어오는 흐름이 없다
    classDef sys fill:#e9e5a8,stroke:#a99f4d,color:#26240c
    class A,B,C,D,E,F,G sys
```

*WMS가 관장하는 창고 내 작업 순서*

## 목차

- [이관 요청서와 할당](./1-이관-요청서와-할당.md)
- [할당과 취소가 동시에 요청된다면](./2-할당과-취소가-동시에-요청된다면.md)
- [분산 락을 걸고, 기다리게 해보다](./3-분산-락을-걸고-기다리게-해보다.md)
- [분산 락과 상태 키 함께 사용하기](./4-분산-락과-상태-키-함께-사용하기.md)

## 함께 읽기

- [『WMS 원리와 이해』](../../wms-원리와-이해/README.md) — 이 장의 용어가 전부 그 책의 것이다. 특히 [5.4 할당(출고지시)](../../wms-원리와-이해/05-출고-프로세스/4-할당-출고지시.md)과 [6.2 재고이동](../../wms-원리와-이해/06-재고관리/2-재고이동.md).
- [11장 OMS 출고 최적화](../11-b마트-oms의-물류주문관리를-통한-출고-최적화/README.md) — 같은 물류 도메인에서 **동시성과 순서**를 다룬 다른 사례.
- [2장 도메인 모듈 분리](../02-전체-서비스를-관통하는-도메인-모듈-안전하게-분리하기/README.md) — 이 장의 문제도 결국 **트랜잭션 경계를 어디에 그을 것인가**의 이야기다.

## 참고

- 원 소스: 우아한형제들 기술블로그, [WMS 재고 이관을 위한 분산 락 사용기](https://techblog.woowahan.com/17416/)
