 

 const textEl = document.getElementById("text");
    const sourceEl = document.getElementById("source");
    const targetEl = document.getElementById("target");
    const btn = document.getElementById("btn");
    const swapBtn = document.getElementById("swapBtn");
    const resultEl = document.getElementById("result");
    const statusEl = document.getElementById("status");
    const charCountEl = document.getElementById("charCount");
    const copyBtn = document.getElementById("copyBtn");
    const speakBtn = document.getElementById("speakBtn");

    function setResult(message, type) {
      resultEl.textContent = message;
      resultEl.classList.remove("empty", "error", "success");
      if (type === "error") resultEl.classList.add("error");
      else if (type === "success") resultEl.classList.add("success");
      else resultEl.classList.add("empty");

      const hasOk = type === "success" && message.trim().length > 0;
      copyBtn.disabled = !hasOk;
      speakBtn.disabled = !hasOk;
    }

    function setStatus(msg, cls) {
      statusEl.textContent = msg || "";
      statusEl.className = "status" + (cls ? " " + cls : "");
    }

    textEl.addEventListener("input", () => {
      charCountEl.textContent = textEl.value.length;
    });

    swapBtn.addEventListener("click", () => {
      const s = sourceEl.value;
      const t = targetEl.value;
      if (s === "auto") return;
      sourceEl.value = t;
      targetEl.value = s;
    });

    async function translate() {
      const text = textEl.value.trim();
      const source = sourceEl.value;
      const target = targetEl.value;

      if (!text) {
        setResult("Translation will appear here.", "empty");
        setStatus("Please enter some text.", "err");
        return;
      }

      if (source !== "auto" && source === target) {
        setStatus("Source and target are the same.", "err");
        return;
      }

      btn.disabled = true;
      setStatus("Translating…", "loading");
      setResult("…", "empty");

      try {
        const response = await fetch("/translate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text, source, target }),
        });

        let data;
        try {
          data = await response.json();
        } catch {
          throw new Error("Invalid response from server.");
        }

        if (!response.ok) {
          throw new Error(data.error || data.message || "Request failed.");
        }

        const out = data.translated ?? data.translation ?? "";
        if (data.error && !out) {
          throw new Error(data.error);
        }

        setResult(out || "(Empty translation)", "success");
        setStatus("Done.", "");
      } catch (e) {
        setResult(e.message || "Something went wrong.", "error");
        setStatus("", "");
      } finally {
        btn.disabled = false;
      }
    }

    btn.addEventListener("click", translate);

    textEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        translate();
      }
    });

    copyBtn.addEventListener("click", async () => {
      const t = resultEl.textContent;
      try {
        await navigator.clipboard.writeText(t);
        setStatus("Copied to clipboard.", "");
        setTimeout(() => setStatus(""), 2000);
      } catch {
        setStatus("Could not copy (permission denied).", "err");
      }
    });

    speakBtn.addEventListener("click", () => {
      const t = resultEl.textContent;
      if (!t || resultEl.classList.contains("error")) return;
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(t);
      u.lang = targetEl.value || "en";
      window.speechSynthesis.speak(u);
    });