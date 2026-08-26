<script>
  import Logo from '../lib/components/Logo.svelte';
  import { api } from '../lib/api.js';
  import { getAuth, toast } from '../lib/stores.svelte.js';
  import { navigate } from '../lib/router.svelte.js';

  const auth = getAuth();

  let days = $state([]); // [{date, messages:[{role,content,time}]}]
  let selectedDay = $state(null);
  let messages = $state([]);
  let draft = $state('');
  let sending = $state(false);
  let loadingHistory = $state(true);
  let showRail = $state(false); // mobile drawer
  let scroller;
  let textarea;

  const SUGGESTIONS = [
    "Hi Daisy! I'm new here 👋",
    'I had a weird day today…',
    'Help me plan my week',
    'I just need to vent about something',
  ];

  function fmtDayLabel(dateStr) {
    const d = new Date(dateStr + 'T12:00:00');
    const today = new Date();
    const yesterday = new Date();
    yesterday.setDate(today.getDate() - 1);
    if (dateStr === today.toISOString().slice(0, 10)) return 'Today';
    if (dateStr === yesterday.toISOString().slice(0, 10)) return 'Yesterday';
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }

  function fmtDaySub(dateStr) {
    return new Date(dateStr + 'T12:00:00').toLocaleDateString('en-US', {
      month: 'long', day: 'numeric', year: 'numeric',
    });
  }

  async function loadHistory(keepSelection = false) {
    loadingHistory = true;
    try {
      const history = await api.getChatHistory();
      days = Array.isArray(history) ? history : [];
      if (keepSelection && selectedDay) {
        selectDay(selectedDay);
      } else if (days.length > 0) {
        selectDay(days[0].date);
      }
    } catch {
      // first-time user or network issue — start fresh
      days = [];
    } finally {
      loadingHistory = false;
    }
  }

  function selectDay(date) {
    const day = days.find((d) => d.date === date);
    selectedDay = date;
    messages = day ? [...day.messages] : [];
    scrollToBottom(true);
  }

  function scrollToBottom(instant = false) {
    requestAnimationFrame(() => {
      scroller?.scrollTo({ top: scroller.scrollHeight, behavior: instant ? 'auto' : 'smooth' });
    });
  }

  async function send(text) {
    const msg = (text ?? draft).trim();
    if (!msg || sending) return;

    draft = '';
    resizeTextarea();
    messages.push({ role: 'user', content: msg, time: nowTime() });
    messages = [...messages];
    sending = true;
    scrollToBottom();

    try {
      const res = await api.sendMessage(msg);
      messages.push({ role: 'ai', content: res.reply, time: nowTime() });
      messages = [...messages];
      loadHistory(true);
    } catch (err) {
      toast(err?.error || 'Daisy could not reply — check your connection', 'error');
    } finally {
      sending = false;
      scrollToBottom();
      textarea?.focus();
    }
  }

  function nowTime() {
    return new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
  }

  function resizeTextarea() {
    if (!textarea) return;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 160) + 'px';
  }

  function onKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }

  // Welcome banner for brand-new users
  let isNewUser = typeof window !== 'undefined' && sessionStorage.getItem('daisy_welcome') === 'new';

  $effect(() => {
    loadHistory();
    textarea?.focus();
  });
</script>

<div class="max-w-6xl mx-auto px-4 sm:px-6 h-[calc(100vh-4rem)] flex flex-col">
  <!-- Mobile day-rail toggle -->
  <div class="md:hidden flex items-center gap-3 py-3">
    <button class="btn-ghost px-4 py-2 text-xs" onclick={() => (showRail = !showRail)}>
      🗂 Past conversations ({days.length})
    </button>
    {#if selectedDay}
      <span class="text-sm text-[var(--color-ink-dim)]">{fmtDayLabel(selectedDay)}</span>
    {/if}
  </div>

  <div class="flex flex-1 min-h-0 gap-5 pb-4">
    <!-- ── History rail ── -->
    <aside
      class="{showRail ? 'fixed inset-y-16 left-0 w-72 z-40 p-4 glass-strong overflow-y-auto rounded-r-3xl' : 'hidden'}
        md:relative md:flex md:flex-col md:w-64 md:p-0 md:bg-transparent md:overflow-hidden shrink-0"
    >
      <h2 class="font-display text-sm font-semibold tracking-widest uppercase text-[var(--color-ink-faint)] mb-3 hidden md:block">
        Conversations
      </h2>

      <div class="flex-1 overflow-y-auto space-y-2 no-scrollbar">
        {#if loadingHistory}
          {#each [1, 2, 3] as i}
            <div class="glass rounded-xl h-14 animate-pulse"></div>
          {/each}
        {:else if days.length === 0}
          <p class="text-sm text-[var(--color-ink-faint)] leading-relaxed px-1">
            No conversations yet.<br />Say hi to Daisy — she'll remember it. 🌼
          </p>
        {:else}
          {#each days as d (d.date)}
            <button
              onclick={() => { selectDay(d.date); showRail = false; }}
              class="w-full text-left px-4 py-3 rounded-xl transition-all duration-200 cursor-pointer group
                {selectedDay === d.date ? 'glass-strong shadow-[inset_0_0_0_1px_rgba(196,181,253,.3)]' : 'hover:bg-white/5'}"
            >
              <div class="flex items-center justify-between">
                <span class="font-medium text-sm {selectedDay === d.date ? 'text-white' : 'text-[var(--color-ink-dim)] group-hover:text-white'}">
                  {fmtDayLabel(d.date)}
                </span>
                <span class="text-[11px] text-[var(--color-ink-faint)]">{d.messages.length} msgs</span>
              </div>
              <div class="text-xs text-[var(--color-ink-faint)] mt-0.5 truncate">
                {d.messages[d.messages.length - 1]?.content.slice(0, 40)}…
              </div>
            </button>
          {/each}
        {/if}
      </div>

      <a href="#/diary" class="btn-ghost w-full py-3 text-sm mt-4 hidden md:inline-flex">
        📖 My diary
      </a>
    </aside>

    <!-- Click-away for mobile drawer -->
    {#if showRail}
      <button class="fixed inset-0 z-30 bg-black/50 cursor-default" aria-label="Close conversations" tabindex="-1" onclick={() => (showRail = false)}></button>
    {/if}

    <!-- ── Chat panel ── -->
    <section class="flex-1 min-w-0 glass rounded-3xl flex flex-col overflow-hidden">
      <!-- Header -->
      <header class="flex items-center gap-3 px-5 py-4 border-b border-white/8 shrink-0">
        <Logo size={38} />
        <div>
          <h1 class="font-display font-semibold">Daisy</h1>
          <p class="text-xs text-[var(--color-ink-dim)] flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse inline-block"></span>
            always here · remembers you
          </p>
        </div>
        <a href="#/personality" class="ml-auto btn-ghost px-4 py-2 text-xs">🎭 Tune personality</a>
      </header>

      <!-- Messages -->
      <div bind:this={scroller} class="flex-1 overflow-y-auto px-5 py-6 space-y-5">
        {#if isNewUser && !loadingHistory}
          <div class="text-center max-w-md mx-auto pt-6 animate-rise">
            <Logo size={64} />
            <h2 class="font-display text-2xl font-bold mt-5">
              Hi{auth.user?.email ? `, ${auth.user.email.split('@')[0]}` : ''} — I'm Daisy 🌼
            </h2>
            <p class="text-[var(--color-ink-dim)] leading-relaxed mt-3">
              I'm your friend, not an assistant. Talk to me like a person — I'll remember the things that matter,
              and every night I'll write your day into your diary.
            </p>
          </div>
          <div class="flex flex-wrap gap-2 justify-center pb-2 animate-fade">
            {#each SUGGESTIONS as s}
              <button class="btn-ghost px-4 py-2 text-[13px]" onclick={() => send(s)}>{s}</button>
            {/each}
          </div>
        {:else if selectedDay}
          <div class="text-center mb-2">
            <span class="inline-block glass rounded-full px-4 py-1.5 text-xs text-[var(--color-ink-dim)]">
              {fmtDaySub(selectedDay)}
            </span>
          </div>
        {/if}

        {#each messages as m, i}
          <div class="flex items-end gap-2.5 {m.role === 'user' ? 'flex-row-reverse' : ''}" style="animation: pop .4s cubic-bezier(.34,1.56,.64,1) both; animation-delay: {Math.min(i * 0.03, 0.3)}s">
            {#if m.role === 'ai'}
              <Logo size={30} />
            {:else}
              <span class="w-7 h-7 shrink-0 rounded-full grid place-items-center text-xs font-bold" style="background:linear-gradient(135deg,#f472b6,#fb7185)">
                {(auth.user?.email || 'Y')[0].toUpperCase()}
              </span>
            {/if}
            <div
              class="max-w-[75%] px-4 py-3 text-[15px] leading-relaxed whitespace-pre-wrap break-words
                {m.role === 'user'
                  ? 'rounded-3xl rounded-br-md text-white'
                  : 'glass rounded-3xl rounded-bl-md'}"
              style={m.role === 'user' ? 'background:linear-gradient(120deg,#7c3aed,#a855f7)' : ''}
            >
              {m.content}
            </div>
            <span class="text-[10px] text-[var(--color-ink-faint)] mb-1">{m.time}</span>
          </div>
        {/each}

        {#if sending}
          <div class="flex items-end gap-2.5 animate-fade">
            <Logo size={30} />
            <div class="glass rounded-3xl rounded-bl-md px-5 py-4 flex items-center gap-1.5">
              <span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>
            </div>
          </div>
        {/if}

        {#if !sending && messages.length > 0}
          <div class="text-center pt-1">
            <button class="text-xs text-[var(--color-ink-faint)] hover:text-white transition-colors cursor-pointer" onclick={() => textarea?.focus()}>
              ✎ Reply to Daisy…
            </button>
          </div>
        {/if}
      </div>

      <!-- Composer -->
      <footer class="p-4 border-t border-white/8 shrink-0">
        <div class="glass-strong rounded-3xl flex items-end gap-2 p-2 pl-5 focus-within:border-[rgba(167,139,250,.6)] focus-within:shadow-[0_0_25px_-8px_rgba(139,92,246,.6)] transition-all duration-300">
          <textarea
            bind:this={textarea}
            bind:value={draft}
            oninput={resizeTextarea}
            onkeydown={onKeydown}
            rows="1"
            placeholder="Tell Daisy anything… (Enter to send)"
            class="flex-1 bg-transparent border-none outline-none resize-none py-3 text-[15px] leading-relaxed placeholder:text-[var(--color-ink-faint)] max-h-40"
          ></textarea>
          <button
            class="btn-primary w-11 h-11 !rounded-full shrink-0 grid place-items-center {!draft.trim() || sending ? 'opacity-50 !cursor-not-allowed' : ''}"
            disabled={!draft.trim() || sending}
            onclick={() => send()}
            aria-label="Send message"
          >
            {#if sending}
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" class="animate-spin"><path d="M21 12a9 9 0 1 1-6.22-8.56"/></svg>
            {:else}
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
            {/if}
          </button>
        </div>
        <p class="text-center text-[11px] text-[var(--color-ink-faint)] mt-2.5">
          Daisy remembers what matters — but she's an AI, be kind to yourself 💜
        </p>
      </footer>
    </section>
  </div>
</div>
