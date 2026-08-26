<script>
  import Logo from '../lib/components/Logo.svelte';
  import { api } from '../lib/api.js';
  import { setAuth, toast } from '../lib/stores.svelte.js';
  import { navigate } from '../lib/router.svelte.js';

  let email = $state('');
  let password = $state('');
  let loading = $state(false);
  let googleLoading = $state(false);
  let showPassword = $state(false);

  async function handleLogin(e) {
    e.preventDefault();
    if (!email || !password) return;
    loading = true;
    try {
      const res = await api.login({ email, password });
      setAuth({ email: res.email, username: res.email }, { access: res.access, refresh: res.refresh });
      toast(`Welcome back! Daisy missed you 🌼`, 'success');
      navigate('/chat');
    } catch (err) {
      if (err.requires_verification) {
        sessionStorage.setItem('pending_email', err.email || email);
        navigate('/verify-otp');
        toast(err.error, 'info');
      } else {
        toast(err.error || 'Login failed', 'error');
      }
    } finally {
      loading = false;
    }
  }

  async function googleLogin() {
    googleLoading = true;
    try {
      const { url } = await api.getGoogleAuthUrl();
      window.location.href = url;
    } catch {
      toast('Could not start Google sign-in', 'error');
      googleLoading = false;
    }
  }
</script>

<div class="min-h-[calc(100vh-4rem)] grid lg:grid-cols-2">
  <!-- Left: form -->
  <div class="flex items-center justify-center px-6 py-16">
    <div class="w-full max-w-md animate-rise">
      <div class="flex items-center gap-3 mb-8">
        <Logo size={44} />
        <div>
          <h1 class="font-display text-2xl font-bold tracking-tight">Welcome back</h1>
          <p class="text-sm text-[var(--color-ink-dim)]">Daisy kept every memory safe.</p>
        </div>
      </div>

      <form onsubmit={handleLogin} class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1.5 text-[var(--color-ink-dim)]" for="login-email">Email</label>
          <input id="login-email" type="email" class="input-field" placeholder="you@anywhere.com" bind:value={email} autocomplete="email" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1.5 text-[var(--color-ink-dim)]" for="login-password">Password</label>
          <div class="relative">
            <input
              id="login-password"
              type={showPassword ? 'text' : 'password'}
              class="input-field pr-12"
              placeholder="••••••••"
              bind:value={password}
              autocomplete="current-password"
            />
            <button
              type="button"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--color-ink-faint)] hover:text-white cursor-pointer"
              onclick={() => (showPassword = !showPassword)}
              aria-label="Toggle password visibility"
            >
              {showPassword ? '🙈' : '👁️'}
            </button>
          </div>
        </div>

        <button type="submit" disabled={loading} class="btn-primary w-full py-3.5 mt-2">
          {#if loading}
            <span class="inline-flex gap-1.5 items-center">
              <span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>
            </span>
          {:else}
            Log in
          {/if}
        </button>
      </form>

      <div class="flex items-center gap-4 my-6">
        <div class="flex-1 h-px bg-white/10"></div>
        <span class="text-xs text-[var(--color-ink-faint)] uppercase tracking-widest">or</span>
        <div class="flex-1 h-px bg-white/10"></div>
      </div>

      <button onclick={googleLogin} disabled={googleLoading} class="btn-ghost w-full py-3.5">
        <svg width="18" height="18" viewBox="0 0 24 24">
          <path fill="#EA4335" d="M12 5.04c1.7 0 3.22.58 4.42 1.73l3.28-3.28C17.7 1.64 15.08.56 12 .56 7.42.56 3.44 3.22 1.53 7.02l3.83 2.97C6.29 7.14 8.9 5.04 12 5.04z"/>
          <path fill="#4285F4" d="M23.49 12.27c0-.85-.08-1.66-.22-2.45H12v4.64h6.45c-.28 1.48-1.12 2.73-2.39 3.57l3.72 2.88c2.17-2 3.71-4.96 3.71-8.64z"/>
          <path fill="#FBBC05" d="M5.37 14.01a6.9 6.9 0 0 1 0-4.42L1.53 6.62a11.46 11.46 0 0 0 0 10.36l3.84-2.97z"/>
          <path fill="#34A853" d="M12 23.04c3.08 0 5.67-1.01 7.56-2.75l-3.72-2.88c-1.03.7-2.35 1.11-3.84 1.11-3.1 0-5.71-2.1-6.64-4.95l-3.83 2.97c1.91 3.8 5.89 6.5 10.47 6.5z"/>
        </svg>
        Continue with Google
      </button>

      <p class="text-center text-sm text-[var(--color-ink-dim)] mt-8">
        New here?
        <a href="#/register" class="text-[var(--color-primary-300)] hover:text-white font-medium ml-1">Create an account</a>
      </p>
    </div>
  </div>

  <!-- Right: ambience panel -->
  <div class="hidden lg:flex items-center justify-center relative overflow-hidden">
    <div
      class="absolute inset-0"
      style="background:radial-gradient(ellipse 70% 60% at 70% 30%,rgba(139,92,246,.18),transparent),radial-gradient(ellipse 60% 50% at 30% 80%,rgba(244,114,182,.12),transparent)"
    ></div>
    <div class="relative max-w-md px-10 stagger">
      <blockquote class="font-hand text-4xl leading-snug text-[var(--color-primary-200)]">
        "I told her about the job offer on Tuesday. She still asks how my first week went."
      </blockquote>
      <p class="mt-6 text-sm text-[var(--color-ink-dim)]">— Maya, talking to Daisy for 214 days straight</p>
      <div class="mt-10 flex gap-3">
        <span class="glass rounded-full px-4 py-2 text-xs">🧠 remembers context</span>
        <span class="glass rounded-full px-4 py-2 text-xs">📖 writes diaries</span>
      </div>
    </div>
  </div>
</div>
