<script>
  import Logo from '../lib/components/Logo.svelte';
  import { setAuth, toast } from '../lib/stores.svelte.js';
  import { navigate } from '../lib/router.svelte.js';

  // Extract tokens from the hash fragment
  // Backend redirects to: FRONTEND_URL/#/auth/google/success?access=...&refresh=...&email=...
  const hashParams = new URLSearchParams(window.location.hash.split('?')[1] || '');
  const access = hashParams.get('access');
  const refresh = hashParams.get('refresh');
  const email = hashParams.get('email');
  const newUser = hashParams.get('new_user') === '1';

  if (access && refresh && email) {
    setAuth({ email, username: email }, { access, refresh });
    toast(newUser ? "Welcome to Daisy! 🌼" : "Welcome back! Daisy missed you 🌼", 'success');
    sessionStorage.setItem('daisy_welcome', 'new');
    navigate('/chat');
  } else {
    toast('Google sign-in failed — no tokens received', 'error');
    navigate('/login');
  }
</script>

<div class="min-h-[calc(100vh-4rem)] flex items-center justify-center">
  <div class="text-center animate-rise">
    <Logo size={64} />
    <p class="mt-6 text-[var(--color-ink-dim)]">Signing you in with Google…</p>
    <div class="flex items-center justify-center gap-1.5 mt-4">
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
    </div>
  </div>
</div>
