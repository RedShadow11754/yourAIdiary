<script>
  let { mood = 'other', size = 'sm' } = $props();

  const MOODS = {
    happy: { emoji: '😊', label: 'Happy', bg: 'rgba(251,191,36,0.14)', fg: '#fcd34d' },
    sad: { emoji: '🌧️', label: 'Sad', bg: 'rgba(96,165,250,0.14)', fg: '#93c5fd' },
    angry: { emoji: '🔥', label: 'Angry', bg: 'rgba(248,113,113,0.14)', fg: '#fca5a5' },
    anxious: { emoji: '🌀', label: 'Anxious', bg: 'rgba(167,139,250,0.16)', fg: '#c4b5fd' },
    excited: { emoji: '✨', label: 'Excited', bg: 'rgba(232,121,249,0.14)', fg: '#f0abfc' },
    lonely: { emoji: '🌙', label: 'Lonely', bg: 'rgba(148,163,184,0.16)', fg: '#cbd5e1' },
    peaceful: { emoji: '🍃', label: 'Peaceful', bg: 'rgba(52,211,153,0.13)', fg: '#6ee7b7' },
    confused: { emoji: '🧭', label: 'Confused', bg: 'rgba(45,212,191,0.13)', fg: '#5eead4' },
    grateful: { emoji: '🤍', label: 'Grateful', bg: 'rgba(251,207,232,0.14)', fg: '#f9a8d4' },
    numb: { emoji: '🌫️', label: 'Numb', bg: 'rgba(203,213,225,0.12)', fg: '#e2e8f0' },
    hopeful: { emoji: '🌅', label: 'Hopeful', bg: 'rgba(253,186,116,0.14)', fg: '#fdba74' },
    frustrated: { emoji: '⚡', label: 'Frustrated', bg: 'rgba(251,146,60,0.14)', fg: '#fdba74' },
    melancholic: { emoji: '🍂', label: 'Melancholic', bg: 'rgba(183,148,244,0.15)', fg: '#d8b4fe' },
    content: { emoji: '☕', label: 'Content', bg: 'rgba(214,211,209,0.14)', fg: '#e7e5e4' },
    overwhelmed: { emoji: '🌊', label: 'Overwhelmed', bg: 'rgba(56,189,248,0.13)', fg: '#7dd3fc' },
    other: { emoji: '📖', label: 'Reflecting', bg: 'rgba(167,139,250,0.14)', fg: '#c4b5fd' },
  };

  const m = $derived(MOODS[mood] || MOODS.other);
</script>

<span
  class="inline-flex items-center gap-1.5 rounded-full font-medium whitespace-nowrap"
  class:px-2.5={size === 'sm'}
  class:py-1={size === 'sm'}
  class:text-xs={size === 'sm'}
  class:px-3.5={size === 'lg'}
  class:py-1.5={size === 'lg'}
  class:text-sm={size === 'lg'}
  style="background:{m.bg};color:{m.fg};border:1px solid color-mix(in srgb, {m.fg} 25%, transparent);"
>
  <span>{m.emoji}</span>{m.label}
</span>
