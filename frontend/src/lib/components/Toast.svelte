<script>
  import { getToasts } from '../stores.svelte.js';

  const toasts = getToasts();

  const ICONS = { success: '✓', error: '✕', info: '✦' };
</script>

<div class="fixed bottom-6 right-6 z-[100] flex flex-col gap-3 max-w-sm">
  {#each toasts.list as t (t.id)}
    <div
      class="glass-strong rounded-2xl px-4 py-3.5 flex items-start gap-3 shadow-2xl animate-pop"
      style="border-color: {t.type === 'error' ? 'rgba(248,113,113,0.35)' : t.type === 'success' ? 'rgba(52,211,153,0.35)' : 'rgba(167,139,250,0.3)'};"
    >
      <span
        class="w-7 h-7 shrink-0 rounded-full grid place-items-center text-sm font-bold"
        style="background: {t.type === 'error' ? 'rgba(248,113,113,0.18)' : t.type === 'success' ? 'rgba(52,211,153,0.18)' : 'rgba(139,92,246,0.2)'}; color: {t.type === 'error' ? '#fca5a5' : t.type === 'success' ? '#6ee7b7' : '#c4b5fd'};"
      >
        {ICONS[t.type] || ICONS.info}
      </span>
      <p class="text-sm leading-relaxed text-[var(--color-ink)] pt-1">{t.message}</p>
      <button class="ml-auto text-[var(--color-ink-faint)] hover:text-white cursor-pointer pt-1" aria-label="Dismiss notification" onclick={() => toasts.dismiss(t.id)}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
      </button>
    </div>
  {/each}
</div>
