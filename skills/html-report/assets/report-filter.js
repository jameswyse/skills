for (const controls of document.querySelectorAll("[data-filter-for]")) {
  const table = document.getElementById(controls.dataset.filterFor);
  if (!table) continue;
  const rows = [...table.tBodies].flatMap((body) => [...body.rows]);
  const search = controls.querySelector("[data-filter-text]");
  const selects = [...controls.querySelectorAll("select[data-filter-key]")];
  const count = controls.querySelector("[data-filter-count]");
  const apply = () => {
    const query = search ? search.value.trim().toLowerCase() : "";
    let shown = 0;
    for (const row of rows) {
      const matches =
        row.textContent.toLowerCase().includes(query) &&
        selects.every((select) => !select.value || row.dataset[select.dataset.filterKey] === select.value);
      row.hidden = !matches;
      if (matches) shown += 1;
    }
    if (count) count.textContent = `${shown} of ${rows.length} shown`;
  };
  controls.addEventListener("input", apply);
  controls.hidden = false;
  apply();
}
