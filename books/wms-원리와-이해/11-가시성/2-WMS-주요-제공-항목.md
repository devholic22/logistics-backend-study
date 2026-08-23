# WMS 주요 제공 항목

> [가시성 (Visibility)](./README.md)

## 빠른 복습
- **가시성 확보는 시스템의 효율성, 고객 만족도, 비용 절감 등에 기여할 수 있는 중요한 기능**이다.
- 가시성을 제공하려면 세 가지가 필요하다 — **실시간 데이터 수집 · 관리된 데이터 기반의 분석 · 시각화 또는 의미 있는 정보로의 가공**.
- WMS가 제공하는 것은 셋이다 — **창고의 실제 상황을 언제든 확인**, **재고의 흐름 추적**, **문제를 즉시 확인하거나 사전에 인지하고 예방할 수 있는 체계**.
- 원서는 두 가지 화면 예시를 든다 — **창고 배치를 그대로 보여주는 Visibility 화면**과 **지표를 모아놓은 Dashboard**.

## 가시성을 만드는 세 가지 작업

> **가시성 확보는 시스템의 효율성, 고객 만족도, 비용 절감 등에 기여할 수 있는 중요한 기능**이다. **WMS 시스템에서 가시성을 제공하기 위해서는 실시간으로 데이터를 수집하고, 관리된 데이터를 기반으로 데이터를 분석하고, 이를 시각화 또는 의미 있는 정보로 가공하는 작업이 중요**하다.

```mermaid
flowchart LR
    COLLECT["실시간 데이터 수집"]
    ANALYZE["데이터 분석<br/>관리된 데이터 기반"]
    VISUAL["시각화 · 의미 있는<br/>정보로 가공"]

    COLLECT -- "① 정제 · 축적" --> ANALYZE
    ANALYZE -- "② 분석 결과 전달" --> VISUAL

    classDef core fill:#93ad70,stroke:#5f7a44,color:#121a08
    classDef sys fill:#e9e5a8,stroke:#a99f4d,color:#26240c
    class ANALYZE,VISUAL core
    class COLLECT sys
```

*수집 → 분석 → 가공. 앞 단계가 부실하면 뒤 단계는 성립하지 않는다*

**"관리된 데이터를 기반으로"** 라는 조건이 이 절의 숨은 요점이다. 수집만 해서는 안 되고 **정제되어 있어야** 분석이 된다. [3절의 2단계가 "1단계에서 데이터가 정제되고 충분히 확보되어야 한다"고 못박는 이유](./3-Visibility-추진단계.md#나-2단계--데이터-분석--오류통보)가 여기서 미리 나온다.

## WMS가 제공하는 것

> **WMS는 실제 창고의 상황을 언제든지 시스템을 통해서 확인할 수 있고, 재고의 흐름을 추적할 수 있으며, 창고에서 발생된 문제를 즉시 확인하거나 사전에 인지하고 미리 예방할 수 있는 체계를 구축할 수 있다.**

| 무엇을 제공하는가 | 성격 |
| --- | --- |
| **창고의 실제 상황을 언제든 확인** | **지금** 어떤가 |
| **재고의 흐름 추적** | **어떻게 여기까지 왔는가** |
| **문제를 즉시 확인하거나 사전 인지·예방** | **앞으로 무엇이 문제가 되는가** |

표를 읽는 법. 세 줄을 이해하기 쉽게 **현재 · 과거 · 미래**로 나눌 수 있다. 다만 엄밀한 일대일 대응은 아니다. 흐름 추적에는 현재 진행 상태와 이력이 함께 쓰이고, 문제 인지에도 현재 규칙과 과거 데이터가 함께 필요하다. [3절의 3단계 성숙도 모델](./3-Visibility-추진단계.md)은 이를 구현 난이도에 따라 **현황 → 분석·통보 → 예측·예방**으로 발전시키는 순서다.

여기서 **사전 인지·예방**은 문제가 절대 발생하지 않도록 보장한다는 뜻이 아니다. 임계치나 예측 결과로 위험 신호를 일찍 발견하고, 사람이 대응할 시간을 확보한다는 의미다.

## 두 가지 화면

원서는 실제 제품(Infor) 화면을 예시로 싣는다. 스크린샷이므로 여기서는 **무엇이 담겨 있는지**만 옮긴다.

### 창고 배치를 그대로 보여주는 화면

**[그림 11-1] WMS Visibility 화면 예시**는 **창고 전체를 3차원 배치도로 그린 화면**이다. 랙과 통로가 실제 배치대로 그려지고, **구역이 색으로 구분**되어 있다. [2장의 존 배치도](../02-wms-주요-프로세스/1-로케이션과-존.md)가 그림이 아니라 **시스템 화면으로 살아 있는 형태**라고 보면 된다.

### 지표를 모아놓은 대시보드

**[그림 11-2] WMS Dashboard 예시**는 **'Warehouse Director'** 라는 제목의 태블릿 화면으로, 네 묶음의 지표가 층층이 놓여 있다.

<div class="tbl" style="overflow-x:auto">
<table>
<thead>
<tr>
<th style="text-align:center; white-space:nowrap">묶음</th>
<th style="text-align:center; white-space:nowrap">지표</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center; white-space:nowrap"><b>Inbound</b></td>
<td style="text-align:left">Appointments · ASNs · ASN lines · Pallets · Cube <b>(일자별 추이 막대)</b></td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>Inventory</b></td>
<td style="text-align:left">Physical Inventory · Supervisor Cycle Counts <b>2</b> · <b>Cycle Count Accuracy 94%</b> · Empty Locations(%) · Held Inventory <b>1,586</b></td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>Locations</b></td>
<td style="text-align:left">Held Locations <b>43</b> · Damaged Locations <b>2</b> · Empty Locations <b>299</b> · <b>Picking Heat</b>(High / M-High / M-Low / Low)</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>Outbound</b></td>
<td style="text-align:left">Appointments · Shipment Orders · Order Lines · Pallets · Cube <b>(일자별 추이 막대)</b></td>
</tr>
</tbody>
</table>
</div>

*원서 [그림 11-2] WMS Dashboard 예시의 지표 구성 (출처: infor.com)*

표를 읽는 법. 네 묶음이 **입고 · 재고 · 로케이션 · 출고**다. 눈여겨볼 점이 셋이다.

- **입고와 출고는 일자별 막대**로, **재고와 로케이션은 현재 값 하나**로 표시된다. **흐름은 추이로, 상태는 숫자로** 보여주는 것이다.
- **Cycle Count Accuracy 94%** 처럼 **정확도 자체가 지표**로 올라와 있다. [재고조사](../06-재고관리/README.md)의 결과가 관리자 화면의 한 칸이 된다.
- **Picking Heat**(피킹 빈도의 열지도)와 **Empty Locations**가 함께 있다. **어디가 바쁘고 어디가 비어 있는지**를 나란히 보여주는 것이며, 이는 [재고보충이나 재배치](../02-wms-주요-프로세스/3-재고이동과-재고보충.md) 판단의 근거가 된다.

## 함께 읽기

- [추진단계 — 이 화면들을 어떤 순서로 만들어 가는지](./3-Visibility-추진단계.md)
- [입고 KPI — 대시보드에 올라가는 지표의 원본](../04-입고-프로세스/6-입고-체크리스트와-KPI.md)
- [작업자별 실적분석 — 같은 이력이 실적 지표가 되는 이야기](../09-권한보안관리/3-보안감사.md#나-작업자별-실적분석)
