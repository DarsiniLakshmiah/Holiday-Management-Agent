/* ── State ──────────────────────────────────────────────── */
let finalMarkdown = '';
let isRunning = false;

const AGENT_KEYS = {
  Holiday_Planner:    'planner',
  Holiday_Researcher: 'researcher',
  Holiday_Writer:     'writer',
};
const STEP_ORDER = ['planner', 'researcher', 'writer'];

/* ── DOM helpers ────────────────────────────────────────── */
const $  = id => document.getElementById(id);
const show = id => $(id).style.display = '';
const hide = id => $(id).style.display = 'none';

function setStepState(key, state) {
  const el = $(`step-${key}`);
  if (!el) return;
  el.classList.remove('active', 'done');
  if (state) el.classList.add(state);
}

function setAgentStatus(key, text, done = false) {
  const el = $(`status-${key}`);
  if (!el) return;
  el.textContent = text;
  el.className = 'agent-status' + (done ? ' done' : '');
}

function appendToAgent(key, chunk) {
  const body = $(`body-${key}`);
  if (!body) return;
  body.textContent += chunk;
  body.classList.add('streaming');
  body.scrollTop = body.scrollHeight;
}

function finaliseAgent(key) {
  const body = $(`body-${key}`);
  if (body) body.classList.remove('streaming');
}

/* ── Main planning flow ─────────────────────────────────── */
async function startPlanning() {
  if (isRunning) return;

  const request = $('trip-input').value.trim();
  if (!request) {
    $('trip-input').focus();
    return;
  }

  isRunning = true;
  finalMarkdown = '';

  // Reset UI
  const btn = $('plan-btn');
  btn.disabled = true;
  btn.innerHTML = '<span class="btn-icon">⏳</span> Planning…';

  hide('placeholder');
  hide('final-section');
  hide('error-block');

  // Show panels
  show('progress-card');
  show('live-log');

  // Reset all agent blocks and steps
  STEP_ORDER.forEach(key => {
    hide(`block-${key}`);
    $(`body-${key}`).textContent = '';
    finaliseAgent(key);
    setAgentStatus(key, 'Waiting…');
    setStepState(key, null);
  });

  try {
    const response = await fetch('/plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ request }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    await readStream(response);

  } catch (err) {
    showError(err.message);
  } finally {
    isRunning = false;
    btn.disabled = false;
    btn.innerHTML = '<span class="btn-icon">✦</span> Plan My Trip';
  }
}

/* ── SSE stream reader ──────────────────────────────────── */
async function readStream(response) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let currentAgent = null;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    // Split on double-newline (SSE event boundary)
    const parts = buffer.split('\n\n');
    buffer = parts.pop(); // keep any incomplete chunk

    for (const part of parts) {
      for (const line of part.split('\n')) {
        if (!line.startsWith('data: ')) continue;
        try {
          const data = JSON.parse(line.slice(6));
          currentAgent = handleEvent(data, currentAgent);
        } catch (_) { /* ignore malformed */ }
      }
    }
  }
}

/* ── Event handler ──────────────────────────────────────── */
function handleEvent(data, currentAgent) {
  if (data.type === 'message') {
    const key = AGENT_KEYS[data.source];
    if (!key) return currentAgent; // ignore unknown agents

    // Switching to a new agent
    if (key !== currentAgent) {
      // Mark previous agent done
      if (currentAgent) {
        finaliseAgent(currentAgent);
        setStepState(currentAgent, 'done');
        setAgentStatus(currentAgent, 'Done ✓', true);
      }

      // Activate new agent
      show(`block-${key}`);
      setStepState(key, 'active');
      setAgentStatus(key, 'Working…');
      currentAgent = key;
    }

    appendToAgent(key, data.content);
    return currentAgent;
  }

  if (data.type === 'done') {
    // Mark the last agent (writer) as done
    if (currentAgent) {
      finaliseAgent(currentAgent);
      setStepState(currentAgent, 'done');
      setAgentStatus(currentAgent, 'Done ✓', true);
    }
    showFinalItinerary(data.content);
    return currentAgent;
  }

  if (data.type === 'error') {
    showError(data.content);
    return currentAgent;
  }

  return currentAgent;
}

/* ── Render final output ────────────────────────────────── */
function showFinalItinerary(markdown) {
  finalMarkdown = markdown;
  const output = $('final-output');
  output.innerHTML = marked.parse(markdown);
  show('final-section');
  $('final-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* ── Download ───────────────────────────────────────────── */
function downloadItinerary() {
  if (!finalMarkdown) return;
  const blob = new Blob([finalMarkdown], { type: 'text/markdown' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = 'itinerary.md';
  a.click();
  URL.revokeObjectURL(url);
}

/* ── Error display ──────────────────────────────────────── */
function showError(message) {
  const block = $('error-block');
  block.textContent = '⚠ Error: ' + message;
  show('error-block');
}

/* ── Allow Ctrl+Enter to submit ─────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  $('trip-input').addEventListener('keydown', e => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      startPlanning();
    }
  });
});
