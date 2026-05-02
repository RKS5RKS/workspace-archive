#!/bin/bash
# Scene Composer - creates video scenes using FFmpeg
# Usage: ./scene_composer.sh <character> <animation> <output.mp4>

CHAR=$1
ANIM=$2
OUTPUT=$3

ASSETS="/home/openclaw/.openclaw/workspace/comic_series/assets"
CHAR_DIR="$ASSETS/characters/$CHAR/parts_detailed"
LOC_DIR="$ASSETS/locations"
OUT_DIR="$ASSETS/output"

# Default values
CHAR=${CHAR:-nomark}
ANIM=${ANIM:-idle}
OUTPUT=${OUTPUT:-$OUT_DIR/scene_test.mp4}

echo "Scene Composer"
echo "=============="
echo "Character: $CHAR"
echo "Animation: $ANIM"
echo "Output: $OUTPUT"
echo ""

# Check if character parts exist
if [ ! -d "$CHAR_DIR" ]; then
    echo "Error: Character directory not found: $CHAR_DIR"
    exit 1
fi

# Check for parts
HEAD="$CHAR_DIR/head.png"
TORSO="$CHAR_DIR/torso.png"
ARM_L="$CHAR_DIR/left_arm.png"
ARM_R="$CHAR_DIR/right_arm.png"
LEG="$CHAR_DIR/leg.png"

echo "Checking assets..."
for part in "$HEAD" "$TORSO" "$ARM_L" "$ARM_R" "$LEG"; do
    if [ -f "$part" ]; then
        echo "  ✓ $(basename $part)"
    else
        echo "  ✗ $(basename $part) - missing"
    fi
done

# For now, create a simple test scene with a solid background
# In a full implementation, this would composite character parts

# Create test frame
ffmpeg -f lavfi -i "color=#1a1a2e:s=1280x720:d=1" \
       -vf "drawtext=text='$CHAR':fontsize=64:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
       -frames:v 1 /tmp/test_frame.png -y 2>/dev/null

echo ""
echo "Created test frame"

# Simple animation test - just repeat the frame
ffmpeg -loop 1 -i /tmp/test_frame.png \
       -c:v libx264 -t 3 -pix_fmt yuv420p \
       -vf "scale=1280:720" \
       "$OUTPUT" -y 2>/dev/null

if [ -f "$OUTPUT" ]; then
    echo "✓ Output: $OUTPUT"
    ls -lh "$OUTPUT"
else
    echo "✗ Failed to create output"
fi