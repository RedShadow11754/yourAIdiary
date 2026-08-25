<script>
  import { api } from '../lib/api.js';
  import { navigate } from '../lib/router.svelte.js';

  let email = $state('');
  let password = $state('');
  let confirmPassword = $state('');
  let loading = $state(false);
  let error = $state('');
  let success = $state('');

  async function handleRegister() {
    if (!email || !password) { error = 'Please fill in all fields'; return; }
    if (password !== confirmPassword) { error = 'Passwords do not match'; return; }
    if (password.length < 8) { error = 'Password must be at least 8 characters'; return; }

    loading = true;
    error = '';
    try {
      await api.register({ email: email.toLowerCase().trim(), password });
      localStorage.setItem('pending_email', email.toLowerCase().trim());
      navigate('/verify-otp');
    } catch (e) {
      error = e.error || e.email?.[0] || e.password?.[0] || 'Registration failed';
    } finally {
      loading = false;
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Enter') handleRegister();
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
        <h1 class="text-2xl font-bold text-white">Create your account</h1>
        <p class="text-white/50 text-sm mt-1">Start your journey with Daisy</p>
      </div>

      {#if error}
        <div class="mb-4 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm animate-slide-up">
          {error}
        </div>
      {/if}

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
            placeholder="Min 8 characters"
            class="w-full px-4 py-3 rounded-xl bg-surface-lighter border border-glass-border text-white placeholder-white/30 text-sm transition-all duration-300"
          />
        </div>
        <div>
          <label class="block text-sm text-white/60 mb-1.5">Confirm Password</label>
          <input
            type="password"
            bind:value={confirmPassword}
            onkeydown={handleKeydown}
            placeholder="Repeat password"
            class="w-full px-4 py-3 rounded-xl bg-surface-lighter border border-glass-border text-white placeholder-white/30 text-sm transition-all duration-300"
          />
        </div>
      </div>

      <button
        onclick={handleRegister}
        disabled={loading}
        class="w-full mt-6 py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold btn-glow hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {#if loading}
          <span class="flex items-center justify-center gap-2">
            <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            Creating account...
          </span>
        {:else}
          Create Account
        {/if}
      </button>

      <!-- Google -->
      <div class="flex items-center gap-3 my-6">
        <div class="flex-1 h-px bg-glass-border"></div>
        <span class="text-xs text-white/30">or</span>
        <div class="flex-1 h-px bg-glass-border"></div>
      </div>

      <a href="http://localhost:8000/api/auth/google/"
         class="w-full py-3 rounded-xl border border-glass-border text-white/70 font-medium hover:bg-surface-lighter hover:text-white transition-all duration-300 flex items-center justify-center gap-2">
        <svg class="w-5 h-5" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
        Sign up with Google
      </a>

      <p class="text-center text-sm text-white/40 mt-6">
        Already have an account?
        <a href="#/login" class="text-primary-light hover:text-primary transition-colors"> Sign in</a>
      </p>
    </div>
  </div>
</div>
