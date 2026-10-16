# BUILD-PROMPT: rebuild this film end to end

Paths: `R=…/walker-vidiyum-mun-shriram-a`, `REEL=$R/youtube/claude-liam-vidiyum-mun-a3-gamedev`, `B=…/brutalist.art`,
`GODOT=~/Downloads/Godot.app/Contents/MacOS/Godot` (4.7.2), recording `~/Desktop/blendersession.mov` (Shriram's; never copied into git).
Never edit `$R/godot`, root docs or git. Never publish. No paid calls.

```text
0. git -C $R rev-parse --short HEAD > $REEL/evidence/source-revision.txt
1. timeout 120 $GODOT --headless --path $R/godot --script res://tests/check_a3_assets.gd --fixed-fps 60 > evidence/check_a3_assets.out.txt
   timeout 120 $GODOT --headless --path $R/godot --script res://tests/check_a3_selftest.gd --fixed-fps 60 > evidence/check_a3_selftest.out.txt
   (the asset check writes evidence/a3/check-a3-<unix>.json in the repo; move it into $REEL/evidence/.)
2. python3 tools/author_sheet.py                       # verbatim anchored excerpts, narration
3. python3 $B/runtime/scripts/generate_audio_kokoro.py $REEL
4. python3 tools/make_media.py                         # terminal stills from real stdout, recording clips, engine stills, conformed audio
5. cd $B && for b in <remotion beats>; do python3 runtime/scripts/remotion_scenes.py $REEL --only $b --force; done
6. python3 tools/build_evidence.py && ./art godot-gamedev --check $REEL --game $R/godot
7. ./art final $REEL --height 2160 --fps 30 --out $REEL/exports/landscape
8. QC frames at 15/50/85 % of every beat; log in _qc/REPORT.md.
```
