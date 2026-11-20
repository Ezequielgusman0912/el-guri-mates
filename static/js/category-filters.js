// Filtro por tipo y material en la página de Mates. Todo pasa en el navegador,
// sin recargar; la elección queda en la dirección (?tipo=torpedo&material=algarrobo)
// para poder compartir el link.
document.addEventListener('DOMContentLoaded', () => {
  const root = document.querySelector('[data-type-filters]');
  const grid = document.querySelector('[data-filter-grid]');
  if (!root || !grid) return;

  const typeChips = [...root.querySelectorAll('.type-chip')];
  const matPills = [...root.querySelectorAll('.mat-pill')];
  const cards = [...grid.querySelectorAll('.product-card')];
  const title = document.querySelector('[data-group-title]');
  const desc = document.querySelector('[data-group-desc]');
  const total = document.querySelector('[data-group-total]');
  const empty = document.querySelector('[data-filter-empty]');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const tipos = typeChips.map((c) => c.dataset.tipo);
  const materiales = matPills.map((p) => p.dataset.material);
  const params = new URLSearchParams(window.location.search);
  const state = {
    tipo: tipos.includes(params.get('tipo')) ? params.get('tipo') : 'todos',
    material: materiales.includes(params.get('material')) ? params.get('material') : 'todos',
  };

  const matches = (card, tipo, material) =>
    (tipo === 'todos' || card.dataset.tipo === tipo) &&
    (material === 'todos' || card.dataset.material === material);

  const saveToUrl = () => {
    const url = new URL(window.location.href);
    ['tipo', 'material'].forEach((key) => {
      if (state[key] === 'todos') url.searchParams.delete(key);
      else url.searchParams.set(key, state[key]);
    });
    window.history.replaceState(null, '', url);
  };

  const render = (animate) => {
    const chip = typeChips.find((c) => c.dataset.tipo === state.tipo);
    typeChips.forEach((c) => c.setAttribute('aria-pressed', String(c === chip)));

    matPills.forEach((pill) => {
      const id = pill.dataset.material;
      const count = cards.filter((card) => matches(card, state.tipo, id)).length;
      pill.querySelector('.mat-count').textContent = count;
      pill.disabled = count === 0 && id !== state.material;
      pill.setAttribute('aria-pressed', String(id === state.material));
    });

    let shown = 0;
    cards.forEach((card) => {
      const visible = matches(card, state.tipo, state.material);
      card.hidden = !visible;
      card.classList.remove('is-entering');
      if (visible) {
        if (animate && !reduceMotion) {
          card.style.animationDelay = `${Math.min(shown * 30, 300)}ms`;
          void card.offsetWidth; // reinicia la animación
          card.classList.add('is-entering');
        }
        shown += 1;
      }
    });

    let heading = chip.dataset.title;
    if (state.material !== 'todos') {
      const pill = matPills.find((p) => p.dataset.material === state.material);
      heading += ` de ${pill.textContent.trim().split(/\s+/)[0].toLowerCase()}`;
    }
    title.textContent = heading;
    desc.textContent = chip.dataset.desc;
    total.textContent = `${shown} ${shown === 1 ? 'mate' : 'mates'}`;
    if (empty) empty.hidden = shown > 0;
  };

  typeChips.forEach((chip) => {
    chip.addEventListener('click', () => {
      state.tipo = chip.dataset.tipo;
      state.material = 'todos';
      saveToUrl();
      render(true);
      chip.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  });

  matPills.forEach((pill) => {
    pill.addEventListener('click', () => {
      state.material = pill.dataset.material;
      saveToUrl();
      render(true);
    });
  });

  document.querySelector('[data-filter-reset]')?.addEventListener('click', () => {
    state.material = 'todos';
    saveToUrl();
    render(true);
  });

  render(false);
});
