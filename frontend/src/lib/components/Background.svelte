<script>
  // Live aurora canvas — drifting light blobs + parallax starfield
  let canvas;
  let mouse = { x: 0.5, y: 0.5 };
  let raf;

  const BLOBS = [
    { hue: [139, 92, 246], r: 0.55, cx: 0.2, cy: 0.25, speed: 0.00016, phase: 0 },
    { hue: [217, 70, 239], r: 0.45, cx: 0.8, cy: 0.15, speed: 0.00012, phase: 2.1 },
    { hue: [34, 211, 238], r: 0.4, cx: 0.65, cy: 0.75, speed: 0.00019, phase: 4.4 },
    { hue: [244, 114, 182], r: 0.35, cx: 0.3, cy: 0.85, speed: 0.00014, phase: 5.6 },
    { hue: [99, 102, 241], r: 0.5, cx: 0.5, cy: 0.5, speed: 0.0001, phase: 1.2 },
  ];

  let stars = [];

  function seedStars(w, h) {
    const count = Math.min(160, Math.floor((w * h) / 14000));
    stars = Array.from({ length: count }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      r: Math.random() * 1.4 + 0.3,
      tw: Math.random() * Math.PI * 2,
      twSpeed: 0.4 + Math.random() * 1.2,
      depth: 0.3 + Math.random() * 0.7,
    }));
  }

  function resize() {
    if (!canvas) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = window.innerWidth * dpr;
    canvas.height = window.innerHeight * dpr;
    canvas.style.width = window.innerWidth + 'px';
    canvas.style.height = window.innerHeight + 'px';
    const ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    seedStars(window.innerWidth, window.innerHeight);
  }

  function draw(t) {
    const ctx = canvas.getContext('2d');
    const w = window.innerWidth;
    const h = window.innerHeight;

    ctx.clearRect(0, 0, w, h);

    // Aurora blobs
    for (const b of BLOBS) {
      const px = (b.cx + Math.sin(t * b.speed + b.phase) * 0.08) * w;
      const py = (b.cy + Math.cos(t * b.speed * 1.3 + b.phase) * 0.07) * h;
      const radius = b.r * Math.max(w, h) * 0.6;

      const [r, g, bl] = b.hue;
      const grad = ctx.createRadialGradient(px, py, 0, px, py, radius);
      grad.addColorStop(0, `rgba(${r},${g},${bl},0.09)`);
      grad.addColorStop(0.55, `rgba(${r},${g},${bl},0.03)`);
      grad.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(px, py, radius, 0, Math.PI * 2);
      ctx.fill();
    }

    // Stars with parallax
    const mx = (mouse.x - 0.5) * 18;
    const my = (mouse.y - 0.5) * 12;
    for (const s of stars) {
      s.tw += 0.02 * s.twSpeed;
      const alpha = 0.25 + Math.abs(Math.sin(s.tw)) * 0.55;
      ctx.fillStyle = `rgba(230,225,255,${alpha})`;
      ctx.beginPath();
      ctx.arc(s.x - mx * s.depth, s.y - my * s.depth, s.r, 0, Math.PI * 2);
      ctx.fill();
    }

    raf = requestAnimationFrame(draw);
  }

  function onMouseMove(e) {
    mouse.x = e.clientX / window.innerWidth;
    mouse.y = e.clientY / window.innerHeight;
  }

  $effect(() => {
    resize();
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!reduced) {
      raf = requestAnimationFrame(draw);
      window.addEventListener('mousemove', onMouseMove);
    } else {
      draw(0);
      cancelAnimationFrame(raf);
    }
    window.addEventListener('resize', resize);
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener('resize', resize);
      window.removeEventListener('mousemove', onMouseMove);
    };
  });
</script>

<canvas bind:this={canvas} class="fixed inset-0 -z-10" aria-hidden="true"></canvas>

<!-- Vignette to deepen edges -->
<div
  class="pointer-events-none fixed inset-0 -z-10"
  style="background: radial-gradient(ellipse 120% 90% at 50% 10%, transparent 40%, rgba(7,6,15,0.75) 100%);"
></div>
