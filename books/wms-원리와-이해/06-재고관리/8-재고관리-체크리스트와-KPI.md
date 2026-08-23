# 재고관리 체크리스트와 KPI

> [재고관리](./README.md)

## 빠른 복습

- 입고·출고와 같은 **범용 예시**다. 각 창고의 특성에 맞게 **수정·보완해서 쓰라**고 명시한다.
- 체크리스트 9개는 입고·출고와 성격이 다르다. **작업 절차가 아니라 창고라는 공간의 상태**를 본다. 청결·설비·출입통제·화재 위험이 들어온다.
- KPI 6개는 **정확도 · 회전 · 공간 · 품질**의 네 갈래다.
- 입고·출고 KPI가 **작업 성적**을 쟀다면, 재고관리 KPI는 **자산의 상태**를 잰다. 그래서 수량이 아니라 **금액 기준 지표가 많다.**

## 가. 재고관리 체크리스트 (예시)

<div class="tbl" style="overflow-x:auto">
<table>
<thead>
<tr>
<th style="text-align:center; white-space:nowrap">순번</th>
<th style="text-align:center; white-space:nowrap">내용</th>
</tr>
</thead>
<tbody>
<tr><td style="text-align:center; white-space:nowrap">1</td><td style="text-align:left; white-space:nowrap">재고는 잘 정리되어 있고 청결한가?</td></tr>
<tr><td style="text-align:center; white-space:nowrap">2</td><td style="text-align:left; white-space:nowrap">재고조사는 주기적으로 잘 시행하고 있는가?</td></tr>
<tr><td style="text-align:center; white-space:nowrap">3</td><td style="text-align:left">창고내 파손되거나 고장난 설비나 장비는 없는가?</td></tr>
<tr><td style="text-align:center; white-space:nowrap">4</td><td style="text-align:left">창고내 재고 적재물이나 작업오류물 등은 적정한가?</td></tr>
<tr><td style="text-align:center; white-space:nowrap">5</td><td style="text-align:left">반품 또는 유통기한 초과 등의 제품이 있는가?</td></tr>
<tr><td style="text-align:center; white-space:nowrap">6</td><td style="text-align:left">외래방문자 출입통제 및 기록관리는 잘 되고 있는가?</td></tr>
<tr><td style="text-align:center; white-space:nowrap">7</td><td style="text-align:left; white-space:nowrap">창고내 흡연 또는 화재의 위험은 없는가?</td></tr>
<tr><td style="text-align:center; white-space:nowrap">8</td><td style="text-align:left">전표 및 기록양식, 출력물 등은 잘 정리 보관되고 있는가?</td></tr>
<tr><td style="text-align:center; white-space:nowrap">9</td><td style="text-align:left">표시물이나 안내판 등이 훼손되거나 적치하지 않은 것들이 있는가?</td></tr>
</tbody>
</table>
</div>

원서 표에는 **확인/비고** 열이 비어 있다. 점검하며 채우는 양식이다.

### 입고·출고 체크리스트와 무엇이 다른가

입고와 출고 체크리스트는 **그날의 작업**을 점검했다. 사전 계획, 인원·장비, 제품 상태, 수량, 출력물 관리 순이었다.

재고관리 체크리스트는 **창고라는 공간 자체**를 본다.

<div class="tbl" style="overflow-x:auto">
<table>
<thead>
<tr>
<th style="text-align:center; white-space:nowrap">성격</th>
<th style="text-align:center; white-space:nowrap">항목</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center; white-space:nowrap"><b>정리 상태</b></td>
<td style="text-align:left">1, 4, 9 — 재고 정리·청결, 적재물, 표시물</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>주기 업무</b></td>
<td style="text-align:left; white-space:nowrap">2 — 재고조사 시행</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>설비</b></td>
<td style="text-align:left; white-space:nowrap">3 — 파손·고장난 설비·장비</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>재고 건전성</b></td>
<td style="text-align:left; white-space:nowrap">5 — 반품·유통기한 초과 제품</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>보안·안전</b></td>
<td style="text-align:left">6, 7 — 외래방문자 출입통제, 흡연·화재 위험</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>문서</b></td>
<td style="text-align:left; white-space:nowrap">8 — 전표·기록양식·출력물</td>
</tr>
</tbody>
</table>
</div>

**보안(6번)과 화재(7번)가 여기서 처음 등장한다.** 입고·출고 체크리스트에는 없던 항목이다. 재고는 그 자리에 오래 머무는 자산이라, 지키고 태우지 않는 것이 관리 항목이 된다.

## 나. 재고관리 KPI (예시)

<div class="tbl" style="overflow-x:auto">
<table>
<thead>
<tr>
<th style="text-align:center; white-space:nowrap">구분</th>
<th style="text-align:center; white-space:nowrap">계산 수식</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center; white-space:nowrap"><b>재고정확도 (%)</b></td>
<td style="text-align:left">재고정확도 = Σ min(실물수량, WMS수량) / Σ max(실물수량, WMS수량) × 100<br>※ 실물 조사 대상 로케이션만 집계</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>재고회전율</b></td>
<td style="text-align:left; white-space:nowrap">재고회전율 = 당월출고금액 / 월평균재고금액</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>재고보유일수</b></td>
<td style="text-align:left">재고보유일수 = 해당 월의 일수 / 재고회전율</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>재고적재율 (%)</b></td>
<td style="text-align:left">재고적재율 = 재고보관된 로케이션수 / 총로케이션수 × 100<br>재고적재율 = 보관재고수량 / 최대적재수량 × 100</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>장기재고율 (%)</b></td>
<td style="text-align:left">장기재고율 = 장기재고금액(6개월이상) / 월평균재고금액 × 100</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>불량재고율 (%)</b></td>
<td style="text-align:left">불량재고율 = 불량재고금액(C등급재고금액) / 월평균재고금액 × 100</td>
</tr>
</tbody>
</table>
</div>

> 수식 교정: 원서의 `재고실사오류수량 / 총보유재고수량 × 100`은 **재고오류율**에 해당한다. 위 표는 로케이션·제품·로트 등 정한 집계 단위마다 실물과 WMS 중 작은 수량을 **일치 수량**, 큰 수량을 **비교 대상 수량**으로 보고 합산한다. 과부족이 서로 상쇄되지 않고 결과가 0~100% 범위를 벗어나지 않는다. 비교 대상 수량의 합이 0이면 재고가 없는 조사이므로 정확도를 계산하지 않는다.
>
> 재고조정용 가상 로케이션처럼 실물이 없고 음수 장부를 허용하는 곳은 재고정확도 집계에서 제외한다. 이런 잔액은 [재고조정](./6-재고조정.md#임시재고-최종-정리)의 **ERP 대사·임시재고 정리 대상**으로 별도 관리한다.

### 수식 적용 전에 기준을 고정한다

- **재고정확도 집계 단위** — 제품만 볼지, `로케이션 × 제품 × 로트`까지 볼지 먼저 정한다. 같은 제품의 A 로케이션이 WMS보다 10개 부족하고 B 로케이션이 10개 많을 때 제품 총량은 같아도, 집계 단위별 `min / max` 방식에서는 두 위치 모두 불일치로 반영된다.
- **집계 대상 로케이션** — 실물을 직접 셀 수 있는 보관·피킹·작업 로케이션만 포함한다. 음수 장부를 허용하는 재고조정용 가상 로케이션은 정확도가 아니라 ERP 대사 항목으로 관리한다.
- **금액 평가 기준** — 재고회전율의 당월출고금액과 월평균재고금액은 원가·표준원가 등 **같은 평가 기준**으로 산출해야 한다.
- **월평균재고** — 일별 재고금액 평균을 쓰거나 단순화해 `(월초재고금액 + 월말재고금액) / 2`를 쓸 수 있다. 어떤 방식을 택하든 기간별로 동일하게 적용한다.
- **기간의 일수** — 보유일수는 30일로 고정하지 않고 28~31일인 **해당 월의 실제 일수**를 쓴다. 30일 예시는 비교를 단순화할 때만 사용한다.
- **장기재고 기준** — “6개월 이상”의 기준일과 마지막 입고일·마지막 출고일·마지막 이동일 중 어느 날짜를 사용할지 정해야 지표를 반복 계산할 수 있다.

### 네 갈래로 읽는다

<div class="tbl" style="overflow-x:auto">
<table>
<thead>
<tr>
<th style="text-align:center; white-space:nowrap">갈래</th>
<th style="text-align:center; white-space:nowrap">지표</th>
<th style="text-align:center; white-space:nowrap">무엇을 보는가</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center; white-space:nowrap"><b>정확도</b></td>
<td style="text-align:left; white-space:nowrap">재고정확도</td>
<td style="text-align:left; white-space:nowrap">전산과 실물이 맞는가</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>회전</b></td>
<td style="text-align:left; white-space:nowrap">재고회전율, 재고보유일수</td>
<td style="text-align:left; white-space:nowrap">재고가 도는가, 며칠치를 쥐고 있는가</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>공간</b></td>
<td style="text-align:left; white-space:nowrap">재고적재율</td>
<td style="text-align:left; white-space:nowrap">창고를 얼마나 쓰고 있는가</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>품질</b></td>
<td style="text-align:left; white-space:nowrap">장기재고율, 불량재고율</td>
<td style="text-align:left; white-space:nowrap">안 나가는 것과 못 쓰는 것이 얼마나 되는가</td>
</tr>
</tbody>
</table>
</div>

**재고적재율에 수식이 두 개**인 것에 주의한다. **로케이션 기준**(칸을 몇 개나 쓰고 있는가)과 **수량 기준**(최대 적재량 대비 얼마나 채웠는가)은 다른 답을 낸다. 칸마다 조금씩만 들어 있으면 로케이션 기준은 높고 수량 기준은 낮다.

**회전율과 보유일수는 같은 값의 앞뒤**다. 30일인 달을 예로 들면 `보유일수 = 30 / 회전율`이므로, 회전율 2면 15일치, 회전율 3이면 10일치를 쥐고 있다는 뜻이다.

### 입고·출고 KPI와 무엇이 다른가

<div class="tbl" style="overflow-x:auto">
<table>
<thead>
<tr>
<th style="text-align:center; white-space:nowrap"></th>
<th style="text-align:center; white-space:nowrap">입고 · 출고 KPI</th>
<th style="text-align:center; white-space:nowrap">재고관리 KPI</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center; white-space:nowrap">재는 대상</td>
<td style="text-align:left; white-space:nowrap"><b>작업의 성적</b> (오류율, 처리시간, 생산성)</td>
<td style="text-align:left; white-space:nowrap"><b>자산의 상태</b> (회전, 적재, 장기·불량)</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">단위</td>
<td style="text-align:left; white-space:nowrap">주로 <b>건수 · 수량</b></td>
<td style="text-align:left; white-space:nowrap">상당수가 <b>금액</b></td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap">시점</td>
<td style="text-align:left; white-space:nowrap">그 작업 건마다</td>
<td style="text-align:left; white-space:nowrap"><b>월 단위</b> (당월출고금액, 월평균재고금액)</td>
</tr>
</tbody>
</table>
</div>

재고관리 KPI에서 **금액이 분모로 자주 등장하는 이유**가 여기 있다. 재고는 창고에 놓인 물건이기 이전에 **묶여 있는 돈**이고, 회전율·장기재고율·불량재고율은 그 돈이 얼마나 잘 돌고 얼마나 죽어 있는지를 재는 지표다.

**불량재고율이 C등급 재고금액으로 정의된 것**도 [재고 상태변경](./4-재고-상태변경.md)과 이어진다. 파손·유통기한 경과로 등급을 낮춘 재고가 그대로 이 지표에 잡힌다.

## 함께 읽기

- 재고정확도의 입력이 되는 재고실사는 [재고조사](./5-재고조사.md)에 있다.
- 입고·출고 쪽 대응 절은 [입고 체크리스트와 KPI](../04-입고-프로세스/6-입고-체크리스트와-KPI.md)와 [출고 체크리스트와 KPI](../05-출고-프로세스/8-출고-체크리스트와-KPI.md)다.
- KPI처럼 품질 목표를 측정 가능한 조건으로 합의하는 방법은 [품질 속성 시나리오](../../아키텍트-첫걸음/3-아키텍처-설계/2-아키텍처-드라이버의-핵심-사항.md#품질-속성-시나리오--어느-수준까지인지를-적는다)에서 이어진다.
