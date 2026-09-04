# 판단·복구 확장 검증 결과

검증일: 2026-09-04
브랜치: feature/git-recovery-learning
기준 커밋: 8db566d
상태: 구현·로컬 기술 검증 완료, 사용자 검토 대기. main 병합 및 원격 push 미실행.

## 실행 결과
- scripts/validate-course.ps1: PASS
- HTML 총 27개 로컬 참조 확인
- 기존 root labs 8페이지 유지 (홈 + 7개 모듈)
- 신규 labs/recovery 8페이지
- SVG 총 12개 (기존 4 + 신규 8), XML과 title/desc 확인
- 신규 페이지 anchor, 제목, 입력 폼 부재, 이미지 alt/크기, 핵심 학습 절차 검사
- 기존 17개 페이지에서 복구 단원 연결 확인
- Java starter 컴파일·실행
- 기존 branch/충돌 흐름 실제 실행
- staged / branch / committed / remote / conflict / delete-conflict / stash / lost / shared: 9개 복구 리허설 PASS
- git diff --check: 오류 없음 (Windows 줄바꿈 변환 경고는 별도)
- 로컬 HTTP 18765의 새 단원과 과정 홈: 200

## 테스트가 실제 확인한 것
stage 해제 후 원본 보존, 전환 거절 재현, 미공유 main과 feature 참조 분리,
bare remote의 분기 이력 통합과 미완성 파일 복원, merge abort 후 원래 tip,
해결 커밋의 두 부모, 미추적 파일 stash 복원, reflog에서 해시 탐색,
revert 후 기존 커밋 조상 관계 보존을 assert로 확인했다.

## 검증 한계
- 실제 학생 계정으로 GitHub PR 승인/보호 규칙/CI check는 실행하지 않았다.
- 브라우저 스크린샷·모바일 렌더링·화면 공유 가독성 검증은 이번 실행에 포함하지 않았다.
- 설명과 모범 복구의 기술 검증은 학생의 독립 수행 능력을 보장하지 않는다.
- 수업 시간 배분은 운영안이며 실제 학급 소요시간 측정이 아니다.
- fixture는 매번 새 임시 디렉터리를 생성하고 삭제하지 않는다. 출력 경로에서 결과 비교 가능.

## 검토 순서
1. labs/recovery/01-state.html: 자세한 설명과 그림의 수준
2. 기존 chapters/07-undo.html: 안전 설명과 연결 방식
3. labs/recovery/03-sync.html: 상태를 보고 복구를 선택하는 흐름
4. labs/recovery/07-independent.html: 정답 안내 없는 변형 문제
승인 후에만 main 병합을 진행한다.
