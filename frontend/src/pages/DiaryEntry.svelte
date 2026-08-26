<script>
  import { api } from '../lib/api.js';
  import { toast } from '../lib/stores.svelte.js';
  import { getRouter, navigate } from '../lib/router.svelte.js';
  import MoodBadge from '../lib/components/MoodBadge.svelte';
  import Logo from '../lib/components/Logo.svelte';
  import { TEMPLATES, downloadDiaryHTML, openPrintView } from '../lib/diaryTemplates.js';

  const router = getRouter();

  let entry = $state(null);
  let loading = $state(true);
  let editing = $state(false);
  let editText = $state('');
  let savingEdit = $state(false);
  let pickerOpen = $state(false);
  let chosenTemplate = $state(TEMPLATES[0].id);

  const tpl = $derived(TEMPLATES.find((t) => t.id === chosenTemplate) || TEMPLATES[0]);

  function fmtFull(dateStr) {
    return new Date(dateStr + 'T12:00:00').toLocaleDateString('en-US', {
      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
    });
  }

  async function load() {
    loading = true;
    try {
      entry = await api.getDiaryEntry(router.params.id);
    } catch {
      toast('Could not load this entry', 'error');
      navigate('/diary');
    } finally {
      loading = false;
    }
  }

  async function saveEdit() {
    if (!editText.trim()) return;
    savingEdit = true;
    try {
      await api.editDiaryEntry(entry.id, editText);
      entry.content = editText;
      entry.is_edited = true;
      editing = false;
      toast('Entry updated ✏️', 'success');
    } catch (err) {
      toast(err?.error || 'Could not save changes', 'error');
    } finally {
      savingEdit = false;
    }
  }

  function download() {
    downloadDiaryHTML(entry, chosenTemplate);
    toast(`Downloaded in "${tpl.name}" style 📥`, 'success');
  }

  function printView() {
    openPrintView(entry, chosenTemplate);
  }

  function onPickerKeydown(e) {
    if (e.key === 'Escape') pickerOpen = false;
  }

  $effect(() => {
    if (router.params.id) load();
  });
</script>

<svelte:window onkeydown={onPickerKeydown} />

<div class="max-w-3xl mx-auto px-6 py-10">
  <button class="btn-ghost px-4 py-2 text-sm mb-8" onclick={() => navigate('/diary')}>← Back to diary</button>

  {#if loading}
    <div class="glass rounded-3xl h-96 animate-pulse"></div>
  {:else if entry}
    <!-- Paper reading card -->
    <article class="glass glow-ring rounded-[2rem] overflow-hidden animate-rise">
      <header class="px-8 md:px-12 pt-10 pb-7 border-b border-white/8 relative">
        <div
          class="absolute inset-x-0 top-0 h-1.5"
          style="background:linear-gradient(90deg,#7c3aed,#d946ef,#22d3ee)"
        ></div>
        <div class="flex flex-wrap items-center gap-4 justify-between">
          <MoodBadge mood={entry.mood} size="lg" />
          {#if entry.is_edited}
            <span class="text-xs text-[var(--color-ink-faint)]">✏️ edited by you</span>
          {/if}
        </div>
        <h1 class="font-display text-2xl md:text-3xl font-bold mt-5">{fmtFull(entry.date)}</h1>
      </header>

      <div class="px-8 md:px-12 py-9">
        {#if editing}
          <textarea
            class="input-field min-h-80 leading-loose"
            bind:value={editText}
            placeholder="Rewrite your story…"
          ></textarea>
          <div class="flex gap-3 mt-5">
            <button class="btn-primary px-7 py-3" onclick={saveEdit} disabled={savingEdit || !editText.trim()}>
              {savingEdit ? 'Saving…' : 'Save changes'}
            </button>
            <button class="btn-ghost px-7 py-3" onclick={() => (editing = false)}>Cancel</button>
          </div>
        {:else}
          <div class="space-y-5 text-[16.5px] leading-[1.95] text-[var(--color-ink)]/90 animate-fade">
            {#each entry.content.split(/\n+/).filter((p) => p.trim()) as para}
              <p class="first:first-letter:text-5xl first:first-letter:font-hand first:first-letter:text-[var(--color-primary-300)] first:first-letter:float-left first:first-letter:mr-2.5 first:first-letter:leading-none">
                {para}
              </p>
            {/each}
          </div>
        {/if}
      </div>

      <footer class="px-8 md:px-12 pb-9 flex flex-wrap items-center gap-3 border-t border-white/8 pt-7">
        <span class="text-sm text-[var(--color-ink-faint)] mr-auto">written with Daisy 🌼</span>
        {#if !editing}
          <button class="btn-ghost px-5 py-2.5 text-sm" onclick={() => { editText = entry.content; editing = true; }}>
            ✏️ Edit
          </button>
          <button class="btn-primary px-7 py-3" onclick={() => (pickerOpen = true)}>
            ⬇ Download this diary
          </button>
        {/if}
      </footer>
    </article>
  {/if}
</div>

<!-- ── Template picker modal ── -->
{#if pickerOpen && entry}
  <div
    class="fixed inset-0 z-[90] bg-black/70 backdrop-blur-sm flex items-end sm:items-center justify-center p-0 sm:p-6 animate-fade"
    role="presentation"
    onclick={(e) => e.target === e.currentTarget && (pickerOpen = false)}
  >
    <div class="glass-strong w-full max-w-4xl max-h-[88vh] rounded-t-3xl sm:rounded-3xl overflow-hidden flex flex-col animate-pop">
      <header class="flex items-center justify-between px-7 py-5 border-b border-white/10 shrink-0">
        <div>
          <h2 class="font-display font-bold text-lg">Choose a diary design</h2>
          <p class="text-xs text-[var(--color-ink-dim)] mt-0.5">12 handcrafted templates · yours forever</p>
        </div>
        <button class="w-9 h-9 rounded-full glass grid place-items-center cursor-pointer hover:border-white/40 transition-colors" aria-label="Close template picker" onclick={() => (pickerOpen = false)}>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
      </header>

      <!-- Selected template preview strip -->
      <div class="px-7 py-4 border-b border-white/10 flex items-center gap-4 shrink-0 flex-wrap">
        <span class="text-sm text-[var(--color-ink-dim)]">Selected:</span>
        <span class="inline-flex items-center gap-2.5 glass rounded-full pl-1.5 pr-4 py-1.5">
          <span class="w-7 h-7 rounded-full border border-white/20" style="background:{tpl.swatch.bg}"></span>
          <strong class="text-sm" style="color:{tpl.swatch.accent}">{tpl.name}</strong>
        </span>
      </div>

      <!-- Template grid -->
      <div class="overflow-y-auto px-7 py-6 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        {#each TEMPLATES as t (t.id)}
          <button
            class="text-left rounded-2xl p-3 cursor-pointer transition-all duration-200 group
              {chosenTemplate === t.id ? 'ring-2 ring-[var(--color-primary-400)] bg-white/8' : 'glass hover:-translate-y-0.5'}"
            onclick={() => (chosenTemplate = t.id)}
          >
            <!-- Mini page mock -->
            <div class="rounded-xl h-32 relative overflow-hidden mb-3 shadow-inner" style="background:{t.swatch.bg}">
              <div class="absolute inset-0 p-3 flex flex-col gap-1.5 opacity-90">
                <div class="h-2 w-14 rounded-full" style="background:{t.swatch.accent};opacity:.85"></div>
                <div class="h-1.5 w-full rounded-full bg-current opacity-15"></div>
                <div class="h-1.5 w-11/12 rounded-full bg-current opacity-15"></div>
                <div class="h-1.5 w-full rounded-full bg-current opacity-15"></div>
                <div class="h-1.5 w-4/5 rounded-full bg-current opacity-15"></div>
                <div class="h-1.5 w-3/5 rounded-full bg-current opacity-10"></div>
                <div class="mt-auto font-hand text-lg leading-none truncate" style="color:{t.swatch.accent}">
                  Dear diary…
                </div>
              </div>
              {#if chosenTemplate === t.id}
                <div class="absolute top-2 right-2 w-6 h-6 rounded-full grid place-items-center text-xs font-bold text-white" style="background:#7c3aed">✓</div>
              {/if}
            </div>
            <div class="font-display font-semibold text-sm" style="color:{chosenTemplate === t.id ? '#fff' : 'inherit'}">{t.name}</div>
            <div class="text-xs text-[var(--color-ink-faint)] leading-snug mt-0.5">{t.desc}</div>
          </button>
        {/each}
      </div>

      <footer class="flex flex-col sm:flex-row gap-3 px-7 py-5 border-t border-white/10 shrink-0">
        <p class="text-xs text-[var(--color-ink-faint)] sm:flex-1 self-center leading-relaxed">
          Downloads as a beautiful HTML keepsake — open it and hit “Save as PDF” to print.
        </p>
        <button class="btn-ghost px-6 py-3 text-sm" onclick={printView}>🖨 Preview & print</button>
        <button class="btn-primary px-7 py-3 text-sm" onclick={download}>⬇ Download</button>
      </footer>
    </div>
  </div>
{/if}
