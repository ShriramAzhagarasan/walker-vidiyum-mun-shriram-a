#!/bin/bash
# Environment rev2 (2026-10-07), after Shriram's playtest 2 ("backgrounds still not sitting right… house and beach… not up to the mark").
# Higher resolution, more detail, and no painted railing or pool (they duplicated the real 3D ones).
cd "$(dirname "$0")/../.."
P=../virtualenvironments/vidiyum-img/bin/python; J=prompts/image_prompts.json
for a in ENV-VILLA ENV-BEACH; do
  pr=$(python3 -c "import json;print(json.load(open('$J'))['env_rev2']['$a'])")
  $P tools/gen/gen_image.py --asset $a --tag rev2 --prompt "$pr" --seeds 611 612 --w 2048 --h 768
done
echo ENV DONE
