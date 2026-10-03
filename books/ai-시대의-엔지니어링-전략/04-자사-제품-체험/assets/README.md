# 04장 도식 소스와 검증

두 도식은 Archify 2.17의 sequence 형식으로 원서 구성도와 의사코드를 요청 순서로 다시 정리한 개념도다. 실제 서비스의 구현이나 모든 호출을 확정한 도식은 아니다.

| 파일 이름 | 검증 경계 |
| --- | --- |
| `01-페이크를-이용한-시나리오-테스트` | 실제 백엔드와 페이크 DOM·DB를 연결한다 |
| `02-브라우저를-포함한-e2e-테스트` | 실제 브라우저의 클릭부터 백엔드·DB까지 연결한다 |

각 이름에 `.json`(원본), `.html`(확대·탐색), `.svg`(본문 삽입)가 대응한다. 도식 내용은 한국어다. HTML의 고정 UI와 문서 언어는 영어 기본값을 사용한다. SVG는 밝은 테마로 고정하고 한국어 및 대체 폰트를 지정했다.

## 재생성

Archify 패키지에서 실행한다. `SOURCE`와 `OUTPUT`은 해당 JSON·HTML의 절대 경로다.

```bash
node bin/archify.mjs validate sequence "$SOURCE" --quality showcase --json
node bin/archify.mjs deliver sequence "$SOURCE" "$OUTPUT" --quality showcase --json
node bin/archify.mjs visual-check "$OUTPUT" --json
```

SVG는 HTML의 `.diagram-container` 안 SVG와 렌더러 스타일에서 추출했다. 밝은 테마의 CSS 변수를 고정 색상으로 치환하고 맥락 문구를 표시했다. HTML 원본은 수정하지 않았다.

## 검증 범위

[validation-receipts.json](./validation-receipts.json)에 JSON·HTML·SVG의 SHA-256과 크기를 기록했다. 두 도식 모두 Showcase 9/9, 오류 0, 경고 0이다. SVG XML 파싱 및 래스터 렌더링 후 한글·화살표·메시지 배치를 직접 확인했다.

Chrome/Chromium을 사용할 수 없어 HTML 자동 브라우저 검증은 `skipped`다. HTML 뷰어 직접 검수와 데스크톱 화면 크기별 검증은 수행하지 않았다. SVG 이미지 검수와 HTML 정적 검증을 별도로 기록했다.
