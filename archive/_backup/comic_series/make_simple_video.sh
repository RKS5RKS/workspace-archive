#!/bin/bash
# Simple Comic Video Creator - Creates slideshow video from assets

OUTPUT_DIR="/home/openclaw/.openclaw/workspace/comic_series"
CHAR_DIR="$OUTPUT_DIR/character_concepts"
LOC_DIR="$OUTPUT_DIR/locations"

echo "🎬 Creating simple comic video..."

# Create a file list for ffmpeg (conatent demuxer)
# Using existing unique images
cat > /tmp/frames.txt << 'EOF'
file '/home/openclaw/.openclaw/workspace/comic_series/locations/futuristic_street_night.jpg'
duration 3
file '/home/openclaw/.openclaw/workspace/comic_series/character_concepts/hero_01_action.jpg'
duration 2
file '/home/openclaw/.openclaw/workspace/comic_series/character_concepts/hero_01_combat.jpg'
duration 2
file '/home/openclaw/.openclaw/workspace/comic_series/character_concepts/villain_01_hands_clasped.jpg'
duration 3
file '/home/openclaw/.openclaw/workspace/comic_series/locations/spaceship_hangar.jpg'
duration 2
EOF

# Create video from image sequence
ffmpeg -y -f concat -safe 0 -i /tmp/frames.txt \
    -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black" \
    -c:v libx264 -pix_fmt yuv420p -crf 23 -shortest \
    "$OUTPUT_DIR/comic_video_output.mp4"

if [ -f "$OUTPUT_DIR/comic_video_output.mp4" ]; then
    echo "✅ Video created: $OUTPUT_DIR/comic_video_output.mp4"
    ls -lh "$OUTPUT_DIR/comic_video_output.mp4"
else
    echo "❌ Failed to create video"
fi