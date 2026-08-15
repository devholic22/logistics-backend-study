# 재고관리

## 재고관리란

> 창고 내 재고를 **최적의 수준으로 유지**하고 이를 **효율적으로 관리**하기 위한 활동

기업의 경쟁력 강화를 위해 중요한 경영활동 중의 하나로 평가된다. **재고비용 절감, 매출 증대** 등의 효과를 기대할 수 있다.

## 주요 기능

<div class="tbl" style="overflow-x:auto">
<table>
<thead>
<tr>
<th style="text-align:center; white-space:nowrap">구분</th>
<th style="text-align:center; white-space:nowrap">기능</th>
<th style="text-align:center; white-space:nowrap">내용</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center; white-space:nowrap">1</td>
<td style="text-align:left; white-space:nowrap"><b>재고 조회</b> (Inventory Report)</td>
<td style="text-align:left; white-space:nowrap">창고 내 재고를 여러 관점으로 실시간 조회</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">2</td>
<td style="text-align:left; white-space:nowrap"><b>재고이동</b> (Move)</td>
<td style="text-align:left">로케이션에서 다른 로케이션으로 재고를 이동시킴</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">3</td>
<td style="text-align:left; white-space:nowrap"><b>재고 보류</b> (Hold)</td>
<td style="text-align:left">특정 제품 또는 로케이션의 재고를 이동이나 할당하지 못하도록 함</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">4</td>
<td style="text-align:left; white-space:nowrap"><b>재고 상태 변경</b> (Status change)</td>
<td style="text-align:left">특정 로케이션의 재고 상태를 변경함 (예: 정상 → 불량, 불량 → 정상)</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">5</td>
<td style="text-align:left"><b>재고 조사</b> (Taking, Cycle count)</td>
<td style="text-align:left; white-space:nowrap">주기적으로 재고가 일치하는지를 확인·관리</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">6</td>
<td style="text-align:left; white-space:nowrap"><b>재고 조정</b> (Adjustment)</td>
<td style="text-align:left">실제 재고와 전산상 재고를 일치시키기 위해 로케이션 재고를 조정함 (사유 관리)</td>
</tr>
</tbody>
</table>
</div>

### 여섯 기능은 세 부류다

```mermaid
%% lint: layout  기능을 성격별로 묶은 분류도다. 재고 흐름이 아니다
flowchart LR
    subgraph SEE["보기"]
        F1["① 재고 조회"]
    end
    subgraph CHG["바꾸기"]
        F2["② 재고이동"]
        F3["③ 재고 보류"]
        F4["④ 재고 상태 변경"]
    end
    subgraph FIT["실물과 맞추기"]
        F5["⑤ 재고 조사"]
        F6["⑥ 재고 조정"]
    end

    F5 -. "차이 발견" .-> F6

    classDef see fill:#e9e5a8,stroke:#a99f4d,color:#26240c
    classDef chg fill:#93ad70,stroke:#5f7a44,color:#121a08
    classDef fit fill:#b9a8d0,stroke:#7f6a9e,color:#1a1224
    class F1 see
    class F2,F3,F4 chg
    class F5,F6 fit
    style SEE fill:none,stroke:#9aa0a6,stroke-dasharray: 4 4
    style CHG fill:none,stroke:#9aa0a6,stroke-dasharray: 4 4
    style FIT fill:none,stroke:#9aa0a6,stroke-dasharray: 4 4
```

*여섯 기능의 성격 — 보기 / 바꾸기 / 실물과 맞추기*

- **보기** — 재고를 건드리지 않는다. 어떤 관점으로 볼 것인가의 문제다.
- **바꾸기** — WMS 안에서 재고의 **위치·가용성·등급**을 바꾼다. 총 수량은 그대로다.
- **실물과 맞추기** — 실물과 전산의 차이를 **발견하고(조사) 메운다(조정)**. 조정 과정에서는 보관·조정 로케이션의 수량 구성이 바뀌고, WMS 전체 수량은 화주와 최종 정산하기 전까지 유지된다.

## 재고관리가 손대는 것

각 기능이 재고의 무엇을 건드리는지 정리하면 헷갈림이 줄어든다.

<div class="tbl" style="overflow-x:auto">
<table>
<thead>
<tr>
<th style="text-align:center; white-space:nowrap">기능</th>
<th style="text-align:center; white-space:nowrap">위치</th>
<th style="text-align:center; white-space:nowrap">가용성</th>
<th style="text-align:center; white-space:nowrap">등급</th>
<th style="text-align:center; white-space:nowrap">총 수량</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center; white-space:nowrap">재고이동</td>
<td style="text-align:center; white-space:nowrap"><b>바뀜</b></td>
<td style="text-align:center; white-space:nowrap"></td>
<td style="text-align:center; white-space:nowrap"></td>
<td style="text-align:center; white-space:nowrap">그대로</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">재고 보류</td>
<td style="text-align:center; white-space:nowrap"></td>
<td style="text-align:center; white-space:nowrap"><b>막힘</b></td>
<td style="text-align:center; white-space:nowrap"></td>
<td style="text-align:center; white-space:nowrap">그대로</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">재고 상태 변경</td>
<td style="text-align:center; white-space:nowrap"></td>
<td style="text-align:center; white-space:nowrap"></td>
<td style="text-align:center; white-space:nowrap"><b>바뀜</b></td>
<td style="text-align:center; white-space:nowrap">그대로</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">재고 조정</td>
<td style="text-align:center; white-space:nowrap"></td>
<td style="text-align:center; white-space:nowrap"></td>
<td style="text-align:center; white-space:nowrap"></td>
<td style="text-align:center; white-space:nowrap"><b>바뀜</b></td>
</tr>
</tbody>
</table>
</div>

## 목차

- [재고 조회](./1-재고-조회.md)
- [재고이동](./2-재고이동.md)
- [재고 보류](./3-재고-보류.md)
- [재고 상태변경](./4-재고-상태변경.md)
- [재고조사](./5-재고조사.md)
- [재고조정](./6-재고조정.md)
- [작업관리](./7-작업관리.md)
- [재고관리 체크리스트와 KPI](./8-재고관리-체크리스트와-KPI.md)

## 함께 읽기

- 2장의 개관은 [재고관리](../2-wms-주요-프로세스/5-재고관리.md)에 있다. 6장은 그것을 상세히 펼친 것이다.
- 보류한 재고를 어디에 두는가에 대한 보충은 [여기](../2-wms-주요-프로세스/5-재고관리.md#보류한-재고는-어디에-두는가)에 정리해 두었다.

