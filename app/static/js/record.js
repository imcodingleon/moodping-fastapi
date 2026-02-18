document.addEventListener('DOMContentLoaded', () => {
    logEvent('record_screen_view');

    let recordData = {
        moodEmoji: null,
        intensity: null,
        moodText: ''
    };

    const sectionEmoji     = document.getElementById('section-emoji');
    const sectionIntensity = document.getElementById('section-intensity');
    const sectionNote      = document.getElementById('section-note');
    const sectionResult    = document.getElementById('section-result');
    const submitBtn        = document.getElementById('submit-btn');

    // ── Step 1: 이모지 선택 ──────────────────────────────────────
    const emojiButtons = document.querySelectorAll('.emoji-btn');
    emojiButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            emojiButtons.forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');

            recordData.moodEmoji = btn.dataset.emoji;

            logEvent('emoji_selected', {emoji: recordData.moodEmoji});
            activateSection(sectionIntensity);
        });
    });

    // ── Step 2: 강도 선택 (0~10) ─────────────────────────────────
    const intensityButtons = document.querySelectorAll('.intensity-btn');
    intensityButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            intensityButtons.forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');

            recordData.intensity = parseInt(btn.dataset.value);

            logEvent('intensity_selected', {intensity: recordData.intensity});
            activateSection(sectionNote);
        });
    });

    // ── Step 3: 메모 입력 & 저장 ─────────────────────────────────
    const noteInput = document.getElementById('note-input');
    noteInput.addEventListener('focus', () => {
        logEvent('text_input_start');
    });

    submitBtn.addEventListener('click', async () => {
        recordData.moodText = noteInput.value.trim();
        const anonId = getAnonId();

        sectionResult.classList.add('visible');
        document.getElementById('loading-spinner').style.display = 'flex';
        document.getElementById('result-content').style.display = 'none';
        setTimeout(() => sectionResult.scrollIntoView({behavior: 'smooth', block: 'end'}), 100);
        submitBtn.disabled = true;

        try {
            const res = await fetch('/mood-records', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    mood_emoji: recordData.moodEmoji,
                    intensity:  recordData.intensity,
                    mood_text:  recordData.moodText,
                    anon_id:    anonId
                })
            });

            if (!res.ok) {
                throw new Error(`HTTP ${res.status}`);
            }

            const result = await res.json();

            logEvent('record_complete', {record_id: result.record_id});

            document.getElementById('loading-spinner').style.display = 'none';
            document.getElementById('result-content').style.display = 'block';

            logEvent('analysis_view', {record_id: result.record_id, status: result.analysis_status});

            if (result.analysis_status === 'success' && result.analysis) {
                const formatted = result.analysis.analysis_text.replace(/\n/g, '<br>');
                document.getElementById('feedback-text').innerHTML = formatted;
            } else {
                document.getElementById('feedback-text').textContent =
                    '에러가 발생했습니다. 기록은 정상적으로 저장되었으나 AI 분석을 불러오지 못했습니다.';
            }

        } catch (error) {
            console.error('오류:', error);
            alert('서버 통신 중 오류가 발생했습니다.');
            submitBtn.disabled = false;
            sectionResult.classList.remove('visible');
        }
    });

    // ── 최종 확인 버튼 ────────────────────────────────────────────
    document.getElementById('confirm-btn').addEventListener('click', () => {
        logEvent('feedback_confirmed').then(() => {
            window.location.href = '/';
        });
    });

    // ── 섹션 활성화 헬퍼 ─────────────────────────────────────────
    function activateSection(element) {
        if (element.classList.contains('disabled-section')) {
            element.classList.remove('disabled-section');
            element.classList.add('active-section');
            setTimeout(() => element.scrollIntoView({behavior: 'smooth', block: 'center'}), 100);
        }
    }
});
