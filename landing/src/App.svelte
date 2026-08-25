<script>
  import { onMount } from 'svelte';
  import gsap from 'gsap';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';
  import Lenis from 'lenis';

  import Navbar from './lib/components/Navbar.svelte';
  import Hero from './lib/components/Hero.svelte';
  import Features from './lib/components/Features.svelte';
  import HowItWorks from './lib/components/HowItWorks.svelte';
  import MemoryTimeline from './lib/components/MemoryTimeline.svelte';
  import ChatPreview from './lib/components/ChatPreview.svelte';
  import Testimonials from './lib/components/Testimonials.svelte';
  import FAQ from './lib/components/FAQ.svelte';
  import CTA from './lib/components/CTA.svelte';
  import Footer from './lib/components/Footer.svelte';
  import { initScrollState } from './lib/stores/scroll.svelte.js';

  let isScrolled = $state(false);

  gsap.registerPlugin(ScrollTrigger);

  // Initialize the scroll state (calls onMount internally)
  initScrollState();

  onMount(() => {
    // Initialize Lenis smooth scrolling
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 1,
      touchMultiplier: 2,
    });

    // Connect GSAP ScrollTrigger to Lenis
    lenis.on('scroll', ScrollTrigger.update);

    const tickerCallback = (time) => {
      lenis.raf(time * 1000);
    };
    gsap.ticker.add(tickerCallback);
    gsap.ticker.lagSmoothing(0);

    // Scroll state tracking
    lenis.on('scroll', (e) => {
      isScrolled = e.scroll > 80;
    });

    // Refresh ScrollTrigger after Lenis initializes
    setTimeout(() => {
      ScrollTrigger.refresh();
    }, 100);

    return () => {
      lenis.destroy();
      gsap.ticker.remove(tickerCallback);
    };
  });

  function scrollToTop() {
    const el = document.querySelector('#hero');
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  }
</script>

<!-- Noise overlay -->
<div class="noise-overlay" aria-hidden="true"></div>

<!-- Navigation -->
<Navbar scrolled={isScrolled} />

<!-- Main Content -->
<main>
  <Hero />
  <Features />
  <HowItWorks />
  <MemoryTimeline />
  <ChatPreview />
  <Testimonials />
  <FAQ />
  <CTA />
</main>

<!-- Footer -->
<Footer />

<!-- Back to top -->
<button
  onclick={scrollToTop}
  class="fixed bottom-8 right-8 z-40 w-12 h-12 rounded-2xl glass flex items-center justify-center text-slate-400 hover:text-white hover:border-iris-500/30 transition-all duration-300 shadow-xl shadow-black/20"
  class:opacity-0={!isScrolled}
  class:opacity-100={isScrolled}
  class:pointer-events-none={!isScrolled}
  class:pointer-events-auto={isScrolled}
  aria-label="Scroll to top"
>
  <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M18 15l-6-6-6 6" />
  </svg>
</button>
