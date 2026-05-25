
# Patch Notes

This overlay adds saved directory listings for the MSO64B retrieval workflow.

## Changes

- `mso64b_retrieve_file.py` now supports `--save-list` with `--list`.
- Saved listings are written under `img/`.
- The script writes both text and JSON listing files.
- HOWTO 004 documents saved listings and the JSON structure.

## Example

```powershell
python scripts/mso64b_retrieve_file.py --list --save-list
```

Default outputs:

```text
img/YYYYMMDD-HHMMSS_mso64b_directory_listing.txt
img/YYYYMMDD-HHMMSS_mso64b_directory_listing.json
```
