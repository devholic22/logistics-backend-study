# 06장 도식과 검증 기록

| 도식 | 본문 | 원본과 결과 |
| --- | --- | --- |
| 고객 발견 인터뷰 | [3절](../3-고객-발견-인터뷰.md#cdi-퍼널) | [JSON](./01-고객-발견-인터뷰.json) · [HTML](./01-고객-발견-인터뷰.html) · [SVG](./01-고객-발견-인터뷰.svg) |
| 안티테제와 기능 선택 | [8절](../8-타깃-오디언스-기반-기능-선택.md#페르소나별-안티테제) | [JSON](./02-안티테제와-기능-선택.json) · [HTML](./02-안티테제와-기능-선택.html) · [SVG](./02-안티테제와-기능-선택.svg) |

본문의 고객 발견 과정과 앱 센터 사례를 재구성했다. 첫 도식은 아이디어를 소개하는 경우와 반대 신호를 얻는 경우를 함께 보여 준다. 둘째 도식은 패튼의 장벽을 콘텐츠 확보와 장르 필터로 함께 해소하는 판단을 보여 준다. 결과를 보장하는 인과 법칙이나 모든 제품에 적용되는 절차는 아니다.

기존 Mermaid 10개 중 과정과 분기가 중요한 2개를 Archify로 대체했다. 나머지 8개는 비교·분류·짧은 순서를 표와 설명으로 정리했다.

## 재생성

Archify 설치 환경에서 `ARCHIFY_ROOT`를 스킬 디렉터리로 지정하고 assets 디렉터리에서 실행한다.

```bash
for stem in 01-고객-발견-인터뷰 02-안티테제와-기능-선택; do
  node "$ARCHIFY_ROOT/bin/archify.mjs" validate workflow "$stem.json" --quality showcase --json
  node "$ARCHIFY_ROOT/bin/archify.mjs" deliver workflow "$stem.json" "$stem.html" --quality showcase --json
  node "$ARCHIFY_ROOT/bin/archify.mjs" visual-check "$stem.html" --json
done
```

SVG는 전달된 HTML의 실제 SVG를 추출한 밝은 테마의 정적 읽기 버전이다. 기존 5장 SVG의 밝은 테마 스타일을 적용했으며 HTML은 전달 후 수정하지 않았다. HTML 재생성 후 SVG 추출과 검증 기록도 갱신해야 한다. 한국어는 `Noto Sans CJK KR` 또는 시스템 sans-serif로 표시한다.

## 검증 범위

[검증 기록](./validation-receipts.json)은 최종 JSON·HTML·SVG의 SHA-256과 검증 범위를 담는다.

- 두 도식 모두 Archify showcase 9/9 통과, 오류 0개·경고 0개.
- SVG XML 파싱 및 1700px PNG 렌더링 후 밝은 테마 시각 확인: 한국어, 노드 글자 간격, 분기·합류와 관계 라벨 확인.
- Chrome/Chromium 미설치로 두 HTML의 `visual-check`는 종료 코드 2, `skipped`. 개별 `.visual-check.json`에 기록했다.
- HTML의 실제 브라우저 동작, 데스크톱 뷰포트별 수용 범위와 어두운 테마는 검증하지 않았다. SVG 확인은 HTML 브라우저 검증을 대신하지 않는다.
- 본문과 도식은 한국어이며 HTML의 고정 Viewer UI와 `<html lang>`은 영어 기본값이다.
