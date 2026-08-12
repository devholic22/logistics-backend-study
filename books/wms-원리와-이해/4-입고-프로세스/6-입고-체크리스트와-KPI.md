# 입고 체크리스트와 KPI

> [입고 프로세스](./README.md)

## 빠른 복습

- 원서가 제시하는 **범용 예시**다. 각 창고의 특성에 맞게 **수정·보완해서 사용**한다.
- 체크리스트 11개 항목은 **사전 준비 → 현장 점검 → 미처리 확인 → 관리 상태 → 외부 관계** 순이다.
- KPI는 여섯 가지다. **입고 오류율, 미입고율, 생산성, 처리시간, 적치 오류율, 단위당 입고비용.**
- 오류율은 대부분 **건수기준과 수량기준을 따로** 잰다. 한 건에 1개가 틀린 것과 1,000개가 틀린 것은 다르기 때문이다.

## 가. 입고 관련 체크리스트 (예시)

<div class="tbl" style="overflow-x:auto">
<table>
<thead>
<tr>
<th style="text-align:center; white-space:nowrap">순번</th>
<th style="text-align:center; white-space:nowrap">내용</th>
</tr>
</thead>
<tbody>
<tr><td style="text-align:center">1</td><td>사전 입고예정 현황을 확인하고 입고 계획을 수립하였는가?</td></tr>
<tr><td style="text-align:center">2</td><td>입고 및 적치 관련 인력과 장비는 적정한가?</td></tr>
<tr><td style="text-align:center">3</td><td>입고 시 외관(포장, 청결, 표기사항) 점검은 정상적으로 이루어지고 있는가?</td></tr>
<tr><td style="text-align:center">4</td><td>제품의 유지온도, 유통기한 관리, 로트번호 관리 등이 정상적으로 이루어지고 있는가?</td></tr>
<tr><td style="text-align:center">5</td><td>입고 수량은 이상이 없는가?</td></tr>
<tr><td style="text-align:center">6</td><td>제품의 적재 상태는 이상이 없는가? (파렛트당 박스 수, 랩핑 상태 등)</td></tr>
<tr><td style="text-align:center">7</td><td>아직 처리되지 않은 입고 사항은 없는가?</td></tr>
<tr><td style="text-align:center">8</td><td>적치 오류 또는 완료되지 않은 품목은 없는가?</td></tr>
<tr><td style="text-align:center">9</td><td>입고 전표, 지시서 등 출력물은 잘 보관·관리되고 있는가?</td></tr>
<tr><td style="text-align:center">10</td><td>입고장의 청결 상태는 이상이 없는가?</td></tr>
<tr><td style="text-align:center">11</td><td>입고 관련 공급처의 불편이나 클레임은 없는가?</td></tr>
</tbody>
</table>
</div>

원서 표에는 **확인·비고** 열이 비어 있다. 실제로 점검하며 채우는 양식이기 때문이다.

항목 순서를 프로세스 단계와 겹쳐 보면 읽기가 쉬워진다.

<div class="tbl" style="overflow-x:auto">
<table>
<thead>
<tr>
<th style="text-align:center; white-space:nowrap">항목</th>
<th style="text-align:center; white-space:nowrap">대응하는 것</th>
</tr>
</thead>
<tbody>
<tr><td style="text-align:center; white-space:nowrap">1, 2</td><td><b>사전 준비</b> — ① 입고예정수신의 목적</td></tr>
<tr><td style="text-align:center; white-space:nowrap">3~6</td><td><b>현장 점검</b> — ② 검수에서 확인하는 항목</td></tr>
<tr><td style="text-align:center; white-space:nowrap">7, 8</td><td><b>미처리 확인</b> — 흘려보낸 건이 없는지 확인</td></tr>
<tr><td style="text-align:center; white-space:nowrap">9, 10</td><td><b>관리 상태</b> — 증빙 보관과 입고장 정리</td></tr>
<tr><td style="text-align:center; white-space:nowrap">11</td><td><b>외부 관계</b> — 공급처 쪽 불만 확인</td></tr>
</tbody>
</table>
</div>

1·2번은 [입고예정수신](./1-입고예정수신.md), 3~6번은 [차량도착과 검수](./2-차량도착과-검수.md)와 대응한다.

## 나. 입고 관련 KPI (예시)

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
<td style="text-align:center; white-space:nowrap"><b>입고 오류율 (%)</b></td>
<td>입고 오류율(건수기준) = 입고오류건수 / 입고예정총건수 × 100<br>입고 오류율(수량기준) = 입고오류수량 / 입고예정총수량 × 100</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>미입고율 (%)</b></td>
<td>미입고율(거래처기준) = 미입고 거래처수 / 입고예정 총거래처수 × 100<br>미입고율(전표기준) = 미입고 전표건수 / 입고예정 총전표수 × 100<br>미입고율(수량기준) = 미입고 수량 / 입고예정 총수량 × 100</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>생산성</b></td>
<td>인당 처리건수 = 입고확정수량 / 투입인원수<br>장비 생산성 = 입고확정수량 / 투입장비수</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>처리시간</b></td>
<td>평균 입고 처리시간 = ∑(입고완료시간 − 입고접수시간) / 입고건수</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>적치 오류율 (%)</b></td>
<td>적치 오류율(건수기준) = 적치오류건수 / 입고확정총건수 × 100<br>적치 오류율(수량기준) = 적치오류수량 / 입고확정총수량 × 100</td>
</tr>
<tr>
<td style="text-align:center; white-space:nowrap"><b>단위당 입고비용</b></td>
<td>단위당 입고비용 = 총입고비용 / 입고량 (인원, 시간, 수량, 건수 등)</td>
</tr>
</tbody>
</table>
</div>

> 원서의 평균 처리시간은 `입고접수시간 − 입고완료시간`으로 표기되어 있어 결과가 음수가 된다. 여기서는 시간 경과를 올바르게 계산하도록 **입고완료시간 − 입고접수시간**으로 바로잡았다.

### 분모가 무엇인지 보라

같은 "오류율"인데 분모가 다르다. 이 차이가 KPI의 의미를 정한다.

- **입고 오류율**의 분모는 **입고예정**이다. 예정 대비 얼마나 틀렸는가 — ①②단계의 성적이다.
- **적치 오류율**의 분모는 **입고확정**이다. 확정된 물량을 얼마나 제대로 놓았는가 — ④⑤단계의 성적이다.

그래서 두 지표는 책임 구간이 다르다. 입고 오류율이 나쁘면 공급처나 검수를, 적치 오류율이 나쁘면 적치 로직이나 현장 작업을 봐야 한다.

### 건수기준과 수량기준을 왜 나누는가

오류율과 미입고율은 대부분 기준을 나눠 잰다. **한 건에 1개가 틀린 것과 한 건에 1,000개가 틀린 것은 건수기준으로는 같지만 수량기준으로는 전혀 다르다.** 미입고율은 여기에 거래처기준과 전표기준까지 더해, 몇 곳이 안 왔는지와 몇 장이 안 왔는지를 따로 본다.

## 함께 읽기

- 원서는 이 표들을 **범용 예시**로 제시하며, 각 창고의 특성에 맞게 수정·보완하여 사용하길 권한다.
- 체크리스트 3~6번이 확인하는 항목의 근거는 [무엇을 확인하는가](./2-차량도착과-검수.md#무엇을-확인하는가)에 있다.
- 적치 오류율이 나쁠 때 볼 곳은 [적치 구현 방식](./4-적치지시.md#어떻게-구현하는가)이다.
