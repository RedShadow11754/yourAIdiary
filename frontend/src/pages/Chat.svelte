<script>
  import { api } from '../lib/api.js';
  import { getAuth } from '../lib/stores.svelte.js';
  import { navigate } from '../lib/router.svelte.js';

  const auth = getAuth();

  $effect(() => {
    if (!auth.isAuthenticated) navigate('/login');
  });

  let messages = $state([]);
  let inputText = $state('');
  let loading = $state(false);
  let chatContainer;
  let historySidebar = $state(false);
  let chatHistory = $state([]);
  let viewingPast = $state(false);
  let viewingDate = $state('');

  // Load chat history on mount
  $effect(() => {
    if (auth.isAuthenticated) {
      loadHistory();
    }
  });

  async function loadHistory() {
    try {
      const data = await api.getChatHistory();
      chatHistory = data;
    } catch (e) {
      console.error('Failed to load history', e);
    }
  }

  function isToday(day) {
    const d = new Date(day + 'T00:00:00');
    const now = new Date();
    return d.getFullYear() === now.getFullYear() &&
           d.getMonth() === now.getMonth() &&
           d.getDate() === now.getDate();
  }

  function loadDayMessages(day) {
    const dayEntry = chatHistory.find(d => d.date === day);
    if (dayEntry) {
      messages = dayEntry.messages.map(m => ({
        role: m.role,
        content: m.content,
        time: m.time,
      }));
      viewingPast = !isToday(day);
      viewingDate = day;
      historySidebar = false;
      inputText = '';
      scrollToBottom();
    }
  }

  function goToToday() {
    messages = [];
    viewingPast = false;
    viewingDate = '';
    inputText = '';
  }

  async function sendMessage() {
    if (!inputText.trim() || loading) return;

    const userMsg = {
      role: 'user',
      content: inputText.trim(),
      time: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
    };
    messages = [...messages, userMsg];
    inputText = '';
    loading = true;
    scrollToBottom();

    try {
      const data = await api.sendMessage(userMsg.content);
      const aiMsg = {
        role: 'ai',
        content: data.reply,
        time: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
      };
      messages = [...messages, aiMsg];
      scrollToBottom();
    } catch (e) {
      messages = [...messages, {
        role: 'ai',
        content: 'Sorry, something went wrong. Try again in a moment.',
        time: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
      }];
    } finally {
      loading = false;
      loadHistory(); // refresh sidebar
    }
  }

  function scrollToBottom() {
    setTimeout(() => {
      if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }
    }, 50);
  }

  function handleKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  function formatDay(day) {
    const date = new Date(day + 'T00:00:00');
    const today = new Date();
    today.setHours(0,0,0,0);
    const diff = today - date;
    if (diff === 0) return 'Today';
    if (diff === 86400000) return 'Yesterday';
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }
</script>

<div class="flex h-screen pt-16">
  <!-- History sidebar -->
  <div class="hidden lg:flex flex-col w-72 border-r border-glass-border/30 bg-surface/80 backdrop-blur-xl">
    <div class="p-4 border-b border-glass-border/30">
      <h2 class="text-sm font-semibold text-white/70 uppercase tracking-wider">History</h2>
    </div>
    <div class="flex-1 overflow-y-auto p-2 space-y-1">
      {#each chatHistory as day}
        <button
          onclick={() => loadDayMessages(day.date)}
          class="w-full text-left px-3 py-2.5 rounded-xl hover:bg-primary/10 transition-all duration-200 group"
        >
          <div class="flex items-center gap-2">
            <span class="text-sm text-white/80 group-hover:text-white transition-colors">
              {formatDay(day.date)}
            </span>
            {#if isToday(day.date)}
              <span class="text-[10px] px-1.5 py-0.5 rounded-full bg-green-400/15 text-green-400 font-medium">Today</span>
            {:else}
              <span class="text-[10px] px-1.5 py-0.5 rounded-full bg-white/5 text-white/30">Read only</span>
            {/if}
          </div>
          <div class="text-xs text-white/40 mt-0.5 truncate">
            {day.messages.length} messages
          </div>
        </button>
      {/each}
      {#if chatHistory.length === 0}
        <p class="text-sm text-white/30 text-center mt-8">No conversations yet</p>
      {/if}
    </div>
  </div>

  <!-- Mobile history overlay -->
  {#if historySidebar}
    <div class="fixed inset-0 z-50 lg:hidden">
      <div class="absolute inset-0 bg-black/50" onclick={() => historySidebar = false}></div>
      <div class="absolute left-0 top-0 bottom-0 w-72 bg-surface border-r border-glass-border/30 animate-slide-left overflow-y-auto">
        <div class="p-4 border-b border-glass-border/30 flex items-center justify-between">
          <h2 class="text-sm font-semibold text-white/70 uppercase tracking-wider">History</h2>
          <button onclick={() => historySidebar = false} class="text-white/50 hover:text-white">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="p-2 space-y-1">
          {#each chatHistory as day}
            <button
              onclick={() => loadDayMessages(day.date)}
              class="w-full text-left px-3 py-2.5 rounded-xl hover:bg-primary/10 transition-all duration-200"
            >
              <div class="flex items-center gap-2">
                <span class="text-sm text-white/80">{formatDay(day.date)}</span>
                {#if isToday(day.date)}
                  <span class="text-[10px] px-1.5 py-0.5 rounded-full bg-green-400/15 text-green-400 font-medium">Today</span>
                {/if}
              </div>
              <div class="text-xs text-white/40 mt-0.5">{day.messages.length} messages</div>
            </button>
          {/each}
        </div>
      </div>
    </div>
  {/if}

  <!-- Chat area -->
  <div class="flex-1 flex flex-col min-w-0">
    <!-- Chat header -->
    <div class="flex items-center gap-3 px-4 py-3 border-b border-glass-border/30 bg-surface/50 backdrop-blur-xl">
      <button onclick={() => historySidebar = true} class="lg:hidden text-white/60 hover:text-white p-1">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
      <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white font-bold text-sm">
        D
      </div>
      <div class="flex-1">
        <h2 class="text-sm font-semibold text-white">Daisy</h2>
        {#if viewingPast}
          <p class="text-xs text-amber-400/80 flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
            Viewing {formatDay(viewingDate)} — Read only
          </p>
        {:else}
          <p class="text-xs text-green-400 flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"></span>
            Online
          </p>
        {/if}
      </div>
      {#if viewingPast}
        <button
          onclick={goToToday}
          class="px-3 py-1.5 rounded-lg text-xs font-medium text-primary-light bg-primary/10 hover:bg-primary/20 transition-all duration-200"
        >
          ← Back to Today
        </button>
      {/if}
    </div>

    <!-- Messages -->
    <div bind:this={chatContainer} class="flex-1 overflow-y-auto px-4 py-6 space-y-4">
      {#if messages.length === 0}
        <div class="flex flex-col items-center justify-center h-full text-center animate-fade">
          <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center text-3xl mb-4 animate-float">
            💬
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Start a conversation</h3>
          <p class="text-white/40 max-w-sm">Say anything! Daisy remembers your past chats and adapts to your mood.</p>
        </div>
      {/if}

      {#each messages as msg, i}
        <div class="flex {msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up" style="animation-delay: {Math.min(i * 0.05, 0.3)}s;">
          {#if msg.role !== 'user'}
            <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white font-bold text-xs mr-2 mt-1 shrink-0">
              D
            </div>
          {/if}
          <div class="max-w-[75%] group">
            <div class="px-4 py-2.5 rounded-2xl text-sm leading-relaxed
              {msg.role === 'user'
                ? 'bg-gradient-to-br from-primary to-primary-dark text-white rounded-br-sm'
                : 'bg-surface-lighter border border-glass-border/50 text-white/90 rounded-bl-sm'
              }"
            >
              {msg.content}
            </div>
            <div class="text-[10px] text-white/30 mt-1 {msg.role === 'user' ? 'text-right' : 'text-left'} px-1">
              {msg.time}
            </div>
          </div>
        </div>
      {/each}

      <!-- Typing indicator -->
      {#if loading}
        <div class="flex justify-start animate-fade">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white font-bold text-xs mr-2 mt-1 shrink-0">
            D
          </div>
          <div class="px-4 py-3 rounded-2xl rounded-bl-sm bg-surface-lighter border border-glass-border/50">
            <div class="flex gap-1.5">
              <div class="w-2 h-2 rounded-full bg-primary-light typing-dot"></div>
              <div class="w-2 h-2 rounded-full bg-primary-light typing-dot"></div>
              <div class="w-2 h-2 rounded-full bg-primary-light typing-dot"></div>
            </div>
          </div>
        </div>
      {/if}
    </div>

    <!-- Input -->
    <div class="px-4 py-3 border-t border-glass-border/30 bg-surface/50 backdrop-blur-xl">
      {#if viewingPast}
        <div class="flex items-center justify-center gap-2 py-2 text-sm text-white/40">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
          You can look back at your past, but you can't change it.
        </div>
      {:else}
        <div class="flex items-end gap-2 max-w-3xl mx-auto">
          <div class="flex-1 relative">
            <textarea
              bind:value={inputText}
              onkeydown={handleKeydown}
              placeholder="Type a message..."
              rows="1"
              class="w-full px-4 py-3 pr-12 rounded-2xl bg-surface-lighter border border-glass-border text-white text-sm placeholder-white/30 resize-none transition-all duration-300 focus:border-primary"
              style="min-height: 48px; max-height: 120px;"
            ></textarea>
          </div>
          <button
            onclick={sendMessage}
            disabled={!inputText.trim() || loading}
            class="w-12 h-12 rounded-xl bg-gradient-to-r from-primary to-accent text-white flex items-center justify-center shrink-0 hover:scale-105 transition-all duration-300 disabled:opacity-30 disabled:cursor-not-allowed btn-glow"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg>
          </button>
        </div>
      {/if}
    </div>
  </div>
</div>
