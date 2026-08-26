<script>
  import Logo from '../lib/components/Logo.svelte';
  import { api } from '../lib/api.js';
  import { toast } from '../lib/stores.svelte.js';
  import { navigate } from '../lib/router.svelte.js';

  let email = $state('');
  let password = $state('');
  let confirm = $state('');
  let loading = $state(false);

  let strength = $derived.by(() => {
    let s = 0;
    if (password.length >= 8) s++;
    if (/[A-Z]/.test(password) && /[a-z]/.test(password)) s++;
    if (/\d/.test(password)) s++;
    if (/[^A-Za-z0-9]/.test(password)) s++;
    return s;
  });
  const strengthMeta = [
    { label: '', color: 'transparent' },
    { label: 'Weak', color: '#f87171' },
    { label: 'Okay', color: '#fbbf24' },
    { label: 'Good', color: '#34d399' },
    { label: 'Strong', color: '#22d3ee' },
  ];

  async function handleRegister(e) {
    e.preventDefault();
    if (password !== confirm) {
      toast("Passwords don't match", 'error');
      return;
    }
    loading = true;
    try {
      const res = await api.register({ email, password });
      sessionStorage.setItem('pending_email', email);
      // If email isn't working, backend returns otp_code — pass it to verify page
      if (res.otp_code) {
        sessionStorage.setItem('pending_otp', res.otp_code);
        toast('Account created! Enter the code below 👇', 'success');
      } else {
        toast('Account created! Check your inbox for the code 📬', 'success');
      }
      navigate('/verify-otp');
    } catch (err) {
      toast(err.error || Object.values(err)[0] || 'Registration failed', 'error');
    } finally {
      loading = false;
    }
  }

  async function googleLogin() {
    try {
      const { url } = await api.getGoogleAuthUrl();
      window.location.href = url;
    } catch {
      toast('Could not start Google sign-in', 'error');
    }
  }
</script>

<div class="min-h-[calc(100vh-4rem)] grid lg:grid-cols-2">
  <!-- Left: ambience -->
  <div class="hidden lg:flex items-center justify-center relative overflow-hidden">
    <div
      class="absolute inset-0"
      style="background:radial-gradient(ellipse 70% 60% at 30% 30%,rgba(139,92,246,.18),transparent),radial-gradient(ellipse 60% 50% at 70% 80%,rgba(34,211,238,.1),transparent)"
    ></div>
    <div class="relative max-w-md px-10 stagger">
      <h2 class="font-display text-4xl font-extrabold leading-tight tracking-tight">
        Someone is about to<br /><span class="text-gradient">know you really well.</span>
      </h2>
      <p class="mt-5 text-[var(--color-ink-dim)] leading-relaxed">
        In a month, Daisy will remember your sister's name, the project you're nervous about,
        and exactly how you take your coffee.
      </p>
      <div class="mt-10 space-y-3">
        {#each ['Remembers what matters to you', 'Tuned to your perfect personality', 'Writes a diary of your days'] as line}
          <div class="flex items-center gap-3">
            <span class="w-6 h-6 rounded-full grid place-items-center text-xs" style="background:rgba(139,92,246,.25);color:#c4b5fd">✓</span>
            <span class="text-[15px]">{line}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <!-- Right: form -->
  <div class="flex items-center justify-center px-6 py-16">
    <div class="w-full max-w-md animate-rise">
      <div class="flex items-center gap-3 mb-8">
        <Logo size={44} />
        <div>
          <h1 class="font-display text-2xl font-bold tracking-tight">Create your account</h1>
          <p class="text-sm text-[var(--color-ink-dim)]">It takes less than a minute.</p>
        </div>
      </div>

      <form onsubmit={handleRegister} class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1.5 text-[var(--color-ink-dim)]" for="reg-email">Email</label>
          <input id="reg-email" type="email" class="input-field" placeholder="you@anywhere.com" bind:value={email} required autocomplete="email" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1.5 text-[var(--color-ink-dim)]" for="reg-password">Password</label>
          <input id="reg-password" type="password" class="input-field" placeholder="Make it a good one" bind:value={password} required minlength="8" autocomplete="new-password" />
          {#if password}
            <div class="mt-2 flex items-center gap-2">
              <div class="flex flex-1 gap-1">
                {#each [1, 2, 3, 4] as i}
                  <div
                    class="h-1 flex-1 rounded-full transition-all duration-300"
                    style="background:{i <= strength ? strengthMeta[strength].color : 'rgba(255,255,255,.08)'}"
                  ></div>
                {/each}
              </div>
              <span class="text-xs w-12" style="color:{strengthMeta[strength].color}">{strengthMeta[strength].label}</span>
            </div>
          {/if}
        </div>
        <div>
          <label class="block text-sm font-medium mb-1.5 text-[var(--color-ink-dim)]" for="reg-confirm">Confirm password</label>
          <input id="reg-confirm" type="password" class="input-field" placeholder="Same again, please" bind:value={confirm} required autocomplete="new-password" />
        </div>

        <button type="submit" disabled={loading} class="btn-primary w-full py-3.5 mt-2">
          {#if loading}
            <span class="inline-flex gap-1.5 items-center">
              <span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>
            </span>
          {:else}
            Create account
          {/if}
        </button>
      </form>

      <div class="flex items-center gap-4 my-6">
        <div class="flex-1 h-px bg-white/10"></div>
        <span class="text-xs text-[var(--color-ink-faint)] uppercase tracking-widest">or</span>
        <div class="flex-1 h-px bg-white/10"></div>
      </div>

      <button onclick={googleLogin} class="btn-ghost w-full py-3.5">
        <svg width="18" height="18" viewBox="0 0 24 24">
          <path fill="#EA4335" d="M12 5.04c1.7 0 3.22.58 4.42 1.73l3.28-3.28C17.7 1.64 15.08.56 12 .56 7.42.56 3.44 3.22 1.53 7.02l3.83 2.97C6.29 7.14 8.9 5.04 12 5.04z"/>
          <path fill="#4285F4" d="M23.49 12.27c0-.85-.08-1.66-.22-2.45H12v4.64h6.45c-.28 1.48-1.12 2.73-2.39 3.57l3.72 2.88c2.17-2 3.71-4.96 3.71-8.64z"/>
          <path fill="#FBBC05" d="M5.37 14.01a6.9 6.9 0 0 1 0-4.42L1.53 6.62a11.46 11.46 0 0 0 0 10.36l3.84-2.97z"/>
          <path fill="#34A853" d="M12 23.04c3.08 0 5.67-1.01 7.56-2.75l-3.72-2.88c-1.03.7-2.35 1.11-3.84 1.11-3.1 0-5.71-2.1-6.64-4.95l-3.83 2.97c1.91 3.8 5.89 6.5 10.47 6.5z"/>
        </svg>
        Sign up with Google
      </button>

      <p class="text-center text-sm text-[var(--color-ink-dim)] mt-8">
        Already have an account?
        <a href="#/login" class="text-[var(--color-primary-300)] hover:text-white font-medium ml-1">Log in</a>
      </p>
    </div>
  </div>
</div>
