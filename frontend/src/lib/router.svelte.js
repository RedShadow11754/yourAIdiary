// Simple hash-based router for Svelte 5
let _currentRoute = $state(window.location.hash.slice(1) || '/');
let _params = $state({});

export function getRouter() {
  return {
    get currentRoute() { return _currentRoute; },
    get params() { return _params; },
  };
}

export function navigate(path) {
  window.location.hash = '#' + path;
}

// Parse route from hash
function parseRoute() {
  const hash = window.location.hash.slice(1) || '/';
  _currentRoute = hash;

  // Extract params from routes like /diary/:id
  const diaryMatch = hash.match(/^\/diary\/(\d+)$/);
  if (diaryMatch) {
    _params = { id: diaryMatch[1] };
  } else {
    _params = {};
  }
}

window.addEventListener('hashchange', parseRoute);
parseRoute();
