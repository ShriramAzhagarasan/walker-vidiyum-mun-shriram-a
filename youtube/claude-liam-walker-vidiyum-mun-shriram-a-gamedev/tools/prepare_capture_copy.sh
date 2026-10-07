#!/bin/sh
# Refresh the isolated capture copy from the frozen game, re-apply the two harness-only changes, import.
#   sh tools/prepare_capture_copy.sh
set -e
REEL="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(cd "$REEL/../.." && pwd)"
GODOT_BIN="${GODOT:-/Users/shriramalagarasan/Downloads/Godot.app/Contents/MacOS/Godot}"
rsync -a --delete --exclude .godot --exclude capture_driver.gd "$REPO/godot/" "$REEL/capture-project/"
python3 - "$REEL/capture-project/project.godot" <<'PY'
import re, sys
p = sys.argv[1]; s = open(p).read()
s = re.sub(r'window/size/window_(width|height)_override=\d+\n', '', s)
s = s.replace('window/size/no_focus=true\n', '')
s = s.replace('window/size/viewport_height=720\n', 'window/size/viewport_height=720\nwindow/size/window_width_override=3840\n'
              'window/size/window_height_override=2160\nwindow/size/no_focus=true\n', 1)
if 'movie_writer/mjpeg_quality' not in s:
    s += '\n[editor]\n\nmovie_writer/mjpeg_quality=0.9\n'
open(p, 'w').write(s)
PY
"$GODOT_BIN" --headless --path "$REEL/capture-project" --import > "$REEL/capture/import.log" 2>&1
echo "--- diff game vs capture copy (expected: project.godot override + capture_driver.gd only)"
diff -rq -x .godot "$REPO/godot" "$REEL/capture-project" || true
diff "$REPO/godot/project.godot" "$REEL/capture-project/project.godot" || true
