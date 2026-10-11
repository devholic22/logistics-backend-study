# 커넥션 풀 도식 재생성

본문의 두 Mermaid 관계 도식을 Archify workflow로 전환했다. 기존 Archify SVG는 변경하지 않았다.

| 원본 | 내용 | 산출물 |
| --- | --- | --- |
| `10-pool-acquire-return.json` | 유휴 연결 재사용, 풀 확장, 최대 크기 대기와 쿼리·반환 | 같은 이름의 HTML·SVG |
| `12-pool-retry-feedback.json` | DB 지연, 연결 점유, 대기열, 타임아웃과 재시도 악순환 | 같은 이름의 HTML·SVG |

- 원본: [tt-a1i/archify](https://github.com/tt-a1i/archify), 설치 패키지 버전 3.0.1.
- 설치: `npx -y skills add tt-a1i/archify --skill archify --agent codex --global --yes`
- `meta.repository.revision`과 노드의 `sources`는 전환 전 본문 커밋을 가리킨다. 실제 애플리케이션 구현을 검증했다는 의미는 아니다.
- HTML의 도식·설명은 한국어이며 기본 Viewer 조작 UI는 영어다.
- [검증 기록](./pool-validation-receipts.json): Showcase 9/9, 오류·경고 0, 실제 Chromium 브라우저 검사와 light/dark 캡처 검수 통과.
- SVG는 검증된 HTML의 **Export → SVG Light**로 내보낸 결과다.
- `1-처리량과-응답-시간.md`의 응답 시간 Gantt는 수치 축이 있는 시간 그래프이므로 Archify 관계 도식으로 바꾸지 않았다.

저장소 루트에서 설치된 `archify/bin/archify.mjs`의 절대 경로를 사용한다. 재생성 시 각 원본의 `meta.output`과 명령 출력 경로를 일치시킨다.

```bash
node /absolute/path/to/archify/bin/archify.mjs finalize workflow \
  books/주니어-백엔드-개발자가-반드시-알아야-할-실무-지식/02-느려진-서비스-어디부터-봐야-할까/assets/10-pool-acquire-return.json \
  books/주니어-백엔드-개발자가-반드시-알아야-할-실무-지식/02-느려진-서비스-어디부터-봐야-할까/assets/10-pool-acquire-return.html \
  --repo-root . --quality showcase --json
```

두 번째 도식도 파일명을 바꾸어 같은 명령으로 재생성한다. 브라우저 자동 탐색이 실패하면 `ARCHIFY_CHROME`에 실행 파일 경로를 지정한다. 변경된 후보를 다시 검증할 때는 `--out-dir`로 새 증거 디렉터리를 사용한다. HTML을 수정하지 않은 상태에서 `visual-check <output.html> --summary --require-provenance`로 캡처를 수집하고 실제 이미지를 검수한다.
