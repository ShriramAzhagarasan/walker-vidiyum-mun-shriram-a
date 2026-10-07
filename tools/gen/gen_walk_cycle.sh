#!/bin/bash
# Walk-cycle frames (2026-10-07), added after Shriram's playtest feedback on static motion.
cd "$(dirname "$0")/../.."
while pgrep -f "tools/gen/gen_audio.py" >/dev/null; do sleep 10; done
P=../virtualenvironments/vidiyum-img/bin/python; J=prompts/image_prompts.json
pre=$(python3 -c "import json;print(json.load(open('$J'))['_pose_prefix'])"); sty=$(python3 -c "import json;print(json.load(open('$J'))['_style'])")
for a in CHAR-HARI-WALK-PASS CHAR-HARI-WALK-B; do
  pose=$(python3 -c "import json;print(json.load(open('$J'))['walk_cycle']['$a'])")
  $P tools/gen/gen_image.py --asset $a --edit design/character/gen/hari-ref.png --prompt "$pre $pose $sty" --seeds 321 322 --w 768 --h 1344
done
echo WALK DONE
