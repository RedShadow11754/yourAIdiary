<script>
  let { size = 36, glow = true } = $props();
</script>

<span
  class="relative inline-flex items-center justify-center rounded-full"
  style="width:{size}px;height:{size}px;"
>
  {#if glow}
    <span
      class="absolute inset-0 rounded-full animate-breathe"
      style="background: radial-gradient(circle, rgba(167,139,250,0.5), transparent 70%); filter: blur(6px);"
    ></span>
  {/if}
  <svg viewBox="0 0 100 100" width={size} height={size} class="relative">
    <defs>
      <radialGradient id="orb" cx="35%" cy="30%" r="80%">
        <stop offset="0%" stop-color="#e9d5ff" />
        <stop offset="45%" stop-color="#8b5cf6" />
        <stop offset="100%" stop-color="#312e81" />
      </radialGradient>
    </defs>
    <circle cx="50" cy="50" r="44" fill="url(#orb)" />
    <!-- petals -->
    <g fill="#f5f3ff" opacity="0.95">
      <ellipse cx="50" cy="22" rx="9" ry="14" />
      <ellipse cx="50" cy="78" rx="9" ry="14" />
      <ellipse cx="22" cy="50" rx="14" ry="9" />
      <ellipse cx="78" cy="50" rx="14" ry="9" />
    </g>
    <circle cx="50" cy="50" r="13" fill="#fdf4ff" />
    <circle cx="46" cy="46" r="4" fill="#c084fc" opacity="0.7" />
  </svg>
</span>
