// Shared quiz engine. Expects a global QUESTIONS array:
// { q: stem HTML, o: [option HTML...], a: index of correct option, r: reasoning HTML }
(function () {
  const container = document.getElementById("questions");
  const letters = "ABCDEF";
  const lettered = item => item.o.length > 2;

  QUESTIONS.forEach((item, i) => {
    const div = document.createElement("div");
    div.className = "q"; div.id = "q" + i;
    let html = `<div class="qn">Question ${i + 1} of ${QUESTIONS.length}</div><p class="stem">${item.q}</p>`;
    item.o.forEach((opt, j) => {
      const lt = lettered(item) ? letters[j] : (j === 0 ? "T" : "F");
      html += `<label><input type="radio" name="q${i}" value="${j}"><span class="lt">${lt}</span><span>${opt}</span></label>`;
    });
    const ans = lettered(item) ? `${letters[item.a]}. ${item.o[item.a]}` : item.o[item.a];
    html += `<div class="reason"><span class="verdict"></span>Correct answer: <b>${ans}</b><br>${item.r}</div>`;
    div.innerHTML = html;
    container.appendChild(div);
  });

  let seconds = 1200, timerId = null;
  const timerEl = document.getElementById("timer");
  const startBtn = document.getElementById("startBtn");
  function renderTime() {
    const m = String(Math.floor(seconds / 60)).padStart(2, "0");
    const s = String(seconds % 60).padStart(2, "0");
    timerEl.textContent = `${m}:${s}`;
    timerEl.classList.toggle("low", seconds <= 120);
  }
  function stop() { if (timerId) { clearInterval(timerId); timerId = null; } startBtn.textContent = "Start 20-min timer"; }
  startBtn.onclick = () => {
    if (timerId) return;
    startBtn.textContent = "Timer running…";
    timerId = setInterval(() => {
      seconds--; renderTime();
      if (seconds <= 0) { stop(); timerEl.textContent = "Time's up"; grade(); }
    }, 1000);
  };

  function grade() {
    stop();
    let score = 0;
    QUESTIONS.forEach((item, i) => {
      const div = document.getElementById("q" + i);
      const chosen = div.querySelector("input:checked");
      const labels = div.querySelectorAll("label");
      labels.forEach(l => l.classList.remove("is-answer", "is-wrong"));
      labels[item.a].classList.add("is-answer");
      const verdict = div.querySelector(".verdict");
      div.classList.remove("correct", "wrong");
      if (chosen && Number(chosen.value) === item.a) {
        score++; div.classList.add("correct"); verdict.textContent = "Correct";
      } else {
        div.classList.add("wrong");
        if (chosen) labels[Number(chosen.value)].classList.add("is-wrong");
        verdict.textContent = chosen ? "Not quite" : "Not answered";
      }
      div.classList.add("show");
    });
    const pct = Math.round(score / QUESTIONS.length * 100);
    const el = document.getElementById("score");
    el.textContent = `You scored ${score} / ${QUESTIONS.length} (${pct}%) — ${pct >= 60 ? "Pass" : "Below the 60% pass mark"}`;
    el.scrollIntoView({ behavior: "smooth", block: "center" });
  }
  document.getElementById("submitBtn").onclick = grade;
  document.getElementById("resetBtn").onclick = () => {
    stop(); seconds = 1200; renderTime();
    document.querySelectorAll(".q input[type=radio]").forEach(r => r.checked = false);
    document.querySelectorAll(".q").forEach(d => {
      d.classList.remove("show", "correct", "wrong");
      d.querySelectorAll("label").forEach(l => l.classList.remove("is-answer", "is-wrong"));
    });
    document.getElementById("score").textContent = "";
    document.getElementById("quiz").scrollIntoView({ behavior: "smooth" });
  };
})();
