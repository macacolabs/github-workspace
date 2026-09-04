# 프로젝트 Git 실습 강사용 해설

학생에게 전체 파일을 배포하지 않는다. 학생이 진단 명령과 선택 이유를 먼저 제시한 후 필요한 단계만 힌트로 제공한다.

## 힌트 단계

1. 관찰 질문: 지금 브랜치와 status는 무엇인가?
2. 범위 질문: 어떤 변경을 보존해야 하는가?
3. 명령 범주: 작업 트리, stage, commit, remote 중 어디를 바꿔야 하는가?
4. 부분 명령: 명령 이름만 제공한다.
5. 전체 절차: 반복 실패 또는 안전 위험이 있을 때만 제공한다.

## Module 01 핵심 해설

- git diff: Working Tree와 index 비교
- git diff --staged: index와 HEAD 비교
- git restore --staged 파일: index에서 내리되 Working Tree 변경 유지
- git restore 파일: Working Tree 변경 폐기 가능, 실행 전 확인 필수
- .gitignore는 이미 추적된 파일을 자동으로 추적 해제하지 않는다.

정상 결과:
- README와 team.md가 서로 다른 commit
- .class와 .env가 status에 나타나지 않음
- 최종 Working Tree clean

## Module 02 핵심 해설

미커밋 변경이 있을 때 switch가 항상 실패하는 것은 아니다. 이동 대상 브랜치와 변경이 겹쳐 데이터 손실 가능성이 있을 때 Git이 전환을 막는다. 학생이 “변경이 있으면 무조건 실패”로 설명하면 수정한다.

정상 결과:
- feature 브랜치에만 새 commit 존재
- 병합 전 main과 feature 포인터가 다름
- 병합 후 main이 feature commit 포함

## Module 03 push rejected 재현

A와 B가 같은 base commit에서 시작해야 한다.

1. A가 새 commit을 origin/main에 push
2. B가 A commit을 받지 않은 상태에서 다른 commit 생성
3. B push는 non-fast-forward로 거절
4. B는 fetch 후 graph로 두 갈래 확인
5. merge 기반 pull로 양쪽 commit 보존
6. 충돌 시 Module 04 적용
7. 최종 push

force push는 정답으로 인정하지 않는다.

## Module 04 충돌 해설

충돌 표시의 ours/theirs는 현재 작업 방향에 의존한다. 명령줄 merge에서 ours는 현재 HEAD, theirs는 병합 대상이다. 학생이 무조건 “내 것/상대 것”으로 말하면 현재 브랜치와 merge 대상을 다시 묻는다.

해결 완료:
- unmerged path 없음
- 충돌 표시 검색 결과 없음
- 해결 commit 존재
- 프로그램 실행 성공
- 두 학생이 최종 결과에 동의

## Module 05 리뷰 판정

좋은 리뷰 예시 구조:

- 위치: members/kim.md의 연락 방법
- 이유: 실제 개인정보가 저장소에 노출될 수 있음
- 요청: 개인 번호 대신 팀 공용 채널 표기로 변경
- 기대 결과: 저장소에 개인정보 없이 연락 경로 제공

단순 칭찬만 있는 리뷰는 통과시키지 않는다.

## Module 06 장애별 기대 선택

- 잘못 stage: restore --staged로 index만 변경
- 잘못된 브랜치, 미커밋: 현재 위치에서 새 feature 브랜치 생성 후 상태 확인
- 공유 commit 취소: revert로 반대 변경의 새 commit 생성
- pull conflict: 반복 pull 금지, status와 충돌 파일부터 확인
- 비밀정보: 즉시 폐기·교체·보고. 파일 삭제 commit만으로 완료 불가

## Explain Gate 보충 질문

학생이 암기 답변만 할 때 실제 저장소를 가리키며 묻는다.

- 현재 HEAD commit 해시는?
- 이 파일은 다음 commit에 포함되는가? 근거는?
- origin/main이 마지막으로 갱신된 시점은?
- 이 PR에서 관계없는 변경은 없는가?
- 지금 명령이 실패하면 어떤 데이터가 보존되는가?
