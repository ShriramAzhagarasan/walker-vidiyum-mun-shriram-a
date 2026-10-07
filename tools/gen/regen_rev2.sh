#!/bin/bash
# Rev2 regenerations (2026-10-07): OVERHEAR, WHITEOUT (prompt fixes), Advay with a visible speaker.
cd "$(dirname "$0")/../.."
P=../virtualenvironments/vidiyum-img/bin/python; J=prompts/image_prompts.json
pre=$(python3 -c "import json;print(json.load(open('$J'))['_pose_prefix'])"); sty=$(python3 -c "import json;print(json.load(open('$J'))['_style'])")
for a in CHAR-HARI-OVERHEAR CHAR-HARI-WHITEOUT; do
  pose=$(python3 -c "import json;print(json.load(open('$J'))['poses_rev2']['$a'])")
  $P tools/gen/gen_image.py --asset $a --tag rev2 --edit design/character/gen/hari-ref.png --prompt "$pre $pose $sty" --seeds 311 312 313 --w 768 --h 1344
done
$P tools/gen/gen_image.py --asset NPC-ADVAY --tag rev2 --prompt "Full-body character design of a loud 26-year-old Indian man just back from studying abroad: light-brown skin, styled undercut hair, a thin gold chain, a black oversized t-shirt, light blue ripped jeans, white sneakers. In one hand he carries a large black cylindrical portable party speaker with a carry strap, clearly visible and about the size of a water bottle. Smug grin, swaggering confident stance, three-quarter front view facing left. $sty" --seeds 411 412
echo REGEN DONE
