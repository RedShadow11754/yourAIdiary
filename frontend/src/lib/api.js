const API_BASE = (import.meta.env.VITE_API_URL || '') + '/api';

async function request(url, options = {}) {
  const token = localStorage.getItem('access_token');

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  let res = await fetch(`${API_BASE}${url}`, { ...options, headers });

  // Auto-refresh token on 401
  if (res.status === 401) {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      const refreshRes = await fetch(`${API_BASE}/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken }),
      });

      if (refreshRes.ok) {
        const data = await refreshRes.json();
        localStorage.setItem('access_token', data.access);
        headers['Authorization'] = `Bearer ${data.access}`;
        res = await fetch(`${API_BASE}${url}`, { ...options, headers });
      } else {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.hash = '#/login';
        throw new Error('Session expired');
      }
    }
  }

  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: 'Request failed' }));
    throw { status: res.status, ...error };
  }

  const text = await res.text();
  if (!text) return {};
  return JSON.parse(text);
}

export const api = {
  // Auth
  register: (data) => request('/auth/register/', { method: 'POST', body: JSON.stringify(data) }),
  verifyOtp: (data) => request('/auth/verify-otp/', { method: 'POST', body: JSON.stringify(data) }),
  resendOtp: (data) => request('/auth/resend-otp/', { method: 'POST', body: JSON.stringify(data) }),
  login: (data) => request('/auth/login/', { method: 'POST', body: JSON.stringify(data) }),
  getGoogleAuthUrl: () => request('/auth/google/'),

  // Chat
  sendMessage: (message) => request('/chat/', { method: 'POST', body: JSON.stringify({ message }) }),
  getChatHistory: () => request('/chat/history/'),

  // Personality
  updatePersonality: (data) =>
    request('/customize_personalization/', { method: 'POST', body: JSON.stringify(data) }),

  // Diary
  getDiaryEntries: () => request('/entries/'),
  getDiaryEntry: (id) => request(`/entries/${id}/`),
  editDiaryEntry: (id, content) =>
    request(`/entries/${id}/edit/`, { method: 'PATCH', body: JSON.stringify({ content }) }),
};
