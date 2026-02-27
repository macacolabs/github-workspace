/**
 * Git & GitHub 강의 사이트 - 메인 JavaScript
 * 기능: 코드 복사, 진행 체크, 이미지 모달, 사이드바, 프로그레스
 */

/* ──────────────────────────────────────────
   1. 코드 블록 복사 버튼
   ────────────────────────────────────────── */
function initCopyButtons() {
  document.querySelectorAll('.code-block').forEach(block => {
    const pre = block.querySelector('pre');
    if (!pre) return;

    const header = block.querySelector('.code-block-header') || (() => {
      const h = document.createElement('div');
      h.className = 'code-block-header';
      block.insertBefore(h, pre);
      return h;
    })();

    // 복사 버튼 추가
    if (!header.querySelector('.copy-btn')) {
      const btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.innerHTML = '<span>📋</span> 복사';
      btn.addEventListener('click', () => {
        const text = pre.innerText
          .replace(/^\$ /gm, '')          // 프롬프트 $ 제거
          .replace(/^# .+\n?/gm, '')      // 주석줄 제거 (선택)
          .trim();
        navigator.clipboard.writeText(text).then(() => {
          btn.innerHTML = '<span>✅</span> 복사됨';
          btn.classList.add('copied');
          setTimeout(() => {
            btn.innerHTML = '<span>📋</span> 복사';
            btn.classList.remove('copied');
          }, 2000);
        }).catch(() => {
          // fallback
          const ta = document.createElement('textarea');
          ta.value = text;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          btn.innerHTML = '<span>✅</span> 복사됨';
          btn.classList.add('copied');
          setTimeout(() => {
            btn.innerHTML = '<span>📋</span> 복사';
            btn.classList.remove('copied');
          }, 2000);
        });
      });
      header.appendChild(btn);
    }
  });
}

/* ──────────────────────────────────────────
   2. 챕터 진행 상태 (localStorage)
   ────────────────────────────────────────── */
const PROGRESS_KEY = 'git-lecture-progress';
const TOTAL_CHAPTERS = 9;

function getProgress() {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY) || '{}');
  } catch { return {}; }
}

function saveProgress(data) {
  localStorage.setItem(PROGRESS_KEY, JSON.stringify(data));
}

function getChapterIdFromUrl() {
  const path = window.location.pathname;
  const match = path.match(/chapters\/(\d+)/);
  return match ? match[1] : null;
}

function getCompletedCount() {
  const progress = getProgress();
  return Object.values(progress).filter(Boolean).length;
}

function updateSidebarProgress() {
  const count = getCompletedCount();
  const pct = Math.round((count / TOTAL_CHAPTERS) * 100);

  const fill = document.querySelector('.progress-bar-fill');
  const label = document.querySelector('.progress-label span:last-child');
  if (fill) fill.style.width = pct + '%';
  if (label) label.textContent = `${count}/${TOTAL_CHAPTERS} 완료`;

  // 사이드바 nav 아이템 완료 표시
  const progress = getProgress();
  document.querySelectorAll('.sidebar-nav a[data-chapter]').forEach(a => {
    const chId = a.dataset.chapter;
    if (progress[chId]) {
      a.classList.add('completed');
    } else {
      a.classList.remove('completed');
    }
  });
}

function initCompleteButton() {
  const btn = document.querySelector('.btn-complete');
  if (!btn) return;

  const chapterId = btn.dataset.chapter || getChapterIdFromUrl();
  if (!chapterId) return;

  const progress = getProgress();

  if (progress[chapterId]) {
    btn.classList.add('done');
    btn.innerHTML = '✅ 완료됨';
  }

  btn.addEventListener('click', () => {
    const prog = getProgress();
    if (prog[chapterId]) {
      // 토글: 완료 해제
      delete prog[chapterId];
      btn.classList.remove('done');
      btn.innerHTML = '⬜ 완료 체크';
    } else {
      prog[chapterId] = true;
      btn.classList.add('done');
      btn.innerHTML = '✅ 완료됨';
      // 축하 애니메이션
      showCompletionToast();
    }
    saveProgress(prog);
    updateSidebarProgress();
    updateHeaderProgress();
  });
}

function updateHeaderProgress() {
  const text = document.querySelector('.chapter-progress-text');
  if (text) {
    const count = getCompletedCount();
    text.textContent = `${count} / ${TOTAL_CHAPTERS} 챕터 완료`;
  }
}

function showCompletionToast() {
  const toast = document.createElement('div');
  toast.style.cssText = `
    position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
    background: var(--green-dim); border: 1px solid var(--green);
    color: var(--green); padding: 12px 24px; border-radius: 8px;
    font-size: 14px; font-weight: 600; z-index: 9999;
    animation: fadeIn 0.3s ease; font-family: var(--font-body);
  `;
  toast.textContent = '🎉 챕터 완료! 다음 챕터로 넘어가세요';
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

/* ──────────────────────────────────────────
   3. 퀴즈 / 체크리스트 인터랙션
   ────────────────────────────────────────── */
function initQuizItems() {
  document.querySelectorAll('.quiz-item').forEach(item => {
    item.addEventListener('click', () => {
      item.classList.toggle('checked');
    });
  });
}

/* ──────────────────────────────────────────
   4. 이미지 모달
   ────────────────────────────────────────── */
function initImageModals() {
  // 모달 컨테이너 생성
  let modal = document.getElementById('img-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'img-modal';
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal-content">
        <button class="modal-close" id="modal-close-btn">✕</button>
        <img id="modal-img" src="" alt="">
      </div>
    `;
    document.body.appendChild(modal);
  }

  const modalImg = document.getElementById('modal-img');
  const closeBtn = document.getElementById('modal-close-btn');

  // 이미지 클릭 시 모달 열기
  document.querySelectorAll('.clickable-img, .git-diagram img, .viz-box img').forEach(img => {
    img.style.cursor = 'zoom-in';
    img.addEventListener('click', () => {
      modalImg.src = img.src;
      modalImg.alt = img.alt;
      modal.classList.add('active');
    });
  });

  // 닫기
  closeBtn.addEventListener('click', () => modal.classList.remove('active'));
  modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.classList.remove('active');
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') modal.classList.remove('active');
  });
}

/* ──────────────────────────────────────────
   5. 사이드바 현재 위치 표시
   ────────────────────────────────────────── */
function initSidebarActiveState() {
  const currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar-nav a').forEach(a => {
    if (currentPath.includes(a.getAttribute('href'))) {
      a.classList.add('active');
    }
  });
}

/* ──────────────────────────────────────────
   6. 모바일 사이드바 토글
   ────────────────────────────────────────── */
function initMobileSidebar() {
  const sidebar = document.querySelector('.sidebar');
  const toggle = document.querySelector('.menu-toggle');
  if (!toggle || !sidebar) return;

  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });

  // 바깥 클릭 시 닫기
  document.addEventListener('click', (e) => {
    if (sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) &&
        !toggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

/* ──────────────────────────────────────────
   7. 다이어그램 탭
   ────────────────────────────────────────── */
function initDiagramTabs() {
  document.querySelectorAll('.diagram-tabs').forEach(tabsEl => {
    const tabs = tabsEl.querySelectorAll('.diagram-tab');
    const parent = tabsEl.closest('.diagram-interactive');
    if (!parent) return;
    const panels = parent.querySelectorAll('.diagram-panel');

    tabs.forEach((tab, i) => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        panels.forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        panels[i]?.classList.add('active');
      });
    });
  });
}

/* ──────────────────────────────────────────
   8. 인덱스 페이지 - 카드 완료 상태 표시
   ────────────────────────────────────────── */
function initIndexPage() {
  const progress = getProgress();
  const count = getCompletedCount();
  const pct = Math.round((count / TOTAL_CHAPTERS) * 100);

  // 전체 진행률 바
  const fill = document.querySelector('.op-fill');
  const pctEl = document.querySelector('.op-pct');
  if (fill) fill.style.width = pct + '%';
  if (pctEl) pctEl.textContent = pct + '%';

  // 카드 상태
  document.querySelectorAll('.chapter-card[data-chapter]').forEach(card => {
    const id = card.dataset.chapter;
    const statusEl = card.querySelector('.card-status');
    if (statusEl && progress[id]) {
      statusEl.textContent = '✅ 완료';
      statusEl.className = 'card-status done';
    }
  });
}

/* ──────────────────────────────────────────
   9. 스크롤 애니메이션
   ────────────────────────────────────────── */
function initScrollAnimations() {
  if (!window.IntersectionObserver) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.section, .git-diagram, .highlight-box, .code-block').forEach(el => {
    observer.observe(el);
  });
}

/* ──────────────────────────────────────────
   10. Git 영역 다이어그램 - 인터랙티브 하이라이트
   ────────────────────────────────────────── */
function initGitAreaDiagram() {
  const areas = document.querySelectorAll('.git-area');
  const arrows = document.querySelectorAll('.git-arrow');

  areas.forEach((area, i) => {
    area.style.cursor = 'pointer';
    area.addEventListener('mouseenter', () => {
      areas.forEach(a => a.style.opacity = '0.4');
      area.style.opacity = '1';
      area.style.transform = 'scale(1.02)';
    });
    area.addEventListener('mouseleave', () => {
      areas.forEach(a => { a.style.opacity = '1'; a.style.transform = ''; });
    });
  });
}

/* ──────────────────────────────────────────
   초기화 진입점
   ────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initCopyButtons();
  initQuizItems();
  initImageModals();
  initSidebarActiveState();
  initMobileSidebar();
  initDiagramTabs();
  initScrollAnimations();
  initGitAreaDiagram();
  initCompleteButton();
  updateSidebarProgress();
  updateHeaderProgress();

  // 인덱스 페이지에서만
  if (document.querySelector('.index-hero')) {
    initIndexPage();
  }
});
