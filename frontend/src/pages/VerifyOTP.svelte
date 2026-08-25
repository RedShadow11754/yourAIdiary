<script>
  import { api } from '../lib/api.js';
  import { setAuth } from '../lib/stores.svelte.js';
  import { navigate } from '../lib/router.svelte.js';

  let email = $state(localStorage.getItem('pending_email') || '');
  let code = $state('');
  let loading = $state(false);
  let error = $state('');
  let success = $state('');
  let resendTimer = $state(60);
  let canResend = $state(false);

  // Countdown timer
  $effect(() => {
    if (resendTimer > 0) {
      const interval = setInterval(() => {
        resendTimer--;
        if (resendTimer <= 0) canResend = true;
      }, 1000);
      return () => clearInterval(interval);
    }
  });

  async function handleVerify() {
    if (!code || code.length !== 6) { error = 'Please enter the 6-digit code'; return; }
    loading = true;
    error = '';
    try {
      const data = await api.verifyOtp({ email, code });
      setAuth(
        { email: data.email },
        { access: data.access, refresh: data.refresh }
      );
      localStorage.removeItem('pending_email');
      navigate('/chat');
    } catch (e) {
      error = e.error || 'Verification failed';
    } finally {
      loading = false;
    }
  }

  async function handleResend() {
    try {
      await api.resendOtp({ email });
      success = 'New code sent! Check your email.';
      resendTimer = 60;
      canResend = false;
      error = '';
    } catch (e) {
      error = e.error || 'Failed to resend code';
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Enter' && code.length === 6) handleVerify();
  }
</script>

<div class="min-h-screen flex items-center justify-center px-4 pt-20">
  <div class="w-full max-w-md animate-scale">
    <div class="glass p-8 rounded-3xl">
      <div class="text-center mb-8">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary to-accent mx-auto flex items-center justify-center text-white text-2xl mb-4">
          📧
        </div>
        <h1 class="text-2xl font-bold text-white">Verify your email</h1>
        <p class="text-white/50 text-sm mt-2">
          We sent a 6-digit code to<br/>
          <span class="text-primary-light">{email}</span>
        </p>
      </div>

      {#if error}
        <div class="mb-4 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm animate-slide-up">
          {error}
        </div>
      {/if}

      {#if success}
        <div class="mb-4 px-4 py-3 rounded-xl bg-green-500/10 border border-green-500/20 text-green-400 text-sm animate-slide-up">
          {success}
        </div>
      {/if}

      <div class="mb-6">
        <label class="block text-sm text-white/60 mb-2 text-center">Verification Code</label>
        <input
          type="text"
          bind:value={code}
          onkeydown={handleKeydown}
          maxlength="6"
          placeholder="000000"
          class="w-full px-4 py-4 rounded-xl bg-surface-lighter border border-glass-border text-white text-center text-2xl tracking-[0.5em] placeholder-white/20 font-mono transition-all duration-300"
        />
      </div>

      <button
        onclick={handleVerify}
        disabled={loading || code.length !== 6}
        class="w-full py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold btn-glow hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {#if loading}
          <span class="flex items-center justify-center gap-2">
            <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            Verifying...
          </span>
        {:else}
          Verify Code
        {/if}
      </button>

      <div class="text-center mt-6">
        {#if canResend}
          <button onclick={handleResend} class="text-sm text-primary-light hover:text-primary transition-colors">
            Resend code
          </button>
        {:else}
          <p class="text-sm text-white/30">
            Resend code in {resendTimer}s
          </p>
        {/if}
      </div>
    </div>
  </div>
</div>
