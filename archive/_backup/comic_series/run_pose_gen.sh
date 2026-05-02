#!/bin/bash
# Character Pose Generator - Creates poses from base character using ffmpeg

BASE_DIR="/home/openclaw/.openclaw/workspace/comic_series"
CHAR_DIR="$BASE_DIR/character_concepts"
LOC_DIR="$BASE_DIR/locations"
OUTPUT_DIR="$BASE_DIR/generated_poses"

mkdir -p "$OUTPUT_DIR"

BASE_CHAR="$CHAR_DIR/hero_01_action.jpg"

echo "🎭 Generating character poses..."
echo "Base: $BASE_CHAR"

# 1. Original
ffmpeg -y -i "$BASE_CHAR" -vf "scale=1280:720" "$OUTPUT_DIR/pose_01_original.jpg" 2>/dev/null

# 2. Mirror
ffmpeg -y -i "$BASE_CHAR" -vf "hflip,scale=1280:720" "$OUTPUT_DIR/pose_02_mirror.jpg" 2>/dev/null

# 3. Zoom
ffmpeg -y -i "$BASE_CHAR" -vf "scale=iw*1.5:ih*1.5,crop=1280:720:100:0,scale=1280:720" "$OUTPUT_DIR/pose_03_zoom.jpg" 2>/dev/null

# 4. Rotated right
ffmpeg -y -i "$BASE_CHAR" -vf "rotate=5*PI/180,scale=1280:720" "$OUTPUT_DIR/pose_04_rotated_right.jpg" 2>/dev/null

# 5. Rotated left
ffmpeg -y -i "$BASE_CHAR" -vf "rotate=-5*PI/180,scale=1280:720" "$OUTPUT_DIR/pose_05_rotated_left.jpg" 2>/dev/null

# 6. Upper body crop
ffmpeg -y -i "$BASE_CHAR" -vf "crop=720:720:280:0,scale=1280:720" "$OUTPUT_DIR/pose_06_upper_body.jpg" 2>/dev/null

# 7. Focused crop
ffmpeg -y -i "$BASE_CHAR" -vf "crop=800:800:240:0,scale=1280:720" "$OUTPUT_DIR/pose_07_focused.jpg" 2>/dev/null

# 8. Mirror + zoom
ffmpeg -y -i "$BASE_CHAR" -vf "hflip,scale=iw*1.3:ih*1.3,crop=1280:720:50:0,scale=1280:720" "$OUTPUT_DIR/pose_08_mirror_zoom.jpg" 2>/dev/null

# 9. Tilt right
ffmpeg -y -i "$BASE_CHAR" -vf "rotate=10*PI/180:ow=hypot(ow,oh):oh=hypot(ow,oh),scale=1280:720" "$OUTPUT_DIR/pose_09_tilt_right.jpg" 2>/dev/null

# 10. Tilt left
ffmpeg -y -i "$BASE_CHAR" -vf "rotate=-10*PI/180:ow=hypot(ow,oh):oh=hypot(ow,oh),scale=1280:720" "$OUTPUT_DIR/pose_10_tilt_left.jpg" 2>/dev/null

# 11. Wide shot
ffmpeg -y -i "$BASE_CHAR" -vf "scale=iw*0.8:ih*0.8,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black" "$OUTPUT_DIR/pose_11_wide.jpg" 2>/dev/null

# 12. Lower crop
ffmpeg -y -i "$BASE_CHAR" -vf "crop=720:720:280:200,scale=1280:720" "$OUTPUT_DIR/pose_12_lower.jpg" 2>/dev/null

echo ""
echo "✅ Generated 12 poses:"
ls -la "$OUTPUT_DIR"/pose_*.jpg

# Create video from poses
echo ""
echo "🎬 Creating video from poses..."

cat > /tmp/pose_concat.txt
for i in $(seq -w 1 12); do
    echo "file '$OUTPUT_DIR/pose_$i.jpg'" >> /tmp/pose_concat.txt
    echo "duration 1.5" >> /tmp/pose_concat.txt
done

ffmpeg -y -f concat -safe 0 -i /tmp/pose_concat.txt \
    -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black" \
    -c:v libx264 -pix_fmt yuv420p -crf 23 -shortest \
    "$OUTPUT_DIR/hero_pose_demo.mp4" 2>/dev/null

echo "✅ Video: $OUTPUT_DIR/hero_pose_demo.mp4"
ls -lh "$OUTPUT_DIR/hero_pose_demo.mp4"

# Create composite scenes
echo ""
echo "🏠 Creating scene composites..."

for loc in "$LOC_DIR/futuristic_street_night.jpg" "$LOC_DIR/spaceship_hangar.jpg"; do
    loc_name=$(basename "$loc" .jpg)
    
    # Scale character for composite
    ffmpeg -y -i "$BASE_CHAR" -vf "scale=400:-1" "$OUTPUT_DIR/temp_char.jpg" 2>/dev/null
    
    # Composite
    ffmpeg -y -i "$loc" -i "$OUTPUT_DIR/temp_char.jpg" -filter_complex "overlay=300:200" \
        "$OUTPUT_DIR/composite_${loc_name}.jpg" 2>/dev/null
    
    echo "   ✅ composite_${loc_name}.jpg"
done

rm -f "$OUTPUT_DIR/temp_char.jpg" /tmp/pose_concat.txt

echo ""
echo "🎉 Complete! All outputs in: $OUTPUT_DIR"