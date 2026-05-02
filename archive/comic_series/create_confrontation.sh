#!/bin/bash
# Confrontation Scene - Nomark vs Villain
# Two characters, dialogue exchange

OUTPUT="/home/openclaw/.openclaw/workspace/comic_series/assets/output"
LOCATIONS="/home/openclaw/.openclaw/workspace/comic_series/assets/locations"
CHAR_NOMARK="/home/openclaw/.openclaw/workspace/comic_series/assets/characters/nomark/parts_detailed"
CHAR_VILLAIN="/home/openclaw/.openclaw/workspace/comic_series/assets/characters/villain/parts_detailed"

mkdir -p "$OUTPUT/confrontation"
rm -f "$OUTPUT/confrontation"/*.png

echo "=== CONFRONTATION SCENE ==="

BACKGROUND="$LOCATIONS/abandoned_warehouse.jpg"

# Dialogue exchange
LINES=(
    "VILLAIN: You can't stop me."
    "NOMARK: Watch me."
    "VILLAIN: You're too late."
    "NOMARK: Never."
)

FRAME_DELAY=36
TOTAL_FRAMES=$((${#LINES[@]} * FRAME_DELAY))

echo "Creating confrontation with ${#LINES[@]} exchanges..."
echo ""

for frame in $(seq 0 $((TOTAL_FRAMES - 1))); do
    frame_num=$(printf "%04d" $frame)
    
    line_idx=$((frame / FRAME_DELAY))
    if [ $line_idx -ge ${#LINES[@]} ]; then
        line_idx=$((${#LINES[@]} - 1))
    fi
    
    DIALOGUE="${LINES[$line_idx]}"
    
    # Characters positioned
    nomark_x=180
    villain_x=400
    
    # Idle animation offset
    breath=$((frame % 24 / 12))
    
    # Create frame with both characters
    ffmpeg -y -f lavfi -i "color=c=#0a0a15:s=640x360" \
           -loop 1 -i "$BACKGROUND" \
           -i "$CHAR_VILLAIN/leg.png" \
           -i "$CHAR_VILLAIN/torso.png" \
           -i "$CHAR_VILLAIN/head.png" \
           -i "$CHAR_NOMARK/leg.png" \
           -i "$CHAR_NOMARK/torso.png" \
           -i "$CHAR_NOMARK/head.png" \
           -filter_complex "
               [0:v][1:v]overlay=0:0[bg];
               [bg][2:v]overlay=$((villain_x+15)):200[legs_v];
               [legs_v][3:v]overlay=$((villain_x)):130[body_v];
               [body_v][4:v]overlay=$((villain_x+35)):80[v1];
               [v1][5:v]overlay=$((nomark_x+15)):200[legs_n];
               [legs_n][6:v]overlay=$((nomark_x)):130[body_n];
               [body_n][7:v]overlay=$((nomark_x+35)):80,
               drawtext=text='$DIALOGUE':fontcolor=yellow:fontsize=22:x=(w-text_w)/2:y=320:shadowcolor=black:shadowx=2:shadowy=2
           " -frames:v 1 "$OUTPUT/confrontation/frame_$frame_num.png" 2>/dev/null
    
    if [ $((frame % 12)) -eq 0 ]; then
        echo "  Frame $frame / $TOTAL_FRAMES"
    fi
done

echo ""
echo "Rendering..."

ffmpeg -framerate 12 -i "$OUTPUT/confrontation/frame_%04d.png" \
       -c:v libx264 -pix_fmt yuv420p -vf scale=640:360 \
       -t 12 "$OUTPUT/confrontation_scene.mp4" -y 2>&1 | grep -E "(Duration|video:)"

echo ""
echo "Result:"
ls -lh "$OUTPUT/confrontation_scene.mp4"