<script>
  import { initAuth, getAuth } from './lib/stores.svelte.js';
  import { getRouter } from './lib/router.svelte.js';
  import Particles from './lib/Particles.svelte';
  import Navbar from './lib/Navbar.svelte';

  import Home from './pages/Home.svelte';
  import Login from './pages/Login.svelte';
  import Register from './pages/Register.svelte';
  import VerifyOTP from './pages/VerifyOTP.svelte';
  import Chat from './pages/Chat.svelte';
  import Personality from './pages/Personality.svelte';
  import Diary from './pages/Diary.svelte';
  import DiaryEntry from './pages/DiaryEntry.svelte';

  initAuth();

  const router = getRouter();

  let CurrentPage = $derived.by(() => {
    const route = router.currentRoute;
    if (route === '/' || route === '') return Home;
    if (route === '/login') return Login;
    if (route === '/register') return Register;
    if (route === '/verify-otp') return VerifyOTP;
    if (route === '/chat') return Chat;
    if (route === '/personality') return Personality;
    if (route === '/diary') return Diary;
    if (route.startsWith('/diary/')) return DiaryEntry;
    return Home;
  });

  // Key for forcing remount on route change
  let routeKey = $derived(router.currentRoute);
</script>

<Particles />
<Navbar />

{#key routeKey}
  <div class="relative z-10">
    <svelte:component this={CurrentPage} />
  </div>
{/key}
