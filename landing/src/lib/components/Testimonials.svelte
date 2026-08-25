<script>
  import { onMount } from 'svelte';
  import gsap from 'gsap';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';

  let sectionRef = $state(null);
  let trackRef = $state(null);
  let cards = $state([]);
  let activeIndex = $state(0);

  const testimonials = [
    {
      name: 'Sarah Chen',
      role: 'Designer',
      avatar: 'SC',
      text: 'Mindful is the first diary that actually feels like a conversation, not a chore. The way it remembers tiny details from weeks ago still surprises me. It\'s like having a friend who truly gets you.',
      rating: 5,
      color: 'from-iris-500/10',
    },
    {
      name: 'Marcus Johnson',
      role: 'Software Engineer',
      avatar: 'MJ',
      text: 'I was skeptical about AI journaling, but Mindful won me over. The pattern recognition is uncanny — it noticed my productivity cycles before I did. This is genuinely useful technology.',
      rating: 5,
      color: 'from-cyan-500/10',
    },
    {
      name: 'Elena Rodríguez',
      role: 'Therapist',
      avatar: 'ER',
      text: 'I\'ve recommended Mindful to several clients. The way it creates a safe space for self-reflection while building a continuous narrative of personal growth is remarkable. It complements therapeutic work beautifully.',
      rating: 5,
      color: 'from-amber-500/10',
    },
    {
      name: 'James Park',
      role: 'Writer',
      avatar: 'JP',
      text: 'As a writer, I need a space where thoughts can breathe. Mindful gives me that and more. The AI doesn\'t interrupt or judge — it just listens and gently helps me find clarity. Beautifully designed.',
      rating: 5,
      color: 'from-emerald-500/10',
    },
  ];

  let isDragging = $state(false);
  let startX = $state(0);
  let scrollLeft = $state(0);

  function setCardRef(el, i) {
    cards[i] = el;
  }

  onMount(() => {
    ScrollTrigger.create({
      trigger: sectionRef,
      start: 'top center+=100',
      onEnter: () => {
        cards.forEach((card, i) => {
          if (!card) return;
          gsap.fromTo(
            card,
            { y: 40, opacity: 0, scale: 0.95 },
            {
              y: 0, opacity: 1, scale: 1,
              duration: 0.7,
              delay: i * 0.15,
              ease: 'power3.out',
            }
          );
        });
      },
    });
  });

  function goTo(index) {
    activeIndex = index;
    if (trackRef) {
      const cardWidth = trackRef.querySelector('.testimonial-card')?.offsetWidth || 400;
      const gap = 24;
      trackRef.scrollTo({
        left: index * (cardWidth + gap),
        behavior: 'smooth',
      });
    }
  }

  function handleDragStart(e) {
    isDragging = true;
    startX = e.pageX - (trackRef?.offsetLeft || 0);
    scrollLeft = trackRef?.scrollLeft || 0;
  }

  function handleDragMove(e) {
    if (!isDragging || !trackRef) return;
    const x = e.pageX - trackRef.offsetLeft;
    const walk = (x - startX) * 1.5;
    trackRef.scrollLeft = scrollLeft - walk;
  }

  function handleDragEnd() {
    isDragging = false;
  }
</script>

<section id="testimonials" bind:this={sectionRef} class="relative section-padding">
  <div class="section-container">
    <!-- Section Header -->
    <div class="text-center mb-16">
      <span class="section-label">Testimonials</span>
      <h2 class="section-title mb-6">
        Loved by Those Who
        <span class="gradient-text">Trust Their Thoughts</span>
      </h2>
      <p class="section-subtitle mx-auto">
        Real stories from people who've made Mindful part of their daily lives.
      </p>
    </div>

    <!-- Testimonials Carousel -->
    <div class="relative max-w-6xl mx-auto">
      <!-- Cards -->
      <div
        bind:this={trackRef}
        role="region"
        aria-label="Testimonials carousel"
        class="flex gap-6 overflow-x-auto pb-4 snap-x snap-mandatory scrollbar-hide {isDragging ? 'cursor-grabbing' : 'cursor-grab'}"
        onmousedown={handleDragStart}
        onmousemove={handleDragMove}
        onmouseup={handleDragEnd}
        onmouseleave={handleDragEnd}
      >
        {#each testimonials as testimonial, i}
          <div
            use:setCardRef={i}
            class="testimonial-card flex-shrink-0 w-[85vw] sm:w-[400px] snap-center opacity-0"
          >
            <div class="glass rounded-3xl p-8 h-full hover:border-iris-500/20 transition-all duration-500">
              <!-- Rating -->
              <div class="flex gap-1 mb-5">
                {#each {length: testimonial.rating} as _}
                  <svg class="w-4 h-4 text-amber-400" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                  </svg>
                {/each}
              </div>

              <!-- Quote -->
              <p class="text-slate-300 leading-relaxed mb-8 text-sm">"{testimonial.text}"</p>

              <!-- Author -->
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-gradient-to-br {testimonial.color} border border-white/10 flex items-center justify-center">
                  <span class="text-sm font-semibold gradient-text-duo">{testimonial.avatar}</span>
                </div>
                <div>
                  <p class="text-sm font-semibold">{testimonial.name}</p>
                  <p class="text-xs text-slate-500">{testimonial.role}</p>
                </div>
              </div>
            </div>
          </div>
        {/each}
      </div>

      <!-- Dots -->
      <div class="flex items-center justify-center gap-2 mt-8">
        {#each testimonials as _, i}
          <button
            onclick={() => goTo(i)}
            class="rounded-full transition-all duration-300 {activeIndex === i ? 'bg-iris-400 w-6' : 'bg-white/20 w-2'} h-2"
            aria-label="Go to testimonial {i + 1}"
          ></button>
        {/each}
      </div>
    </div>
  </div>
</section>
