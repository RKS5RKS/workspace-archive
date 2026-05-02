#!/bin/bash
# Pose Transition Generator
# Creates animations between poses using FFmpeg

ASSETS="/home/openclaw/.openclaw/workspace/comic_series/assets/characters"
OUT="/home/openclaw/.openclaw/workspace/comic_series/assets/output"
mkdir -p "$OUT"

# Function to create transition between two poses
create_transition() {
    local char=$1
    local pose1=$2
    local pose2=$3
    local name="${char}_${pose1}_to_${pose2}"
    
    local p1="$ASSETS/$char/poses/${pose1}.png"
    local p2="$ASSETS/$char/poses/${pose2}.png"
    
    if [ ! -f "$p1" ] || [ ! -f "$p2" ]; then
        echo "Missing: $p1 or $p2"
        return
    fi
    
    echo "Creating transition: $name"
    
    # Create frames with crossfade using filter_complex
    ffmpeg -y -i "$p1" -i "$p2" -filter_complex "
    [0:v]trim=0:1,setpts=PTS-STARTPTS,format=rgba[v0];
    [1:v]trim=0:1,setpts=PTS-STARTPTS,format=rgba[v1];
    [v0][v1]xfade=transition=fade:duration=0.5:offset=0.5,format=rgb24
    " -c:v libx264 -pix_fmt yuv420p -r 30 "$OUT/${name}.mp4" 2>/dev/null
    
    echo "  Created: $OUT/${name}.mp4"
}

# Create transitions for Nomark
create_transition "nomark" "standing" "walking"
create_transition "nomark" "walking" "standing"
create_transition "nomark" "standing" "victory"
create_transition "nomark" "victory" "standing"
create_transition "nomark" "standing" "defeated"
create_transition "nomark" "defeated" "standing"
create_transition "nomark" "standing" "punching"
create_transition "nomark" "punching" "standing"
create_transition "nomark" "standing" "running"
create_transition "nomark" "running" "standing"
create_transition "nomark" "standing" "sitting"
create_transition "nomark" "sitting" "standing"

# Create transitions for Villain
create_transition "villain" "standing" "punching"
create_transition "villain" "punching" "standing"
create_transition "villain" "standing" "victory"
create_transition "villain" "standing" "defeated"

# Create transitions for Ally
create_transition "ally" "standing" "walking"
create_transition "ally" "standing" "victory"
create_transition "ally" "standing" "defeated"

echo ""
echo "Done! Created transition videos in $OUT/"