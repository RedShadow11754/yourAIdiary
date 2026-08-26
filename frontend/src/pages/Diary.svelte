<script>
  import { api } from '../lib/api.js';
  import { toast } from '../lib/stores.svelte.js';
  import MoodBadge from '../lib/components/MoodBadge.svelte';
  import Logo from '../lib/components/Logo.svelte';

  let entries = $state([]);
  let loading = $state(true);
  let filter = $state('all');
  let query = $state('');

  const FILTERS = ['all', 'happy', 'excited', 'grateful', 'peaceful', 'hopeful', 'sad', 'anxious'];

  function fmtDate(dateStr) {
    return new Date(dateStr + 'T12:00:00').toLocaleDateString('en-US', {
      weekday: 'short', month: 'short', day: 'numeric',
    });
  }

  function excerpt(text, n = 130) {
    return text.length > n ? text.slice(0, n).trimEnd() + '…' : text;
  }

  let filtered = $derived(
    entries.filter(
      (e) =>
        (filter === 'all' || e.mood === filter) &&
        (!query || e.content.toLowerCase().includes(query.toLowerCase()))
    )
  );

  let streak = $derived.by(() => {
    if (entries.length < 2) return entries.length;
    let s = 1;
    for (let i = 1; i < entries.length; i++) {
      const prev = new Date(entries[i - 1].date + 'T12:00:00');
      const cur = new Date(entries[i].date + 'T12:00:00');
      if ((prev - cur) / 86400000 === 1) s++;
      else break;
    }
    return s;
  });

  $effect(() => {
    api
      .getDiaryEntries()
      .then((data) => (entries = Array.isArray(data) ? data : []))
      .catch(() => toast('Could not load diary', 'error'))
      .finally(() => (loading = false));
  });
</script>

<div class="max-w-5xl mx-auto px-6 py-12">
  <header class="mb-10 animate-rise">
    <p class="text-sm tracking-[0.3em] uppercase text-[var(--color-primary-300)] font-medium mb-2">Your story</p>
    <h1 class="font-display text-3xl md:text-4xl font-bold tracking-tight">
      The <span class="text-gradient-warm">Diary</span> 📖
    </h1>

    {#if !loading && entries.length > 0}
      <div class="flex flex-wrap gap-3 mt-6">
        <div class="glass rounded-2xl px-5 py-3">
          <div class="font-display text-2xl font-bold">{entries.length}</div>
          <div class="text-xs text-[var(--color-ink-dim)]">entries written</div>
        </div>
        <div class="glass rounded-2xl px-5 py-3">
          <div class="font-display text-2xl font-bold">🔥 {streak}</div>
          <div class="text-xs text-[var(--color-ink-dim)]">day streak</div>
        </div>
        <input
          type="search"
          class="input-field flex-1 min-w-48 self-stretch"
          placeholder="Search your memories…"
          bind:value={query}
        />
      </div>
    {/if}
  </header>

  <!-- Mood filters -->
  {#if !loading && entries.length > 0}
    <div class="flex gap-2 overflow-x-auto no-scrollbar pb-2 mb-8 animate-fade">
      {#each FILTERS as f}
        <button
          onclick={() => (filter = f)}
          class="px-4 py-2 rounded-full text-sm whitespace-nowrap transition-all duration-200 cursor-pointer capitalize
            {filter === f ? 'btn-primary !py-2' : 'glass hover:border-[rgba(196,181,253,.45)]'}"
        >
          {f === 'all' ? '✦ All moods' : f}
        </button>
      {/each}
    </div>
  {/if}

  {#if loading}
    <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
      {#each [1, 2, 3, 4, 5, 6] as i}
        <div class="glass rounded-3xl h-56 animate-pulse"></div>
      {/each}
    </div>
  {:else if entries.length === 0}
    <div class="text-center py-24 animate-rise">
      <Logo size={72} />
      <h2 class="font-display text-2xl font-bold mt-6">Your diary is waiting to be born</h2>
      <p class="text-[var(--color-ink-dim)] max-w-md mx-auto mt-3 leading-relaxed">
        Chat with Daisy today — tomorrow morning, your first entry will be here,
        written and ready to keep forever.
      </p>
      <a href="#/chat" class="btn-primary px-8 py-3.5 mt-8 inline-flex">Start chatting →</a>
    </div>
  {:else if filtered.length === 0}
    <p class="text-center text-[var(--color-ink-dim)] py-20">No entries match that filter. Try another mood ✨</p>
  {:else}
    <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 stagger">
      {#each filtered as e (e.id)}
        <a href={`#/diary/${e.id}`} class="group block glass card-hover rounded-3xl p-6 relative overflow-hidden">
          <div
            class="absolute inset-x-0 top-0 h-1 opacity-70"
            style="background:linear-gradient(90deg,#7c3aed,#d946ef,#22d3ee)"
          ></div>
          <div class="flex items-center justify-between mb-3">
            <span class="text-xs text-[var(--color-ink-faint)] uppercase tracking-wider">{fmtDate(e.date)}</span>
            {#if e.is_edited}<span title="edited" class="text-xs">✏️</span>{/if}
          </div>
          <MoodBadge mood={e.mood} />
          <p class="mt-4 text-sm leading-relaxed text-[var(--color-ink-dim)] group-hover:text-[var(--color-ink)] transition-colors">
            {excerpt(e.content)}
          </p>
          <span class="inline-flex items-center gap-1.5 text-xs text-[var(--color-primary-300)] mt-4 opacity-0 group-hover:opacity-100 transition-opacity">
            Read & download →
          </span>
        </a>
      {/each}
    </div>
  {/if}
</div>
