# ANIMATED VIDEO AGENT SYSTEM (from ChatGPT)

## PART 1/3 - OVERVIEW & TOOLS

### OVERVIEW:
Create consistent animated videos using reusable characters, locations, and assets. No AI video generation — everything is pre-built and controlled.

### TOOLS REQUIRED:

1) ASSET CREATION
- Adobe Illustrator / Adobe Photoshop (2D)
- Blender (3D, optional)

2) RIGGING (CRITICAL)
- Adobe Character Animator
- Spine 2D
- Live2D Cubism
- Blender (3D rigs)

3) ANIMATION / SCENE BUILDING
- Adobe After Effects
- Toon Boom Harmony
- Blender

4) AUDIO
- ElevenLabs (voice)
- CapCut or Adobe Premiere Pro (editing)

5) AUTOMATION (AGENT CONTROL)
- Python or Node.js
- Blender Python API
- After Effects scripting (ExtendScript)
- FFmpeg

### FILE STRUCTURE:

/project
  /characters/nomark
    rig.file
    /poses
    /expressions
    /animations (walk, idle, talk)
  /locations (alley, rooftop, street)
  /props (hoodie, mask)
  /audio
  /scenes
  /renders

## PART 2/3 - WORKFLOW

### STEP 1 — SCRIPT GENERATION
Agent creates:
- Dialogue
- Scene list
- Actions per scene

Example:
Scene 1:
- Location: alley_night
- Character: Nomark
- Action: walking forward
- Dialogue: "They thought no one was watching."

### STEP 2 — ASSET SELECTION
Agent pulls from library:
- Character rig
- Background/location
- Props

IMPORTANT:
No generation — only reuse for consistency.

### STEP 3 — SCENE ASSEMBLY
Agent:
- Loads scene template
- Inserts character rig
- Applies animation presets (walk, idle, talk)

### STEP 4 — VOICE + LIP SYNC
- Generate voice using ElevenLabs
- Sync mouth movement to audio (auto or scripted)

### STEP 5 — CAMERA + MOTION
Agent applies:
- Camera angles
- Zooms
- Scene cuts

### STEP 6 — RENDER
- Export scenes
- Combine video
- Add sound + music

## PART 3/3 - KEY REQUIREMENTS

- Pre-built character rigs (mandatory)
- Animation preset library
- Organized asset storage
- Basic scripting capability

### SIMPLEST FAST SETUP:

1) Build character in Adobe Character Animator
2) Use audio-driven animation
3) Export scenes
4) Edit in CapCut

### BEST STACK (SCALABLE CONTENT):

- Adobe Character Animator (character animation)
- Adobe After Effects (scene building)
- ElevenLabs (voice)
- CapCut (final editing)
- Python (automation)

### RESULT:

- Same character every video
- Same environments
- Unlimited scalable content
- Full control over branding/style