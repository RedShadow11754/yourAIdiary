// ── Daisy Diary Template Engine ──────────────────────────────
// 12 handcrafted printable diary designs. Each renders a fully
// self-contained HTML document (works offline, prints beautifully).

const MOOD_META = {
  happy: ['😊', 'Happy'], sad: ['🌧️', 'Sad'], angry: ['🔥', 'Angry'],
  anxious: ['🌀', 'Anxious'], excited: ['✨', 'Excited'], lonely: ['🌙', 'Lonely'],
  peaceful: ['🍃', 'Peaceful'], confused: ['🧭', 'Confused'], grateful: ['🤍', 'Grateful'],
  numb: ['🌫️', 'Numb'], hopeful: ['🌅', 'Hopeful'], frustrated: ['⚡', 'Frustrated'],
  melancholic: ['🍂', 'Melancholic'], content: ['☕', 'Content'],
  overwhelmed: ['🌊', 'Overwhelmed'], other: ['📖', 'Reflecting'],
};

function esc(s) {
  return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function paragraphs(content) {
  return String(content ?? '')
    .split(/\n{1,}/)
    .map((p) => p.trim())
    .filter(Boolean)
    .map((p) => `<p>${esc(p)}</p>`)
    .join('\n');
}

function prettyDate(dateStr) {
  const d = new Date(dateStr + (dateStr.length === 10 ? 'T12:00:00' : ''));
  if (isNaN(d)) return esc(dateStr);
  return d.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
}

const PRINT_HELPER = `
<div class="no-print" onclick="window.print()" style="position:fixed;bottom:24px;right:24px;z-index:99;cursor:pointer;font-family:Georgia,serif;padding:12px 22px;border-radius:999px;color:#fff;background:#7c3aed;box-shadow:0 8px 30px rgba(124,58,237,.5);font-size:14px;">🖨 Save as PDF</div>
`;

function doc(body, css, fonts = '') {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Daisy Diary</title>
${fonts ? `<link rel="preconnect" href="https://fonts.googleapis.com"><link href="${fonts}" rel="stylesheet">` : ''}
<style>
*{margin:0;padding:0;box-sizing:border-box;}
@media print{.no-print{display:none!important;}body{-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
${css}
</style>
</head>
<body>
${body}
${PRINT_HELPER}
</body>
</html>`;
}

/* ══════════════ TEMPLATES ══════════════ */

export const TEMPLATES = [
  {
    id: 'midnight-velvet',
    name: 'Midnight Velvet',
    desc: 'Deep navy & gold — for starlit thoughts',
    swatch: { bg: 'linear-gradient(150deg,#0d1025,#1a1f45)', accent: '#e8c97a', font: "'Cormorant Garamond',serif" },
  },
  {
    id: 'kraft-paper',
    name: 'Kraft Paper',
    desc: 'Warm craft paper with stitched edges',
    swatch: { bg: 'linear-gradient(150deg,#c9a87c,#b08d5f)', accent: '#5b4230', font: "'Caveat',cursive" },
  },
  {
    id: 'vintage-letter',
    name: 'Vintage Letter',
    desc: 'A sepia letter from a gentler time',
    swatch: { bg: 'linear-gradient(150deg,#f3e9d2,#e6d3b3)', accent: '#7a5c3e', font: "'Cormorant Garamond',serif" },
  },
  {
    id: 'botanical',
    name: 'Botanical',
    desc: 'Sage greens and quiet garden air',
    swatch: { bg: 'linear-gradient(150deg,#dde8dc,#b9cfba)', accent: '#3e5c40', font: "'Cormorant Garamond',serif" },
  },
  {
    id: 'minimal-white',
    name: 'Minimal White',
    desc: 'Clean lines. Nothing extra.',
    swatch: { bg: 'linear-gradient(150deg,#ffffff,#eceef2)', accent: '#111827', font: "'Inter',sans-serif" },
  },
  {
    id: 'aurora-glass',
    name: 'Aurora Glass',
    desc: "Daisy's signature night-glow look",
    swatch: { bg: 'linear-gradient(150deg,#171130,#2a1b52)', accent: '#c4b5fd', font: "'Sora',sans-serif" },
  },
  {
    id: 'sepia-journal',
    name: 'Sepia Journal',
    desc: 'Aged pages with ruled lines',
    swatch: { bg: 'linear-gradient(150deg,#efe0c8,#dcc9a5)', accent: '#6b4f2e', font: "'Caveat',cursive" },
  },
  {
    id: 'pastel-dream',
    name: 'Pastel Dream',
    desc: 'Soft pink & lavender clouds',
    swatch: { bg: 'linear-gradient(150deg,#fbe4ef,#e4dcfb)', accent: '#9d5c8f', font: "'Caveat',cursive" },
  },
  {
    id: 'editorial',
    name: 'The Editorial',
    desc: 'Your day, front-page news',
    swatch: { bg: 'linear-gradient(150deg,#fafaf7,#e8e6df)', accent: '#1a1a1a', font: "'Special Elite',monospace" },
  },
  {
    id: 'watercolor',
    name: 'Watercolor Bloom',
    desc: 'Painted washes of gentle color',
    swatch: { bg: 'linear-gradient(140deg,#cfe8f5,#f5d9ec 60%,#fdf3d8)', accent: '#48657a', font: "'Cormorant Garamond',serif" },
  },
  {
    id: 'noir-type',
    name: 'Noir Typewriter',
    desc: 'Charcoal pages, typewriter soul',
    swatch: { bg: 'linear-gradient(150deg,#232323,#161616)', accent: '#d4d4d4', font: "'Special Elite',monospace" },
  },
  {
    id: 'sunrise',
    name: 'Sunrise',
    desc: 'Peach dawn for hopeful days',
    swatch: { bg: 'linear-gradient(150deg,#ffe3c2,#ffb99e)', accent: '#8a4b2f', font: "'Sora',sans-serif" },
  },
];

/* ── Per-template renderers ── */

function midnightVelvet(e) {
  const [emo, mood] = MOOD_META[e.mood] || MOOD_META.other;
  return doc(
    `<main><header><div class="orn">✦ ✦ ✦</div><h1>${prettyDate(e.date)}</h1>
     <div class="mood">${emo} ${mood}</div></header><article>${paragraphs(e.content)}</article>
     <footer>— written with Daisy 🌼 —</footer></main>`,
    `body{background:#0d1025;color:#e6e2d6;font-family:'Cormorant Garamond',Georgia,serif;display:flex;justify-content:center;padding:70px 20px;
     background-image:radial-gradient(circle at 80% 10%,rgba(232,201,122,.07),transparent 40%),radial-gradient(circle at 15% 85%,rgba(120,120,220,.06),transparent 45%);}
     main{max-width:640px;width:100%;border:1px solid rgba(232,201,122,.35);outline:1px solid rgba(232,201,122,.15);outline-offset:6px;padding:56px 52px;background:rgba(255,255,255,.015);}
     header{text-align:center;margin-bottom:44px;}
     .orn{color:#e8c97a;letter-spacing:14px;font-size:13px;margin-bottom:18px;}
     h1{font-weight:500;font-size:30px;color:#e8c97a;letter-spacing:1px;}
     .mood{margin-top:14px;font-size:15px;color:#b9b39f;font-style:italic;}
     article p{font-size:19px;line-height:1.95;margin-bottom:22px;text-align:justify;}
     article p:first-child::first-letter{font-size:52px;float:left;line-height:.9;padding-right:10px;color:#e8c97a;}
     footer{text-align:center;margin-top:50px;color:#7d7867;font-style:italic;font-size:15px;}`
  );
}

function kraftPaper(e) {
  const [emo, mood] = MOOD_META[e.mood] || MOOD_META.other;
  return doc(
    `<main><div class="tape"></div><h1>Dear Diary,</h1>
     <div class="meta">${prettyDate(e.date)} · feeling ${mood.toLowerCase()} ${emo}</div>
     <article>${paragraphs(e.content)}</article>
     <div class="sign">— ${mood} day</div></main>`,
    `body{background:#a98d68;font-family:'Caveat',cursive;display:flex;justify-content:center;padding:60px 16px;
     background-image:repeating-linear-gradient(45deg,rgba(0,0,0,.02) 0 2px,transparent 2px 4px);}
     main{position:relative;max-width:620px;width:100%;background:#c9a87c;padding:58px 46px 46px;color:#4a3421;
     box-shadow:0 20px 60px rgba(60,40,15,.35);border-radius:4px;}
     main::before{content:'';position:absolute;inset:10px;border:2px dashed rgba(90,66,48,.5);pointer-events:none;border-radius:2px;}
     .tape{position:absolute;top:-14px;left:50%;transform:translateX(-50%) rotate(-2deg);width:130px;height:32px;background:rgba(240,230,210,.75);box-shadow:0 2px 8px rgba(0,0,0,.15);}
     h1{font-size:44px;margin-bottom:4px;}
     .meta{font-family:Inter,sans-serif;font-size:13px;color:#6d5540;margin-bottom:30px;}
     article p{font-size:25px;line-height:1.65;margin-bottom:18px;}
     .sign{font-size:28px;text-align:right;margin-top:26px;color:#5b4230;}`
  );
}

function vintageLetter(e) {
  const [emo, mood] = MOOD_META[e.mood] || MOOD_META.other;
  return doc(
    `<main><div class="salutation">My dearest diary,</div>
     <article>${paragraphs(e.content)}</article>
     <div class="close">Yours truly,<br><span class="sig">me, on a ${mood.toLowerCase()} day ${emo}</span></div>
     <div class="post">Penned ${prettyDate(e.date)} · with Daisy</div></main>`,
    `body{background:#efe6d0;font-family:'Cormorant Garamond',Georgia,serif;color:#4d3a26;display:flex;justify-content:center;padding:60px 16px;
     background-image:radial-gradient(ellipse at 50% -10%,rgba(122,92,62,.12),transparent 55%),radial-gradient(ellipse at 50% 110%,rgba(122,92,62,.1),transparent 55%);}
     main{max-width:600px;width:100%;background:linear-gradient(#f6eed9,#efe3c8);padding:64px 56px;box-shadow:0 14px 50px rgba(90,70,40,.3);position:relative;}
     main::after{content:'';position:absolute;inset:12px;border:1px solid rgba(122,92,62,.35);pointer-events:none;}
     .salutation{font-style:italic;font-size:30px;margin-bottom:30px;}
     article p{font-size:20px;line-height:1.9;margin-bottom:20px;}
     .close{margin-top:36px;font-size:21px;font-style:italic;}
     .sig{font-size:26px;color:#7a5c3e;}
     .post{margin-top:34px;font-size:14px;color:#8a7050;letter-spacing:2px;text-transform:uppercase;text-align:center;}`
  );
}

function botanical(e) {
  const [emo, mood] = MOOD_META[e.mood] || MOOD_META.other;
  return doc(
    `<svg class="leaf l1" viewBox="0 0 100 100" fill="none"><path d="M50 5 C80 30 80 70 50 95 C20 70 20 30 50 5Z" stroke="#5d7d5f" stroke-width="2"/><path d="M50 12 V88 M50 35 L32 22 M50 35 L68 22 M50 60 L30 45 M50 60 L70 45" stroke="#5d7d5f" stroke-width="1.5"/></svg>
     <svg class="leaf l2" viewBox="0 0 100 100" fill="none"><path d="M50 5 C80 30 80 70 50 95 C20 70 20 30 50 5Z" stroke="#5d7d5f" stroke-width="2"/></svg>
     <main><span class="chip">${emo} ${mood}</span><h1>${prettyDate(e.date)}</h1>
     <article>${paragraphs(e.content)}</article>
     <footer>grown with care · Daisy 🌿</footer></main>`,
    `body{background:linear-gradient(#e7eee5,#d3e0d1);font-family:'Cormorant Garamond',Georgia,serif;color:#33473a;display:flex;justify-content:center;padding:70px 16px;}
     .leaf{position:fixed;width:150px;opacity:.5;} .l1{top:36px;left:36px;} .l2{bottom:36px;right:36px;transform:rotate(160deg);}
     main{max-width:600px;width:100%;background:rgba(255,255,255,.72);backdrop-filter:blur(4px);padding:56px 52px;border-radius:18px;box-shadow:0 16px 50px rgba(60,90,60,.18);}
     .chip{display:inline-block;font-family:Inter,sans-serif;font-size:13px;background:#dde8dc;color:#3e5c40;padding:6px 16px;border-radius:999px;margin-bottom:16px;}
     h1{font-size:29px;font-weight:500;margin-bottom:34px;padding-bottom:18px;border-bottom:1px solid #b9cfba;}
     article p{font-size:19px;line-height:1.95;margin-bottom:20px;}
     footer{margin-top:40px;text-align:center;font-style:italic;color:#5d7d5f;font-size:16px;}`
  );
}

function minimalWhite(e) {
  const [emo, mood] = MOOD_META[e.mood] || MOOD_META.other;
  return doc(
    `<main><header><span class="kicker">Diary entry</span><h1>${prettyDate(e.date)}</h1>
     <div class="sub">Mood · ${mood}</div></header><article>${paragraphs(e.content)}</article>
     <footer><span class="dot"></span> Daisy</footer></main>`,
    `body{background:#fff;color:#111827;font-family:Inter,-apple-system,sans-serif;display:flex;justify-content:center;padding:80px 20px;}
     main{max-width:560px;width:100%;}
     .kicker{font-size:12px;letter-spacing:4px;text-transform:uppercase;color:#9ca3af;}
     h1{font-size:32px;font-weight:700;margin:10px 0 6px;letter-spacing:-.5px;}
     .sub{font-size:14px;color:#6b7280;margin-bottom:44px;padding-bottom:24px;border-bottom:1px solid #e5e7eb;}
     article p{font-size:17px;line-height:1.9;margin-bottom:22px;color:#374151;}
     footer{margin-top:48px;display:flex;align-items:center;gap:8px;font-size:13px;color:#9ca3af;}
     .dot{width:6px;height:6px;border-radius:99px;background:#8b5cf6;}`
  );
}

function auroraGlass(e) {
  const [emo, mood] = MOOD_META[e.mood] || MOOD_META.other;
  return doc(
    `<main><div class="orb">🌼</div><h1>${prettyDate(e.date)}</h1>
     <div class="mood">${emo} ${mood}</div><article>${paragraphs(e.content)}</article>
     <footer>written with Daisy</footer></main>`,
    `body{min-height:100vh;background:#0b0918;color:#ece8fa;font-family:Sora,sans-serif;display:flex;justify-content:center;align-items:flex-start;padding:70px 16px;
     background-image:radial-gradient(ellipse 60% 40% at 20% 0%,rgba(139,92,246,.22),transparent),radial-gradient(ellipse 50% 35% at 85% 20%,rgba(217,70,239,.14),transparent),radial-gradient(ellipse 55% 40% at 60% 100%,rgba(34,211,238,.1),transparent);}
     main{max-width:620px;width:100%;background:rgba(255,255,255,.045);border:1px solid rgba(196,181,253,.2);border-radius:26px;padding:56px 50px;backdrop-filter:blur(20px);box-shadow:0 30px 80px -20px rgba(124,58,237,.4);}
     .orb{width:54px;height:54px;border-radius:99px;background:linear-gradient(135deg,#7c3aed,#d946ef);display:grid;place-items:center;font-size:24px;margin-bottom:24px;box-shadow:0 0 40px rgba(168,85,247,.5);}
     h1{font-size:24px;font-weight:600;}
     .mood{margin:10px 0 34px;color:#c4b5fd;font-size:15px;}
     article p{font-size:16.5px;line-height:1.95;margin-bottom:20px;color:#d8d3ee;}
     footer{margin-top:38px;color:#6e6693;font-size:13px;letter-spacing:2px;text-transform:uppercase;}`,
    'https://fonts.googleapis.com/css2?family=Sora:wght@400;600&display=swap'
  );
}

function sepiaJournal(e) {
  const [emo, mood] = MOOD_META[e.mood] || MOOD_META.other;
  return doc(
    `<main><div class="head"><span class="date">${prettyDate(e.date)}</span><span class="moodline">${emo} ${mood}</span></div>
     <article>${paragraphs(e.content)}</article></main>`,
    `body{background:#2b2118;font-family:'Caveat',cursive;display:flex;justify-content:center;padding:50px 14px;}
     main{max-width:600px;width:100%;background:linear-gradient(#efe0c8,#e2cda6);color:#4a3826;padding:52px 48px;box-shadow:inset 0 0 80px rgba(107,79,46,.35),0 20px 60px rgba(0,0,0,.5);
     background-image:repeating-linear-gradient(transparent 0 37px,rgba(107,79,46,.25) 37px 38px);}
     .head{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px;border-bottom:2px solid rgba(107,79,46,.5);padding-bottom:12px;margin-bottom:30px;}
     .date{font-size:27px;}
     .moodline{font-size:22px;color:#6b4f2e;}
     article p{font-size:24px;line-height:38px;margin-bottom:0;}
     @media print{body{background:#fff}}`
  );
}

function pastelDream(e) {
  const [emo, mood] = MOOD_META[e.mood] || MOOD_META.other;
  return doc(
    `<main><div class="cloud c1"></div><div class="cloud c2"></div>
     <span class="pill">${emo} ${mood}</span><h1>${prettyDate(e.date)}</h1>
     <article>${paragraphs(e.content)}</article>
     <footer>sweet dreams, written by Daisy 🎀</footer></main>`,
    `body{background:linear-gradient(135deg,#fbe4ef,#e4dcfb 55%,#dcebfa);font-family:'Caveat',cursive;color:#6d4a67;display:flex;justify-content:center;padding:70px 16px;}
     main{position:relative;overflow:hidden;max-width:600px;width:100%;background:rgba(255,255,255,.65);backdrop-filter:blur(8px);border-radius:30px;padding:58px 52px;box-shadow:0 20px 60px rgba(180,140,190,.3);border:1px solid rgba(255,255,255,.8);}
     .cloud{position:absolute;border-radius:99px;filter:blur(40px);opacity:.55;} .c1{width:220px;height:220px;background:#f9c6dd;top:-70px;right:-60px;} .c2{width:260px;height:260px;background:#cabdf5;bottom:-90px;left:-80px;}
     .pill{position:relative;display:inline-block;font-family:Inter,sans-serif;font-size:13px;background:#fff;color:#9d5c8f;padding:6px 18px;border-radius:999px;box-shadow:0 4px 14px rgba(157,92,143,.25);}
     h1{position:relative;font-size:42px;margin:14px 0 28px;}
     article{position:relative;} article p{font-size:25px;line-height:1.7;margin-bottom:18px;}
     footer{position:relative;margin-top:32px;text-align:center;font-size:22px;color:#9d5c8f;}`
  );
}

function editorial(e) {
  const [emo, mood] = MOOD_META[e.mood] || MOOD_META.other;
  return doc(
    `<main><div class="masthead">THE DAILY REFLECTION</div>
     <div class="rule"></div>
     <div class="dateline">${prettyDate(e.date).toUpperCase()} · MOOD DESK: ${mood.toUpperCase()} ${emo} · PRICE: ONE HONEST THOUGHT</div>
     <div class="rule thick"></div>
     <h1>A Day Worth Remembering</h1>
     <article>${paragraphs(e.content)}</article>
     <div class="colophon">Set in type by Daisy · All rights reserved by your heart</div></main>`,
    `body{background:#fafaf7;color:#1a1a1a;font-family:'Special Elite',Courier,monospace;display:flex;justify-content:center;padding:50px 16px;}
     main{max-width:640px;width:100%;background:#fff;padding:44px 40px;box-shadow:0 10px 40px rgba(0,0,0,.12);}
     .masthead{text-align:center;font-size:30px;letter-spacing:4px;}
     .rule{border-top:3px double #1a1a1a;margin:10px 0;} .rule.thick{border-top:1px solid #1a1a1a;}
     .dateline{text-align:center;font-size:11px;padding:6px 0;border-top:1px solid #1a1a1a;border-bottom:1px solid #1a1a1a;letter-spacing:1px;}
     h1{text-align:center;font-size:34px;margin:26px 0;}
     article{column-count:1;column-gap:34px;} @media(min-width:720px){article{column-count:2;}}
     article p{font-size:15px;line-height:1.8;margin-bottom:16px;text-align:justify;hyphens:auto;}
     article p::first-letter{font-size:30px;font-weight:bold;}
     .colophon{margin-top:26px;text-align:center;font-size:11px;border-top:1px solid #1a1a1a;padding-top:10px;letter-spacing:2px;}`
  );
}

function watercolor(e) {
  const [emo, mood] = MOOD_META[e.mood] || MOOD_META.other;
  return doc(
    `<main><div class="wash w1"></div><div class="wash w2"></div><div class="wash w3"></div>
     <div class="inner"><span class="moodtag">${emo} ${mood}</span><h1>${prettyDate(e.date)}</h1>
     <article>${paragraphs(e.content)}</article>
     <footer>painted from memory · Daisy 🎨</footer></div></main>`,
    `body{background:#fdfcf8;font-family:'Cormorant Garamond',Georgia,serif;color:#3f5464;display:flex;justify-content:center;padding:70px 16px;}
     main{position:relative;max-width:620px;width:100%;}
     .wash{position:absolute;border-radius:50%;filter:blur(50px);opacity:.5;}
     .w1{width:300px;height:300px;background:#bcdcef;top:-60px;left:-60px;}
     .w2{width:280px;height:280px;background:#f2c7e3;top:20%;right:-70px;}
     .w3{width:320px;height:320px;background:#faedbc;bottom:-80px;left:10%;}
     .inner{position:relative;background:rgba(255,255,255,.55);backdrop-filter:blur(6px);border-radius:24px;padding:58px 52px;box-shadow:0 18px 60px rgba(120,150,170,.25);}
     .moodtag{display:inline-block;font-family:Inter,sans-serif;font-size:13px;color:#48657a;background:rgba(255,255,255,.8);padding:6px 16px;border-radius:999px;}
     h1{font-size:30px;font-weight:500;margin:14px 0 30px;color:#48657a;}
     article p{font-size:20px;line-height:1.9;margin-bottom:20px;}
     footer{margin-top:36px;text-align:center;font-style:italic;color:#7a93a5;}`
  );
}

function noirType(e) {
  const [emo, mood] = MOOD_META[e.mood] || MOOD_META.other;
  return doc(
    `<main><div class="bar">ENTRY Nº ${esc(String(e.id ?? '')) || '—'} // CLASSIFICATION: PERSONAL</div>
     <h1>> ${prettyDate(e.date)}</h1>
     <div class="status">STATUS: LOGGED · MOOD: ${mood.toUpperCase()} ${emo}</div>
     <hr>
     <article>${paragraphs(e.content)}</article>
     <div class="end">// END OF ENTRY — DAISY v1.0_</div></main>`,
    `body{background:#161616;color:#d4d4d4;font-family:'Special Elite',Courier,monospace;display:flex;justify-content:center;padding:60px 16px;}
     main{max-width:600px;width:100%;background:#1f1f1f;border:1px solid #3a3a3a;padding:46px 44px;box-shadow:0 0 60px rgba(0,0,0,.6);}
     .bar{font-size:11px;letter-spacing:2px;color:#888;border:1px dashed #444;padding:8px 12px;margin-bottom:26px;}
     h1{font-size:21px;color:#eee;font-weight:normal;}
     .status{font-size:12px;color:#777;margin:8px 0 18px;}
     hr{border:none;border-top:1px solid #3a3a3a;margin-bottom:24px;}
     article p{font-size:15.5px;line-height:1.9;margin-bottom:18px;color:#ccc;}
     .end{margin-top:30px;color:#666;font-size:12px;animation:none;}`
  );
}

function sunrise(e) {
  const [emo, mood] = MOOD_META[e.mood] || MOOD_META.other;
  return doc(
    `<main><div class="sun"></div><h1>${prettyDate(e.date)}</h1>
     <div class="mood">${emo} ${mood} — a new page</div><article>${paragraphs(e.content)}</article>
     <footer>every sunrise is a blank page · Daisy ☀️</footer></main>`,
    `body{background:linear-gradient(160deg,#fff7ec,#ffe3c2 45%,#ffc3ad);font-family:Sora,sans-serif;color:#6b3a26;display:flex;justify-content:center;padding:70px 16px;}
     main{max-width:600px;width:100%;background:rgba(255,255,255,.7);backdrop-filter:blur(8px);border-radius:26px;padding:56px 50px;box-shadow:0 20px 60px rgba(200,120,80,.28);}
     .sun{width:64px;height:64px;border-radius:99px;background:radial-gradient(circle at 35% 35%,#fff3d6,#ffb36b);box-shadow:0 0 50px rgba(255,170,90,.8);margin-bottom:26px;}
     h1{font-size:26px;font-weight:700;color:#7c4527;}
     .mood{margin:10px 0 32px;font-size:15px;color:#a05f3d;}
     article p{font-size:16.5px;line-height:1.95;margin-bottom:20px;color:#5f3a28;}
     footer{margin-top:38px;text-align:center;font-size:13.5px;color:#a05f3d;}`
  );
}

const RENDERERS = {
  'midnight-velvet': midnightVelvet,
  'kraft-paper': kraftPaper,
  'vintage-letter': vintageLetter,
  botanical,
  'minimal-white': minimalWhite,
  'aurora-glass': auroraGlass,
  'sepia-journal': sepiaJournal,
  'pastel-dream': pastelDream,
  editorial,
  watercolor,
  'noir-type': noirType,
  sunrise,
};

/** Render an entry as a complete standalone HTML string */
export function renderTemplate(entry, templateId) {
  const fn = RENDERERS[templateId] || auroraGlass;
  return fn(entry);
}

/** Download an entry as a self-contained .html file */
export function downloadDiaryHTML(entry, templateId) {
  const html = renderTemplate(entry, templateId);
  const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `daisy-diary-${entry.date}.html`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
}

/** Open the rendered diary in a new tab with a print helper button */
export function openPrintView(entry, templateId) {
  const html = renderTemplate(entry, templateId);
  const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  window.open(url, '_blank');
  setTimeout(() => URL.revokeObjectURL(url), 60000);
}
