# 8장 Archify 도식

8장 전체 문서를 검토하고 출시 판단·확장성 판단·페르소나별 결정과 검증을 workflow로 작성했습니다. 단순 비교·나열은 본문 표와 문장으로 정리했습니다.

| 도식 | 원본과 본문 이미지 | Showcase | 브라우저 증거 | 시각 검수 |
| --- | --- | --- | --- | --- |
| [어포던스 출시 판단](./01-affordance-timing.html) | [JSON](./01-affordance-timing.json) · [SVG](./01-affordance-timing.svg) | 9/9 · 오류 0 · 경고 0 | passed | passed |
| [확장 가능한 기능의 판단](./02-extension-scenarios.html) | [JSON](./02-extension-scenarios.json) · [SVG](./02-extension-scenarios.svg) | 9/9 · 오류 0 · 경고 0 | passed | passed |
| [페르소나별 결정과 검증](./03-persona-decisions.html) | [JSON](./03-persona-decisions.json) · [SVG](./03-persona-decisions.svg) | 9/9 · 오류 0 · 경고 0 | passed | passed |

## 검증 범위

- `validate`와 `deliver`: 세 도식 모두 Showcase 9/9, 오류·경고 0. 원본·HTML 해시 및 바이트 수는 [validation-receipts.json](./validation-receipts.json)에 기록했습니다.
- `visual-check`: 1440×900, 1600×1000, 1920×1080, 2048×1320의 밝은 테마 측정 모두 통과했습니다. 가로·세로 넘침이 없습니다.
- 화면 캡처: 1440×900과 2048×1320의 밝은·어두운 테마를 직접 검수했습니다. 기록은 [visual-review.json](./visual-review.json), 자동 측정은 각 도식의 `.visual-check.json`에 있습니다.
- 한국어 글꼴 누락을 실행 환경의 Noto Sans CJK KR 설치로 해결한 뒤 최종 캡처를 다시 생성했습니다. 화면 크기에 따른 넘침은 원본의 노드 높이를 조정해 해결했습니다.
- 본문용 SVG는 최종 HTML의 SVG와 스타일을 추출했습니다. 별도 Archify 산출물 검증 주장은 HTML에만 적용됩니다.
- 검색·focus·export의 개별 동작은 검증하지 않았습니다.

본문과 도식 내용은 한국어입니다. 고정 Viewer UI와 `<html lang>`은 영어로 표시됩니다.

## 화면 증거 보관 제한

자동 승인 검토가 PNG 캡처의 외부 업로드를 거부해, 화면 캡처와 캡처를 참조하는 contact sheet는 이 PR에 포함하지 않았습니다. 로컬에서 수행한 화면 검수 결과와 원본 HTML 해시, 자동 브라우저 측정 수치는 JSON 기록에 보존했습니다. `.visual-check.json`의 캡처 파일명은 검수 당시 로컬 증거를 가리키며 저장소 파일 링크가 아닙니다.
