<script>
  import { onMount } from 'svelte';
  import gsap from 'gsap';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';

  let sectionRef = $state(null);
  let contentRef = $state(null);

  onMount(() => {
    if (contentRef) {
      gsap.fromTo(
        contentRef,
        { y: 60, opacity: 0 },
        {
          y: 0, opacity: 1,
          duration: 1,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: sectionRef,
            start: 'top bottom-=100',
            toggleActions: 'play none none reverse',
          },
        }
      );
    }
  });
</script>

<section id="cta" bind:this={sectionRef} class="relative section-padding">
  <!-- Background -->
  <div class="absolute inset-0 overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-b from-midnight-900 via-iris-950/30 to-midnight-900"></div>
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-radial from-iris-500/10 via-iris-500/5 to-transparent rounded-full blur-[80px] animate-pulse-glow"></div>
  </div>

  <div bind:this={contentRef} class="section-container relative z-10 opacity-0">
    <div class="max-w-4xl mx-auto text-center">
      <!-- Icon -->
      <div class="w-16 h-16 rounded-2xl bg-gradient-primary mx-auto mb-8 flex items-center justify-center shadow-2xl shadow-iris-500/20">
        <svg class="w-8 h-8 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 2L2 7l10 5 10-5-10-5z" />
          <path d="M2 17l10 5 10-5" />
          <path d="M2 12l10 5 10-5" />
        </svg>
      </div>

      <!-- Heading -->
      <h2 class="font-display text-4xl md:text-5xl lg:text-7xl font-bold leading-tight mb-6">
        Ready to Start Your
        <span class="gradient-text">Conversation?</span>
      </h2>

      <p class="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
        Join thousands of people who've discovered the power of a diary that truly listens. 
        Your first entry is just a moment away.
      </p>

      <!-- CTA Buttons -->
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
        <button class="btn-primary text-lg px-12 py-5 group">
          Get Started Free
          <svg class="ml-2 w-5 h-5 inline-block transition-transform group-hover:translate-x-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>
        <button class="btn-secondary text-lg px-12 py-5">
          <svg class="mr-2 w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
            <polyline points="14 2 14 8 20 8" />
          </svg>
          View Documentation
        </button>
      </div>

      <!-- Trust badges -->
      <div class="flex flex-wrap items-center justify-center gap-6 text-sm text-slate-500">
        <span class="flex items-center gap-1.5">
          <svg class="w-4 h-4 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 11-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </svg>
          No credit card required
        </span>
        <span class="flex items-center gap-1.5">
          <svg class="w-4 h-4 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
          </svg>
          End-to-end encrypted
        </span>
        <span class="flex items-center gap-1.5">
          <svg class="w-4 h-4 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" />
          </svg>
          Free for early adopters
        </span>
      </div>
    </div>
  </div>
</section>
