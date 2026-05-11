# NOMARK Animation Project - Status & Plan

## Current State (May 4, 2026)

### What We Have
- 2D SVG character assets (vector art)
- Body parts (PNG): torso, arms, legs, face, mask, hood, eyes, hands, shoes
- Pose library (SVG): walking, standing, running, jumping, punching, etc.
- Expressions (SVG): neutral, happy, angry
- Props: hoodie, mask
- Animation frames: walk, idle, run (GIF + PNG frames)
- Documentation: SPEC.md, RIG_SPEC.md, ANIMATION_SPEC.md

### The Problem
The 2D assets CANNOT be rigged properly. You (Ryan) noted that assets weren't 3D, causing rigging problems. The rig spec requires 3D/bone-based rigging but we only have 2D layers.

### Solution Agreed Upon

**Step 1: Install Blender on DigitalOcean Server**
- Server: ubuntu-s-1vcpu-1gb-nyc1
- SSH key available at /home/openclaw/.openclaw/credentials/ssh/id_ed25519
- Need to resolve hostname to connect

**Step 2: Use Mixamo (Free)**
- Download free 3D character model
- Re-skin/re-texture to look like NOMARK
- Download free animations (walk, run, idle, etc.)

**Step 3: Create Videos**
- Build scenes in Blender
- Render videos
- Deliver to Ryan

### Why This Works
- Mixamo has pre-rigged characters (no manual rigging needed)
- Auto-rigging feature
- Thousands of free animations
- Blender can re-texture to match NOMARK's design:
  - Dark hoodie (#0D0D0D, #1A1A1A)
  - Face mask (black)
  - Neon accents (cyan #00FFFF, pink #FF0080)
  - White glowing eyes

### Tools Needed
- Blender (free, open source)
- Mixamo account (free)
- SSH access to server

### Who's Doing What
- **Ryan**: Install Blender on server (once we connect)
- **Crystal**: All the 3D work - re-skin, animate, render, deliver

---

## Server Access Details

### Connection Info
- **IP:** 143.244.145.155
- **User:** root
- **SSH Key:** /home/openclaw/.openclaw/credentials/ssh/id_ed25519
- **Blender:** /usr/bin/blender
- **Project Dir:** /root/nomark_project/

### SSH Client
- Successfully installed paramiko (Python SSH library)
- Can connect via Python if we get the right IP/hostname

---

## Next Steps
1. Get correct server IP/hostname from DigitalOcean dashboard
2. Connect via SSH
3. Install Blender on server
4. Begin 3D workflow

---

*Last updated: 2026-05-04*