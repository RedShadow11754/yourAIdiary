<script>
  import Logo from '../lib/components/Logo.svelte';
  import { api } from '../lib/api.js';
  import { toast } from '../lib/stores.svelte.js';

  let userName = $state('');
  let sliders = $state([
    { key: 'warmth', label: 'Warmth', icon: '🫂', desc: 'How tender and caring Daisy feels', value: 2 },
    { key: 'sassiness', label: 'Sassiness', icon: '💅', desc: 'A little attitude goes a long way', value: 2 },
    { key: 'banter', label: 'Banter', icon: '😄', desc: 'Playful teasing and jokes', value: 2 },
    { key: 'directness', label: 'Directness', icon: '🎯', desc: 'Straight talk vs gentle hints', value: 2 },
    { key: 'verbosity', label: 'Verbosity', icon: '💬', desc: 'Short and snappy, or rich and detailed', value: 2 },
    { key: 'emoji', label: 'Emoji', icon: '✨', desc: 'How much Daisy decorates her texts', value: 2 },
  ]);
  let customPrompt = $state('');
  let saving = $state(false);
  let savedFlash = $state(false);

  const LEVELS = ['Low', 'Medium', 'High'];

  function tonePreview() {
    const get = (k) => sliders.find((s) => s.key === k).value;
    let t = '';
    if (get('warmth') === 3) t = "Oh sweetheart, I've been thinking about you — ";
    else if (get('warmth') === 1) t = "Hey. ";
    else t = "Hey you. ";

    if (get('banter') === 3) t += "don't think I didn't notice you went quiet on me again 😏 ";
    else if (get('banter') >= 2) t += "look who decided to show up ";

    if (get('directness') === 3) t += "you should just talk to them. Today. ";
    else if (get('directness') === 1) t += "maybe sleeping on it could help? only if you want though ";
    else t += "honestly, talking to them might be the move. ";

    if (get('verbosity') === 1) return t.trim();
    if (get('verbosity') === 3) {
      t += "And listen — whatever happens, I'll be right here. We can figure out exactly what you want to say together, word by word if you need. ";
    } else {
      t += "I'm here either way. ";
    }
    return t + (get('emoji') === 3 ? '💜✨🌼' : get('emoji') === 2 ? ' 💜' : '');
  }

  async function save() {
    saving = true;
    try {
      await api.updatePersonality({
        user_name: userName || undefined,
        ...Object.fromEntries(sliders.map((s) => [s.key, s.value])),
        custom_prompt: customPrompt || undefined,
      });
      savedFlash = true;
      setTimeout(() => (savedFlash = false), 2200);
      toast("Daisy's personality updated ✨", 'success');
    } catch (err) {
      toast(err?.error || 'Could not save personality', 'error');
    } finally {
      saving = false;
    }
  }
</script>

<div class="max-w-5xl mx-auto px-6 py-12">
  <header class="text-center mb-12 animate-rise">
    <div class="flex justify-center mb-4"><Logo size={56} /></div>
    <h1 class="font-display text-3xl md:text-4xl font-bold tracking-tight">
      Tune <span class="text-gradient">your Daisy</span>
    </h1>
    <p class="mt-3 text-[var(--color-ink-dim)] max-w-lg mx-auto leading-relaxed">
      Shape how she talks to you. Change it anytime — she adapts instantly.
    </p>
  </header>

  <div class="grid lg:grid-cols-5 gap-8 items-start">
    <!-- Sliders -->
    <div class="lg:col-span-3 glass rounded-3xl p-7 space-y-7 animate-rise">
      <div>
        <label class="block text-sm font-medium mb-2 text-[var(--color-ink-dim)]" for="daisy-name">What should she call you?</label>
        <input id="daisy-name" type="text" class="input-field" placeholder="Your name or nickname" bind:value={userName} maxlength="50" />
      </div>

      {#each sliders as s, i}
        <div>
          <div class="flex items-baseline justify-between mb-1.5">
            <label class="font-medium text-[15px]" for={`slider-${s.key}`}>{s.icon} {s.label}</label>
            <span
              class="text-xs font-semibold px-2.5 py-0.5 rounded-full transition-colors"
              style="background:rgba(139,92,246,{0.15 + s.value * 0.1});color:#d6c9ff"
            >
              {LEVELS[s.value - 1]}
            </span>
          </div>
          <p class="text-xs text-[var(--color-ink-faint)] mb-2.5">{s.desc}</p>
          <input
            id={`slider-${s.key}`}
            type="range"
            min="1"
            max="3"
            step="1"
            bind:value={s.value}
            class="w-full accent-[#a78bfa] cursor-pointer h-1.5"
            aria-label={s.label}
          />
          <div class="flex justify-between text-[10px] uppercase tracking-widest text-[var(--color-ink-faint)] mt-1">
            <span>Low</span><span>Medium</span><span>High</span>
          </div>
        </div>
      {/each}

      <div>
        <label class="block text-sm font-medium mb-2 text-[var(--color-ink-dim)]" for="custom-prompt">
          Anything else? <span class="text-[var(--color-ink-faint)] font-normal">(optional)</span>
        </label>
        <textarea
          id="custom-prompt"
          class="input-field resize-none min-h-24"
          placeholder='e.g. "Call me by my middle name" · "Never mention mornings" · "Talk like a pirate on Fridays"'
          bind:value={customPrompt}
        ></textarea>
      </div>

      <button class="btn-primary w-full py-3.5" onclick={save} disabled={saving}>
        {#if saving}
          Saving…
        {:else if savedFlash}
          ✓ Saved — Daisy is adjusting…
        {:else}
          Save personality
        {/if}
      </button>
    </div>

    <!-- Live preview -->
    <div class="lg:col-span-2 lg:sticky lg:top-24 animate-rise" style="animation-delay:.15s">
      <div class="glass glow-ring rounded-3xl p-6">
        <h2 class="font-display font-semibold mb-4 flex items-center gap-2">
          <Logo size={26} /> Live preview
        </h2>
        <div class="glass rounded-2xl rounded-tl-md px-4 py-4 text-[15px] leading-relaxed min-h-32">
          "{tonePreview()}"
        </div>
        <p class="text-xs text-[var(--color-ink-faint)] mt-4 leading-relaxed">
          Move the sliders and watch Daisy's voice change in real time.
        </p>
        <a href="#/chat" class="btn-primary w-full py-3 mt-5 inline-flex">Go chat with her →</a>
      </div>
    </div>
  </div>
</div>
