'use strict';
(() => {
  const map = document.querySelector('#scenario-map');
  const label = document.querySelector('#scenario_text');
  const error = document.querySelector('#map-error');
  let selection = 0;
  document.querySelectorAll('input[type="radio"]').forEach(input => {
    input.addEventListener('change', () => {
      const temperature = document.querySelector('input[name="temp"]:checked').value;
      const precipitation = document.querySelector('input[name="prec"]:checked').value;
      const version = ++selection;
      const next = new Image();
      map.setAttribute('aria-busy', 'true');
      error.textContent = '';
      next.onload = () => {
        if (version !== selection) return;
        map.src = next.src;
        map.alt = `Dominant Land Cover Type — temperature change ${temperature} °C, precipitation change ${precipitation} mm`;
        label.textContent = `${temperature} °C | ${precipitation} mm`;
        map.removeAttribute('aria-busy');
      };
      next.onerror = () => {
        if (version !== selection) return;
        map.removeAttribute('aria-busy');
        error.textContent = 'The scenario map could not be loaded. Please check your connection and select the scenario again.';
      };
      next.src = `assets/maps/t${temperature}_p${precipitation}.webp`;
    });
  });
})();
