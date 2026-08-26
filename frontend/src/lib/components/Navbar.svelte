<script>
  import { getAuth, logout } from '../stores.svelte.js';
  import { navigate } from '../router.svelte.js';
  import Logo from './Logo.svelte';

  let { route = '/' } = $props();
  const auth = getAuth();

  let menuOpen = $state(false);

  const links = [
    { href: '/chat', label: 'Chat' },
    { href: '/diary', label: 'Diary' },
    { href: '/personality', label: 'Personality' },
  ];

  function go(path) {
    menuOpen = false;
    if (path === '/logout') {
      logout();
      return;
    }
    navigate(path);
  }
</script>

<header class="fixed top-0 inset-x-0 z-50">
  <div class="glass-strong border-x-0 border-t-0 rounded-none">
    <nav class="mx-auto max-w-6xl flex items-center justify-between px-5 h-16">
      <button class="flex items-center gap-2.5 cursor-pointer" onclick={() => go(auth.isAuthenticated ? '/chat' : '/')}>
        <Logo size={32} />
        <span class="font-display font-bold text-lg tracking-tight">Daisy</span>
      </button>

      <!-- Desktop -->
      <div class="hidden md:flex items-center gap-1">
        {#if auth.isAuthenticated}
          {#each links as l}
            <button
              onclick={() => go(l.href)}
              class="px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 cursor-pointer
                {route.startsWith(l.href) ? 'text-white bg-white/10 shadow-[inset_0_0_0_1px_rgba(196,181,253,0.25)]' : 'text-[var(--color-ink-dim)] hover:text-white hover:bg-white/5'}"
            >
              {l.label}
            </button>
          {:else}
            <span></span>
          {/each}
          <div class="mx-3 h-6 w-px bg-white/10"></div>
          <div class="flex items-center gap-2 pr-1">
            <span
              class="w-8 h-8 rounded-full grid place-items-center text-sm font-bold"
              style="background:linear-gradient(135deg,#7c3aed,#d946ef);"
            >
              {(auth.user?.email || 'D')[0].toUpperCase()}
            </span>
          </div>
          <button class="btn-ghost px-4 py-2 text-sm" onclick={() => go('/logout')}>Log out</button>
        {:else}
          <a href="#/login" class="btn-ghost px-5 py-2 text-sm">Log in</a>
          <a href="#/register" class="btn-primary px-5 py-2 text-sm ml-2">Meet Daisy</a>
        {/if}
      </div>

      <!-- Mobile toggle -->
      <button
        class="md:hidden w-10 h-10 grid place-items-center rounded-full glass cursor-pointer"
        onclick={() => (menuOpen = !menuOpen)}
        aria-label="Menu"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          {#if menuOpen}
            <path d="M18 6L6 18M6 6l12 12" />
          {:else}
            <path d="M3 6h18M3 12h18M3 18h12" />
          {/if}
        </svg>
      </button>
    </nav>

    <!-- Mobile menu -->
    {#if menuOpen}
      <div class="md:hidden px-5 pb-5 flex flex-col gap-2 animate-fade">
        {#if auth.isAuthenticated}
          {#each links as l}
            <button
              onclick={() => go(l.href)}
              class="text-left px-4 py-3 rounded-xl glass text-sm font-medium cursor-pointer
                {route.startsWith(l.href) ? 'text-white' : 'text-[var(--color-ink-dim)]'}"
            >
              {l.label}
            </button>
          {/each}
          <button class="btn-ghost py-3 text-sm mt-1" onclick={() => go('/logout')}>Log out</button>
        {:else}
          <a href="#/login" class="btn-ghost py-3 text-sm">Log in</a>
          <a href="#/register" class="btn-primary py-3 text-sm">Meet Daisy</a>
        {/if}
      </div>
    {/if}
  </div>
</header>

<!-- Spacer so content never hides under fixed nav -->
<div class="h-16"></div>
