# Riff notes (evidence-led, nothing imagined)

- The rename mutation is the film's best moment: 22 timing checks stayed green while the shader no longer had the
  uniform the driver wrote. Source: `logs/mutations/m2_uniform_renamed_60fps.log`.
- "Same bytes, different meaning": the six hint-quad numbers were predicted before the shader existed and captured
  exactly (`CHANGE-BRIEF.md` §2.5, `TEST-REPORT.md` A5.6).
- Normal depth barely changes the look; that matches the curl ratio drifting to 0.637 on a polished, flat marble.
- On-screen contrast 3.46:1 vs predicted 4.47:1 before transparency: the bright scene behind the 60 % bar lowers it.
