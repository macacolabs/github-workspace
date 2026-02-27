/* =============================================
   practice.js — 실습 섹션 인터랙션
   - Step 완료 체크
   - 상태 패널 탭 전환
   - 시나리오 토글
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {

    /* ── 1. Step 완료 체크 ── */
    document.querySelectorAll('.practice-step').forEach(step => {
        const check = step.querySelector('.step-check-btn');
        if (!check) return;
        check.addEventListener('click', () => {
            step.classList.toggle('step-done');
            const isDone = step.classList.contains('step-done');
            check.textContent = isDone ? '✅ 완료' : '⬜ 완료';
            check.classList.toggle('done', isDone);
            updateMissionProgress(step.closest('.practice-section'));
        });
    });

    /* ── 2. 미션 진행률 업데이트 ── */
    function updateMissionProgress(section) {
        if (!section) return;
        const total = section.querySelectorAll('.practice-step').length;
        const done = section.querySelectorAll('.practice-step.step-done').length;
        const bar = section.querySelector('.mission-progress-fill');
        const label = section.querySelector('.mission-progress-label');
        if (bar) bar.style.width = `${(done / total) * 100}%`;
        if (label) label.textContent = `${done} / ${total} 완료`;
        if (done === total && total > 0) {
            section.classList.add('mission-complete');
        } else {
            section.classList.remove('mission-complete');
        }
    }

    /* ── 3. 상태 패널 탭 전환 ── */
    document.querySelectorAll('.state-panel').forEach(panel => {
        const tabs = panel.querySelectorAll('.state-tab');
        const views = panel.querySelectorAll('.state-view');

        tabs.forEach((tab, i) => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                views.forEach(v => v.classList.remove('active'));
                tab.classList.add('active');
                if (views[i]) views[i].classList.add('active');
            });
        });

        // 첫 번째 탭 활성화
        if (tabs[0]) tabs[0].classList.add('active');
        if (views[0]) views[0].classList.add('active');
    });

    /* ── 4. 시나리오 토글 ── */
    document.querySelectorAll('.scenario-card').forEach(card => {
        const header = card.querySelector('.scenario-header');
        const body = card.querySelector('.scenario-body');
        if (!header || !body) return;

        // 기본 접힘
        body.style.display = 'none';

        header.addEventListener('click', () => {
            const isOpen = body.style.display !== 'none';
            body.style.display = isOpen ? 'none' : 'block';
            card.classList.toggle('open', !isOpen);
            header.querySelector('.scenario-toggle-icon').textContent = isOpen ? '▶' : '▼';
        });
    });

});
