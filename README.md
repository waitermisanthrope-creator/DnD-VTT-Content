# DnD-VTT-Content

Public curated data registry for DnD-VTT Unity.

- `catalog/v1/index.json`: live catalog, including the original CC0 Lanternfolk test race.
- `packages/`: small declarative JSON, exact bytes and SHA-256 in catalog entries.
- `schemas/catalog-entry-v1.schema.json`: runtime manifest shared with Assets.
- Existing `demo-race.json` is retained as a historical prototype; it is no longer advertised as active content.

Unity integration is in `DnD-VTT/experiment/unity-vtt`. Storage and character integration have executable tests; device QA remains pending. Unsupported gameplay categories are shown as unavailable. No JavaScript, DLLs or user executable mods are accepted.
