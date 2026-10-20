# DnD-VTT-Content

Public curated data registry for DnD-VTT Unity.

- `catalog/v1/index.json`: live catalog, including the original CC0 Lanternfolk test race.
- `packages/`: small declarative JSON, exact bytes and SHA-256 in catalog entries.
- `schemas/catalog-entry-v1.schema.json`: runtime manifest shared with Assets.
- Existing `demo-race.json` is retained as a historical prototype; it is no longer advertised as active content.

Unity integration is in `DnD-VTT/experiment/unity-vtt`. Storage and character integration have executable tests; device QA remains pending. Unsupported gameplay categories are shown as unavailable. No JavaScript, DLLs or user executable mods are accepted.

## Modular client 1.00.08

`catalog/v2/index.json` is consumed by Unity 1.00.08+. The v1 catalog remains unchanged for 1.00.07 and earlier clients. New packages are individual declarative race/class/feat records and project map documents; manifests pin exact SHA-256 and byte lengths. Existing character IDs remain unchanged. No executable plugins are included.

The mechanical metadata has newly written short descriptions, without republishing sourcebook prose or art. Stat changes, initial character parameters and pending choices use the currently supported Unity handlers; full combat automation and class advancement are not provided by these data packages. Extra classes that replace a race remain import-only in Unity. Feat stat bonuses are applied; other feat effects and additional prerequisites require manual handling.

Legacy third-party PNG/model files have NOT been relicensed or republished. Their exact provenance review remains BLOCKED. The new map-surface package provides original procedural checker patterns under the same legacy map keys; these are replacements, not byte-identical copies of the original images. The original files stay in the application's source repository, outside the minimal player's dependency graph. Maps preserve model references and show placeholders when a model package is missing.
