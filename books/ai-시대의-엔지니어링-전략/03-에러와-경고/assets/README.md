# 03장 도식 소스와 검증

본문의 세 도식은 Archify 2.17의 workflow v2로 작성했다. 단순 비교는 본문의 표로 정리했다.

| 파일 이름 | 내용 |
| --- | --- |
| `01-에러의-대상과-복구-행동` | 최종 사용자와 개발자의 복구 행동 분기 |
| `02-진단의-정보-체인` | 원본 맥락 보존과 정보 유실의 차이 |
| `03-허용-확인-거부의-분기` | 정상 입력, 의심스러운 입력, 금지된 입력의 분기 |

각 이름에 `.json`(원본), `.html`(확대·탐색), `.svg`(본문 삽입)가 대응한다. HTML은 고정 UI와 문서 언어에 영어 기본값을 사용하며, 도식의 내용은 한국어다. SVG는 밝은 테마로 고정하고 한국어 폰트와 일반 sans-serif 대체 폰트를 지정했다.

## 재생성

Archify 패키지에서 다음 명령을 실행한다. `SOURCE`와 `OUTPUT`은 저장소 안 해당 JSON·HTML의 절대 경로다.

```bash
node bin/archify.mjs validate workflow "$SOURCE" --quality showcase --json
node bin/archify.mjs deliver workflow "$SOURCE" "$OUTPUT" --quality showcase --json
node bin/archify.mjs visual-check "$OUTPUT" --json
```

SVG는 HTML의 `.diagram-container` 안 SVG와 렌더러 스타일에서 추출했다. 밝은 테마의 CSS 변수를 고정 색상으로 치환하고, 맥락 문구를 표시했다. HTML 원본은 수정하지 않았다.

## 검증 기록

[validation-receipts.json](./validation-receipts.json)에 JSON·HTML·SVG의 SHA-256과 크기를 기록했다. 세 도식 모두 Showcase 9/9, 오류 0, 경고 0이다. SVG XML 파싱 및 래스터 렌더링 후 한글·화살표·문구 배치를 직접 확인했다.

Chrome/Chromium을 사용할 수 없어 HTML의 자동 브라우저 검증은 `skipped`이며 HTML 뷰어를 직접 검수했다고 주장하지 않는다. SVG 이미지 검수와 HTML의 자동 정적 검증은 별도 결과다.
