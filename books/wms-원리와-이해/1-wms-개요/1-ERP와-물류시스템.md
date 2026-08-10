# ERP와 물류시스템

> [[1. WMS 개요/index|WMS 개요]]

## 빠른 복습

- ERP는 부문별 최적화가 아니라 **전사 차원의 최적화**를 목표로 기업 활동과 데이터를 통합 관리하는 시스템이다.
- 발전 순서는 `MRP → MRP II → ERP → Extended ERP`이고, 각 단계는 앞 단계에서 드러난 "부족한 자원"을 하나씩 끌어안으면서 확장됐다.
- 시장이 B2C·다품종 소량·글로벌 협업으로 바뀌자 ERP만으로 감당하기 어려운 물류 업무가 생겼다.
- 그 영역을 특화해 맡는 것이 물류시스템이고, 대표적으로 **OMS·WMS·TMS**가 있다.
- 물류시스템은 독립적으로 운영되지 않는다. ERP와 실시간으로 정보를 주고받으며 **ERP를 지원하는 목적**으로 개발됐다.

## ERP란 무엇인가

ERP(Enterprise Resource Planning)는 기업 활동에 필요한 인사, 재무회계, 관리회계, 영업, 구매/자재, 생산 관련 프로그램과 각종 데이터를 통합하여 관리하는 시스템이다. 핵심은 "통합"이 아니라 통합의 **목적**에 있다. 부문별로 각자의 성과를 극대화하는 것이 아니라, 전사 차원에서 최적화하여 기업 전체의 성과를 향상시키는 것이 ERP의 존재 이유다.

## 부족한 자원을 하나씩 발견해온 과정

ERP는 처음부터 지금의 모습이 아니었다. 공장에서 겪은 문제를 하나 풀면 그 다음 병목이 드러나는 식으로 확장됐다.

**1단계 — MRP(Materials Requirement Planning), 원부자재 소요 계획**

공장에서 제품을 생산하려면 원부자재가 부족하지 않아야 한다. 부족할 품목을 미리 계산해 사전에 발주함으로써 생산량을 최대한 높이려는 시스템이 MRP다.

**2단계 — MRP II(Manufacturing Resource Planning), 생산능력까지 확장**

그런데 원부자재를 부족하지 않게 공급해도 그것을 가공할 **설비가 부족할 수 있다**. 여기서 MRP II 개념이 나왔다. 생산에 필요한 인력과 공장 설비의 능력을 함께 종합적으로 고려하고 이를 생산 계획과 관리에 반영하면서, 훨씬 정교한 생산 관리 체계를 갖출 수 있게 됐다.

**3단계 — ERP, 돈과 영업까지 확장**

MRP II도 한계가 있었다. 원부자재를 매입하고 생산 설비를 도입하려면 결국 **'돈'이라는 유한한 자원**이 필요하다. 그리고 영업 활동을 통해 만들어진 제품이 잘 팔려야 그 제품이 다시 돈과 이익으로 환원되어 생산활동에 재투입된다. 즉 영업 상황을 보면서 부족하거나 잘 팔리는 제품 위주로 생산해야 한다. 이 순환을 관리하기 위해 재무를 포함한 ERP가 등장했다.

**4단계 — Extended ERP, 고객과 협력사까지 확장**

기업 내부를 넘어 고객과 협력사까지 관리 범위에 들어온 형태다.

이 과정을 거쳐 ERP는 재무회계를 기반으로 인사, 구매, 생산, 영업, 물류 등 기업의 모든 활동을 관리하고 최적화하는 시스템이 되었다. 각 단위 활동의 극대화가 아니라 **기업 이윤의 극대화**를 위한 필수 시스템으로 자리 잡았다.

<div class="tbl" style="overflow-x:auto">
<table>
<thead>
<tr>
<th style="text-align:center; white-space:nowrap">단계</th>
<th style="text-align:center; white-space:nowrap">관리 범위</th>
<th style="text-align:center; white-space:nowrap">새로 끌어안은 자원</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center; white-space:nowrap">MRP</td>
<td style="text-align:left; white-space:nowrap">원부자재 소요 계획</td>
<td style="text-align:center; white-space:nowrap">자재</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">MRP II</td>
<td style="text-align:left; white-space:nowrap">MRP + 인력·설비 등 생산능력</td>
<td style="text-align:center; white-space:nowrap">인력, 설비</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">ERP</td>
<td style="text-align:left; white-space:nowrap">MRP II + 재무 등 전사</td>
<td style="text-align:center; white-space:nowrap">돈, 영업</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">Extended ERP</td>
<td style="text-align:left; white-space:nowrap">ERP + 고객·협력사</td>
<td style="text-align:center; white-space:nowrap">외부 관계</td>
</tr>
</tbody>
</table>
</div>

## 기업 환경의 변화

기업 환경은 계속 움직인다.

- 고객의 다양한 요구를 반영하기 위해 **다품종 소량 체제를 넘어 고객별 맞춤형**으로 진화하고 있다.
- 오프라인 위주의 B2B 시장에서 고객과 직접 거래하는 **모바일 B2C 시장**으로 빠르게 이동하고 있다.
- 기업 단위의 생산·구매·영업·마케팅 활동에서 벗어나 **기업 간 글로벌 협업**도 필수 활동이 되었다.

이에 맞춰 ERP도 고객 관계 관리(CRM, Customer Relationship Management)와 공급망관리(SCM, Supply Chain Management) 같은 시스템과 통합하거나 확장할 수 있는 방향으로 발전하고 있다.

## 물류시스템이 따로 필요해진 이유

과거, 즉 생산력과 영업력만 있으면 되었던 시기에는 전문적인 물류관리 시스템에 대한 요구가 거의 없었다. ERP 시스템만으로도 충분히 업무가 가능했다.

상황이 바뀐 계기는 두 가지다. 시장이 글로벌화되었고, B2B 위주의 시장에서 직접 고객을 상대하는 B2C 채널이 다양해졌다. 그 결과 다품종 소량생산이 일반화되었고, 유통기한·로트번호·일련번호 등을 관리해야 하는 복잡한 물류시스템의 필요성이 대두됐다.

물류시스템은 전체 최적화 관점의 ERP가 대응하기 어려운 재고관리, 주문, 수배송 등 다양하고 복잡한 물류 업무를 효율적으로 수행할 수 있도록 **특화된 시스템**이다. 중요한 것은 위치다. 물류시스템은 독립적으로 운영되지 않고, ERP와 실시간으로 정보를 주고받으면서 ERP를 지원하기 위한 목적으로 개발됐다.

<div class="tbl" style="overflow-x:auto">
<table>
<thead>
<tr>
<th style="text-align:center; white-space:nowrap">시스템</th>
<th style="text-align:center; white-space:nowrap">풀 네임</th>
<th style="text-align:center; white-space:nowrap">맡는 일</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center; white-space:nowrap">OMS</td>
<td style="text-align:left; white-space:nowrap">Order Management System</td>
<td style="text-align:left">주문을 접수하고 ERP와 연계하며, 주문 접수를 대행</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">WMS</td>
<td style="text-align:left">Warehouse Management System</td>
<td style="text-align:left">창고에 보관된 제품을 체계적으로 보관하고 출고</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">TMS</td>
<td style="text-align:left">Transportation Management System</td>
<td style="text-align:left; white-space:nowrap">차량 등 운송수단으로 고객에게 안전하게 전달</td>
</tr>
</tbody>
</table>
</div>

## 함께 읽기

- WMS의 정의와 기본 목적은 [[1. WMS 개요/2. WMS 시스템이란|WMS 시스템이란]]에서 이어진다.
