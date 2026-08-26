// Auth + toast state using Svelte 5 runes

/* ── Auth ─────────────────────────────────── */
let _user = $state(null);
let _isAuthenticated = $state(false);

export function getAuth() {
  return {
    get user() { return _user; },
    get isAuthenticated() { return _isAuthenticated; },
  };
}

export function initAuth() {
  // Handle Google OAuth redirect: /auth/google/success?access=..&refresh=..&email=..
  if (window.location.pathname === '/auth/google/success') {
    const params = new URLSearchParams(window.location.search);
    const access = params.get('access');
    const refresh = params.get('refresh');
    const email = params.get('email');
    const isNew = params.get('new_user') === '1';
    if (access && refresh && email) {
      setAuth({ email, username: email }, { access, refresh });
      window.sessionStorage.setItem('daisy_welcome', isNew ? 'new' : 'back');
      window.history.replaceState({}, '', '/');
      window.location.hash = '#/chat';
    }
  }

  const token = localStorage.getItem('access_token');
  const userData = localStorage.getItem('user');
  if (token && userData) {
    try {
      _user = JSON.parse(userData);
      _isAuthenticated = true;
    } catch {
      logout();
    }
  }
}

export function setAuth(userData, tokens) {
  _user = userData;
  _isAuthenticated = true;
  localStorage.setItem('access_token', tokens.access);
  localStorage.setItem('refresh_token', tokens.refresh);
  localStorage.setItem('user', JSON.stringify(userData));
}

export function logout() {
  _user = null;
  _isAuthenticated = false;
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
  window.location.hash = '#/';
}

/* ── Toasts ───────────────────────────────── */
let _toasts = $state([]);

export function getToasts() {
  return {
    get list() { return _toasts; },
    dismiss(id) {
      _toasts = _toasts.filter((t) => t.id !== id);
    },
  };
}

export function toast(message, type = 'info', duration = 3800) {
  const id = Math.random().toString(36).slice(2);
  _toasts.push({ id, message, type });
  setTimeout(() => {
    _toasts = _toasts.filter((t) => t.id !== id);
  }, duration);
}
