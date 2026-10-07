"""Logged audio generation: Stable Audio Open 1.0 (SFX) and MusicGen stereo-medium (music).

Appends one JSON row per output to gen/audio_log.jsonl (asset, model, prompt, negative prompt,
seed, duration, steps/guidance, output path, seconds). Raw WAVs go to gen/raw/audio/.
  python tools/gen/gen_audio.py sfx   [ASSET ...]
  python tools/gen/gen_audio.py music [ASSET ...]
"""
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import soundfile as sf
import torch

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "gen" / "raw" / "audio"
LOG = ROOT / "gen" / "audio_log.jsonl"
DEV = "mps" if torch.backends.mps.is_available() else "cpu"

SFX = {
    "SFX-PHONE-BUZZ": ("A smartphone vibrating on a hard table, two short buzzing pulses, close and dry, no ringtone.", 2.5),
    "SFX-CLUE": ("A single soft ding of a small brass temple bell, gentle and clean, short natural decay.", 2.5),
    "SFX-KEYS": ("Car keys on a key ring jingling as they are picked up and handed over, close-up foley.", 2.0),
    "SFX-DAWN-CRASH": ("A distant truck horn on a highway at dawn swelling louder and longer, then a long screeching tyre skid, outdoors, no impact.", 5.0),
    "SFX-SAFE-DAWN": ("Gentle sea waves lapping on a sandy beach at dawn, crows cawing in the distance, calm and quiet.", 9.0),
}
SFX_NEG = "music, speech, voice, low quality, distortion, clipping"
SFX_SEEDS = [11, 22, 33]

MUSIC = {
    "MUS-PARTY": "Energetic electronic dance music for a beach house party at night, four-on-the-floor kick drum, deep synth bass, bright plucked synth hook, 124 bpm, steady loopable groove, no vocals.",
    "MUS-GAANA": "Chennai gaana street folk music, fast lively hand percussion on frame drums and a barrel drum, a harmonium playing a repeating melody, raw energetic outdoor night groove, 112 bpm, no vocals.",
}
MUSIC_SEEDS = [7, 8]
MUSIC_SECONDS = 30


def log(row):
    with LOG.open("a") as f:
        f.write(json.dumps(row) + "\n")


def run_sfx(ids):
    from diffusers import StableAudioPipeline
    from diffusers import EDMDPMSolverMultistepScheduler
    pipe = StableAudioPipeline.from_pretrained("stabilityai/stable-audio-open-1.0", torch_dtype=torch.float32).to(DEV)
    # 2026-10-07: the model's default stochastic sampler (CosineDPMSolver sde-dpmsolver++ via torchsde) is broken in
    # this torch 2.14 / diffusers 0.40 setup: run 1 hit a RecursionError; final_sigmas_type=sigma_min gave all-NaN
    # (written as silence). Deterministic EDM DPM-Solver++ with the model's own sigma settings works.
    pipe.scheduler = EDMDPMSolverMultistepScheduler(sigma_min=0.3, sigma_max=500, sigma_data=1.0, sigma_schedule="exponential",
                                                    prediction_type="v_prediction", algorithm_type="dpmsolver++", solver_order=2)
    sr = pipe.vae.sampling_rate
    for aid in ids:
        prompt, dur = SFX[aid]
        for seed in SFX_SEEDS:
            t0 = time.time()
            g = torch.Generator("cpu").manual_seed(seed)
            audio = pipe(prompt, negative_prompt=SFX_NEG, num_inference_steps=50, guidance_scale=7.0,
                         audio_end_in_s=dur, num_waveforms_per_prompt=1, generator=g).audios[0]
            out = RAW / f"{aid}_sao_s{seed}.wav"
            sf.write(out, audio.T.float().cpu().numpy(), sr)
            log({"time": datetime.now().isoformat(timespec="seconds"), "asset": aid,
                 "model": "stabilityai/stable-audio-open-1.0", "prompt": prompt, "negative_prompt": SFX_NEG,
                 "seed": seed, "seed_generator": "torch cpu Generator", "duration_s": dur, "steps": 50,
                 "guidance": 7.0, "scheduler": "EDMDPMSolverMultistep dpmsolver++ order 2, sigma 0.3-500 exponential, v_prediction", "sample_rate": sr, "output": str(out.relative_to(ROOT)),
                 "seconds": round(time.time() - t0, 1), "device": DEV})
            print("OK", out.name, round(time.time() - t0, 1), "s", flush=True)


def run_music(ids):
    from transformers import AutoProcessor, MusicgenForConditionalGeneration
    proc = AutoProcessor.from_pretrained("facebook/musicgen-stereo-medium")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-stereo-medium").to(DEV)
    sr = model.config.audio_encoder.sampling_rate
    tokens = int(MUSIC_SECONDS * model.config.audio_encoder.frame_rate)
    for aid in ids:
        prompt = MUSIC[aid]
        for seed in MUSIC_SEEDS:
            t0 = time.time()
            torch.manual_seed(seed)
            inputs = proc(text=[prompt], padding=True, return_tensors="pt").to(DEV)
            wav = model.generate(**inputs, do_sample=True, guidance_scale=3.0, max_new_tokens=tokens)
            data = wav[0].float().cpu().numpy().T  # (samples, channels)
            out = RAW / f"{aid}_musicgen_s{seed}.wav"
            sf.write(out, data, sr)
            log({"time": datetime.now().isoformat(timespec="seconds"), "asset": aid,
                 "model": "facebook/musicgen-stereo-medium", "prompt": prompt, "seed": seed,
                 "seed_note": "torch.manual_seed before generate", "duration_s": MUSIC_SECONDS,
                 "max_new_tokens": tokens, "guidance": 3.0, "do_sample": True, "sample_rate": sr,
                 "output": str(out.relative_to(ROOT)), "seconds": round(time.time() - t0, 1), "device": DEV})
            print("OK", out.name, round(time.time() - t0, 1), "s", flush=True)


if __name__ == "__main__":
    RAW.mkdir(parents=True, exist_ok=True)
    kind, ids = sys.argv[1], sys.argv[2:]
    if kind == "sfx":
        run_sfx(ids or list(SFX))
    else:
        run_music(ids or list(MUSIC))
