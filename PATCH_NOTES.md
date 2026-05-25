# MSO64B Patch Notes

This ZIP is structured for extraction at the repository root.

It contains repository-relative paths only. When extracted into an existing clone, Windows should prompt before overwriting existing files.

## Intended use

From the local repo root:

1. Extract this ZIP into the repository root.
2. Accept overwrite prompts.
3. Review changes with `git status` and `git diff`.
4. Commit and push locally.

## Main changes

- Document PyVISA as the primary scripted interface.
- Preserve the confirmed CREATE bench VISA resource.
- Add save and retrieve scripts for screen images.
- Add HOWTO 004 for retrieving a saved screen image.
- Keep generated images and data under ignored local paths such as `img/`.
