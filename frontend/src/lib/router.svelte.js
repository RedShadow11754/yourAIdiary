// Tiny hash router for Svelte 5 runes
let _currentRoute = $state(window.location.hash.slice(1) || '/');
let _params = $state({});

function parseRoute() {
  const hash = window.location.hash.slice(1) || '/';
  _currentRoute = hash.split('?')[0];

  const diaryMatch = _currentRoute.match(/^\/diary\/(\d+)$/);
  _params = diaryMatch ? { id: diaryMatch[1] } : {};
}

export function getRouter() {
  return {
    get currentRoute() { return _currentRoute; },
    get params() { return _params; },
  };
}

export function navigate(path) {
  window.location.hash = '#' + path;
}

window.addEventListener('hashchange', parseRoute);
parseRoute();
