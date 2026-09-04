# 프로젝트 Git 준비도 강사용 판정표

## 판정 원칙

버튼 완료 상태는 참고만 한다. 저장소 상태, 실제 GitHub 기록, 실행 결과, 학생 설명으로 판정한다.

## Critical Fail

다음 중 하나라도 발생하면 즉시 중단하고 안전 복구 후 재평가한다.

- main에 승인 없이 직접 push
- push --force 또는 force-with-lease를 승인 없이 사용
- reset --hard, clean -fd로 필요한 변경 손실
- 충돌 상대의 변경을 확인하지 않고 삭제
- 실제 비밀정보를 commit 또는 외부 공유
- 다른 학생의 명령과 답변을 그대로 복사
- 실행하지 않은 검증을 했다고 기록

## 모듈별 체크

### 01 상태와 커밋

- status, diff, diff --staged의 대상을 구분한다.
- README와 team.md 변경이 목적별 커밋으로 분리됐다.
- .env, class, IDE 파일이 추적되지 않는다.
- restore --staged 후 작업 파일은 보존된다.
- team.md의 문장과 요구사항이 일치하고 충돌 표시가 없다.

### 02 기능 브랜치

- clean main에서 feature 브랜치를 만들었다.
- branch --show-current로 작업 위치를 확인한다.
- main..HEAD 차이를 설명한다.
- 병합 전후 commit graph를 읽는다.
- 브랜치 전환 오류에서 데이터 손실 명령을 사용하지 않는다.

### 03 원격 동기화

- origin과 origin/main을 구분한다.
- upstream 추적 관계를 branch -vv로 설명한다.
- 실제 push rejected 오류를 보존한다.
- fetch 후 local과 remote 차이를 확인한다.
- 원격 변경을 보존한 뒤 push한다.

### 04 충돌

- 같은 줄 충돌이 실제 발생했다.
- status에서 unmerged path를 찾는다.
- ours와 theirs를 현재 병합 방향으로 설명한다.
- 최종 내용은 두 학생이 합의한다.
- 충돌 표시가 없고 실행 검증이 성공한다.

### 05 PR 협업

- Issue에 목적과 완료조건이 있다.
- PR에 목적, 변경, 검증이 있다.
- 리뷰가 파일, 줄, 이유, 기대 결과를 포함한다.
- 리뷰 반영이 새 commit으로 남는다.
- 병합 후 local main이 최신 상태다.

### 06 장애 대응

- 해결 전 보존할 변경을 식별한다.
- 오류 원문과 직전 명령을 제공한다.
- 잘못 stage한 파일을 작업 손실 없이 내린다.
- 잘못된 브랜치 작업을 새 feature에 보존한다.
- 공유 commit은 이력 보존 방식으로 취소한다.
- 비밀정보 사고에서 폐기·교체·보고를 우선한다.

## 종합평가 점검표

| 항목 | 통과 증거 | 결과 |
|---|---|---|
| Issue | 목적과 완료조건 | |
| main 최신화 | fetch 또는 pull 전후 근거 | |
| 기능 브랜치 | 올바른 이름과 시작 commit | |
| 작은 commit | 문서와 코드 변경 분리 | |
| 검증 | Markdown 내용·누락·충돌 표시 확인 | |
| push | 원격 feature 존재 | |
| PR | 목적·변경·검증 | |
| 리뷰 | 구체적인 동료 피드백 | |
| 리뷰 반영 | 새 commit | |
| 충돌 | 오류·합의·해결 commit | |
| 병합 | GitHub 기록 | |
| 최종 상태 | clean main, 최신 origin/main | |
| Explain Gate | 상태 변화와 팀 영향 설명 | |

## 판정

- PASS: 모든 필수 증거, Critical Fail 없음, Explain Gate 통과
- 재실습: 한 단계 힌트 후 안전하게 완료했지만 독립 수행 부족
- 재평가: Critical Fail 또는 핵심 상태를 설명하지 못함

## 반복 수행

종합평가 PASS만으로 최종 독립 수행을 판정하지 않는다. 실제 프로젝트의 서로 다른 작업 3회에서 다음을 연속 확인한다.

1. 작업 전 main 최신화
2. feature 브랜치
3. 작은 commit
4. 실행 검증
5. PR과 리뷰
6. 병합 후 동기화
7. 문제 발생 시 근거 있는 도움 요청

3회 연속 통과하면 프로젝트 Git 독립 수행 PASS로 기록한다.
