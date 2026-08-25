<script>
  import { onMount } from 'svelte';
  import gsap from 'gsap';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';

  let sectionRef = $state(null);
  let faqItems = $state([]);
  let openIndex = $state(null);

  const faqs = [
    {
      question: 'How is Mindful different from other diary apps?',
      answer: 'Mindful isn\'t just a place to write — it\'s an AI companion that truly understands you. Unlike traditional diary apps that are passive storage, Mindful actively remembers context across conversations, recognizes patterns in your thoughts and emotions, and grows more insightful the more you use it. It\'s like having a journal that journals back.',
    },
    {
      question: 'Is my data private and secure?',
      answer: 'Absolutely. Privacy is foundational to Mindful. Your entries are end-to-end encrypted, anonymized by default, and never used for AI training. We don\'t sell or share your data. Your thoughts belong to you, period. We\'re also GDPR and CCPA compliant.',
    },
    {
      question: 'How does the AI memory actually work?',
      answer: 'Think of it as a thoughtful friend who remembers what matters. When you write, the AI extracts meaningful details — not just keywords, but emotions, relationships, struggles, and victories. It builds a rich understanding of your life context over time. When you mention something, it can connect it to past entries, offering continuity and deeper insight.',
    },
    {
      question: 'Can I use Mindful on my phone?',
      answer: 'Yes! Mindful is fully responsive and works beautifully on any device. Whether you\'re on desktop, tablet, or phone, the experience is seamless. We also have native mobile apps coming soon for iOS and Android.',
    },
    {
      question: 'Is there a free tier? What about pricing?',
      answer: 'We\'re currently in Early Access, which includes full access to all features at no cost. As we launch, we\'ll introduce a freemium model — a generous free tier for daily journaling, and a premium plan for advanced features like deeper memory analysis, mood insights, and unlimited history. Early Access users get a special lifetime rate.',
    },
    {
      question: 'How much time do I need to spend each day?',
      answer: 'As little or as much as you like! Some users write a few sentences a day, others have long conversations. Mindful adapts to your style. Even 2-3 minutes of daily reflection can build meaningful continuity. The AI doesn\'t demand — it simply listens whenever you\'re ready to share.',
    },
  ];

  function setFaqItemRef(el, i) {
    faqItems[i] = el;
  }

  onMount(() => {
    faqItems.forEach((item, i) => {
      if (!item) return;
      gsap.fromTo(
        item,
        { y: 20, opacity: 0 },
        {
          y: 0, opacity: 1,
          duration: 0.5,
          delay: i * 0.1,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: item,
            start: 'top bottom-=50',
            toggleActions: 'play none none reverse',
          },
        }
      );
    });
  });

  function toggle(index) {
    openIndex = openIndex === index ? null : index;
  }
</script>

<section id="faq" bind:this={sectionRef} class="relative section-padding bg-midnight-950/30">
  <div class="section-container">
    <!-- Section Header -->
    <div class="text-center mb-16">
      <span class="section-label">FAQ</span>
      <h2 class="section-title mb-6">
        Questions? We've Got
        <span class="gradient-text-duo">Answers</span>
      </h2>
      <p class="section-subtitle mx-auto">
        Everything you need to know about Mindful. Still have questions? We're here to help.
      </p>
    </div>

    <!-- FAQ Items -->
    <div class="max-w-3xl mx-auto space-y-3">
      {#each faqs as faq, i}
        <div
          use:setFaqItemRef={i}
          class="glass rounded-2xl overflow-hidden transition-all duration-300 opacity-0 {openIndex === i ? 'border-iris-500/20' : ''}"
        >
          <button
            onclick={() => toggle(i)}
            class="w-full flex items-center justify-between p-5 md:p-6 text-left transition-colors hover:bg-white/[0.02]"
            aria-expanded={openIndex === i}
          >
            <span class="font-display font-medium text-sm md:text-base pr-4">{faq.question}</span>
            <svg
              class="w-5 h-5 flex-shrink-0 shrink-0 text-slate-400 transition-transform duration-300 {openIndex === i ? 'rotate-180' : ''}"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            >
              <path d="M6 9l6 6 6-6" />
            </svg>
          </button>
          {#if openIndex === i}
            <div class="px-5 md:px-6 pb-5 md:pb-6 animate-fade-in">
              <p class="text-slate-400 text-sm leading-relaxed">{faq.answer}</p>
            </div>
          {/if}
        </div>
      {/each}
    </div>
  </div>
</section>
