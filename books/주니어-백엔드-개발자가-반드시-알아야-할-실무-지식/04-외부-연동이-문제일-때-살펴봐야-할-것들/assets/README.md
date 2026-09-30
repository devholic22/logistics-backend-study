# 외부 WMS 연동 도식

본문에서는 SVG를 표시하고, HTML은 다운로드 후 브라우저에서 열어 탐색할 수 있다. JSON은 archify 재생성 원본이다. 본문·노드는 한글이며 뷰어의 고정 UI는 영어로 표시된다.

| 원본 | 유형 | 설명 |
| --- | --- | --- |
| `01-http-connection-boundaries.json` | architecture | 내부 요청 경로와 외부 요청 경로 |
| `02-alb-timeout-propagation.json` | sequence | ALB idle 종료 이후에도 외부 작업이 남는 상황 |
| `03-sync-async-structure.json` | architecture | 접수 응답과 Worker 실행의 분리 |

```bash
node "$ARCHIFY_ROOT/bin/archify.mjs" validate architecture 01-http-connection-boundaries.json --quality showcase --json
node "$ARCHIFY_ROOT/bin/archify.mjs" deliver architecture 01-http-connection-boundaries.json 01-http-connection-boundaries.html --quality showcase --json
```

다른 파일에도 대응하는 유형으로 같은 명령을 적용한다. SVG는 검증된 HTML의 SVG 및 관련 스타일을 추출하고 light 테마 색상을 고정한 정적 미리보기다. HTML의 탐색 메뉴와 하단 설명 카드는 SVG에 포함되지 않는다.

세 HTML 모두 showcase 9개 항목 통과, 오류 0건·경고 0건이다. SHA-256 및 상세 결과는 `validation-receipts.json`에 기록했다. 브라우저 부재로 HTML 화면·인터랙션 검증은 수행하지 못했으며, SVG는 한글 폰트로 실제 렌더링하여 시각 확인했다.
