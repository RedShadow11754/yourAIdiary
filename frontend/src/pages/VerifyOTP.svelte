<script>
  import Logo from '../lib/components/Logo.svelte';
  import { api } from '../lib/api.js';
  import { setAuth, toast } from '../lib/stores.svelte.js';
  import { navigate } from '../lib/router.svelte.js';

  let email = $state(sessionStorage.getItem('pending_email') || '');
  let manualEmail = $state(false);
  let loading = $state(false);
  let resendIn = $state(0);

  // Auto-fill OTP if passed from register flow (when email isn't working)
  const savedOtp = sessionStorage.getItem('pending_otp') || '';
  let digits = $state(savedOtp ? savedOtp.split('').concat(['', '', '', '', '', '']).slice(0, 6) : ['', '', '', '', '', '']);

  let code = $derived(digits.join(''));

  const boxes = [];

  if (!manualEmail && !email) manualEmail = true;

  // Resend countdown
  $effect(() => {
    if (resendIn <= 0) return;
    const t = setTimeout(() => resendIn--, 1000);
    return () => clearTimeout(t);
  });

  function onInput(i, e) {
    const v = e.target.value.replace(/\D/g, '').slice(-1);
    digits[i] = v;
    digits = [...digits];
    if (v && i < 5) boxes[i + 1]?.focus();
    if (code.length === 6 && !code.includes('')) verify();
  }

  function onKeydown(i, e) {
    if (e.key === 'Backspace' && !digits[i] && i > 0) {
      boxes[i - 1]?.focus();
    }
  }

  function onPaste(e) {
    e.preventDefault();
    const text = (e.clipboardData?.getData('text') || '').replace(/\D/g, '').slice(0, 6);
    if (!text) return;
    for (let i = 0; i < 6; i++) digits[i] = text[i] || '';
    digits = [...digits];
    boxes[Math.min(text.length, 5)]?.focus();
    if (text.length === 6) verify();
  }

  async function verify() {
    if (loading || code.length !== 6 || code.includes('')) return;
    loading = true;
    try {
      const res = await api.verifyOtp({ email, code });
      setAuth({ email: res.email, username: res.email }, { access: res.access, refresh: res.refresh });
      sessionStorage.removeItem('pending_email');
      sessionStorage.setItem('daisy_welcome', 'new');
      toast('Verified! Daisy can\'t wait to meet you 🌼', 'success');
      navigate('/chat');
    } catch (err) {
      toast(err.error || 'Invalid or expired code', 'error');
      digits = ['', '', '', '', '', ''];
      boxes[0]?.focus();
    } finally {
      loading = false;
    }
  }

  async function resend() {
    if (resendIn > 0 || !email) return;
    try {
      await api.resendOtp({ email });
      resendIn = 45;
      toast('New code sent ✈️', 'success');
    } catch (err) {
      toast(err.error || 'Could not resend code', 'error');
    }
  }
</script>

<div class="min-h-[calc(100vh-4rem)] flex items-center justify-center px-6 py-16">
  <div class="w-full max-w-md text-center animate-rise">
    <div class="flex justify-center mb-6">
      <div class="relative">
        <span class="absolute inset-0 rounded-full animate-breathe" style="background:radial-gradient(circle,rgba(168,85,247,.5),transparent 70%);filter:blur(14px)"></span>
        <Logo size={72} glow={false} />
      </div>
    </div>

    <h1 class="font-display text-3xl font-bold tracking-tight">Check your inbox</h1>
    <p class="mt-3 text-[var(--color-ink-dim)]">
      {#if manualEmail}
        Enter your email and the 6-digit code we sent you.
      {:else}
        We sent a 6-digit code to
        <button class="text-[var(--color-primary-300)] font-medium underline underline-offset-4 cursor-pointer" onclick={() => (manualEmail = true)}>
          {email}
        </button>
      {/if}
    </p>

    {#if manualEmail}
      <input type="email" class="input-field mt-6 text-center" placeholder="you@anywhere.com" bind:value={email} />
    {/if}

    <!-- OTP boxes -->
    <div class="flex gap-2.5 justify-center mt-8" onpaste={onPaste}>
      {#each [0, 1, 2, 3, 4, 5] as i}
        <input
          bind:this={boxes[i]}
          type="text"
          inputmode="numeric"
          maxlength="2"
          value={digits[i]}
          oninput={(e) => onInput(i, e)}
          onkeydown={(e) => onKeydown(i, e)}
          class="w-12 h-15 sm:w-14 sm:h-16 rounded-2xl glass-strong text-center font-display text-2xl font-bold transition-all duration-200
            {digits[i] ? 'border-[var(--color-primary-400)] shadow-[0_0_20px_-4px_rgba(139,92,246,.7)]' : ''}"
          style="padding-top:4px;"
          aria-label="Digit {i + 1}"
        />
      {/each}
    </div>

    {#if loading}
      <div class="flex items-center justify-center gap-1.5 mt-8">
        <span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>
        <span class="ml-2 text-sm text-[var(--color-ink-dim)]">Verifying…</span>
      </div>
    {:else}
      <button
        class="btn-primary w-full py-3.5 mt-8"
        disabled={code.length !== 6 || code.includes('')}
        onclick={verify}
      >
        Verify & enter
      </button>
    {/if}

    <p class="mt-6 text-sm text-[var(--color-ink-faint)]">
      Didn't get it?
      {#if resendIn > 0}
        <span>Resend in {resendIn}s</span>
      {:else}
        <button class="text-[var(--color-primary-300)] hover:text-white font-medium cursor-pointer" onclick={resend}>Resend code</button>
      {/if}
    </p>
  </div>
</div>
