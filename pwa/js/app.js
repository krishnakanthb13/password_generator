const AUTH_CONFIG = {
    // Priority: 1. LocalStorage (custom) -> 2. Environment (default)
    apiKey: localStorage.getItem('passforge_api_key') || 'default_secret_key'
};

const state = {
    currentType: 'random',
    config: {
        random: { length: 16, uppercase: true, lowercase: true, digits: true, symbols: true, easy_read: false, easy_say: false, balanced: false, no_repeats: false, min_upper: 0, min_lower: 0, min_digits: 0, min_symbols: 0, include: '', exclude: '' },
        phrase: { words: 4, separator: '-', capitalize: false, easy_read: false },
        pin: { length: 6 },
        wifi: { length: 16, simple: false },
        otp: { otp_digits: 6, period: 30 },
        uuid: { uppercase: false },
        leet: { words: 3, separator: '-' },
        pronounce: { length: 12 },
        license: { segments: 4, segment_length: 4 },
        pattern: { grid: 3 },
        phonetic: { text: '', length: 8 },
        recovery: {},
        analyze: { password: '' },
        base64: { length: 32, url_safe: true },
        jwt: { bits: 256, hex: false }
    },
    presets: {},
    history: [],
    searchQuery: ''
};

// UI Elements
const elements = {
    passwordDisplay: document.getElementById('password-display'),
    entropyValue: document.getElementById('entropy-value'),
    generateBtn: document.getElementById('generate-btn'),
    copyBtn: document.getElementById('copy-btn'),
    controlsContainer: document.getElementById('controls-container'),
    pageTitle: document.getElementById('page-title'),
    navItems: document.querySelectorAll('.nav-item'),
    themeToggle: document.getElementById('theme-toggle'),
    themeIcon: document.getElementById('theme-icon'),
    themeText: document.getElementById('theme-text'),
    qrContainer: document.getElementById('qr-container'),
    historyList: document.getElementById('history-list'),
    toast: document.getElementById('toast'),
    toastMessage: document.getElementById('toast-message'),
    apiKeyInput: document.getElementById('api-key-input'),
    saveKeyBtn: document.getElementById('save-key-btn'),
    forceReloadBtn: document.getElementById('force-reload-btn'),
    keyStatusBadge: document.getElementById('key-status-badge')
};

const controlSchema = {
    random: [
        { id: 'preset', label: 'Security Preset', type: 'preset' },
        { id: 'length', label: 'Length', type: 'range', min: 4, max: 128, step: 1 },
        { id: 'uppercase', label: 'Uppercase', type: 'checkbox' },
        { id: 'lowercase', label: 'Lowercase', type: 'checkbox' },
        { id: 'digits', label: 'Digits', type: 'checkbox' },
        { id: 'symbols', label: 'Symbols', type: 'checkbox' },
        { id: 'easy_read', label: 'Easy to Read', type: 'checkbox' },
        { id: 'easy_say', label: 'Easy to Say', type: 'checkbox' },
        { id: 'no_repeats', label: 'No Repeats', type: 'checkbox' },
        { id: 'balanced', label: 'Balanced Ratio', type: 'checkbox' },
        { id: 'include', label: 'Include Chars', type: 'text' },
        { id: 'exclude', label: 'Exclude Chars', type: 'text' }
    ],
    phrase: [
        { id: 'words', label: 'Words', type: 'range', min: 2, max: 12, step: 1 },
        { id: 'separator', label: 'Separator', type: 'select', options: ['-', '_', '.', ' ', ','] },
        { id: 'capitalize', label: 'Capitalize', type: 'checkbox' }
    ],
    pin: [
        { id: 'length', label: 'Length', type: 'range', min: 4, max: 16, step: 1 }
    ],
    wifi: [
        { id: 'length', label: 'Length', type: 'range', min: 8, max: 63, step: 1 },
        { id: 'simple', label: 'Alpha-only', type: 'checkbox' }
    ],
    leet: [
        { id: 'words', label: 'Words', type: 'range', min: 2, max: 8, step: 1 },
        { id: 'separator', label: 'Separator', type: 'select', options: ['-', '_', '.', ','] }
    ],
    license: [
        { id: 'segments', label: 'Segments', type: 'range', min: 2, max: 10, step: 1 },
        { id: 'segment_length', label: 'Length', type: 'range', min: 2, max: 10, step: 1 }
    ],
    pattern: [
        { id: 'grid', label: 'Grid Size', type: 'select', options: [3, 4, 5] }
    ],
    phonetic: [
        { id: 'text', label: 'Text to Phonetic', type: 'text' },
        { id: 'length', label: 'Random Length', type: 'range', min: 4, max: 32, step: 1 }
    ],
    analyze: [
        { id: 'password', label: 'Password to Check', type: 'text' }
    ],
    base64: [
        { id: 'length', label: 'Byte Length', type: 'range', min: 8, max: 128, step: 1 },
        { id: 'url_safe', label: 'URL Safe', type: 'checkbox' }
    ],
    jwt: [
        { id: 'bits', label: 'Bit Length', type: 'range', min: 128, max: 1024, step: 64 },
        { id: 'hex', label: 'Output as Hex', type: 'checkbox' }
    ],
    pronounce: [
        { id: 'length', label: 'Length', type: 'range', min: 6, max: 32, step: 1 }
    ],
    otp: [
        { id: 'otp_digits', label: 'Digits', type: 'select', options: [6, 8] },
        { id: 'period', label: 'Period (s)', type: 'range', min: 15, max: 120, step: 15 }
    ],
    uuid: [
        { id: 'uppercase', label: 'Uppercase', type: 'checkbox' }
    ],
    recovery: []
};

async function init() {
    await fetchPresets();
    await attemptBootstrap();

    // Setup Navigation
    elements.navItems.forEach(btn => {
        btn.addEventListener('click', () => {
            const type = btn.dataset.type;
            if (type) switchTab(type);
        });
    });

    // Theme Toggle
    if (elements.themeToggle) {
        elements.themeToggle.addEventListener('click', toggleTheme);
    }

    // Initial Theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    // Action Buttons
    if (elements.generateBtn) elements.generateBtn.addEventListener('click', generate);
    if (elements.copyBtn) elements.copyBtn.addEventListener('click', copyToClipboard);

    // Initial Security Check
    updateKeyStatus();

    // Click password display to copy
    if (elements.passwordDisplay) {
        elements.passwordDisplay.addEventListener('click', copyToClipboard);
    }

    // Start
    renderControls();
    generate();
    fetchHistory();

    // History Copy Event Delegation
    if (elements.historyList) {
        elements.historyList.addEventListener('click', (e) => {
            const btn = e.target.closest('.history-copy-btn');
            if (btn) {
                const index = btn.dataset.index;
                const item = state.history[index];
                if (item) copyText(item.password);
            }
        });
    }

    // Register Service Worker for PWA features
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('./sw.js').catch(() => {
                // Fail silently in development/non-HTTPS
            });
        });
    }

    // Security: API Key Handling
    if (elements.apiKeyInput) {
        elements.apiKeyInput.value = localStorage.getItem('passforge_api_key') || '';
    }
    if (elements.saveKeyBtn) {
        elements.saveKeyBtn.addEventListener('click', () => {
            const newKey = elements.apiKeyInput.value.strip ? elements.apiKeyInput.value.strip() : elements.apiKeyInput.value.trim();
            localStorage.setItem('passforge_api_key', newKey);
            AUTH_CONFIG.apiKey = newKey || 'default_secret_key';
            showToast("Security key updated!");
            updateKeyStatus();
            if (state.currentType === 'history') fetchHistory();
        });
    }

    if (elements.forceReloadBtn) {
        elements.forceReloadBtn.addEventListener('click', async () => {
            showToast("Force refreshing app...", "warning");

            // Unregister Service Workers
            if ('serviceWorker' in navigator) {
                const registrations = await navigator.serviceWorker.getRegistrations();
                for (let registration of registrations) {
                    await registration.unregister();
                }
            }

            // Clear Caches
            if ('caches' in window) {
                const keys = await caches.keys();
                for (let key of keys) {
                    await caches.delete(key);
                }
            }

            // Hard reload
            window.location.reload(true);
        });
    }
}

async function fetchPresets() {
    try {
        const res = await fetch('/api/presets');
        if (res.ok) {
            state.presets = await res.json();
        } else {
            const errorData = await res.json().catch(() => ({}));
            showToast(`Failed to load presets: ${errorData.detail || res.statusText}`, "danger");
        }
    } catch (err) {
        showToast("Network error loading security presets", "danger");
    }
}

function switchTab(type) {
    elements.navItems.forEach(n => n.classList.remove('active'));
    const activeBtn = Array.from(elements.navItems).find(n => n.dataset.type === type);
    if (activeBtn) activeBtn.classList.add('active');

    state.currentType = type;
    if (activeBtn) {
        elements.pageTitle.textContent = activeBtn.querySelector('span').textContent + (type === 'history' ? '' : ' Generator');
    }

    // Toggle Sections
    const generatorSection = document.querySelector('.generator-section');
    const historySection = document.getElementById('history-section');
    const searchInput = document.getElementById('history-search');

    if (type === 'history') {
        generatorSection.classList.add('hidden');
        historySection.classList.remove('hidden');
        fetchHistory(); // Ensure fresh data

        // Setup search listener if not already attached (simple check)
        if (searchInput && !searchInput.dataset.listening) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    state.searchQuery = e.target.value;
                    fetchHistory();
                }, 300);
            });
            searchInput.dataset.listening = "true";
        }
    } else {
        generatorSection.classList.remove('hidden');
        historySection.classList.add('hidden');
        renderControls();
        // Clear display or regenerate? Regenerate feels snappier.
        if (type !== 'analyze') generate();
        else {
            elements.passwordDisplay.textContent = 'Enter password...';
            elements.entropyValue.textContent = '0';
            elements.qrContainer.innerHTML = '<div class="qr-placeholder"><i data-lucide="search" style="width: 40px; height: 40px;"></i></div>';
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    }
}

function renderControls() {
    elements.controlsContainer.innerHTML = '';

    // Add class for specific layouts (like random grid)
    elements.controlsContainer.className = `controls-container type-${state.currentType}`;

    const schema = controlSchema[state.currentType];
    if (!schema) return;

    schema.forEach(ctrl => {
        const item = document.createElement('div');
        item.className = 'control-item';

        if (ctrl.type === 'range') {
            const val = state.config[state.currentType][ctrl.id];
            item.innerHTML = `
                <div class="control-label">
                    <span>${ctrl.label}</span>
                    <span id="val-${ctrl.id}">${val}</span>
                </div>
                <input type="range" id="input-${ctrl.id}" min="${ctrl.min}" max="${ctrl.max}" step="${ctrl.step}" value="${val}">
            `;
            const input = item.querySelector('input');
            input.addEventListener('input', (e) => {
                const newValue = e.target.value;
                state.config[state.currentType][ctrl.id] = parseInt(newValue);
                document.getElementById(`val-${ctrl.id}`).textContent = newValue;
            });
        } else if (ctrl.type === 'checkbox') {
            const checked = state.config[state.currentType][ctrl.id] ? 'checked' : '';
            item.innerHTML = `
                <label class="checkbox-item">
                    <input type="checkbox" id="input-${ctrl.id}" ${checked}>
                    <span>${ctrl.label}</span>
                </label>
            `;
            const input = item.querySelector('input');
            input.addEventListener('change', (e) => {
                state.config[state.currentType][ctrl.id] = e.target.checked;
            });
        } else if (ctrl.type === 'select') {
            const selected = state.config[state.currentType][ctrl.id];
            item.innerHTML = `
                <div class="control-label">
                    <span>${ctrl.label}</span>
                </div>
                <select id="input-${ctrl.id}" class="glass input-glass">
                    ${ctrl.options.map(opt => `<option value="${opt}" ${opt == selected ? 'selected' : ''}>${opt === ' ' ? 'Space' : opt}</option>`).join('')}
                </select>
            `;
            const input = item.querySelector('select');
            input.addEventListener('change', (e) => {
                state.config[state.currentType][ctrl.id] = e.target.value;
            });
        } else if (ctrl.type === 'text') {
            const val = state.config[state.currentType][ctrl.id] || '';
            item.innerHTML = `
                <div class="control-label">
                    <span>${ctrl.label}</span>
                </div>
                <input type="text" id="input-${ctrl.id}" class="glass input-glass">
            `;
            const input = item.querySelector('input');
            input.value = val; // Programmatic assignment to avoid XSS
            input.addEventListener('input', (e) => {
                state.config[state.currentType][ctrl.id] = e.target.value;
            });
        } else if (ctrl.type === 'preset') {
            item.innerHTML = `
                <div class="control-label">
                    <span>${ctrl.label}</span>
                </div>
                <select id="input-preset" class="glass input-glass">
                    <option value="">Custom (Manual)</option>
                </select>
            `;
            const select = item.querySelector('select');

            // Programmatically add options to prevent XSS from preset keys
            Object.keys(state.presets).forEach(name => {
                const opt = document.createElement('option');
                opt.value = name;
                opt.textContent = name.charAt(0).toUpperCase() + name.slice(1);
                select.appendChild(opt);
            });

            select.addEventListener('change', (e) => {
                const presetName = e.target.value;
                if (!presetName) return;
                const preset = state.presets[presetName];

                // Update config from preset
                Object.keys(preset).forEach(key => {
                    if (key !== 'command') {
                        let configKey = key;
                        if (key.startsWith('min_')) {
                            configKey = key.replace('min_uppercase', 'min_upper').replace('min_lowercase', 'min_lower');
                        }
                        state.config[state.currentType][configKey] = preset[key];
                    }
                });
                renderControls();
                generate();
            });
        }

        elements.controlsContainer.appendChild(item);
    });
}

async function generate() {
    if (elements.generateBtn) {
        elements.generateBtn.disabled = true;
        elements.generateBtn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Generating...';
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    const config = state.config[state.currentType] || {};

    // Analyze Mode
    if (state.currentType === 'analyze') {
        try {
            const password = config.password || '';
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password })
            });
            const data = await response.json();
            if (response.ok) {
                elements.passwordDisplay.innerHTML = colorizePassword(password || "No input");
                elements.entropyValue.textContent = data.entropy || 0;

                let detailsHtml = `Score: ${data.strength?.score}/4<br>`;
                if (data.strength?.warning) {
                    detailsHtml += `Warning: ${escapeHtml(data.strength.warning)}<br>`;
                }
                if (data.strength?.suggestions?.length) {
                    detailsHtml += `Tip: ${escapeHtml(data.strength.suggestions[0])}`;
                }

                elements.qrContainer.innerHTML = `<div style="text-align:left; font-size:0.85rem; padding:1rem; color:var(--text-primary); line-height:1.5;">${detailsHtml}</div>`;
            } else {
                showToast(data.detail, "danger");
            }
        } catch (err) {
            showToast("Failed to analyze password", "danger");
        } finally {
            if (elements.generateBtn) {
                elements.generateBtn.disabled = false;
                elements.generateBtn.innerHTML = '<i data-lucide="search"></i> Analyze';
                if (typeof lucide !== 'undefined') lucide.createIcons();
            }
        }
        return;
    }

    // Generator Mode
    // Prepare query params
    const params = new URLSearchParams();
    params.append('type', state.currentType);
    params.append('log', 'true');

    Object.keys(config).forEach(key => {
        params.append(key, config[key]);
    });

    try {
        const response = await fetch(`/api/generate?${params.toString()}`);
        const data = await response.json();

        if (response.ok) {
            state.lastGenerated = data.password; // Store raw password
            elements.passwordDisplay.innerHTML = colorizePassword(data.password);
            elements.entropyValue.textContent = data.entropy;

            if (data.qr) {
                elements.qrContainer.innerHTML = `<img src="data:image/png;base64,${data.qr}" alt="QR Code">`;
            } else {
                elements.qrContainer.innerHTML = '<div class="qr-placeholder"><i data-lucide="qr-code"></i></div>';
                if (typeof lucide !== 'undefined') lucide.createIcons();
            }

            // Optimization: Append to local state immediately instead of doing a full re-fetch
            const historyEntry = {
                password: data.password,
                generator_type: data.type,
                timestamp: new Date().toISOString()
            };
            state.history.unshift(historyEntry);
            if (state.history.length > 50) state.history.pop();
            renderHistory();
        } else {
            const msg = typeof data.detail === 'object' ? JSON.stringify(data.detail) : data.detail;
            showToast("Error: " + msg, "danger");
        }
    } catch (err) {
        showToast("Connection failed", "danger");
    } finally {
        if (elements.generateBtn) {
            elements.generateBtn.disabled = false;
            elements.generateBtn.innerHTML = '<i data-lucide="zap"></i> Generate New';
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    }
}

async function copyToClipboard() {
    // Use the stored raw password to avoid whitespace/span artifacts from colorized HTML
    const text = state.lastGenerated || elements.passwordDisplay.textContent;
    if (!text || text === 'Initializing...' || text === 'Enter password...') {
        showToast("Nothing to copy yet", "danger");
        return;
    }
    try {
        await navigator.clipboard.writeText(text);
        showToast("Copied to clipboard!");
    } catch (err) {
        // Fallback for older browsers / non-HTTPS contexts
        try {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.opacity = '0';
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showToast("Copied to clipboard!");
        } catch (fallbackErr) {
            showToast("Failed to copy", "danger");
        }
    }
}

// History
async function fetchHistory() {
    try {
        // Search
        const searchInput = document.getElementById('history-search');
        const query = searchInput ? searchInput.value : '';

        const url = `/api/history?limit=50${query ? `&search=${encodeURIComponent(query)}` : ''}`;
        const res = await fetch(url, {
            headers: { 'X-API-Key': AUTH_CONFIG.apiKey }
        });
        if (res.ok) {
            const data = await res.json();
            state.history = data;
            renderHistory();
        } else if (res.status === 401) {
            showToast("History access denied. Please enter your API Key.", "danger");
            updateKeyStatus();
        }
    } catch (err) {
        showToast("Failed to sync history", "danger");
    }
}

function renderHistory() {
    if (!elements.historyList) return;
    elements.historyList.innerHTML = state.history.map((item, index) => `
        <div class="history-item">
            <div class="history-content">
                <div class="history-item-pwd">${colorizePassword(item.password)}</div>
                <div class="history-item-meta">${escapeHtml(item.generator_type)} • ${new Date(item.timestamp).toLocaleString()}</div>
            </div>
            <button class="icon-btn history-copy-btn" data-index="${index}" title="Copy">
                <i data-lucide="copy"></i>
            </button>
        </div>
    `).join('');
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function colorizePassword(password) {
    if (typeof password !== 'string') return password;
    return Array.from(password).map(char => {
        let className = 'symbol';
        if (/[A-Z]/.test(char)) className = 'upper';
        else if (/[a-z]/.test(char)) className = 'lower';
        else if (/[0-9]/.test(char)) className = 'digit';
        else if (/\s|\n|\t|[-_]/.test(char)) return escapeHtml(char);

        return `<span class="${className}">${escapeHtml(char)}</span>`;
    }).join('');
}

function escapeHtml(text) {
    if (typeof text !== 'string') return text;
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

async function copyText(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast("Copied from history!");
    } catch (err) {
        showToast("Failed to copy from history", "danger");
    }
}

// Theme
function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.getAttribute('data-theme') === 'dark';
    const nextTheme = isDark ? 'light' : 'dark';

    html.setAttribute('data-theme', nextTheme);
    localStorage.setItem('theme', nextTheme);
    updateThemeIcon(nextTheme);
}

function updateThemeIcon(theme) {
    if (elements.themeIcon && elements.themeText) {
        const isDark = theme === 'dark';
        elements.themeIcon.setAttribute('data-lucide', isDark ? 'moon' : 'sun');
        elements.themeText.textContent = isDark ? 'Dark Mode' : 'Light Mode';
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }
}

let toastTimeout;
function showToast(message, type = "success") {
    if (!elements.toast || !elements.toastMessage) return;

    // Clear existing timeout to handle rapid toasts
    if (toastTimeout) clearTimeout(toastTimeout);

    elements.toastMessage.textContent = message;
    elements.toast.classList.remove('hidden');

    toastTimeout = setTimeout(() => {
        elements.toast.classList.add('hidden');
    }, 3000);
}

async function updateKeyStatus() {
    if (!elements.keyStatusBadge) return;

    try {
        const url = `/api/history?limit=1`;
        const res = await fetch(url, {
            headers: { 'X-API-Key': AUTH_CONFIG.apiKey }
        });

        if (res.ok) {
            elements.keyStatusBadge.innerText = "Unlocked";
            elements.keyStatusBadge.style.background = "rgba(34, 197, 94, 0.2)";
            elements.keyStatusBadge.style.color = "#22c55e";
            elements.keyStatusBadge.style.borderColor = "#22c55e";
        } else {
            elements.keyStatusBadge.innerText = "Locked";
            elements.keyStatusBadge.style.background = "rgba(239, 68, 68, 0.2)";
            elements.keyStatusBadge.style.color = "#ef4444";
            elements.keyStatusBadge.style.borderColor = "#ef4444";
        }
    } catch (err) {
        // Silent fail
    }
}

async function attemptBootstrap() {
    // Skip if already have a custom key that works
    if (localStorage.getItem('passforge_api_key')) return;

    try {
        const res = await fetch('/api/bootstrap');
        if (res.ok) {
            const data = await res.json();
            if (data.apiKey && data.apiKey !== 'default_secret_key') {
                localStorage.setItem('passforge_api_key', data.apiKey);
                AUTH_CONFIG.apiKey = data.apiKey;
                if (elements.apiKeyInput) elements.apiKeyInput.value = data.apiKey;
                showToast("Authenticated automatically via Local Trust");
                updateKeyStatus();
            }
        }
    } catch (e) {
        console.log("Bootstrap skipped: Remote access or server no supports bootstrap");
    }
}

// Initialize
init();
