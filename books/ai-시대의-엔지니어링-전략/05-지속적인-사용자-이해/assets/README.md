# 05장 도식과 검증 기록

| 도식 | 본문 | 원본과 결과 |
| --- | --- | --- |
| 사용자 지원 플라이휠 | [6절](../6-사용자-지원-플라이휠.md#플라이휠) | [SVG](./01-사용자-지원-플라이휠.svg) · [HTML](./01-사용자-지원-플라이휠.html) · [JSON](./01-사용자-지원-플라이휠.json) |

원서의 지원 → 지속적인 연결 → 피드백과 통찰 → 제품·지원 개선 → 다음 지원의 순환을 재구성했다. 각 화살표는 작동을 보장하는 인과 법칙이 아니라 팀이 만들어야 할 연결을 보여 준다. 단순 분류와 비교 도식 10개는 본문 표로 바꿨다.

## 재생성

Archify가 설치된 환경에서 다음 명령을 실행한다. `ARCHIFY_ROOT`는 해당 스킬 디렉터리를 가리킨다.

```bash
node "$ARCHIFY_ROOT/bin/archify.mjs" validate workflow 01-사용자-지원-플라이휠.json --quality showcase --json
node "$ARCHIFY_ROOT/bin/archify.mjs" deliver workflow 01-사용자-지원-플라이휠.json 01-사용자-지원-플라이휠.html --quality showcase --json
node "$ARCHIFY_ROOT/bin/archify.mjs" visual-check 01-사용자-지원-플라이휠.html --json
```

SVG는 전달된 HTML의 실제 SVG와 클래식 밝은 테마 스타일을 추출하고 색상 변수를 고정한 정적 읽기 버전이다. 한국어 폰트는 시스템의 `Noto Sans CJK KR` 또는 sans-serif를 사용한다. HTML 재생성과 정적 SVG 추출은 별도 작업이다.

## 검증 범위

[검증 기록](./validation-receipts.json)에 최종 JSON·HTML·SVG의 SHA-256을 기록했다.

- Archify showcase 9/9 통과, 오류 0개·경고 0개.
- SVG XML 파싱과 밝은 테마 PNG 렌더링 후 시각 검토: 한국어, 네 단계와 화살표 확인.
- Chrome/Chromium 미설치로 HTML `visual-check`는 종료 코드 2, `skipped`. HTML의 실제 브라우저 동작·뷰포트별 레이아웃·어두운 테마는 검증하지 않았다.
- HTML은 `deliver` 이후 수정하지 않았다. 정적 SVG 검토는 HTML 브라우저 검증을 대신하지 않는다.
- 본문과 도식은 한국어이며 HTML의 고정 Viewer UI와 `<html lang>`은 영어로 표시된다.
