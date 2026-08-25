<script>
  import { onMount } from 'svelte';
  import gsap from 'gsap';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';

  let sectionRef = $state(null);
  let memoryCards = $state([]);
  let currentMessageIndex = $state(0);

  const chatMessages = [
    { role: 'user', text: 'I\'ve been feeling really anxious about my presentation tomorrow.' },
    { role: 'ai', text: 'I hear you. Public speaking can be nerve-wracking. Remember last month when you were worried about that team meeting, and it went really well? This is the same — you\'ve got this. Want to practice together?', memory: 'Remembered your fear of public speaking — logged on March 15' },
    { role: 'user', text: 'You remember that? Yeah, you\'re right. It did go well. I just get so in my head about these things.' },
    { role: 'ai', text: 'It\'s natural to get in your head — it shows you care. I\'ve noticed you often underestimate yourself before big moments, but you always rise to the occasion. That\'s real strength.', memory: 'Identified pattern: self-doubt before achievements (5 instances)' },
    { role: 'user', text: 'Thanks, that actually helps a lot. I feel better already.' },
    { role: 'ai', text: 'I\'m glad. That\'s what I\'m here for. I\'ll check in on you tomorrow after your presentation to see how it went. 🤗', memory: 'Set reminder: Check in on presentation outcome' },
  ];

  let memories = [
    { title: 'Public Speaking Anxiety', detail: 'First mentioned feeling anxious about presenting on March 15. Tracked through 5 conversations.', icon: 'brain', color: 'from-iris-500/20 to-cyan-500/10' },
    { title: 'Self-Doubt Pattern', detail: 'Consistent pattern of self-doubt before achievements. Identified 5 instances over 3 months.', icon: 'trend', color: 'from-amber-500/20 to-rose-500/10' },
    { title: 'Growth Milestone', detail: 'Successfully delivered presentation and felt proud. AI noted emotional growth and resilience.', icon: 'sparkles', color: 'from-emerald-500/20 to-teal-500/10' },
  ];

  let isPlaying = $state(false);
  let intervalId = $state(null);
  let showMemoryPanel = $state(false);

  function setMemoryCardRef(el, i) {
    memoryCards[i] = el;
  }

  onMount(() => {
    ScrollTrigger.create({
      trigger: sectionRef,
      start: 'top center+=100',
      onEnter: () => {
        setTimeout(() => startAutoPlay(), 500);
      },
    });

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  });

  function startAutoPlay() {
    if (isPlaying) return;
    isPlaying = true;
    currentMessageIndex = 0;
    showMemoryPanel = false;

    intervalId = setInterval(() => {
      currentMessageIndex++;
      if (currentMessageIndex >= chatMessages.length) {
        clearInterval(intervalId);
        intervalId = null;
        isPlaying = false;
        setTimeout(() => {
          showMemoryPanel = true;
          animateMemoryCards();
        }, 800);
      }
    }, 1800);
  }

  function animateMemoryCards() {
    memoryCards.forEach((card, i) => {
      if (!card) return;
      gsap.fromTo(
        card,
        { y: 30, opacity: 0, scale: 0.95 },
        {
          y: 0, opacity: 1, scale: 1,
          duration: 0.6,
          delay: i * 0.2,
          ease: 'power3.out',
        }
      );
    });
  }

  function resetChat() {
    if (intervalId) clearInterval(intervalId);
    intervalId = null;
    isPlaying = false;
    currentMessageIndex = 0;
    showMemoryPanel = false;
  }
</script>

<section id="chat-preview" bind:this={sectionRef} class="relative section-padding overflow-hidden">
  <!-- Background subtle gradient -->
  <div class="absolute inset-0 bg-gradient-to-b from-midnight-900 via-iris-950/20 to-midnight-900 pointer-events-none"></div>

  <div class="section-container relative z-10">
    <!-- Section Header -->
    <div class="text-center mb-16">
      <span class="section-label">Live Preview</span>
      <h2 class="section-title mb-6">
        Conversations That Become
        <span class="gradient-text">Lasting Memories</span>
      </h2>
      <p class="section-subtitle mx-auto">
        Watch how a simple conversation evolves into something the AI remembers and builds upon.
      </p>
    </div>

    <!-- Main Content -->
    <div class="max-w-5xl mx-auto">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Chat Panel -->
        <div class="glass rounded-3xl p-6 md:p-8">
          <!-- Chat Header -->
          <div class="flex items-center justify-between mb-6 pb-4 border-b border-white/5">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-xl bg-gradient-primary flex items-center justify-center">
                <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2L2 7l10 5 10-5-10-5z" />
                  <path d="M2 17l10 5 10-5" />
                  <path d="M2 12l10 5 10-5" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-semibold">Mindful</p>
                <p class="text-xs text-slate-500">Online · Always listening</p>
              </div>
            </div>
            {#if !isPlaying && currentMessageIndex === 0}
              <button
                onclick={startAutoPlay}
                class="text-xs px-4 py-2 rounded-full bg-iris-500/20 text-iris-300 hover:bg-iris-500/30 transition-all"
              >
                ▶ Play Demo
              </button>
            {:else if currentMessageIndex >= chatMessages.length}
              <button
                onclick={resetChat}
                class="text-xs px-4 py-2 rounded-full bg-white/5 text-slate-400 hover:bg-white/10 transition-all"
              >
                ↻ Replay
              </button>
            {:else}
              <span class="text-xs text-emerald-400 flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                AI is typing...
              </span>
            {/if}
          </div>

          <!-- Messages -->
          <div class="space-y-4 min-h-[320px]">
            {#each chatMessages as msg, i}
              {#if i <= currentMessageIndex}
                <div
                  class="flex {msg.role === 'ai' ? 'justify-start' : 'justify-end'}"
                >
                  <div
                    class="max-w-[85%] animate-fade-in-up"
                    style="animation-delay: 0.1s"
                  >
                    <div
                      class="rounded-2xl px-4 py-3 text-sm leading-relaxed {msg.role === 'ai' ? 'glass rounded-bl-sm' : 'bg-gradient-primary/20 rounded-br-sm'}"
                    >
                      {msg.text}
                    </div>
                    {#if msg.memory && i === currentMessageIndex && currentMessageIndex === chatMessages.length - 1}
                      <div class="mt-2 text-xs text-amber-400/70 flex items-center gap-1.5 animate-fade-in">
                        <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
                        </svg>
                        {msg.memory}
                      </div>
                    {:else if msg.memory && i !== chatMessages.length - 1 && msg.role === 'ai' && i < currentMessageIndex}
                      <div class="mt-1.5 text-[10px] text-cyan-500/50 flex items-center gap-1">
                        <svg class="w-2.5 h-2.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                        </svg>
                        Memory stored
                      </div>
                    {/if}
                  </div>
                </div>
              {/if}
            {/each}

            {#if !isPlaying && currentMessageIndex === 0}
              <div class="flex items-center justify-center h-48 text-slate-600">
                <div class="text-center">
                  <svg class="w-10 h-10 mx-auto mb-3 opacity-30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2v10z" />
                  </svg>
                  <p class="text-sm">Click "Play Demo" to see Mindful in action</p>
                </div>
              </div>
            {/if}
          </div>
        </div>

        <!-- Memory Panel -->
        <div class="glass rounded-3xl p-6 md:p-8">
          <div class="flex items-center gap-2 mb-6 pb-4 border-b border-white/5">
            <svg class="w-5 h-5 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
            </svg>
            <h3 class="font-display font-semibold">AI Memory Bank</h3>
          </div>

          {#if !showMemoryPanel}
            <div class="flex items-center justify-center h-48 text-slate-600">
              <div class="text-center">
                <div class="w-12 h-12 rounded-full border-2 border-slate-700 border-t-iris-400 animate-spin mx-auto mb-3"></div>
                <p class="text-sm">Memories form as you chat...</p>
              </div>
            </div>
          {:else}
            <div class="space-y-4">
              {#each memories as memory, i}
                <div
                  use:setMemoryCardRef={i}
                  class="rounded-2xl p-4 bg-gradient-to-br {memory.color} border border-white/5 opacity-0"
                >
                  <div class="flex items-start gap-3">
                    <div class="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center flex-shrink-0 shrink-0">
                      {#if memory.icon === 'brain'}
                        <svg class="w-4 h-4 text-iris-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                          <path d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2z" />
                        </svg>
                      {:else if memory.icon === 'trend'}
                        <svg class="w-4 h-4 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                          <path d="M13 17V3m0 0l4 4m-4-4l-4 4M3 21l4-4 4 4 5-5 4 4" />
                        </svg>
                      {:else}
                        <svg class="w-4 h-4 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                          <path d="M12 3v2m0 14v2m-7-9H3m18 0h-2m-1.64-6.36L15.54 5.6M8.46 18.4l-2.82 2.82m0-14.84L8.46 5.6M15.54 18.4l2.82 2.82" />
                        </svg>
                      {/if}
                    </div>
                    <div>
                      <h4 class="text-sm font-semibold mb-1">{memory.title}</h4>
                      <p class="text-xs text-slate-400 leading-relaxed">{memory.detail}</p>
                    </div>
                  </div>
                </div>
              {/each}
            </div>
          {/if}
        </div>
      </div>
    </div>
  </div>
</section>
