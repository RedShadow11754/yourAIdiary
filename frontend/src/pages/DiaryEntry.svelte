<script>
  import { api } from '../lib/api.js';
  import { getAuth } from '../lib/stores.svelte.js';
  import { navigate, getRouter } from '../lib/router.svelte.js';

  const auth = getAuth();
  const router = getRouter();

  $effect(() => {
    if (!auth.isAuthenticated) navigate('/login');
  });

  let entry = $state(null);
  let loading = $state(true);
  let editing = $state(false);
  let editContent = $state('');
  let saving = $state(false);
  let saved = $state(false);

  const moodEmojis = {
    happy: '😊', sad: '😢', angry: '😤', anxious: '😰', excited: '🤩',
    lonely: '😔', peaceful: '😌', confused: '😵‍💫', grateful: '🙏', numb: '😶',
    hopeful: '🌟', frustrated: '😤', melancholic: '🥀', content: '☺️',
    overwhelmed: '🤯', other: '📝',
  };

  $effect(() => {
    if (router.params.id && auth.isAuthenticated) {
      loadEntry(router.params.id);
    }
  });

  async function loadEntry(id) {
    loading = true;
    try {
      entry = await api.getDiaryEntry(id);
      editContent = entry.content;
    } catch (e) {
      console.error('Failed to load entry', e);
    } finally {
      loading = false;
    }
  }

  function startEditing() {
    editContent = entry.content;
    editing = true;
  }

  function cancelEditing() {
    editing = false;
    editContent = entry.content;
  }

  async function saveEdit() {
    if (!editContent.trim()) return;
    saving = true;
    try {
      await api.editDiaryEntry(router.params.id, editContent.trim());
      entry = { ...entry, content: editContent.trim(), is_edited: true };
      editing = false;
      saved = true;
      setTimeout(() => saved = false, 3000);
    } catch (e) {
      console.error('Failed to save', e);
    } finally {
      saving = false;
    }
  }

  function formatDate(d) {
    return new Date(d + 'T00:00:00').toLocaleDateString('en-US', {
      weekday: 'long', month: 'long', day: 'numeric', year: 'numeric',
    });
  }
</script>

<div class="min-h-screen pt-24 pb-16 px-4">
  <div class="max-w-2xl mx-auto">
    <!-- Back button -->
    <a href="#/diary" class="inline-flex items-center gap-1.5 text-sm text-white/40 hover:text-white/70 transition-colors mb-6 animate-fade">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
      Back to diary
    </a>

    {#if loading}
      <div class="glass p-8 rounded-3xl animate-shimmer">
        <div class="h-6 bg-white/5 rounded w-1/3 mb-6"></div>
        <div class="space-y-3">
          <div class="h-3 bg-white/5 rounded w-full"></div>
          <div class="h-3 bg-white/5 rounded w-5/6"></div>
          <div class="h-3 bg-white/5 rounded w-4/5"></div>
        </div>
      </div>
    {:else if entry}
      {#if saved}
        <div class="mb-4 px-4 py-3 rounded-xl bg-green-500/10 border border-green-500/20 text-green-400 text-sm animate-slide-up">
          ✓ Entry updated!
        </div>
      {/if}

      <div class="glass p-8 rounded-3xl animate-scale">
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="text-2xl">{moodEmojis[entry.mood] || '📝'}</span>
              <span class="text-xs px-2.5 py-1 rounded-full bg-primary/15 text-primary-light capitalize font-medium">
                {entry.mood}
              </span>
            </div>
            <p class="text-white/40 text-sm">{formatDate(entry.date)}</p>
          </div>

          {#if !editing}
            <button
              onclick={startEditing}
              class="px-4 py-2 rounded-xl border border-glass-border text-sm text-white/60 hover:text-white hover:border-primary/50 transition-all duration-300 flex items-center gap-1.5"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
              Edit
            </button>
          {/if}
        </div>

        <!-- Content -->
        {#if editing}
          <div class="space-y-4">
            <textarea
              bind:value={editContent}
              rows="15"
              class="w-full px-4 py-4 rounded-xl bg-surface-lighter border border-glass-border text-white/90 text-sm leading-relaxed resize-none transition-all duration-300"
            ></textarea>
            <div class="flex gap-2">
              <button
                onclick={saveEdit}
                disabled={saving}
                class="px-6 py-2.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white text-sm font-medium hover:scale-[1.02] transition-all duration-300 disabled:opacity-50"
              >
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
              <button
                onclick={cancelEditing}
                class="px-6 py-2.5 rounded-xl border border-glass-border text-white/60 text-sm hover:text-white transition-all duration-300"
              >
                Cancel
              </button>
            </div>
          </div>
        {:else}
          <div class="prose prose-invert max-w-none">
            <div class="text-white/80 text-sm leading-[1.8] whitespace-pre-wrap font-serif">
              {entry.content}
            </div>
          </div>
        {/if}

        <!-- Narrative thread -->
        {#if entry.narrative_thread && !editing}
          <div class="mt-8 pt-6 border-t border-glass-border/30">
            <p class="text-xs text-white/30 uppercase tracking-wider mb-2">Narrative Thread</p>
            <p class="text-sm text-white/50 italic">{entry.narrative_thread}</p>
          </div>
        {/if}
      </div>
    {/if}
  </div>
</div>
