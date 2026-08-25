<script>
  import { api } from '../lib/api.js';
  import { setAuth, getAuth } from '../lib/stores.svelte.js';
  import { navigate } from '../lib/router.svelte.js';

  const auth = getAuth();

  // Redirect if already logged in
  $effect(() => {
    if (auth.isAuthenticated) navigate('/chat');
  });

  let email = $state('');
  let password = $state('');
  let loading = $state(false);
  let error = $state('');

  async function handleLogin() {
    if (!email || !password) { error = 'Please fill in all fields'; return; }
    loading = true;
    error = '';
    try {
      const data = await api.login({ email: email.toLowerCase().trim(), password });
      setAuth({ email: data.email }, { access: data.access, refresh: data.refresh });
      navigate('/chat');
    } catch (e) {
      if (e.requires_verification) {
        navigate('/verify-otp');
        return;
      }
      error = e.error || e.message || 'Login failed';
    } finally {
      loading = false;
    }
  }

  async function handleGoogleLogin() {
    try {
      const data = await api.getGoogleAuthUrl();
      if (data.url) window.location.href = data.url;
    } catch (e) {
      error = 'Google login unavailable';
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Enter') handleLogin();
  }
</script>

<div class="min-h-screen flex items-center justify-center px-4 pt-20">
  <div class="w-full max-w-md animate-scale">
    <div class="glass p-8 rounded-3xl">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary to-accent mx-auto flex items-center justify-center text-white font-bold text-2xl mb-4 animate-float">
          D
        </div>
        <h1 class="text-2xl font-bold text-white">Welcome back</h1>
        <p class="text-white/50 text-sm mt-1">Sign in to continue to Daisy</p>
      </div>

      <!-- Error -->
      {#if error}
        <div class="mb-4 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm animate-slide-up">
          {error}
        </div>
      {/if}

      <!-- Form -->
      <div class="space-y-4">
        <div>
          <label class="block text-sm text-white/60 mb-1.5">Email</label>
          <input
            type="email"
            bind:value={email}
            onkeydown={handleKeydown}
            placeholder="you@example.com"
            class="w-full px-4 py-3 rounded-xl bg-surface-lighter border border-glass-border text-white placeholder-white/30 text-sm transition-all duration-300"
          />
        </div>
        <div>
          <label class="block text-sm text-white/60 mb-1.5">Password</label>
          <input
            type="password"
            bind:value={password}
            onkeydown={handleKeydown}
            placeholder="••••••••"
            class="w-full px-4 py-3 rounded-xl bg-surface-lighter border border-glass-border text-white placeholder-white/30 text-sm transition-all duration-300"
          />
        </div>
      </div>

      <!-- Login button -->
      <button
        onclick={handleLogin}
        disabled={loading}
        class="w-full mt-6 py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold btn-glow hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {#if loading}
          <span class="flex items-center justify-center gap-2">
            <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            Signing in...
          </span>
        {:else}
          Sign In
        {/if}
      </button>

      <!-- Divider -->
      <div class="flex items-center gap-3 my-6">
        <div class="flex-1 h-px bg-glass-border"></div>
        <span class="text-xs text-white/30">or</span>
        <div class="flex-1 h-px bg-glass-border"></div>
      </div>

      <!-- Google -->
      <button
        onclick={handleGoogleLogin}
        class="w-full py-3 rounded-xl border border-glass-border text-white/70 font-medium hover:bg-surface-lighter hover:text-white transition-all duration-300 flex items-center justify-center gap-2"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
        Continue with Google
      </button>

      <!-- Footer -->
      <p class="text-center text-sm text-white/40 mt-6">
        Don't have an account?
        <a href="#/register" class="text-primary-light hover:text-primary transition-colors"> Sign up</a>
      </p>
    </div>
  </div>
</div>
