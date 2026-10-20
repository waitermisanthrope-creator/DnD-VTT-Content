# Publishing and moderation (foundation)

This public repository holds **approved** small JSON packages and metadata. Unreviewed uploads and personal data must never be committed here.

## Workflow

1. Author creates a data-only package and a manifest matching `schemas/catalog-entry-v1.schema.json` for runtime catalog entries; the older package-manifest schema is an archive proposal.
2. Author submits a package for review through a future private intake mechanism. Until that exists, maintainers accept submissions through an agreed private channel; **do not post unpublished assets in public issues**.
3. Maintainer checks authorship/licensing, allowed file types, path traversal, decompression size, hashes, dependencies, and gameplay compatibility. Automated checks supplement, not replace, human review.
4. Approved immutable archive is published as a versioned Release asset (or later object storage).
5. Catalog entry is added only after the asset is accessible and verified; catalog must contain the exact HTTPS URL, byte count and SHA-256.
6. Rejections and revisions remain private. Never silently overwrite a published package version.

## Implemented pilot and remaining limitations

- Unity `experiment/unity-vtt` reads this repository's `catalog/v1/index.json` and the separate Assets registry. It no longer uses the application repository's legacy test catalog.
- The CC0 Lanternfolk race is published, hash/size verified from its public URL, and covered by real C# install/restart/uninstall/reinstall and character creation/save tests. Native GUI/device QA remains separate.
- Runtime supports curated single JSON payloads for races, primitive objects and color materials, plus trusted platform-specific AssetBundle files. Other gameplay categories are displayed but activation remains unavailable.
- ZIP archives and arbitrary `.dndpack` files are not installed or extracted by this client. Do not list a source-only archive as a playable package.
- The older `package-manifest-v1.schema.json` describes a future archive layout; runtime uses `catalog-entry-v1.schema.json` with exact bytes, hash, URL, platform and Unity version.
- Small data JSON is versioned in this repository; heavy binaries are Release assets after trusted Unity builds. Never overwrite an already published package version.
- User-created content requires explicit distribution permission. No unreviewed scripts, projects, DLLs or executable mods are accepted.
