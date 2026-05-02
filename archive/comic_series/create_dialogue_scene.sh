#!/bin/bash
# Dialogue Scene - Character idle with talking animation
# Shows dialogue appearing with character

OUTPUT="/home/openclaw/.openclaw/workspace/comic_series/assets/output"
LOCATIONS="/home/openclaw/.openclaw/workspace/comic_series/assets/locations"
CHAR="/home/openclaw/.openclaw/workspace/comic_series/assets/characters/nomark/parts_detailed"

mkdir -p "$OUTPUT/dialogue_scene"
rm -f "$OUTPUT/dialogue_scene"/*.png

echo "=== DIALOGUE SCENE ==="

# Use an existing location
BACKGROUND="$LOCATIONS/futuristic_street_night.jpg"

# Dialogue lines
LINES=(
    "I've been watching from the shadows."
    "Every move they make."
    "Every secret they keep."
    "Tonight... everything changes."
)

FRAME_DELAY=36  # 3 seconds per line at 12fps
TOTAL_FRAMES=$((${#LINES[@]} * FRAME_DELAY))

echo "Creating dialogue scene with ${#LINES[@]} lines..."
echo ""

for frame in $(seq 0 $((TOTAL_FRAMES - 1))); do
    frame_num=$(printf "%04d" $frame)
    
    # Which line are we on?
    line_idx=$((frame / FRAME_DELAY))
    if [ $line_idx -ge ${#LINES[@]} ]; then
        line_idx=$((${#LINES[@]} - 1))
    fi
    
    DIALOGUE="${LINES[$line_idx]}"
    
    # Calculate fade in/out for text
    frame_in_line=$((frame % FRAME_DELAY))
    if [ $frame_in_line -lt 6 ]; then
        # Fade in - use alpha (simulated with drawbox)
        alpha=$((frame_in_line * 40))
    elif [ $frame_in_line -gt $((FRAME_DELAY - 6)) ]; then
        # Fade out
        alpha=$(((FRAME_DELAY - frame_in_line) * 40))
    else
        alpha=255
    fi
    
    # Idle breathing animation
    breath_offset=$(( (frame / 6) % 2 ))
    
    # Create frame
    ffmpeg -y -f lavfi -i "color=c=#0a0a15:s=640x360" \
           -loop 1 -i "$BACKGROUND" \
           -i "$CHAR/leg.png" \
           -i "$CHAR/torso.png" \
           -i "$CHAR/head.png" \
           -i "$CHAR/left_arm.png" \
           -i "$CHAR/right_arm.png" \
           -filter_complex "
               [0:v][1:v]overlay=0:0[bg];
               [bg][2:v]overlay=250:200[legs];
               [legs][3:v]overlay=$((265)):130[body];
               [body][4:v]overlay=$((220)):135[arm1];
               [arm1][5:v]overlay=$((285)):135[arm2];
               [arm2][6:v]overlay=$((245)):80,
               drawtext=text='$DIALOGUE':fontcolor=white:fontsize=20:x=(w-text_w)/2:y=320:shadowcolor=black:shadowx=2:shadowy=2
           " -frames:v 1 "$OUTPUT/dialogue_scene/frame_$frame_num.png" 2>/dev/null
    
    if [ $((frame % 12)) -eq 0 ]; then
        echo "  Frame $frame / $TOTAL_FRAMES"
    fi
done

DURATION=$(echo "scale=1; $TOTAL_FRAMES / 12" | bc)
echo ""
echo "Rendering video (${DURATION}s)..."

ffmpeg -framerate 12 -i "$OUTPUT/dialogue_scene/frame_%04d.png" \
       -c:v libx264 -pix_fmt yuv420p -vf scale=640:360 \
       -t $DURATION "$OUTPUT/dialogue_scene.mp4" -y 2>&1 | grep -E "(Duration|video:)"

echo ""
echo "Result:"
ls -lh "$OUTPUT/dialogue_scene.mp4"