# Motion Comic Pipeline

A pure Python + FFmpeg pipeline for generating animated video content without AI services.

## Quick Start

```bash
# Generate character poses
python3 generate_poses.py

# Create pose transitions
./create_pose_transitions.sh

# Create a scene with multiple characters
./create_team_scene.sh
```

## Directory Structure

```
comic_series/
├── generate_poses.py       # Generate character poses (PPM -> PNG)
├── create_pose_transitions.sh  # Animate between poses
├── create_locations.sh     # Generate background images
├── create_complete_scene.sh    # Full scene with background
├── create_dialogue_scene.sh   # Scene with text overlays
├── create_confrontation.sh    # 2-character fight scene
├── create_team_scene.sh        # 3-character scene
├── ffmpeg_anim.sh         # Generic FFmpeg animation
├── assets/
│   ├── characters/
│   │   ├── nomark/poses/  # Nomark (blue) - 9 poses
│   │   ├── villain/poses/ # Villain (red) - 9 poses
│   │   └── ally/poses/    # Ally (green) - 9 poses
│   ├── locations/          # Background images
│   └── output/             # Generated videos
```

## Character Poses (9 per character)

| Pose | Description |
|------|-------------|
| standing | Neutral standing |
| walking | Walking stride |
| punching | Arm extended |
| crouching | Sneaking/crouch |
| looking | Head turned |
| sitting | Seated |
| running | Full sprint |
| victory | Arms raised V |
| defeated | Slumped, head down |

## Pose Transitions

Transitions are generated between pose pairs. Examples:
- `nomark_standing_to_walking.mp4`
- `nomark_standing_to_victory.mp4`
- `nomark_standing_to_defeated.mp4`

## Creating Custom Scenes

### Single character on background:
```bash
ffmpeg -y -f lavfi -i "color=c=#202030:s=640x360" \
       -i "assets/characters/nomark/poses/standing.png" \
       -filter_complex "[0:v][1:v]overlay=250:80" \
       -c:v libx264 -pix_fmt yuv420p output/scene.mp4
```

### Two characters (confrontation):
```bash
./create_confrontation.sh
```

### Three characters (team):
```bash
./create_team_scene.sh
```

## Text/Dialogue Overlays

Use FFmpeg drawtext filter:
```bash
ffmpeg -i input.mp4 -vf "drawtext=text='Hello':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-50" output.mp4
```

## Adding New Characters

Edit `generate_poses.py`:
1. Add color definitions
2. Create pose functions
3. Add to `save_all_poses()`

## Requirements

- Python 3
- FFmpeg (with libx264)

No external APIs or AI services required.