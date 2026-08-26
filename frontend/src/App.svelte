<script>
  import { initAuth, getAuth } from './lib/stores.svelte.js';
  import { getRouter } from './lib/router.svelte.js';
  import Background from './lib/components/Background.svelte';
  import Navbar from './lib/components/Navbar.svelte';
  import Toast from './lib/components/Toast.svelte';

  import Home from './pages/Home.svelte';
  import Login from './pages/Login.svelte';
  import Register from './pages/Register.svelte';
  import VerifyOTP from './pages/VerifyOTP.svelte';
  import Chat from './pages/Chat.svelte';
  import Personality from './pages/Personality.svelte';
  import Diary from './pages/Diary.svelte';
  import DiaryEntry from './pages/DiaryEntry.svelte';
  import GoogleSuccess from './pages/GoogleSuccess.svelte';

  initAuth();

  const router = getRouter();
  const auth = getAuth();

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
    if (route === '/auth/google/success') return GoogleSuccess;
    return Home;
  });

  // Route guards: authed users skip auth pages; guests skip app pages
  $effect(() => {
    const route = router.currentRoute;
    const isAuthPage = ['/login', '/register', '/verify-otp', '/auth/google/success'].includes(route);
    if (auth.isAuthenticated && isAuthPage) {
      window.location.hash = '#/chat';
    }
    if (!auth.isAuthenticated && !isAuthPage && route !== '/' && route !== '') {
      window.location.hash = '#/login';
    }
  });
</script>

<Background />
<Navbar route={router.currentRoute} />

{#key router.currentRoute}
  <main class="relative z-10 min-h-[calc(100vh-4rem)]">
    <svelte:component this={CurrentPage} />
  </main>
{/key}

<Toast />
