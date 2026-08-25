<script>
  import { onMount } from 'svelte';
  import gsap from 'gsap';
  import ParticleBackground from './ParticleBackground.svelte';

  let heroRef = $state(null);
  let badgeRef = $state(null);
  let titleRef = $state(null);
  let subtitleRef = $state(null);
  let ctaRef = $state(null);
  let statsRef = $state(null);

  onMount(() => {
    const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

    tl.fromTo(badgeRef, { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8 })
      .fromTo(titleRef, { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 1 }, '-=0.4')
      .fromTo(subtitleRef, { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8 }, '-=0.6')
      .fromTo(ctaRef, { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, '-=0.4')
      .fromTo(statsRef, { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, '-=0.2');

    return () => {
      tl.kill();
    };
  });

  function scrollToFeatures(e) {
    e.preventDefault();
    const el = document.querySelector('#features');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function scrollToHowItWorks(e) {
    e.preventDefault();
    const el = document.querySelector('#how-it-works');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
</script>

<section
  id="hero"
  bind:this={heroRef}
  class="relative min-h-screen flex items-center justify-center overflow-hidden pt-20"
>
  <!-- Three.js Particle Background -->
  <ParticleBackground />

  <!-- Ambient Gradient Orbs -->
  <div class="absolute inset-0 overflow-hidden pointer-events-none">
    <div class="absolute -top-1/4 -left-1/4 w-1/2 h-1/2 bg-iris-500/20 rounded-full blur-[120px] animate-pulse-glow"></div>
    <div class="absolute -bottom-1/4 -right-1/4 w-1/2 h-1/2 bg-cyan-500/15 rounded-full blur-[120px] animate-pulse-glow" style="animation-delay: 1.5s"></div>
    <div class="absolute top-1/3 right-1/4 w-1/4 h-1/4 bg-amber-500/10 rounded-full blur-[100px] animate-pulse-glow" style="animation-delay: 3s"></div>
  </div>

  <!-- Grid Overlay -->
  <div class="absolute inset-0 opacity-[0.03]" style="background-image: linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px); background-size: 60px 60px;"></div>

  <div class="relative z-10 section-container text-center">
    <!-- Badge -->
    <div bind:this={badgeRef} class="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-8 opacity-0">
      <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
      <span class="text-sm font-medium text-slate-300">Now in Early Access</span>
    </div>

    <!-- Main Title -->
    <h1
      bind:this={titleRef}
      class="font-display text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold leading-[1.05] tracking-tight mb-6 opacity-0"
    >
      <span class="block">Your Thoughts</span>
      <span class="gradient-text block">Deserve to Be Remembered</span>
    </h1>

    <!-- Subtitle -->
    <p
      bind:this={subtitleRef}
      class="section-subtitle mx-auto text-slate-400 text-lg sm:text-xl md:text-2xl mb-10 opacity-0"
    >
      An AI companion that listens, learns, and grows with you — 
      <span class="text-white/70">turning every conversation into a lasting memory.</span>
    </p>

    <!-- CTA Buttons -->
    <div bind:this={ctaRef} class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16 opacity-0">
      <a href="#features" onclick={scrollToFeatures} class="btn-primary text-lg px-10 py-4">
        Start Your Journey
        <svg class="ml-2 w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M5 12h14M12 5l7 7-7 7" />
        </svg>
      </a>
      <a
        href="#how-it-works"
        onclick={scrollToHowItWorks}
        class="btn-secondary text-lg px-10 py-4"
      >
        <svg class="mr-2 w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10" />
          <polygon points="10 8 16 12 10 16 10 8" fill="currentColor" />
        </svg>
        See How It Works
      </a>
    </div>

    <!-- Stats -->
    <div bind:this={statsRef} class="flex flex-wrap items-center justify-center gap-8 md:gap-16 opacity-0">
      {#each [
        { value: '10K+', label: 'Active Users' },
        { value: '1M+', label: 'Memories Saved' },
        { value: '4.9', label: 'Avg. Rating' },
      ] as stat}
        <div class="text-center">
          <p class="font-display text-3xl md:text-4xl font-bold gradient-text-duo">{stat.value}</p>
          <p class="text-sm text-slate-500 mt-1">{stat.label}</p>
        </div>
      {/each}
    </div>
  </div>

  <!-- Scroll Indicator -->
  <div class="absolute bottom-8 left-1/2 -translate-x-1/2 z-10 animate-bounce">
    <svg class="w-6 h-6 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M7 13l5 5 5-5M7 6l5 5 5-5" />
    </svg>
  </div>
</section>
