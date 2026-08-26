<script>
  let { children, maxTilt = 10, scale = 1.02, class: klass = '' } = $props();

  let el;
  let transform = $state('perspective(900px)');

  function onMove(e) {
    const rect = el.getBoundingClientRect();
    const px = (e.clientX - rect.left) / rect.width - 0.5;
    const py = (e.clientY - rect.top) / rect.height - 0.5;
    const rx = (-py * maxTilt).toFixed(2);
    const ry = (px * maxTilt).toFixed(2);
    transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) scale(${scale})`;
  }

  function onLeave() {
    transform = 'perspective(900px) rotateX(0deg) rotateY(0deg) scale(1)';
  }
</script>

<div
  bind:this={el}
  role="presentation"
  class={`tilt ${klass}`}
  style="transform: {transform};"
  onpointermove={onMove}
  onpointerleave={onLeave}
>
  {@render children()}
</div>
