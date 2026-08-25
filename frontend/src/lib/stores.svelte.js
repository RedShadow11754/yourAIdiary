// Auth state using Svelte 5 runes
let _user = $state(null);
let _isAuthenticated = $state(false);

export function getAuth() {
  return {
    get user() { return _user; },
    get isAuthenticated() { return _isAuthenticated; },
  };
}

export function initAuth() {
  const token = localStorage.getItem('access_token');
  const userData = localStorage.getItem('user');
  if (token && userData) {
    _user = JSON.parse(userData);
    _isAuthenticated = true;
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
}
