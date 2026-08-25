<script>
  import { onMount } from 'svelte';
  import * as THREE from 'three';

  let canvas;
  let scene, camera, renderer;
  let particles;
  let mouseX = 0;
  let mouseY = 0;
  let animationId;

  const PARTICLE_COUNT = 1200;
  const CONNECTION_DISTANCE = 120;

  onMount(() => {
    if (!canvas) return;

    // Scene
    scene = new THREE.Scene();

    // Camera
    camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
    camera.position.z = 60;

    // Renderer
    renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: true,
      antialias: true,
    });
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Particles
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(PARTICLE_COUNT * 3);
    const colors = new Float32Array(PARTICLE_COUNT * 3);
    const sizes = new Float32Array(PARTICLE_COUNT);

    const color1 = new THREE.Color('#7C3AED');
    const color2 = new THREE.Color('#06B6D4');
    const color3 = new THREE.Color('#F59E0B');

    for (let i = 0; i < PARTICLE_COUNT; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 100;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 100;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 50;

      const color = Math.random();
      let c;
      if (color < 0.5) c = color1.clone().lerp(color2, Math.random());
      else c = color2.clone().lerp(color3, Math.random());

      colors[i * 3] = c.r;
      colors[i * 3 + 1] = c.g;
      colors[i * 3 + 2] = c.b;

      sizes[i] = Math.random() * 2 + 0.5;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    const material = new THREE.PointsMaterial({
      size: 0.3,
      vertexColors: true,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending,
      sizeAttenuation: true,
    });

    particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // Mouse tracking
    function handleMouseMove(e) {
      mouseX = (e.clientX / window.innerWidth) * 2 - 1;
      mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
    }

    function handleResize() {
      if (!canvas || !renderer) return;
      const w = canvas.clientWidth;
      const h = canvas.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    }

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('resize', handleResize);

    // Animation
    let time = 0;
    function animate() {
      animationId = requestAnimationFrame(animate);
      time += 0.001;

      if (particles) {
        const positions = particles.geometry.attributes.position.array;
        const origPositions = positions.slice();

        // Gentle wave motion
        for (let i = 0; i < PARTICLE_COUNT; i++) {
          const x = origPositions[i * 3];
          const y = origPositions[i * 3 + 1];
          const z = origPositions[i * 3 + 2];

          positions[i * 3] = x + Math.sin(time + y * 0.5) * 0.3;
          positions[i * 3 + 1] = y + Math.cos(time + x * 0.5) * 0.3;
          positions[i * 3 + 2] = z + Math.sin(time * 0.5 + (x + y) * 0.3) * 0.2;
        }

        particles.geometry.attributes.position.needsUpdate = true;

        // Rotate slowly
        particles.rotation.x += (mouseY * 0.05 - particles.rotation.x) * 0.02;
        particles.rotation.y += (mouseX * 0.1 - particles.rotation.y) * 0.02;
      }

      renderer.render(scene, camera);
    }

    animate();

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
      scene.clear();
    };
  });
</script>

<div class="particle-container">
  <canvas
    bind:this={canvas}
    class="particle-canvas"
  ></canvas>
</div>

<style>
  .particle-container {
    position: absolute;
    inset: 0;
    z-index: 0;
    overflow: hidden;
  }

  .particle-canvas {
    width: 100%;
    height: 100%;
    display: block;
  }
</style>
