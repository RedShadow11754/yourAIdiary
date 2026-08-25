<script>
  import { onMount } from 'svelte';
  import gsap from 'gsap';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';

  let sectionRef = $state(null);
  let milestones = $state([]);
  let progressBar = $state(null);

  const memoryData = [
    { day: 'Day 1', title: 'First Entry', desc: 'You write your first thoughts. The AI begins learning your voice.', icon: 'circle', complete: true },
    { day: 'Week 1', title: 'Building Context', desc: 'The AI identifies your communication style and emotional patterns.', icon: 'circle', complete: true },
    { day: 'Month 1', title: 'Memory Formation', desc: 'Your first connections form. The AI links related entries and surfaces meaningful patterns.', icon: 'star', complete: true },
    { day: 'Month 3', title: 'Deep Understanding', desc: 'The AI recognizes recurring themes, tracks personal growth, and offers insightful reflections.', icon: 'star', complete: true },
    { day: 'Month 6', title: 'True Companionship', desc: 'Mindful becomes a trusted companion. It anticipates your needs and celebrates your growth.', icon: 'sparkles', complete: true },
    { day: 'Year 1+', title: 'Your Living History', desc: 'A rich tapestry of your inner world. The AI has watched you grow, change, and flourish.', icon: 'sparkles', complete: false },
  ];

  function setMilestoneRef(el, i) {
    milestones[i] = el;
  }

  onMount(() => {
    if (progressBar) {
      gsap.fromTo(
        progressBar,
        { scaleY: 0, transformOrigin: 'top center' },
        {
          scaleY: 1,
          duration: 2,
          ease: 'none',
          scrollTrigger: {
            trigger: sectionRef,
            start: 'top center',
            end: 'bottom center',
            scrub: 1.5,
          },
        }
      );
    }

    milestones.forEach((ms, i) => {
      if (!ms) return;
      gsap.fromTo(
        ms,
        { x: i % 2 === 0 ? -60 : 60, opacity: 0, scale: 0.95 },
        {
          x: 0, opacity: 1, scale: 1,
          duration: 0.8,
          delay: i * 0.15,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: ms,
            start: 'top bottom-=80',
            toggleActions: 'play none none reverse',
          },
        }
      );
    });
  });
</script>

<section id="timeline" bind:this={sectionRef} class="relative section-padding overflow-hidden">
  <!-- Background elements -->
  <div class="absolute right-0 top-1/3 w-96 h-96 bg-iris-500/5 rounded-full blur-[100px] pointer-events-none"></div>
  <div class="absolute left-0 bottom-1/3 w-96 h-96 bg-cyan-500/5 rounded-full blur-[100px] pointer-events-none"></div>

  <div class="section-container relative z-10">
    <!-- Section Header -->
    <div class="text-center mb-16 md:mb-20">
      <span class="section-label">The Memory Timeline</span>
      <h2 class="section-title mb-6">
        Watch Your Story
        <span class="gradient-text">Grow Over Time</span>
      </h2>
      <p class="section-subtitle mx-auto">
        Every entry adds a thread to the tapestry of your life. Here's how your relationship with Mindful deepens.
      </p>
    </div>

    <!-- Timeline -->
    <div class="relative max-w-5xl mx-auto">
      <!-- Center line -->
      <div class="absolute left-8 md:left-1/2 top-0 bottom-0 w-px bg-white/5 md:-translate-x-px">
        <div
          bind:this={progressBar}
          class="w-full h-full bg-gradient-to-b from-iris-500 via-cyan-500 to-amber-500 origin-top"
        ></div>
      </div>

      <!-- Milestones -->
      <div class="space-y-12 md:space-y-20">
        {#each memoryData as milestone, i}
          <div
            use:setMilestoneRef={i}
            class="relative flex flex-col md:flex-row items-start gap-6 md:gap-12 opacity-0 {i % 2 === 1 ? 'md:flex-row-reverse' : ''}"
          >
            <!-- Icon -->
            <div
              class="relative z-10 flex-shrink-0 w-16 h-16 rounded-2xl glass flex items-center justify-center mx-auto md:mx-0 md:absolute md:left-1/2 md:-translate-x-1/2 transition-all duration-500 {milestone.complete ? 'border-iris-500/30' : 'border-white/5'}"
            >
              {#if milestone.icon === 'star'}
                <svg class="w-6 h-6 text-amber-400" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                </svg>
              {:else if milestone.icon === 'sparkles'}
                <svg class="w-6 h-6 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M12 3v2m0 14v2m-7-9H3m18 0h-2m-1.64-6.36L15.54 5.6M8.46 18.4l-2.82 2.82m0-14.84L8.46 5.6M15.54 18.4l2.82 2.82" />
                </svg>
              {:else}
                <svg class="w-5 h-5 text-iris-400" viewBox="0 0 24 24" fill="currentColor">
                  <circle cx="12" cy="12" r="10" />
                </svg>
              {/if}
            </div>

            <!-- Content Card -->
            <div
              class="flex-1 glass rounded-2xl p-6 md:p-8 transition-all duration-500 hover:border-iris-500/20 {i % 2 === 0 ? 'md:mr-20' : 'md:ml-20'}"
            >
              <span class="text-xs font-semibold uppercase tracking-wider text-iris-400 mb-2 block">{milestone.day}</span>
              <h3 class="font-display text-xl font-semibold mb-3">{milestone.title}</h3>
              <p class="text-slate-400 leading-relaxed text-sm">{milestone.desc}</p>

              <!-- Progress indicator -->
              <div class="mt-4 flex items-center gap-2">
                <div
                  class="w-1.5 h-1.5 rounded-full {milestone.complete ? 'bg-emerald-400' : 'bg-slate-600'}"
                ></div>
                <span class="text-xs text-slate-500">
                  {milestone.complete ? 'Achieved' : 'Coming soon'}
                </span>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
</section>
