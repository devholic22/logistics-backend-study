# 3장 Archify 도식

기존 Mermaid 6개를 workflow 4개와 sequence 2개로 전환했다. 본문에는 SVG를 표시하며, 각 도식의 대화형 HTML과 원본 JSON을 함께 연결한다.

| 파일 이름 | 내용 | 유형 |
| --- | --- | --- |
| `01-db-pressure` | DB 부하에서 API 처리량 저하까지의 영향 | workflow |
| `02-read-replicas` | Primary 쓰기·복제와 Replica 조회 경로 | workflow |
| `03-retry-feedback` | 느린 쿼리와 중복 재시도의 악순환 | workflow |
| `04-replica-lag` | 변경 직후 Replica 조회의 과거 상태 반환 사례 | sequence |
| `05-transaction-boundary` | 회원·약관 동의 저장과 commit·rollback | workflow |
| `06-transactional-outbox` | 가입 트랜잭션과 별도 worker의 발송·결과 기록 | sequence |

## 의미와 범위

- 이 도식은 학습 문서의 예시를 설명한다. 저장소 애플리케이션에 구현되었거나 운영 성능을 측정했다는 의미는 아니다.
- DB 부하와 처리량 저하는 자원 경합·포화 조건에서의 인과관계다.
- 두 Replica로 향하는 조회 선은 읽기 분산의 가능한 경로이며, 매번 두 곳에 동시에 질의한다는 뜻은 아니다.
- 복제 지연은 가능한 실행 순서 하나다. 복제가 항상 마지막에만 실행된다는 보장은 없다.
- 트랜잭션의 회원 저장 오류는 바로 rollback하며, 약관 저장까지 진행한 경로도 성공 여부에 따라 commit·rollback한다.
- Outbox의 성공·재시도 실패 기록은 서로 다른 대안 경로다. 발송 이후 처리 완료 기록 전 종료에 따른 중복 위험과 멱등성 설명은 본문에 보존했다.
- 설명은 한국어다. 고정 Viewer UI와 HTML lang은 영어로 표시된다. 한글 렌더링에는 운영체제의 한글 글꼴이 필요하다.

## 재생성과 검증

[Archify](https://github.com/tt-a1i/archify) 스킬 2.17을 사용했다. workflow 원본은 schema v2, sequence는 schema v1이다. 버전이 달라지면 재생성 결과와 검증을 다시 확인한다.

```bash
node /absolute/path/to/archify/bin/archify.mjs validate workflow 01-db-pressure.json --quality showcase --json
node /absolute/path/to/archify/bin/archify.mjs deliver workflow 01-db-pressure.json 01-db-pressure.html --quality showcase --json
node /absolute/path/to/archify/bin/archify.mjs visual-check 01-db-pressure.html --json
```

위 명령은 이 디렉터리에서 실행한다. 다른 도식은 표의 유형·파일 이름으로 바꾼다. SVG는 검증된 HTML의 Export → SVG로 내보낸 원본이며 밝은·어두운 테마를 지원한다.

[최종 검증 기록](./validation-receipts.json)에 원본·HTML·SVG의 SHA-256과 검증 범위를 기록했다.

- 모든 도식의 validate·deliver: Showcase 9/9, 구성 오류·경고 0.
- 자동 브라우저: Chromium에서 1440×900, 1600×1000, 1920×1080, 2048×1320의 페이지 넘침·가독성·Viewer UI 검사 통과. 개별 `*.browser.json`에 측정값을 보관한다.
- 별도 이미지 검수: 1440×900·2048×1320의 light/dark 캡처 24장과 SVG 6개를 확인했다. 한글·노드·화살표·레이블의 가림과 잘림을 점검했다.
- 캡처 PNG는 로컬 검수용이며 커밋하지 않았다. 자동 검사 결과와 이미지 검수 판정은 분리해서 기록했다.
- HTML 검색·focus 등 개별 인터랙션 전체를 테스트한 결과는 아니다. SVG export 동작은 실제 브라우저에서 확인했다.
