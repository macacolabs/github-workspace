# 검토 후 수정 사항 — 2026-09-04

검토 브랜치: feature/git-recovery-learning. 사용자 승인 전 main 병합 금지.

## 페이지에서 확인

- labs/recovery/index.html: 개정 안내, 실제 복구 ZIP 다운로드, PowerShell 준비,
  공통 진단, 보존·명령 선택, 실패 시 중단, 도움 요청, 검증, 원격수업 재진입.
- labs/01-local-commits.html: starter 초기 커밋과 마지막 변경 보존 커밋 추가.
- labs/02-feature-branch.html: 연습 위치 보관·복귀, 심화 선택 실습 표시.
- labs/03~06 및 사이드바: 원격 → PR → 충돌 → 장애 대응 연결.
- chapters/07-undo.html: reset 안전 순위 대신 상태별 영향으로 설명.
- assets/visuals/state-index.svg: add와 commit 화살표 방향·라벨 수정.
- css/recovery.css: 작은 화면에서는 본문을 유지하고 도식 내부에서 스크롤.

## 재실행 가능한 검증

`powershell -File scripts/validate-course.ps1`

- 기존 링크·SVG·Java·충돌 테스트.
- Python 일반 실행 및 -O에서 9개 복구 시나리오씩 검사.
- verify_learning_path.py: HTML의 Git 명령 24개를 복사한 starter에서 실행,
  다음 모듈의 clean 조건 및 clone 후 ignore 규칙 전달 확인.
- 복구 ZIP의 파일 목록과 소스 바이트 일치 확인.

## 확인 범위와 한계

375px 브라우저에서 복구 홈과 상태 페이지의 문서 너비 369px 확인.
이미지 로딩 및 복구 홈 실제 화면 확인. 모든 단말의 시각 검증은 아님.
학습 경로 테스트는 모듈 01의 Git 명령을 추출해 실행하며, 텍스트 편집을
모사한다. 전체 4시간 실제 학생 수업 및 실제 GitHub 2인 PR 검증은 별도다.
4시간 내 독립 복구 숙달을 보장하지 않으며, 심화는 이후 반복 시간으로 분리한다.

## 승인 전 남은 확인

1. 사용자 화면 검토: 설명 깊이와 개정 범위.
2. 실제 수업 계정으로 2인 PR·리뷰·권한 흐름 리허설.
3. 사용자 승인 후 커밋·배포·병합 범위를 결정한다.
