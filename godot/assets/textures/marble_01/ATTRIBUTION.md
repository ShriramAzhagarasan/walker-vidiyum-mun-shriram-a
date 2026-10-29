# Texture attribution

| Files | Asset | Author | Licence | Source |
|---|---|---|---|---|
| `marble_01_diff_2k.png`, `marble_01_rough_2k.png`, `marble_01_nor_gl_2k.png`, `marble_01_nor_dx_2k.png` | Marble 01 (`marble_01`), 2K PNG | Rob Tuytel | CC0 1.0 | <https://polyhaven.com/a/marble_01> |
| `godot/tests/data/curl/floor_tiles_06_nor_gl_2k.png`, `floor_tiles_06_nor_dx_2k.png` (curl-check calibration only, not used in the game) | Floor Tiles 06 (`floor_tiles_06`), 2K PNG | Rob Tuytel | CC0 1.0 | <https://polyhaven.com/a/floor_tiles_06> |

Downloaded 2026-10-29 from `dl.polyhaven.org` via the Poly Haven API; file sizes match the API listing.
CC0 needs no attribution; it is given anyway. Files are unmodified.

Import settings (CHANGE-BRIEF.md §2.2): diff and rough VRAM Compressed, normal_map Disabled, mipmaps on; nor_gl VRAM
Compressed, normal_map Enable, mipmaps on; nor_dx Lossless, no mipmaps (calibration only). `detect_3d/compress_to=0` on
all four so the editor cannot change the compression on first use in 3D (F9). The calibration folder has a `.gdignore`,
so Godot does not import it; `normal_map_check.gd` reads the raw PNG bytes.
