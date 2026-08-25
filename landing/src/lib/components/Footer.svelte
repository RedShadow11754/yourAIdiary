<script>
  let currentYear = new Date().getFullYear();

  const footerLinks = [
    {
      title: 'Product',
      links: [
        { label: 'Features', href: '#features' },
        { label: 'How It Works', href: '#how-it-works' },
        { label: 'Pricing', href: '#' },
        { label: 'Changelog', href: '#' },
      ],
    },
    {
      title: 'Company',
      links: [
        { label: 'About', href: '#' },
        { label: 'Blog', href: '#' },
        { label: 'Careers', href: '#' },
        { label: 'Contact', href: '#' },
      ],
    },
    {
      title: 'Support',
      links: [
        { label: 'Documentation', href: '#' },
        { label: 'FAQ', href: '#faq' },
        { label: 'Status', href: '#' },
        { label: 'Community', href: '#' },
      ],
    },
    {
      title: 'Legal',
      links: [
        { label: 'Privacy Policy', href: '#' },
        { label: 'Terms of Service', href: '#' },
        { label: 'Cookie Policy', href: '#' },
        { label: 'GDPR', href: '#' },
      ],
    },
  ];
</script>

<footer class="relative border-t border-white/5 bg-midnight-950/50">
  <div class="section-container py-16 md:py-20">
    <div class="grid grid-cols-2 md:grid-cols-5 gap-8 md:gap-12">
      <!-- Brand -->
      <div class="col-span-2 md:col-span-1">
        <a href="/" class="flex items-center gap-3 mb-6" onclick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }}>
          <div class="w-9 h-9 rounded-xl bg-gradient-primary flex items-center justify-center shadow-lg shadow-iris-500/20">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
          </div>
          <span class="font-display font-semibold text-lg">Mindful</span>
        </a>
        <p class="text-sm text-slate-500 leading-relaxed mb-6">
          Your AI companion that remembers. Private, intelligent, and personal — turning conversations into lasting memories.
        </p>
        <!-- Social Icons -->
        <div class="flex items-center gap-3">
          {#each ['twitter', 'github', 'discord'] as social}
            <a href="#" class="w-9 h-9 rounded-xl glass flex items-center justify-center text-slate-400 hover:text-white hover:border-iris-500/30 transition-all duration-300" aria-label={social}>
              {#if social === 'twitter'}
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                </svg>
              {:else if social === 'github'}
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                </svg>
              {:else}
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2v10z" />
                </svg>
              {/if}
            </a>
          {/each}
        </div>
      </div>

      <!-- Link Columns -->
      {#each footerLinks as group}
        <div>
          <h4 class="font-display text-sm font-semibold text-white mb-4">{group.title}</h4>
          <ul class="space-y-3">
            {#each group.links as link}
              <li>
                <a
                  href={link.href}
                  class="text-sm text-slate-500 hover:text-slate-300 transition-colors duration-200"
                >
                  {link.label}
                </a>
              </li>
            {/each}
          </ul>
        </div>
      {/each}
    </div>

    <!-- Bottom Bar -->
    <div class="mt-12 pt-8 border-t border-white/5 flex flex-col md:flex-row items-center justify-between gap-4">
      <p class="text-xs text-slate-600">
        &copy; {currentYear} Mindful. All rights reserved.
      </p>
      <p class="text-xs text-slate-600">
        Made with <span class="text-red-400">&#9829;</span> for the thoughtful minds.
      </p>
    </div>
  </div>
</footer>
