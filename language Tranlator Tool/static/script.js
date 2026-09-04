document.addEventListener('DOMContentLoaded', () => {
  const sourceLang = document.getElementById('sourceLang');
  const targetLang = document.getElementById('targetLang');
  const inputText = document.getElementById('inputText');
  const outputText = document.getElementById('outputText');
  const charCount = document.getElementById('charCount');
  const swapBtn = document.getElementById('swapBtn');
  const copyBtn = document.getElementById('copyBtn');
  const clearBtn = document.getElementById('clearBtn');
  const micBtn = document.getElementById('micBtn');
  const themeToggle = document.getElementById('themeToggle');
  const historyList = document.getElementById('historyList');

  const MAX_CHARS = 500;
  let debounceTimer; 

  // --- Dark Mode Logic (No Emojis!) ---
  if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-theme');
  }

  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    if (document.body.classList.contains('dark-theme')) {
      localStorage.setItem('theme', 'dark');
    } else {
      localStorage.setItem('theme', 'light');
    }
  });

  // --- Dynamic Typography Logic ---
  function updateFontFamily() {
    if (targetLang.value === 'ur' || targetLang.value === 'ar') {
      outputText.classList.add('urdu-text');
    } else {
      outputText.classList.remove('urdu-text');
    }
  }

  targetLang.addEventListener('change', updateFontFamily);
  updateFontFamily(); // Run once on load

  // --- History UI Logic ---
  function renderHistory() {
    const history = JSON.parse(localStorage.getItem('translationHistory') || '[]');
    if (history.length === 0) {
      historyList.innerHTML = '<p style="color: var(--text-muted); font-size: 0.9rem;">No recent translations yet.</p>';
      return;
    }

    historyList.innerHTML = history.map(item => `
      <div class="history-item" onclick="loadHistoryItem('${item.sourceText.replace(/'/g, "\\'")}', '${item.translatedText.replace(/'/g, "\\'")}', '${item.source}', '${item.target}')">
        <div class="history-langs">${item.source.toUpperCase()} ➔ ${item.target.toUpperCase()}</div>
        <div class="history-text"><strong>Original:</strong> ${item.sourceText}</div>
        <div class="history-text"><strong>Translation:</strong> ${item.translatedText}</div>
      </div>
    `).join('');
  }

  window.loadHistoryItem = function(sourceText, translatedText, source, target) {
    inputText.value = sourceText;
    outputText.value = translatedText;
    sourceLang.value = source;
    targetLang.value = target;
    updateCharCount();
    updateFontFamily();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  function saveToHistory(sourceText, translatedText, source, target) {
    const history = JSON.parse(localStorage.getItem('translationHistory') || '[]');
    if (history.length > 0 && history[0].sourceText === sourceText && history[0].target === target) return;
    
    history.unshift({ sourceText, translatedText, source, target, date: new Date().toISOString() });
    localStorage.setItem('translationHistory', JSON.stringify(history.slice(0, 5)));
    renderHistory();
  }

  // --- Core Translation Logic ---
  function updateCharCount() {
    const length = inputText.value.length;
    charCount.textContent = `${length} / ${MAX_CHARS}`;
    if (length > MAX_CHARS * 0.9) {
      charCount.classList.add('warning');
    } else {
      charCount.classList.remove('warning');
    }
  }

  async function translateText() {
    const text = inputText.value.trim();
    if (!text) {
      outputText.value = '';
      return;
    }
    
    outputText.placeholder = 'Translating...';
    try {
      const response = await fetch('/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, source: sourceLang.value, target: targetLang.value })
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      
      outputText.value = data.translatedText;
      saveToHistory(text, data.translatedText, sourceLang.value, targetLang.value);
    } catch (error) {
      outputText.value = 'Error: ' + (error.message || 'Translation failed.');
    } finally {
      outputText.placeholder = 'Translation will appear here...';
    }
  }

  inputText.addEventListener('input', () => {
    updateCharCount();
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => { translateText(); }, 800); 
  });

  targetLang.addEventListener('change', () => {
    if (inputText.value.trim()) translateText();
  });

  clearBtn.addEventListener('click', () => {
    inputText.value = '';
    outputText.value = '';
    updateCharCount();
  });

  swapBtn.addEventListener('click', () => {
    if (sourceLang.value === 'auto') return; 
    const tempLang = sourceLang.value;
    sourceLang.value = targetLang.value;
    targetLang.value = tempLang;

    const tempText = inputText.value;
    inputText.value = outputText.value;
    outputText.value = tempText;
    
    updateCharCount();
    updateFontFamily();
    if (inputText.value) translateText();
  });

  copyBtn.addEventListener('click', async () => {
    if (!outputText.value) return;
    try {
      await navigator.clipboard.writeText(outputText.value);
      copyBtn.textContent = 'Copied!';
      setTimeout(() => copyBtn.textContent = 'Copy', 2000);
    } catch (error) {
      console.error('Could not copy text.');
    }
  });

  // --- Voice Logic ---
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    
    micBtn.addEventListener('click', () => {
      recognition.lang = sourceLang.value === 'auto' ? 'en-US' : sourceLang.value;
      recognition.start();
      micBtn.classList.add('recording');
    });

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      inputText.value = transcript;
      updateCharCount();
      translateText(); 
    };

    recognition.onend = () => { micBtn.classList.remove('recording'); };
  } else {
    micBtn.style.display = 'none'; 
  }

  updateCharCount();
  renderHistory();
});