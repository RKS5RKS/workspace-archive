#!/bin/bash
# Simple FFmpeg Animation Pipeline (Fixed v2)
# Works with FFmpeg only - no Python dependencies

OUTPUT_DIR="/home/openclaw/.openclaw/workspace/comic_series/assets/output"
ASSETS_DIR="/home/openclaw/.openclaw/workspace/comic_series/assets"

echo "=== FFmpeg Animation Pipeline ==="
echo ""

# Clean up old files
mkdir -p "$OUTPUT_DIR/anim_test"
rm -f "$OUTPUT_DIR/anim_test/"*.png "$OUTPUT_DIR/anim_test.mp4"

# Create 24 frames of walking animation (2 seconds at 12fps)
echo "Creating frames..."
frame_num=0
for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23; do
    # Moving position (walk effect)
    x_pos=$((300 + i * 10))
    
    # Background (dark alley)
    ffmpeg -f lavfi -i "color=c=#0a0a15:s=640x360" \
           -frames:v 1 "$OUTPUT_DIR/anim_test/bg_$frame_num.png" -y 2>/dev/null
    
    # Character (blue nomark)
    ffmpeg -f lavfi -i "color=c=#3264c8:s=80x150" \
           -frames:v 1 "$OUTPUT_DIR/anim_test/char_$frame_num.png" -y 2>/dev/null
    
    # Composite
    ffmpeg -i "$OUTPUT_DIR/anim_test/bg_$frame_num.png" -i "$OUTPUT_DIR/anim_test/char_$frame_num.png" \
           -filter_complex "[0:v][1:v] overlay=$x_pos:180" \
           -frames:v 1 "$OUTPUT_DIR/anim_test/frame_$frame_num.png" -y 2>/dev/null
    
    rm -f "$OUTPUT_DIR/anim_test/bg_$frame_num.png" "$OUTPUT_DIR/anim_test/char_$frame_num.png"
    
    echo "  Frame $frame_num / 23"
    frame_num=$((frame_num + 1))
done

echo "Rendering video..."
ffmpeg -framerate 12 -i "$OUTPUT_DIR/anim_test/frame_%d.png" \
       -c:v libx264 -pix_fmt yuv420p -vf "scale=640:360" \
       -t 2 "$OUTPUT_DIR/anim_test.mp4" -y 2>&1 | grep -E "(Duration|video:|error)"
       
echo ""
echo "=== Result ==="
ls -lh "$OUTPUT_DIR/anim_test.mp4"

# Verify
duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_DIR/anim_test.mp4" 2>/dev/null)
echo "Duration: ${duration}s"