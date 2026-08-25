<script>
  import { getAuth, logout } from './stores.svelte.js';
  import { navigate, getRouter } from './router.svelte.js';

  const auth = getAuth();
  const router = getRouter();

  function handleLogout() {
    logout();
    navigate('/login');
  }

  let mobileOpen = $state(false);
</script>

<nav class="fixed top-0 left-0 right-0 z-50 glass border-b border-glass-border/30">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16">
      <!-- Logo -->
      <a href="#/" class="flex items-center gap-2 group">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white font-bold text-lg group-hover:scale-110 transition-transform duration-300">
          D
        </div>
        <span class="text-xl font-bold gradient-text hidden sm:block">Daisy</span>
      </a>

      <!-- Desktop nav -->
      <div class="hidden md:flex items-center gap-1">
        {#if auth.isAuthenticated}
          <a href="#/chat" class="nav-link {router.currentRoute === '/chat' ? 'active' : ''}">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
            Chat
          </a>
          <a href="#/diary" class="nav-link {router.currentRoute === '/diary' ? 'active' : ''}">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
            Diary
          </a>
          <a href="#/personality" class="nav-link {router.currentRoute === '/personality' ? 'active' : ''}">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            Personality
          </a>
          <div class="ml-3 pl-3 border-l border-glass-border">
            <span class="text-sm text-primary-light mr-3">{auth.user?.email}</span>
            <button onclick={handleLogout} class="text-sm text-white/60 hover:text-accent transition-colors">
              Logout
            </button>
          </div>
        {:else}
          <a href="#/login" class="nav-link {router.currentRoute === '/login' ? 'active' : ''}">Login</a>
          <a href="#/register" class="ml-2 px-4 py-2 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-medium hover:shadow-lg hover:shadow-primary/25 transition-all duration-300 hover:scale-105">
            Get Started
          </a>
        {/if}
      </div>

      <!-- Mobile menu button -->
      <button onclick={() => mobileOpen = !mobileOpen} class="md:hidden text-white/70 hover:text-white p-2">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          {#if mobileOpen}
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          {:else}
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          {/if}
        </svg>
      </button>
    </div>
  </div>

  <!-- Mobile menu -->
  {#if mobileOpen}
    <div class="md:hidden glass border-t border-glass-border/30 animate-slide-up">
      <div class="px-4 py-3 space-y-2">
        {#if auth.isAuthenticated}
          <a href="#/chat" onclick={() => mobileOpen = false} class="block px-4 py-2 rounded-lg hover:bg-primary/10 transition-colors">Chat</a>
          <a href="#/diary" onclick={() => mobileOpen = false} class="block px-4 py-2 rounded-lg hover:bg-primary/10 transition-colors">Diary</a>
          <a href="#/personality" onclick={() => mobileOpen = false} class="block px-4 py-2 rounded-lg hover:bg-primary/10 transition-colors">Personality</a>
          <button onclick={() => { mobileOpen = false; handleLogout(); }} class="block w-full text-left px-4 py-2 rounded-lg hover:bg-red-500/10 text-red-400 transition-colors">Logout</button>
        {:else}
          <a href="#/login" onclick={() => mobileOpen = false} class="block px-4 py-2 rounded-lg hover:bg-primary/10 transition-colors">Login</a>
          <a href="#/register" onclick={() => mobileOpen = false} class="block px-4 py-2 rounded-lg bg-primary/20 text-primary-light transition-colors text-center">Get Started</a>
        {/if}
      </div>
    </div>
  {/if}
</nav>

<style>
  .nav-link {
    display: flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0.5rem 0.75rem;
    border-radius: 0.75rem;
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.6);
    transition: all 0.2s;
  }
  .nav-link:hover {
    color: white;
    background: rgba(124, 58, 237, 0.1);
  }
  .nav-link.active {
    color: #a78bfa;
    background: rgba(124, 58, 237, 0.15);
  }
</style>
