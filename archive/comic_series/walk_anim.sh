#!/bin/bash
# Walking Animation using FFmpeg with character parts
# Composites character parts and creates walking animation

OUTPUT="/home/openclaw/.openclaw/workspace/comic_series/assets/output"
CHAR="$OUTPUT/../characters/nomark/parts_detailed"

echo "Creating walking animation..."

# Background color (dark alley)
BG_COLOR="#0f0f19"

# Create 24 frames
for frame in $(seq 0 23); do
    # Calculate position offset (walking)
    x_offset=$((300 + frame * 5))
    
    # Leg swing
    leg_l_y=$((180 + frame % 2 * 5))
    leg_r_y=$((180 + (frame + 1) % 2 * 5))
    
    # Build filter complex for this frame
    # Using FFmpeg to overlay parts
    ffmpeg -f lavfi -i "color=c=$BG_COLOR:s=640x360" \
           -i "$CHAR/leg.png" \
           -i "$CHAR/torso.png" \
           -i "$CHAR/head.png" \
           -i "$CHAR/left_arm.png" \
           -i "$CHAR/right_arm.png" \
           -filter_complex "
               [1:v]overlay=$x_offset:$leg_l_y[leg1];
               [leg1][2:v]overlay=$((x_offset+15)):180[body];
               [body][4:v]overlay=$((x_offset-30)):200[arm1];
               [arm1][5:v]overlay=$((x_offset+75)):200[arm2];
               [arm2][3:v]overlay=$((x_offset+35)):100
           " -frames:v 1 "$OUTPUT/walk_frames/frame_$(printf '%02d' $frame).png" -y 2>/dev/null
    
    echo "Frame $frame"
done

echo "Rendering video..."
ffmpeg -framerate 12 -i "$OUTPUT/walk_frames/frame_%02d.png" \
       -c:v libx264 -pix_fmt yuv420p -vf scale=640:360 \
       -t 2 "$OUTPUT/walking_character.mp4" -y 2>&1 | grep -E "(Duration|video:|error)"

echo ""
echo "Result:"
ls -lh "$OUTPUT/walking_character.mp4"