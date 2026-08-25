<script>
  import { onMount } from 'svelte';
  import gsap from 'gsap';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';

  let sectionRef = $state(null);
  let steps = $state([]);
  let lineRef = $state(null);

  const timeline = [
    {
      step: '01',
      title: 'Start Writing Naturally',
      description: 'Open your diary and start typing — or speaking. No templates, no pressure. Your AI companion listens and learns from every word.',
      icon: 'edit',
    },
    {
      step: '02',
      title: 'AI Understands the Context',
      description: 'It doesn\'t just read words — it grasps emotions, picks up on recurring themes, and connects new entries to past conversations.',
      icon: 'sparkles',
    },
    {
      step: '03',
      title: 'Memories Are Formed',
      description: 'Meaningful moments are distilled into memories. The AI remembers your hopes, fears, joys — building a rich understanding of your inner world.',
      icon: 'heart',
    },
    {
      step: '04',
      title: 'Growth Over Time',
      description: 'Each session deepens the connection. You\'ll receive insights, reflections, and gentle prompts that show just how far you\'ve come.',
      icon: 'trend',
    },
  ];

  function setStepRef(el, i) {
    steps[i] = el;
  }

  onMount(() => {
    // Animate connection line
    if (lineRef) {
      gsap.fromTo(
        lineRef,
        { scaleY: 0 },
        {
          scaleY: 1,
          duration: 1.5,
          ease: 'power2.inOut',
          scrollTrigger: {
            trigger: sectionRef,
            start: 'top center',
            end: 'bottom center',
            scrub: 1,
          },
        }
      );
    }

    // Animate steps
    steps.forEach((step, i) => {
      if (!step) return;
      gsap.fromTo(
        step,
        { x: i % 2 === 0 ? -50 : 50, opacity: 0 },
        {
          x: 0,
          opacity: 1,
          duration: 0.8,
          delay: i * 0.2,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: step,
            start: 'top bottom-=100',
            toggleActions: 'play none none reverse',
          },
        }
      );
    });
  });
</script>

<section id="how-it-works" bind:this={sectionRef} class="relative section-padding bg-midnight-950/50">
  <div class="section-container">
    <!-- Section Header -->
    <div class="text-center mb-16 md:mb-20">
      <span class="section-label">How It Works</span>
      <h2 class="section-title mb-6">
        Your Journey with
        <span class="gradient-text-duo">Mindful</span>
      </h2>
      <p class="section-subtitle mx-auto">
        From your first entry to deep self-discovery — here's how Mindful becomes your companion.
      </p>
    </div>

    <!-- Timeline -->
    <div class="relative max-w-3xl mx-auto">
      <!-- Connection Line -->
      <div class="absolute left-8 md:left-1/2 top-0 bottom-0 w-px overflow-hidden md:-translate-x-px">
        <div
          bind:this={lineRef}
          class="w-full h-full bg-gradient-to-b from-iris-500 via-cyan-500 to-amber-500 origin-top"
        ></div>
      </div>

      <!-- Steps -->
      <div class="space-y-16 md:space-y-24">
        {#each timeline as item, i}
          <div
            use:setStepRef={i}
            class="relative flex flex-col md:flex-row items-start gap-6 md:gap-8"
            class:md:flex-row-reverse={i % 2 === 1}
          >
            <!-- Step Number -->
            <div class="relative z-10 flex-shrink-0 w-16 h-16 rounded-2xl glass flex items-center justify-center mx-auto md:mx-0 md:absolute md:left-1/2 md:-translate-x-1/2">
              <span class="font-display text-lg font-bold gradient-text-duo">{item.step}</span>
            </div>

            <!-- Content Card -->
            <div
              class="flex-1 glass rounded-2xl p-6 md:p-8 hover:border-iris-500/20 transition-all duration-500"
              class:md:mr-20={i % 2 === 0}
              class:md:ml-20={i % 2 === 1}
            >
              <div class="flex items-start gap-4">
                <div class="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center flex-shrink-0 shrink-0">
                  {#if item.icon === 'edit'}
                    <svg class="w-5 h-5 text-iris-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
                      <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
                    </svg>
                  {:else if item.icon === 'sparkles'}
                    <svg class="w-5 h-5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M12 3v2m0 14v2m-7-9H3m18 0h-2m-1.64-6.36L15.54 5.6M8.46 18.4l-2.82 2.82m0-14.84L8.46 5.6M15.54 18.4l2.82 2.82" />
                    </svg>
                  {:else if item.icon === 'heart'}
                    <svg class="w-5 h-5 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" />
                    </svg>
                  {:else}
                    <svg class="w-5 h-5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M13 17V3m0 0l4 4m-4-4l-4 4M3 21l4-4 4 4 5-5 4 4" />
                    </svg>
                  {/if}
                </div>
                <div>
                  <h3 class="font-display text-xl font-semibold mb-2">{item.title}</h3>
                  <p class="text-slate-400 leading-relaxed text-sm">{item.description}</p>
                </div>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
</section>
