# BUILD-PROMPT — build this film end to end (PHASE 2)

Paste into Claude Code. Paths: `R=…/walker-vidiyum-mun-shriram-a`, `REEL=$R/youtube/claude-liam-walker-vidiyum-mun-shriram-a-gamedev`,
`B=…/brutalist.art`, `GODOT=~/Downloads/Godot.app/Contents/MacOS/Godot` (4.7.2). Never edit `$R/godot`, root docs or git. Never publish.

```text
Read $B/skills/make/godot-gamedev/SKILL.md (+ references/evidence.md) and $REEL/CAPTURE.md, FACTCHECK.md. Then, after the code freeze:

0. Confirm all five SFX exist: ls $R/godot/assets/audio/sfx/{phone_buzz,clue_saved,keys_exchanged,dawn_crash,safe_dawn}.*
   and that the game's own import has run (each has a .import).
1. sh $REEL/tools/prepare_capture_copy.sh          # rsync + 4K/no_focus override + headless import; diff must show only
                                                   # project.godot + capture_driver.gd
2. Final take (~11-12 min; do not touch the window; it cannot take focus):
   cd $REEL && $GODOT --path capture-project --script res://capture_driver.gd --resolution 3840x2160 \
     --write-movie "$REEL/capture/run-01.avi" --fixed-fps 30 -- take=run-01 > capture/run-01.log 2>&1
   Require "CAPTURE OK" in capture/run-01.log and a summary row with foreign_events 0.
3. Transcode, keeping the audio (~3 min):
   ffmpeg -y -i capture/run-01.avi -map 0:a -c:a pcm_s16le capture/run-01.wav
   ffmpeg -y -i capture/run-01.avi -map 0:v -c:v libx264 -preset fast -crf 12 -pix_fmt yuv420p -r 30 capture/run-01.mp4
   Check SFX audible: ffmpeg -i capture/run-01.wav -af volumedetect -f null -  (and listen around each sfx_event t).
4. python3 tools/make_trace_images.py && python3 tools/render_test_output.py --take run-01
5. python3 tools/author_sheet.py --take run-01      # re-locates excerpts, clip ranges, build id, walk line
   Re-verify every FACTCHECK.md row marked RE-VERIFY; edit narration in author_sheet.py if a fact changed.
6. python3 $B/runtime/scripts/generate_audio_kokoro.py $REEL    (only changed beats are needed: --only Bxx …)
7. python3 tools/conform_timeline.py                 # exact-frame gameplay, labelled holds, game audio mix, cue times
8. python3 $B/runtime/scripts/remotion_scenes.py $REEL --force   (~6 s render per s of beat; ~30-35 min for 17 beats;
   can be split: --only B00 … in parallel shells is NOT allowed on the same reel — run sequentially)
9. python3 tools/build_evidence.py && python3 tools/write_docs.py
10. cd $B && ./art godot-gamedev --check $REEL --game $R/godot      # must PASS
11. ./art final $REEL --height 2160 --fps 30 --out $REEL/exports/landscape
    If GATE T reports only false positives on real game footage, document them in $REEL/_qc/GATE-T-OVERRIDE.md and
    follow the A1 precedent (compile.py directly); any other failure must be fixed.
12. Visual QC: ffmpeg -i <export> -vf fps=2 _qc/frames/%05d.png plus 15/50/85 % of every beat; read them; log in
    _qc/REPORT.md. Listen across every narration/game-audio transition; confirm B14 has no voice and the outro has no game audio.
13. Report the 4K MP4 path, `open "<path>"`, SHA-256, component coverage, limitations. Never publish.
```
