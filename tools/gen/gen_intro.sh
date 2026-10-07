#!/bin/bash
# Intro motion-comic stills (2026-10-07), added at Shriram's request for a title + intro sequence.
cd "$(dirname "$0")/../.."
P=../virtualenvironments/vidiyum-img/bin/python; J=prompts/image_prompts.json
for a in INTRO-1-ECR INTRO-2-ROCK INTRO-4-DAWN; do
  pr=$(python3 -c "import json;print(json.load(open('$J'))['intro']['$a'])")
  $P tools/gen/gen_image.py --asset $a --prompt "$pr" --seeds 701 702 --w 1536 --h 864
done
pr=$(python3 -c "import json;print(json.load(open('$J'))['intro_edit']['INTRO-3-ARRIVAL'])")
$P tools/gen/gen_image.py --asset INTRO-3-ARRIVAL --edit design/character/gen/hari-ref.png --prompt "$pr" --seeds 701 702 --w 1536 --h 864
echo INTRO DONE
