<script>
  import { api } from '../lib/api.js';
  import { getAuth } from '../lib/stores.svelte.js';
  import { navigate } from '../lib/router.svelte.js';

  const auth = getAuth();

  $effect(() => {
    if (!auth.isAuthenticated) navigate('/login');
  });

  let userName = $state('user');
  let sassiness = $state(2);
  let warmth = $state(2);
  let banter = $state(2);
  let directness = $state(2);
  let verbosity = $state(2);
  let emoji = $state(2);
  let customPrompt = $state('');
  let loading = $state(false);
  let saved = $state(false);
  let error = $state('');

  const traits = [
    { key: 'sassiness', label: 'Sassiness', icon: '😏', desc: 'How much attitude she gives you', left: 'Chill', right: 'Savage' },
    { key: 'warmth', label: 'Warmth', icon: '🥰', desc: 'How caring and affectionate she is', left: 'Reserved', right: 'Toasty' },
    { key: 'banter', label: 'Banter', icon: '😂', desc: 'How much she jokes around', left: 'Serious', right: 'Comedian' },
    { key: 'directness', label: 'Directness', icon: '🎯', desc: 'How blunt she is with you', left: 'Gentle', right: 'Brutal honesty' },
    { key: 'verbosity', label: 'Verbosity', icon: '📝', desc: 'How much she talks', left: 'Short & sweet', right: 'Novelist' },
    { key: 'emoji', label: 'Emoji Usage', icon: '✨', desc: 'How many emojis she uses', left: 'No emojis', right: '🎉🥳✨💯🔥' },
  ];

  function getTraitValue(key) {
    if (key === 'sassiness') return sassiness;
    if (key === 'warmth') return warmth;
    if (key === 'banter') return banter;
    if (key === 'directness') return directness;
    if (key === 'verbosity') return verbosity;
    return emoji;
  }

  function setTraitValue(key, val) {
    if (key === 'sassiness') sassiness = val;
    else if (key === 'warmth') warmth = val;
    else if (key === 'banter') banter = val;
    else if (key === 'directness') directness = val;
    else if (key === 'verbosity') verbosity = val;
    else emoji = val;
  }

  async function handleSave() {
    loading = true;
    error = '';
    try {
      await api.updatePersonality({
        user_name: userName || 'user',
        sassiness,
        warmth,
        banter,
        directness,
        verbosity,
        emoji,
        custom_prompt: customPrompt || null,
      });
      saved = true;
      setTimeout(() => saved = false, 3000);
    } catch (e) {
      error = e.error || 'Failed to save';
    } finally {
      loading = false;
    }
  }

  const levelLabels = ['Low', 'Medium', 'High'];
</script>

<div class="min-h-screen pt-24 pb-16 px-4">
  <div class="max-w-2xl mx-auto">
    <!-- Header -->
    <div class="text-center mb-10 animate-slide-up">
      <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary to-accent mx-auto flex items-center justify-center text-white text-2xl mb-4 animate-float">
        🎨
      </div>
      <h1 class="text-3xl font-bold text-white mb-2">Customize Daisy</h1>
      <p class="text-white/50 text-sm">Adjust her personality to match your vibe</p>
    </div>

    {#if error}
      <div class="mb-4 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm animate-slide-up">
        {error}
      </div>
    {/if}

    {#if saved}
      <div class="mb-4 px-4 py-3 rounded-xl bg-green-500/10 border border-green-500/20 text-green-400 text-sm animate-slide-up flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
        Personality saved!
      </div>
    {/if}

    <div class="space-y-4">
      <!-- Name -->
      <div class="glass p-6 rounded-2xl animate-slide-up" style="animation-delay: 0.1s;">
        <label class="block text-sm text-white/60 mb-2">What should she call you?</label>
        <input
          type="text"
          bind:value={userName}
          placeholder="Your name"
          class="w-full px-4 py-3 rounded-xl bg-surface-lighter border border-glass-border text-white placeholder-white/30 text-sm transition-all duration-300"
        />
      </div>

      <!-- Trait sliders -->
      {#each traits as trait, i}
        {@const val = getTraitValue(trait.key)}
        {@const pct = ((val - 1) / 2) * 100}
        <div class="glass p-6 rounded-2xl animate-slide-up" style="animation-delay: {0.05 * (i + 2)}s;">
          <div class="flex items-center gap-2 mb-1">
            <span class="text-xl">{trait.icon}</span>
            <h3 class="text-sm font-semibold text-white">{trait.label}</h3>
          </div>
          <p class="text-xs text-white/40 mb-4">{trait.desc}</p>

          <div class="relative">
            <input
              type="range"
              min="1"
              max="3"
              step="1"
              value={val}
              oninput={(e) => setTraitValue(trait.key, parseInt(e.target.value))}
              class="w-full h-2 rounded-full appearance-none cursor-pointer"
              style="background: linear-gradient(to right, rgba(124,58,237,0.3) 0%, rgba(124,58,237,0.3) {pct}%, rgba(37,29,64,1) {pct}%, rgba(37,29,64,1) 100%);"
            />
            <div class="flex justify-between mt-2 text-[10px] text-white/30">
              <span>{trait.left}</span>
              <span class="text-primary-light font-medium text-xs">
                {levelLabels[val - 1]}
              </span>
              <span>{trait.right}</span>
            </div>
          </div>
        </div>
      {/each}

      <!-- Custom prompt -->
      <div class="glass p-6 rounded-2xl animate-slide-up" style="animation-delay: 0.4s;">
        <label class="block text-sm text-white/60 mb-2">Custom instruction (optional)</label>
        <p class="text-xs text-white/30 mb-3">Tell Daisy anything special about how you want her to behave</p>
        <textarea
          bind:value={customPrompt}
          placeholder="e.g. Never mention politics. Use Gen-Z slang sometimes."
          rows="3"
          class="w-full px-4 py-3 rounded-xl bg-surface-lighter border border-glass-border text-white placeholder-white/30 text-sm resize-none transition-all duration-300"
        ></textarea>
      </div>

      <!-- Save button -->
      <div class="pt-2 animate-slide-up" style="animation-delay: 0.5s;">
        <button
          onclick={handleSave}
          disabled={loading}
          class="w-full py-3.5 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold btn-glow hover:scale-[1.02] transition-all duration-300 disabled:opacity-50"
        >
          {#if loading}
            Saving...
          {:else if saved}
            ✓ Saved!
          {:else}
            Save Personality
          {/if}
        </button>
      </div>
    </div>
  </div>
</div>

<style>
  input[type="range"]::-webkit-slider-thumb {
    appearance: none;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #f472b6);
    cursor: pointer;
    border: 2px solid #0f0a1a;
    box-shadow: 0 0 10px rgba(124, 58, 237, 0.5);
    transition: transform 0.2s;
  }
  input[type="range"]::-webkit-slider-thumb:hover {
    transform: scale(1.2);
  }
  input[type="range"]::-moz-range-thumb {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #f472b6);
    cursor: pointer;
    border: 2px solid #0f0a1a;
    box-shadow: 0 0 10px rgba(124, 58, 237, 0.5);
  }
</style>
