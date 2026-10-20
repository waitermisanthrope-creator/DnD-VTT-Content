# Publishing and moderation (foundation)

This public repository holds **approved** package metadata only. Unreviewed uploads and personal data must never be committed here.

## Workflow

1. Author creates a data-only package and a manifest matching `schemas/package-manifest-v1.schema.json`.
2. Author submits a package for review through a future private intake mechanism. Until that exists, maintainers accept submissions through an agreed private channel; **do not post unpublished assets in public issues**.
3. Maintainer checks authorship/licensing, allowed file types, path traversal, decompression size, hashes, dependencies, and gameplay compatibility. Automated checks supplement, not replace, human review.
4. Approved immutable archive is published as a versioned Release asset (or later object storage).
5. Catalog entry is added only after the asset is accessible and verified; catalog must contain the exact HTTPS URL, byte count and SHA-256.
6. Rejections and revisions remain private. Never silently overwrite a published package version.

## Important limitations

- The existing Unity 1.00.06 prototype reads the *legacy test catalog* from the application repository; switching it to this catalog is a separate integration step.
- Unity currently supports a single verified JSON file, **not** arbitrary `.dndpack` ZIP archives. This schema describes the intended next-generation package format; do not advertise it as installable yet.
- The catalog is intentionally empty until an end-to-end verified package and client are ready.
- GitHub Releases are a bootstrap distribution mechanism, not a guaranteed unlimited CDN.
- User-created content must have explicit distribution permission and a valid license. Official trademarks and game content require separate rights review.
