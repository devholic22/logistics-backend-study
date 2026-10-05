# Logistics Backend Study

물류 도메인과 백엔드 아키텍처, 유지보수하기 좋은 코드를 함께 학습하며 정리한 문서 저장소다.

## 학습 문서

- [전체 책 목록](./books/README.md)
- [WMS 원리와 이해](./books/wms-원리와-이해/README.md)
- [아키텍트 첫걸음](./books/아키텍트-첫걸음/README.md)
- [내 코드가 불안한 개발자를 위한 좋은 코드의 기준](./books/내-코드가-불안한-개발자를-위한-좋은-코드의-기준/README.md)
- [요즘 우아한 백엔드 개발](./books/요즘-우아한-백엔드-개발/README.md) — 물류 시스템과 백엔드 운영 관련 장을 선별
- [AI 시대의 엔지니어링 전략](./books/ai-시대의-엔지니어링-전략/README.md)
- [주니어 백엔드 개발자가 반드시 알아야 할 실무 지식](./books/주니어-백엔드-개발자가-반드시-알아야-할-실무-지식/README.md)

## mini-WMS 애플리케이션

현재는 도메인 기능을 구현하기 전의 단일 모듈 Spring Boot 골격이다.
Java 21이 필요하며 Gradle은 저장소의 wrapper를 사용한다.

```bash
./gradlew test
./gradlew bootRun
```

애플리케이션이 시작되면 다음 명령으로 상태를 확인할 수 있다.

```bash
curl http://localhost:8080/actuator/health
```

데이터베이스, 영속성 기술과 업무 API는 각각의 요구사항과 기술 결정이 준비된 뒤 추가한다.
