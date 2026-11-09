#!/bin/bash
# Scripted / fixture captures for the A6 film (windowed, real renderer; never --rendering-driver). Writes only into the reel.
R=/Users/shriramalagarasan/Desktop/NortheasternUniversity/Fall2026/virtualenvironments/walker-vidiyum-mun-shriram-a; REEL=/Users/shriramalagarasan/Desktop/NortheasternUniversity/Fall2026/virtualenvironments/walker-vidiyum-mun-shriram-a/youtube/claude-liam-vidiyum-mun-a6-gamedev
cd $R
godot --path godot --write-movie $REEL/capture/walk_effects.avi --fixed-fps 30 --resolution 1920x1080 -s $REEL/tools/capture_walk_effects.gd -- $REEL/evidence/walk_effects_frames.txt > $REEL/_qc/capture_walk.log 2>&1
godot --path godot res://previews/footstep_scuff_preview.tscn --write-movie $REEL/capture/scuff_retrigger_dark.avi --fixed-fps 30 --resolution 1280x720 --quit-after 60 -- retrigger > $REEL/_qc/capture_scuff.log 2>&1
godot --path godot res://previews/string_light_moths_preview.tscn --write-movie $REEL/capture/moths_r3_preview.avi --fixed-fps 30 --resolution 1280x720 --quit-after 150 > $REEL/_qc/capture_moths.log 2>&1
echo done
