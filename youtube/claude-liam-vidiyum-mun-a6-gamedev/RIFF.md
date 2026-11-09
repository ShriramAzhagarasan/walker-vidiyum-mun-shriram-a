# Riff notes (evidence-led)

- The Godot 3 name mutation: the scene loaded cleanly and the effect still fired, while its speed silently read 0.0;
  only the read-back test noticed (`logs/a6-mutations/m1_godot3_name.log`, TEST-REPORT.md A6.2).
- Effect B's tuning is the honest story: two reasonable fixes (size, colour) and a failed prediction before the real
  cause, an almost transparent agent-made texture, was found (TUNING.md Effect B r2–r3).
- The GPU price could not be measured: the profiler's GPU column read 0.0 ms everywhere on Metal (TEST-REPORT.md A6.6).
