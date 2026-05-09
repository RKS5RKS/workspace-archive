# REFERENCE.md - Crystal's Permanent Source of Truth

**Updated: 2026-05-08** — This is THE source for critical info. Update it whenever it changes.

---

## Core Files (Always in Root)
- `AGENTS.md` — Behavior rules
- `IDENTITY.md` — Who I am
- `SOUL.md` — My operating directives
- `MEMORY.md` — Long-term memory
- `HEARTBEAT.md` — Periodic check list
- `TOOLS.md` — Local tool config and credentials
- `REFERENCE.md` — This file (source of truth for critical info)

---

## Critical Locations

### NOMARK Animation
- **Server IP:** 143.244.145.155
- **SSH Key:** `~/.openclaw/credentials/ssh/id_ed25519`
- **GLB File:** `/root/nomark_project/exports/nomark_walk.glb`
- **Pipeline Script:** `memory/nomark_pipeline_v2.py`
- **Read This First:** `memory/NOMARK_ANIMATION_README.md`

#### CRITICAL Camera Settings (FIXES CLIPPING!)
- **Camera Location:** `(0, -6, 1.2)` — This shows the FULL BODY
- **Camera Rotation:** `(1.54, 0, 0)` — 2% tilt down for full body
- **Model:** Use `nomark_walk.glb` (Mannequin) - has full body visibility
- **Samples:** Always use `8` (not default 64/128) for fast rendering
- **Output Format:** `AVI_RAW` + ffmpeg conversion to MP4

### Discord
- **Server ID:** 1487626689956806798
- **Channel (general):** 1487626690560790680
- **Bot User ID:** 1487628729856294972

### GitHub Archive
- **Repo:** https://github.com/RKS5RKS/workspace-archive
- **Branch:** main

---

## Model Lock (CRITICAL)
- **Always use:** `openrouter/minimax/minimax-m2.5`
- **Never switch** to Gemini, GPT-OSS, or any other model without Ryan's direct permission
