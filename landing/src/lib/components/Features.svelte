<script>
  import { onMount } from 'svelte';
  import gsap from 'gsap';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';

  let sectionRef = $state(null);
  let cards = $state([]);

  const features = [
    {
      icon: 'brain',
      title: 'Truly Understands You',
      description: 'Beyond keywords — our AI grasps context, emotion, and nuance across conversations, building a genuine understanding of who you are.',
      gradient: 'from-iris-500/20 to-cyan-500/10',
      border: 'border-iris-500/20',
    },
    {
      icon: 'memory',
      title: 'Long-Term Memory',
      description: 'Every chat becomes a lasting memory. The AI recalls past conversations, remembers important details, and connects the dots over time.',
      gradient: 'from-cyan-500/20 to-emerald-500/10',
      border: 'border-cyan-500/20',
    },
    {
      icon: 'shield',
      title: 'Private by Design',
      description: 'Your thoughts are yours alone. End-to-end encrypted, anonymized by default, and never used for training. True privacy, no compromises.',
      gradient: 'from-amber-500/20 to-rose-500/10',
      border: 'border-amber-500/20',
    },
    {
      icon: 'sparkles',
      title: 'Grows With You',
      description: 'The more you share, the more insightful it becomes. Your AI companion evolves, offering deeper reflections and better support over time.',
      gradient: 'from-purple-500/20 to-pink-500/10',
      border: 'border-purple-500/20',
    },
    {
      icon: 'chat',
      title: 'Natural Conversations',
      description: 'No rigid formats or templates. Just talk naturally, like you would with a trusted friend who always listens without judgment.',
      gradient: 'from-sky-500/20 to-indigo-500/10',
      border: 'border-sky-500/20',
    },
    {
      icon: 'trend',
      title: 'Insightful Patterns',
      description: 'Discover hidden patterns in your thoughts and emotions. Get gentle insights about your wellbeing, mood trends, and personal growth.',
      gradient: 'from-emerald-500/20 to-teal-500/10',
      border: 'border-emerald-500/20',
    },
  ];

  const iconPaths = {
    brain: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2z',
    memory: 'M22 12h-4l-3 9L9 3l-3 9H2',
    shield: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z',
    sparkles: 'M12 3v2m0 14v2m-7-9H3m18 0h-2m-1.64-6.36L15.54 5.6M8.46 18.4l-2.82 2.82m0-14.84L8.46 5.6M15.54 18.4l2.82 2.82M12 7a5 5 0 100 10 5 5 0 000-10z',
    chat: 'M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2v10z',
    trend: 'M13 17V3m0 0l4 4m-4-4l-4 4M3 21l4-4 4 4 5-5 4 4',
  };

  function setCardRef(el, i) {
    cards[i] = el;
  }

  onMount(() => {
    cards.forEach((card, i) => {
      if (!card) return;
      gsap.fromTo(
        card,
        { y: 60, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.8,
          delay: i * 0.15,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: card,
            start: 'top bottom-=80',
            toggleActions: 'play none none reverse',
          },
        }
      );
    });
  });
</script>

<section id="features" bind:this={sectionRef} class="relative section-padding">
  <div class="section-container">
    <!-- Section Header -->
    <div class="text-center mb-16 md:mb-20">
      <span class="section-label">Features</span>
      <h2 class="section-title mb-6">
        Everything You Need for
        <span class="gradient-text-duo">Deeper Self-Discovery</span>
      </h2>
      <p class="section-subtitle mx-auto">
        Mindful combines cutting-edge AI with thoughtful design to create a diary experience 
        that feels less like logging and more like connecting.
      </p>
    </div>

    <!-- Features Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 md:gap-6">
      {#each features as feature, i}
        <div
          use:setCardRef={i}
          class="group relative p-8 rounded-2xl glass glass-hover cursor-default transition-all duration-500"
        >
          <!-- Gradient overlay -->
          <div class="absolute inset-0 rounded-2xl bg-gradient-to-br {feature.gradient} opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

          <div class="relative z-10">
            <!-- Icon -->
            <div class="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center mb-5 group-hover:scale-110 transition-transform duration-300">
              <svg class="w-6 h-6 text-iris-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d={iconPaths[feature.icon]} />
              </svg>
            </div>

            <!-- Content -->
            <h3 class="font-display text-xl font-semibold mb-3 group-hover:text-white transition-colors">
              {feature.title}
            </h3>
            <p class="text-slate-400 leading-relaxed text-sm group-hover:text-slate-300 transition-colors">
              {feature.description}
            </p>
          </div>

          <!-- Corner glow -->
          <div class="absolute -bottom-px -right-px w-32 h-32 rounded-br-2xl bg-gradient-to-tl from-iris-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        </div>
      {/each}
    </div>
  </div>
</section>
