# DB 쿼리 개선 점검 순서

> [성능을 좌우하는 DB 설계와 쿼리](./README.md)

> [!NOTE]
> **추측보다 실행 계획과 운영 지표를 먼저 확인하세요**
>
> 느린 쿼리를 재현하고 실행 계획, 스캔 범위, 호출 빈도를 순서대로 점검하면 개선 우선순위를 정할 수 있습니다.

## 빠른 복습

- 느린 API에서 DB가 실제로 차지하는 시간을 확인한 뒤 slow query와 호출 빈도를 본다.
- 운영과 비슷한 데이터 분포에서 실행 계획과 실제 읽은 행을 비교한다.
- 새 인덱스 전에 기존 인덱스·요구사항·조회 범위를 조정할 수 있는지 확인한다.
- 개선 전후의 p95·p99, CPU, buffer read와 쓰기 비용을 함께 검증한다.

1. 느린 API의 trace에서 실제로 DB가 차지하는 시간을 확인한다.
2. slow query log와 호출 빈도를 함께 확인한다.
3. 운영 환경과 비슷한 데이터 분포에서 `EXPLAIN`을 확인한다.
4. 추정 행 수와 실제 행 수, scan 방식, 정렬과 임시 테이블 여부를 확인한다.
5. 먼저 읽는 행과 반환하는 컬럼 수를 줄일 수 있는지 검토한다.
6. 기존 인덱스로 해결할 수 있는지 확인한 뒤 새 인덱스를 설계한다.
7. 인덱스 적용 전후의 p95·p99, buffer read, CPU와 쓰기 비용을 비교한다.
8. 데이터가 계속 늘어났을 때의 실행 시간도 부하 테스트한다.

## 핵심 정리

- DB 성능은 데이터 크기뿐 아니라 조회 패턴, 호출 빈도와 실행 계획의 조합으로 결정된다.
- 인덱스는 조건절 하나가 아니라 필터, 정렬, 그룹화와 페이지네이션을 기준으로 설계한다.
- 선택도는 중요한 판단 기준이지만 값의 분포와 실제로 자주 찾는 값이 더 중요할 수 있다.
- 커버링 인덱스는 테이블 접근을 줄일 수 있지만 DBMS와 행 상태에 따라 실제 index-only scan 여부가 달라진다.
- 인덱스를 늘리면 쓰기, 저장 공간과 운영 비용도 함께 늘어난다.
- 반복 집계는 사전 계산할 수 있지만 원자성, 멱등성, hot row와 불일치를 설계해야 한다.
- 큰 OFFSET 대신 안정적인 정렬 키를 이용한 keyset pagination을 고려한다.
- 정확한 전체 건수가 필요하면 제거하는 대신 집계·캐시·읽기 분산 방법을 선택한다.
- 오래된 데이터 관리는 DBMS별 공간 회수 방식과 파티셔닝 비용을 확인해야 한다.
- 읽기 복제본은 조회 처리량을 늘릴 수 있지만 복제 지연과 read-after-write 문제가 있다.
- query timeout은 계층별 deadline과 실제 DB cancellation이 함께 동작하는지 확인해야 한다.
- 상태를 변경하는 트랜잭션과 변경 직후의 조회는 replica lag를 고려해 primary를 사용한다.
- 배치는 구간을 나눌 수 있지만 checkpoint, 멱등한 반영과 지연 도착 데이터를 함께 설계해야 한다.
- 같은 의미의 조인 키는 타입과 collation을 일치시키고 암묵적 형 변환을 피한다.
- 큰 테이블의 DDL은 실제 알고리즘, metadata lock, 임시 공간과 복제 영향을 확인한다.
- DB 연결 수는 모든 인스턴스의 pool 합계와 DB의 포화점을 기준으로 제한한다.
- DB와 외부 시스템의 이중 쓰기는 로컬 트랜잭션만으로 원자성을 보장할 수 없으므로 outbox, 멱등성, 보상과 대사 절차를 사용한다.
- 모든 개선은 추측이 아니라 실행 계획과 실제 지표로 검증한다.

## 참고 자료

- [MySQL 8.4: Optimization and Indexes](https://dev.mysql.com/doc/refman/8.4/en/optimization-indexes.html)
- [MySQL 8.4: Understanding the Query Execution Plan](https://dev.mysql.com/doc/refman/8.4/en/execution-plan-information.html)
- [MySQL 8.4: FULLTEXT Indexes](https://dev.mysql.com/doc/refman/8.4/en/column-indexes.html)
- [MySQL 8.4: Correlated Subqueries](https://dev.mysql.com/doc/refman/8.4/en/correlated-subqueries.html)
- [PostgreSQL: Index-Only Scans and Covering Indexes](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
- [PostgreSQL: LIMIT and OFFSET](https://www.postgresql.org/docs/current/queries-limit.html)
- [PostgreSQL: Table Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
- [MySQL 8.4: Replication FAQ](https://dev.mysql.com/doc/refman/8.4/en/faqs-replication.html)
- [PostgreSQL: Client Connection Defaults and Statement Timeout](https://www.postgresql.org/docs/current/runtime-config-client.html)
- [PostgreSQL: Canceling Requests in Progress](https://www.postgresql.org/docs/current/protocol-flow.html#PROTOCOL-FLOW-CANCELING-REQUESTS)
- [MySQL 8.4: Type Conversion and Indexed Columns](https://dev.mysql.com/doc/refman/8.4/en/cast-functions.html)
- [MySQL 8.4: ALTER TABLE Algorithms and Locks](https://dev.mysql.com/doc/refman/8.4/en/alter-table.html)
- [MySQL 8.4: Online DDL Performance and Concurrency](https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-performance.html)
- [MySQL 8.4: Too Many Connections](https://dev.mysql.com/doc/refman/8.4/en/too-many-connections.html)
- [AWS Prescriptive Guidance: Transactional Outbox Pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)
