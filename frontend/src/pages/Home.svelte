<script>
  import Logo from '../lib/components/Logo.svelte';
  import Tilt from '../lib/components/Tilt.svelte';
  import { getAuth } from '../lib/stores.svelte.js';

  const auth = getAuth();

  const features = [
    {
      icon: '🧠',
      title: 'Actually remembers you',
      text: 'Daisy builds a living memory of your life — your people, your wins, your hard weeks — and brings it into every conversation.',
    },
    {
      icon: '🎭',
      title: 'A personality you tune',
      text: 'Slide Daisy from gentle to savage, poetic to blunt, emoji-heavy to minimal. Your friend, your rules.',
    },
    {
      icon: '📖',
      title: 'Diaries written for you',
      text: 'Every night, your day becomes a beautifully written diary entry — then download it in one of 12 gorgeous designs.',
    },
    {
      icon: '🌙',
      title: 'Always there, never judging',
      text: '3am spiral or lunchbreak rant — Daisy picks up exactly where you left off. No small talk required.',
    },
  ];

  const steps = [
    { n: '01', title: 'Say hi', text: 'Create an account in seconds — email or Google.' },
    { n: '02', title: 'Talk like humans do', text: 'Vent, dream, ramble. No scripts, no prompts to learn.' },
    { n: '03', title: 'Watch it remember', text: 'Daisy quietly learns what matters to you over time.' },
    { n: '04', title: 'Keep your story', text: 'Wake up to a diary of your day. Download, keep forever.' },
  ];
</script>

<div class="relative">
  <!-- ── HERO ─────────────────────────────── -->
  <section class="mx-auto max-w-6xl px-6 pt-16 pb-24 md:pt-24 md:pb-32 text-center">
    <div class="stagger">
      <div class="flex justify-center mb-8" style="animation-delay:0s">
        <div class="relative">
          <span class="absolute inset-0 rounded-full animate-breathe" style="background:radial-gradient(circle,rgba(168,85,247,.55),transparent 70%);filter:blur(18px)"></span>
          <Logo size={88} glow={false} />
        </div>
      </div>

      <p class="text-sm tracking-[0.35em] uppercase text-[var(--color-primary-300)] font-medium mb-6">
        An AI friend who actually remembers
      </p>

      <h1 class="font-display font-extrabold leading-[1.05] tracking-tight text-4xl sm:text-6xl lg:text-7xl max-w-4xl mx-auto">
        Talk today.
        <br />
        <span class="text-gradient">Read about it tomorrow.</span>
      </h1>

      <p class="mt-7 text-lg md:text-xl text-[var(--color-ink-dim)] max-w-2xl mx-auto leading-relaxed">
        Daisy listens like a best friend, remembers like an elephant,
        and writes your life into a diary so beautiful you'll want to print it.
      </p>

      <div class="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
        <a href="#/register" class="btn-primary px-9 py-4 text-base w-full sm:w-auto">
          Meet Daisy — free
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        </a>
        <a href="#/login" class="btn-ghost px-9 py-4 text-base w-full sm:w-auto">I already have an account</a>
      </div>

      <p class="mt-5 text-xs text-[var(--color-ink-faint)]">No credit card · Your memories stay yours</p>
    </div>

    <!-- Floating chat teaser -->
    <div class="mt-20 relative mx-auto max-w-lg animate-float-slow">
      <div class="glass glow-ring rounded-3xl p-6 text-left">
        <div class="flex items-start gap-3 mb-4">
          <Logo size={34} />
          <div class="glass rounded-2xl rounded-tl-sm px-4 py-3 text-sm leading-relaxed animate-pop">
            Hey! You seemed nervous before the interview yesterday… how did it go? 🤞
          </div>
        </div>
        <div class="flex items-start gap-3 flex-row-reverse">
          <span class="w-9 h-9 shrink-0 rounded-full grid place-items-center text-sm font-bold" style="background:linear-gradient(135deg,#f472b6,#fb7185)">J</span>
          <div class="rounded-2xl rounded-tr-sm px-4 py-3 text-sm leading-relaxed animate-pop" style="background:linear-gradient(120deg,#7c3aed,#a855f7)">
            I GOT IT!! 🎉 they literally asked about the project I vented to you about last week
          </div>
        </div>
        <div class="flex items-center gap-1.5 mt-4 pl-12">
          <span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>
        </div>
      </div>
    </div>
  </section>

  <!-- ── FEATURES ─────────────────────────── -->
  <section class="mx-auto max-w-6xl px-6 pb-28">
    <h2 class="font-display text-3xl md:text-4xl font-bold text-center tracking-tight mb-3">
      More than a chatbot
    </h2>
    <p class="text-center text-[var(--color-ink-dim)] mb-14 max-w-md mx-auto">
      Daisy is built on memory, personality, and storytelling.
    </p>

    <div class="grid sm:grid-cols-2 gap-6">
      {#each features as f}
        <Tilt>
          <div class="glass card-hover rounded-3xl p-7 h-full h-min-[210px]">
            <div class="tilt-inner">
              <span class="text-4xl block mb-4">{f.icon}</span>
              <h3 class="font-display font-semibold text-xl mb-2">{f.title}</h3>
              <p class="text-[var(--color-ink-dim)] leading-relaxed text-[15px]">{f.text}</p>
            </div>
          </div>
        </Tilt>
      {/each}
    </div>
  </section>

  <!-- ── HOW IT WORKS ─────────────────────── -->
  <section class="mx-auto max-w-5xl px-6 pb-28">
    <h2 class="font-display text-3xl md:text-4xl font-bold text-center tracking-tight mb-14">
      How it <span class="text-gradient-warm">works</span>
    </h2>
    <div class="grid md:grid-cols-4 gap-8">
      {#each steps as s, i}
        <div class="relative stagger">
          <div class="font-display text-5xl font-extrabold text-transparent" style="-webkit-text-stroke:1.5px rgba(167,139,250,.45);animation-delay:{i * 0.09}s">
            {s.n}
          </div>
          <h3 class="font-display font-semibold mt-3 mb-1.5">{s.title}</h3>
          <p class="text-sm text-[var(--color-ink-dim)] leading-relaxed">{s.text}</p>
          {#if i < steps.length - 1}
            <div class="hidden md:block absolute top-6 -right-4 w-8 shimmer-line h-px"></div>
          {/if}
        </div>
      {/each}
    </div>
  </section>

  <!-- ── DIARY TEASER + CTA ───────────────── -->
  <section class="mx-auto max-w-4xl px-6 pb-32">
    <div class="glass glow-ring rounded-[2rem] p-10 md:p-14 text-center relative overflow-hidden">
      <div
        class="pointer-events-none absolute inset-0"
        style="background:radial-gradient(ellipse 60% 50% at 50% -20%,rgba(168,85,247,.25),transparent)"
      ></div>
      <div class="relative">
        <div class="text-5xl mb-6 animate-float inline-block">📖</div>
        <h2 class="font-display text-3xl md:text-4xl font-bold tracking-tight mb-4">
          Your life, beautifully written
        </h2>
        <p class="text-[var(--color-ink-dim)] max-w-lg mx-auto mb-8 leading-relaxed">
          Every day you talk to Daisy becomes a diary entry — then choose from
          <strong class="text-white">12 stunning templates</strong> and download it as a keepsake.
        </p>
        <a href={auth.isAuthenticated ? '#/diary' : '#/register'} class="btn-primary px-8 py-3.5">
          Start your first entry
        </a>
      </div>
    </div>
  </section>

  <footer class="border-t border-white/5 py-10 text-center text-sm text-[var(--color-ink-faint)]">
    Made with 💜 by Daisy · your memories are yours alone
  </footer>
</div>
