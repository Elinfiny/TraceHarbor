/* Private operator controls. No provider key, new inference or capture on load. */
(() => {
  const panel = document.createElement('section');
  panel.setAttribute('aria-label', 'Admitted recording controls');
  const load = document.createElement('button');
  load.textContent = 'Load admitted runtime case'; load.type = 'button';
  load.addEventListener('click', async () => {
    load.disabled = true;
    await run(async () => {
      const response = await fetch('/demo68.json', {credentials:'same-origin',cache:'no-store',redirect:'error'});
      if (!response.ok) throw Error('Admitted case unavailable.');
      return response.text();
    });
    load.disabled = false;
  });
  const ready = document.createElement('button');
  ready.textContent = 'Check recorded-call admission'; ready.type = 'button';
  ready.addEventListener('click', () => loadRuntimeStatus());
  const message = document.createElement('p');
  message.textContent = 'Start the separate private tab recorder first. Select only this TraceHarbor tab. The first recorded chunk must be acknowledged before the single AI action becomes available. No retry.';
  panel.append(load, ready, message); document.body.prepend(panel);
})();
