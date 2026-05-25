
# Patch Notes

This overlay updates the MSO64B PyVISA workflow.

## Changes

- `mso64b_save_image.py` now generates unique scope-side PNG filenames by default.
- Generated names use `YYYYMMDD-HHMMSS_mso64b_<label>.png`.
- `mso64b_retrieve_file.py` can list scope-side files with `--list`.
- Retrieval writes to `img/` by default.
- HOWTO 003 and HOWTO 004 document the save/list/retrieve workflow.
- README now describes the unique screenshot naming pattern.

## Typical command sequence

```powershell
python scripts/mso64b_save_image.py --label probe-comp-ch2
python scripts/mso64b_retrieve_file.py --list
python scripts/mso64b_retrieve_file.py --scope-path "C:/YYYYMMDD-HHMMSS_mso64b_probe-comp-ch2.png"
```
