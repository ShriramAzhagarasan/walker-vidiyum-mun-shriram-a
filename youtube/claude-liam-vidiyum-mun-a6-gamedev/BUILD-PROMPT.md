# BUILD-PROMPT: rebuild this film end to end

Paths: `R=…/walker-vidiyum-mun-shriram-a`, `REEL=$R/youtube/claude-liam-vidiyum-mun-a6-gamedev`, `B=…/brutalist.art`,
`godot` on PATH (4.7.2). Never edit `$R/godot`, root docs or git. Never publish. No paid calls.

```text
0. git -C $R log -1 --format=%h -- godot scripts > $REEL/evidence/source-revision.txt   # 52fa183
1. $REEL/tools/run_captures.sh                         # scripted walk + fixture previews, windowed Movie Maker
2. python3 tools/author_sheet.py                       # verbatim anchored excerpts, narration
3. cd $B && python3 runtime/scripts/generate_audio_kokoro.py $REEL
4. python3 tools/make_media.py                         # strips, log/table stills, own media, conformed audio, cues
5. cd $B && for b in <remotion beats>; do python3 runtime/scripts/remotion_scenes.py $REEL --only $b --force; done
6. python3 tools/build_evidence.py && ./art godot-gamedev --check $REEL --game $R/godot
7. ./art final $REEL --height 2160 --fps 30 --out $REEL/exports/landscape
8. QC frames across every beat; log in _qc/REPORT.md.
```
