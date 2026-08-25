<script>
  import { api } from '../lib/api.js';
  import { getAuth } from '../lib/stores.svelte.js';
  import { navigate } from '../lib/router.svelte.js';

  const auth = getAuth();

  $effect(() => {
    if (!auth.isAuthenticated) navigate('/login');
  });

  let entries = $state([]);
  let loading = $state(true);

  $effect(() => {
    if (auth.isAuthenticated) loadEntries();
  });

  async function loadEntries() {
    loading = true;
    try {
      entries = await api.getDiaryEntries();
    } catch (e) {
      console.error('Failed to load diary', e);
    } finally {
      loading = false;
    }
  }

  const moodEmojis = {
    happy: '😊', sad: '😢', angry: '😤', anxious: '😰', excited: '🤩',
    lonely: '😔', peaceful: '😌', confused: '😵‍💫', grateful: '🙏', numb: '😶',
    hopeful: '🌟', frustrated: '😤', melancholic: '🥀', content: '☺️',
    overwhelmed: '🤯', other: '📝',
  };

  function formatDate(d) {
    return new Date(d + 'T00:00:00').toLocaleDateString('en-US', {
      weekday: 'long', month: 'long', day: 'numeric', year: 'numeric',
    });
  }

  let downloading = $state(false);

  async function downloadAllDiary() {
    if (entries.length === 0) return;
    downloading = true;
    try {
      // Fetch full content for every entry
      const fullEntries = [];
      for (const e of entries) {
        try {
          const full = await api.getDiaryEntry(e.id);
          fullEntries.push(full);
        } catch {
          fullEntries.push(e); // fallback to preview
        }
      }

      let text = '═══════════════════════════════════════\n';
      text += '           MY DIARY\n';
      text += '═══════════════════════════════════════\n\n';

      for (const e of fullEntries) {
        const emoji = moodEmojis[e.mood] || '📝';
        text += `${emoji} ${formatDate(e.date)} — ${e.mood}\n`;
        text += '───────────────────────────────────────\n';
        text += `${e.content}\n`;
        if (e.narrative_thread) {
          text += `\n  Narrative: ${e.narrative_thread}\n`;
        }
        text += '\n\n';
      }

      text += '═══════════════════════════════════════\n';
      text += `  Exported on ${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}\n`;
      text += '═══════════════════════════════════════\n';

      const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `diary-${new Date().toISOString().slice(0, 10)}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('Download failed', e);
    } finally {
      downloading = false;
    }
  }
</script>

<div class="min-h-screen pt-24 pb-16 px-4">
  <div class="max-w-3xl mx-auto">
    <!-- Header -->
    <div class="text-center mb-10 animate-slide-up">
      <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary to-accent mx-auto flex items-center justify-center text-white text-2xl mb-4 animate-float">
        📖
      </div>
      <h1 class="text-3xl font-bold text-white mb-2">Your Diary</h1>
      <p class="text-white/50 text-sm">Automatically written in your voice, every day</p>
      {#if entries.length > 0}
        <button
          onclick={downloadAllDiary}
          disabled={downloading}
          class="mt-4 inline-flex items-center gap-2 px-5 py-2.5 rounded-xl border border-glass-border text-sm text-white/60 hover:text-white hover:border-primary/50 hover:bg-primary/5 transition-all duration-300 disabled:opacity-50"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          {downloading ? 'Exporting...' : 'Download Entire Diary'}
        </button>
      {/if}
    </div>

    {#if loading}
      <div class="space-y-4">
        {#each [1,2,3] as _}
          <div class="glass p-6 rounded-2xl animate-shimmer">
            <div class="h-4 bg-white/5 rounded w-1/3 mb-3"></div>
            <div class="h-3 bg-white/5 rounded w-2/3 mb-2"></div>
            <div class="h-3 bg-white/5 rounded w-1/2"></div>
          </div>
        {/each}
      </div>
    {:else if entries.length === 0}
      <div class="text-center py-20 animate-fade">
        <div class="text-6xl mb-4">📝</div>
        <h3 class="text-xl font-semibold text-white mb-2">No entries yet</h3>
        <p class="text-white/40 max-w-sm mx-auto">Daisy will write your first diary entry after you have a meaningful conversation with her.</p>
      </div>
    {:else}
      <div class="space-y-4">
        {#each entries as entry, i}
          <a
            href="#/diary/{entry.id}"
            class="block glass p-6 rounded-2xl glass-hover animate-slide-up cursor-pointer"
            style="animation-delay: {Math.min(i * 0.08, 0.5)}s;"
          >
            <div class="flex items-start justify-between gap-4">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-lg">{moodEmojis[entry.mood] || '📝'}</span>
                  <span class="text-xs px-2 py-0.5 rounded-full bg-primary/15 text-primary-light capitalize">
                    {entry.mood}
                  </span>
                  {#if entry.is_edited}
                    <span class="text-xs px-2 py-0.5 rounded-full bg-accent/15 text-accent-light">
                      ✏️ Edited
                    </span>
                  {/if}
                </div>
                <p class="text-sm text-white/50 mb-1">{formatDate(entry.date)}</p>
                <p class="text-sm text-white/70 line-clamp-2 leading-relaxed">
                  {entry.content?.substring(0, 200)}{entry.content?.length > 200 ? '...' : ''}
                </p>
              </div>
              <svg class="w-5 h-5 text-white/20 shrink-0 mt-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </div>
          </a>
        {/each}
      </div>
    {/if}
  </div>
</div>
