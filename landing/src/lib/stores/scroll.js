import { onMount } from 'svelte';

/**
 * Reactive scroll state using Svelte 5 runes.
 * Tracks scroll progress, direction, and active section.
 */
export function createScrollState() {
  let scrollY = $state(0);
  let scrollProgress = $state(0);
  let scrollDirection = $state('down');
  let lastScrollY = $state(0);
  let activeSection = $state('hero');

  const sections = ['hero', 'features', 'how-it-works', 'timeline', 'chat-preview', 'testimonials', 'faq', 'cta'];

  function handleScroll() {
    scrollY = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    scrollProgress = docHeight > 0 ? Math.min(scrollY / docHeight, 1) : 0;
    scrollDirection = scrollY > lastScrollY ? 'down' : 'up';
    lastScrollY = scrollY;

    // Determine active section
    for (let i = sections.length - 1; i >= 0; i--) {
      const el = document.getElementById(sections[i]);
      if (el && el.offsetTop - 200 <= scrollY) {
        activeSection = sections[i];
        break;
      }
    }
  }

  onMount(() => {
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  });

  return {
    get scrollY() { return scrollY; },
    get scrollProgress() { return scrollProgress; },
    get scrollDirection() { return scrollDirection; },
    get activeSection() { return activeSection; },
  };
}
