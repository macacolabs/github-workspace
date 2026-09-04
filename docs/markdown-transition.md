# Git + Markdown 학생 실습 전환

학생 필수 환경: Git과 텍스트 편집기. Windows 명령은 기본 PowerShell 사용.
학생에게 Python, JDK, 실행 스크립트를 요구하지 않는다.

## 반영

- 기본 실습은 README.md, team.md, members 문서를 수정·검토한다.
- starter ZIP은 README.md, team.md, .gitignore, members/.gitkeep만 포함한다.
- 복구 9종은 git-markdown-practice.md의 공통 준비와 상황별 명령으로 직접 만든다.
- MD에는 예상 상태, 복구 명령, 복구 후 관찰 결과까지 포함한다.
- HTML 시작 명령도 직접 실습으로 교체했다. 기존 도식은 유지한다.
- Java는 examples/optional-java에 보존하고 Python 도구는 강사용 회귀 검증 전용이다.

## 검증

- verify_markdown_practice.py는 MD의 실제 PowerShell 블록으로 9종 준비·복구를 실행한다.
- verify_learning_path.py는 학생 ZIP과 실습 01 HTML 명령으로 clean 상태 및 clone 후 ignore 규칙을 검사한다.
- 링크·SVG는 validate-course.ps1로 검사한다.
- 실제 GitHub 2인 PR·권한·리뷰와 학생 수업 소요시간 검증은 별도다.

이 문서는 이전 recovery-review-changes.md의 학생 Python·Java 요구를 대체한다.
main 병합은 사용자 승인 전까지 수행하지 않는다.
