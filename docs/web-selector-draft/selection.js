/*
 * Track B selector — pure-static rule evaluation.
 *
 * Loads matrix.json (single source of truth) and binds form events to:
 *   1) findRunner       — resolve (jdk, framework) -> runner key
 *   2) evaluateRejection — apply matrix.rejectedCombinations against {jdk, framework, status}
 *   3) buildUrl         — assemble GitHub Releases download URL
 *
 * No framework, no build chain. Migrates verbatim to upstream gh-pages.
 */

const RELEASE_BASE = 'https://github.com/JasonMMo/nexacroN-fullstack/releases/download';

async function loadMatrix() {
  const res = await fetch('./matrix.json');
  if (!res.ok) throw new Error('matrix.json fetch failed: ' + res.status);
  const json = await res.json();
  return json.nexacroVersions.nexacroN;
}

function findRunner(matrix, jdk, framework) {
  const jdkNum = Number(jdk);
  for (const [key, r] of Object.entries(matrix.runners)) {
    if (r.jdk === jdkNum && r.framework === framework) return key;
  }
  return null;
}

function evaluateRejection(matrix, jdk, framework, runnerKey) {
  const runner = runnerKey ? matrix.runners[runnerKey] : null;
  const ctx = {
    jdk: Number(jdk),
    framework,
    status: runner ? runner.status : undefined,
  };
  for (const rule of matrix.rejectedCombinations) {
    const m = rule.match;
    const matches = Object.keys(m).every(k => ctx[k] === m[k]);
    if (matches) return rule.reason;
  }
  return null;
}

function buildUrl(runnerKey, packaging, channel) {
  return `${RELEASE_BASE}/${channel}/${runnerKey}.${packaging}`;
}

function readForm() {
  const jdk = document.querySelector('input[name="jdk"]:checked').value;
  const framework = document.getElementById('framework').value;
  const channel = document.querySelector('input[name="channel"]:checked').value;
  return { jdk, framework, channel };
}

function render(matrix) {
  const { jdk, framework, channel } = readForm();
  const runnerKey = findRunner(matrix, jdk, framework);
  const runner = runnerKey ? matrix.runners[runnerKey] : null;

  const rRunner = document.getElementById('r-runner');
  const rServlet = document.getElementById('r-servlet');
  const rPkg = document.getElementById('r-pkg');
  const rUrl = document.getElementById('r-url');
  const btn = document.getElementById('download');
  const rejectBox = document.getElementById('reject');

  if (!runnerKey) {
    rRunner.textContent = '(매칭 런너 없음)';
    rServlet.textContent = rPkg.textContent = rUrl.textContent = '—';
    btn.setAttribute('aria-disabled', 'true');
    btn.removeAttribute('href');
    rejectBox.classList.add('show');
    rejectBox.textContent = `선택한 조합 (jdk=${jdk}, framework=${framework}) 에 대응하는 런너가 정의되지 않았습니다.`;
    return;
  }

  rRunner.textContent = runnerKey;
  rServlet.textContent = runner.servletApi;
  rPkg.textContent = runner.packaging;

  const reason = evaluateRejection(matrix, jdk, framework, runnerKey);
  if (reason) {
    rUrl.textContent = '—';
    btn.setAttribute('aria-disabled', 'true');
    btn.removeAttribute('href');
    rejectBox.classList.add('show');
    rejectBox.textContent = reason;
    return;
  }

  const url = buildUrl(runnerKey, runner.packaging, channel);
  rUrl.textContent = url;
  btn.setAttribute('href', url);
  btn.setAttribute('aria-disabled', 'false');
  btn.setAttribute('download', `${runnerKey}.${runner.packaging}`);
  rejectBox.classList.remove('show');
  rejectBox.textContent = '';
}

async function init() {
  let matrix;
  try {
    matrix = await loadMatrix();
  } catch (e) {
    document.getElementById('reject').classList.add('show');
    document.getElementById('reject').textContent = 'matrix.json 로드 실패: ' + e.message;
    return;
  }
  const update = () => render(matrix);
  document.querySelectorAll('input[name="jdk"], input[name="channel"]').forEach(el => {
    el.addEventListener('change', update);
  });
  document.getElementById('framework').addEventListener('change', update);
  update();
}

document.addEventListener('DOMContentLoaded', init);
