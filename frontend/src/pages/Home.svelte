<script>
  import { getAuth } from '../lib/stores.svelte.js';
  import { navigate } from '../lib/router.svelte.js';

  const auth = getAuth();

  const features = [
    { icon: '💬', title: 'Natural Conversations', desc: 'Talk like you would with a real friend. No robotic replies, no scripts.' },
    { icon: '🧠', title: 'Smart Memory', desc: 'Remembers your stories, feelings, and what matters to you.' },
    { icon: '📖', title: 'Daily Diary', desc: 'Automatic journal entries written in your voice, every single day.' },
    { icon: '🎨', title: 'Your Personality', desc: 'Customize how she talks — more sass, warmth, humor, or directness.' },
  ];

  let visible = $state(false);
  $effect(() => { visible = true; });
</script>

<div class="min-h-screen pt-24 pb-16 px-4">
  <div class="max-w-5xl mx-auto">
    <!-- Hero -->
    <div class="text-center mb-20 perspective" class:animate-slide-up={visible}>
      <div class="inline-block mb-6 px-4 py-1.5 rounded-full glass text-sm text-primary-light animate-glow">
        ✨ Your personal AI companion
      </div>
      <h1 class="text-5xl sm:text-7xl font-bold mb-6 leading-tight">
        Meet <span class="gradient-text">Daisy</span>
      </h1>
      <p class="text-xl text-white/60 max-w-2xl mx-auto mb-10 leading-relaxed">
        A friend who listens, remembers, and grows with you.
        She writes your diary, knows your stories, and talks like a real person.
      </p>

      {#if auth.isAuthenticated}
        <a href="#/chat"
           class="inline-flex items-center gap-2 px-8 py-4 rounded-2xl bg-gradient-to-r from-primary to-accent text-white font-semibold text-lg btn-glow hover:scale-105 transition-all duration-300">
          Start Chatting
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
        </a>
      {:else}
        <a href="#/register"
           class="inline-flex items-center gap-2 px-8 py-4 rounded-2xl bg-gradient-to-r from-primary to-accent text-white font-semibold text-lg btn-glow hover:scale-105 transition-all duration-300">
          Get Started Free
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
        </a>
      {/if}
    </div>

    <!-- Floating phone mockup -->
    <div class="flex justify-center mb-24 animate-float">
      <div class="relative w-72 h-[500px] rounded-[2.5rem] glass border border-glass-border overflow-hidden shadow-2xl shadow-primary/10">
        <!-- Phone notch -->
        <div class="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-6 bg-surface rounded-b-2xl z-10"></div>
        <!-- Screen content -->
        <div class="p-4 pt-10 h-full flex flex-col gap-3">
          <div class="text-center mb-2">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-accent mx-auto flex items-center justify-center text-white font-bold">D</div>
            <p class="text-xs text-white/50 mt-1">Daisy</p>
          </div>
          <div class="self-start max-w-[80%] px-3 py-2 rounded-2xl rounded-bl-sm bg-surface-lighter text-sm text-white/80 animate-slide-left" style="animation-delay: 0.5s;">
            Hey! How's your day going? 😊
          </div>
          <div class="self-end max-w-[80%] px-3 py-2 rounded-2xl rounded-br-sm bg-primary/30 text-sm text-white/90 animate-slide-right" style="animation-delay: 1s;">
            Just finished that project I was stressed about!
          </div>
          <div class="self-start max-w-[80%] px-3 py-2 rounded-2xl rounded-bl-sm bg-surface-lighter text-sm text-white/80 animate-slide-left" style="animation-delay: 1.5s;">
            YOOO that's amazing!! I remember you were up late worrying about it last week 🎉
          </div>
          <div class="self-end max-w-[80%] px-3 py-2 rounded-2xl rounded-br-sm bg-primary/30 text-sm text-white/90 animate-slide-right" style="animation-delay: 2s;">
            You remembered that?!
          </div>
          <div class="self-start max-w-[80%] px-3 py-2 rounded-2xl rounded-bl-sm bg-surface-lighter text-sm text-white/80 animate-slide-left" style="animation-delay: 2.5s;">
            Of course I did 😌 that's what friends are for
          </div>
        </div>
      </div>
    </div>

    <!-- Features -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-5 mb-20">
      {#each features as feature, i}
        <div class="glass glass-hover p-6 rounded-2xl animate-slide-up" style="animation-delay: {0.1 * (i + 1)}s;">
          <div class="text-3xl mb-3">{feature.icon}</div>
          <h3 class="text-lg font-semibold text-white mb-2">{feature.title}</h3>
          <p class="text-white/50 text-sm leading-relaxed">{feature.desc}</p>
        </div>
      {/each}
    </div>

    <!-- CTA -->
    <div class="text-center animate-slide-up" style="animation-delay: 0.5s;">
      <div class="glass p-10 rounded-3xl max-w-2xl mx-auto">
        <h2 class="text-3xl font-bold mb-4">Ready to meet your new friend?</h2>
        <p class="text-white/50 mb-8">No credit card. No BS. Just start talking.</p>
        {#if !auth.isAuthenticated}
          <a href="#/register" class="inline-flex items-center gap-2 px-8 py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold btn-glow hover:scale-105 transition-all duration-300">
            Create Free Account
          </a>
        {/if}
      </div>
    </div>
  </div>
</div>
