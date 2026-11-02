# BUILD-PROMPT: rebuild this film end to end

Paths: `R=…/walker-vidiyum-mun-shriram-a`, `REEL=$R/youtube/claude-liam-vidiyum-mun-a5-gamedev`, `B=…/brutalist.art`,
`godot` on PATH (4.7.2). Never edit `$R/godot`, root docs or git. Never publish. No paid calls.

```text
0. echo bb2c156 > $REEL/evidence/source-revision.txt; export A5_FILM_REV=bb2c156   # last commit touching godot/ or scripts/
   git -C $R diff --stat bb2c156 HEAD -- godot scripts                                 # must be empty
1. godot --path $R/godot --write-movie $REEL/capture/glow_motion.avi --fixed-fps 30 \
       -s $REEL/tools/capture_glow_motion.gd -- $REEL/evidence/glow_motion_frames.txt        # scripted, windowed
   godot --path $R/godot -s $REEL/tools/capture_standard_sphere.gd -- $REEL/evidence/standard_generated_sphere.png
2. python3 tools/author_sheet.py                       # verbatim anchored excerpts, narration
3. python3 $B/runtime/scripts/generate_audio_kokoro.py $REEL
4. python3 tools/make_media.py                         # log/table stills from real files, engine stills, clips, conformed audio
5. cd $B && for b in <remotion beats>; do python3 runtime/scripts/remotion_scenes.py $REEL --only $b --force; done
6. python3 tools/build_evidence.py && ./art godot-gamedev --check $REEL --game $R/godot
7. ./art final $REEL --height 2160 --fps 30 --out $REEL/exports/landscape
8. QC frames across every beat; log in _qc/REPORT.md.
```
