#!/bin/bash
# Complete Scene Creator with Dialogue
# Creates animated scene with character, location, and dialogue

OUTPUT="/home/openclaw/.openclaw/workspace/comic_series/assets/output"
LOCATIONS="/home/openclaw/.openclaw/workspace/comic_series/assets/locations"
CHAR="/home/openclaw/.openclaw/workspace/comic_series/assets/characters/nomark/parts_detailed"

mkdir -p "$OUTPUT/final_scene"
rm -f "$OUTPUT/final_scene"/*.png

echo "=== COMPLETE SCENE CREATOR ==="
echo ""

# Scene settings
LOCATION="neon_alley.jpg"
BACKGROUND="$LOCATIONS/$LOCATION"
if [ ! -f "$BACKGROUND" ]; then
    BACKGROUND="$LOCATIONS/alley_night.png"
fi

DIALOGUE="They thought no one was watching."
DURATION=4
FPS=12
FRAMES=$((DURATION * FPS))

echo "Settings:"
echo "  Background: $BACKGROUND"
echo "  Dialogue: \"$DIALOGUE\""
echo "  Duration: ${DURATION}s"
echo ""

# Create frames with character and dialogue
echo "Creating $FRAMES frames..."

for frame in $(seq 0 $((FRAMES - 1))); do
    frame_num=$(printf "%04d" $frame)
    
    # Character walking position (start left, walk to center)
    progress=$((frame * 100 / FRAMES))
    char_x=$((100 + progress * 3))
    
    # Arm swing animation
    arm_offset=$((frame % 2 * 10))
    
    # Create frame with background, character, and text
    ffmpeg -y -f lavfi -i "color=c=#0a0a15:s=640x360" \
           -loop 1 -i "$BACKGROUND" \
           -i "$CHAR/leg.png" \
           -i "$CHAR/torso.png" \
           -i "$CHAR/head.png" \
           -i "$CHAR/left_arm.png" \
           -i "$CHAR/right_arm.png" \
           -filter_complex "
               [0:v][1:v]overlay=0:0[bg];
               [bg][2:v]overlay=$char_x:200[legs];
               [legs][3:v]overlay=$((char_x+15)):130[body];
               [body][4:v]overlay=$((char_x-30)):135[arm1];
               [arm1][5:v]overlay=$((char_x+75)):135[arm2];
               [arm2][6:v]overlay=$((char_x+35)):80,
               drawtext=text='$DIALOGUE':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=320:shadowcolor=black:shadowx=2:shadowy=2
           " -frames:v 1 "$OUTPUT/final_scene/frame_$frame_num.png" 2>/dev/null
    
    if [ $((frame % 12)) -eq 0 ]; then
        echo "  Frame $frame / $FRAMES"
    fi
done

echo ""
echo "Rendering video..."

ffmpeg -framerate $FPS -i "$OUTPUT/final_scene/frame_%04d.png" \
       -c:v libx264 -pix_fmt yuv420p -vf scale=640:360 \
       -t $DURATION "$OUTPUT/complete_scene.mp4" -y 2>&1 | grep -E "(Duration|video:)"

echo ""
echo "=== RESULT ==="
ls -lh "$OUTPUT/complete_scene.mp4"

# Get duration
duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT/complete_scene.mp4" 2>/dev/null)
echo "Duration: ${duration}s"