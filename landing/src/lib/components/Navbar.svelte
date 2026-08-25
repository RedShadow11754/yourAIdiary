<script>
  import { onMount } from 'svelte';
  import gsap from 'gsap';

  let { scrolled = false } = $props();

  let isMobileOpen = $state(false);
  let navRef = $state(null);

  const navLinks = [
    { label: 'Features', href: '#features' },
    { label: 'How It Works', href: '#how-it-works' },
    { label: 'Timeline', href: '#timeline' },
    { label: 'Testimonials', href: '#testimonials' },
    { label: 'FAQ', href: '#faq' },
  ];

  function scrollTo(e, href) {
    e.preventDefault();
    isMobileOpen = false;
    const el = document.querySelector(href);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function toggleMobile() {
    isMobileOpen = !isMobileOpen;
  }

  onMount(() => {
    if (navRef) {
      gsap.fromTo(
        navRef,
        { y: -20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out' }
      );
    }
  });
</script>

<nav
  bind:this={navRef}
  class="fixed top-0 left-0 right-0 z-50 transition-all duration-500"
  class:scrolled
>
  <div
    class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 transition-all duration-500"
    class:py-4={!scrolled}
    class:py-3={scrolled}
  >
    <div
      class="flex items-center justify-between rounded-2xl transition-all duration-500 px-6"
      class:glass={scrolled}
      class:bg-transparent={!scrolled}
    >
      <!-- Logo -->
      <a href="/" class="flex items-center gap-3 group" onclick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }}>
        <div class="w-9 h-9 rounded-xl bg-gradient-primary flex items-center justify-center shadow-lg shadow-iris-500/20 group-hover:shadow-iris-500/40 transition-all duration-300 group-hover:scale-105">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2L2 7l10 5 10-5-10-5z" />
            <path d="M2 17l10 5 10-5" />
            <path d="M2 12l10 5 10-5" />
          </svg>
        </div>
        <span class="font-display font-semibold text-lg tracking-tight">Mindful</span>
      </a>

      <!-- Desktop Nav -->
      <div class="hidden md:flex items-center gap-1">
        {#each navLinks as link}
          <a
            href={link.href}
            onclick={(e) => scrollTo(e, link.href)}
            class="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white rounded-xl transition-all duration-300 hover:bg-white/5"
          >
            {link.label}
          </a>
        {/each}
        <div class="w-px h-6 bg-white/10 mx-3"></div>
        <a
          href="#cta"
          onclick={(e) => scrollTo(e, '#cta')}
          class="btn-primary text-sm !px-5 !py-2.5"
        >
          Get Started
        </a>
      </div>

      <!-- Mobile Toggle -->
      <button
        class="md:hidden relative w-10 h-10 flex items-center justify-center rounded-xl hover:bg-white/5 transition-colors"
        onclick={toggleMobile}
        aria-label="Toggle menu"
      >
        <div class="w-5 h-4 relative flex flex-col justify-between">
          <span
            class="block w-full h-0.5 bg-white rounded-full transition-all duration-300 origin-center"
            class:rotate-45={isMobileOpen}
            class:translate-y-[7px]={isMobileOpen}
          ></span>
          <span
            class="block w-full h-0.5 bg-white rounded-full transition-all duration-300"
            class:opacity-0={isMobileOpen}
          ></span>
          <span
            class="block w-full h-0.5 bg-white rounded-full transition-all duration-300 origin-center"
            class:-rotate-45={isMobileOpen}
            class:-translate-y-[7px]={isMobileOpen}
          ></span>
        </div>
      </button>
    </div>
  </div>

  <!-- Mobile Menu -->
  {#if isMobileOpen}
    <div
      class="md:hidden absolute top-full left-4 right-4 mt-2 glass rounded-2xl p-4 shadow-2xl shadow-black/50 animate-fade-in-up"
    >
      <div class="flex flex-col gap-2">
        {#each navLinks as link}
          <a
            href={link.href}
            onclick={(e) => { scrollTo(e, link.href); }}
            class="px-4 py-3 text-sm font-medium text-slate-300 hover:text-white rounded-xl transition-all duration-300 hover:bg-white/5"
          >
            {link.label}
          </a>
        {/each}
        <hr class="border-white/5 my-2" />
        <a
          href="#cta"
          onclick={(e) => { scrollTo(e, '#cta'); isMobileOpen = false; }}
          class="btn-primary text-sm !px-5 !py-3 text-center"
        >
          Get Started Free
        </a>
      </div>
    </div>
  {/if}
</nav>

<style>
  nav.scrolled .glass {
    background: rgba(10, 10, 26, 0.85);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
  }
</style>
