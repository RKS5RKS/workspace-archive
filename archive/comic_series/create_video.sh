#!/bin/bash
# Comic Video Creator - Creates animated videos from generated assets
# Usage: ./create_video.sh [output_name]

set -e

OUTPUT_DIR="/home/openclaw/.openclaw/workspace/comic_series"
CHAR_DIR="$OUTPUT_DIR/character_concepts"
LOC_DIR="$OUTPUT_DIR/locations"
OUTPUT_NAME="${1:-comic_scene.mp4}"

echo "🎬 Comic Video Creator"
echo "======================"

# Select a few representative images for the demo
# Using unique images (not _v2, _v3 etc duplicates)
HERO_IMAGES=(
    "$CHAR_DIR/hero_01_action.jpg"
    "$CHAR_DIR/hero_01_combat.jpg"
    "$CHAR_DIR/hero_01_aiming.jpg"
)

VILLAIN_IMAGES=(
    "$CHAR_DIR/villain_01_hands_clasped.jpg"
    "$CHAR_DIR/villain_01_speaking.jpg"
    "$CHAR_DIR/villain_01_looking_down_intent.jpg"
)

LOCATION_IMAGES=(
    "$LOC_DIR/futuristic_street_night.jpg"
    "$LOC_DIR/spaceship_hangar.jpg"
    "$LOC_DIR/abandoned_factory.jpg"
)

# Verify we have ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg not found. Installing..."
    apt-get update && apt-get install -y ffmpeg
fi

# Create temp directory for processed frames
TEMP_DIR=$(mktemp -d)
echo "📁 Using temp directory: $TEMP_DIR"

# Function to create a slide with transition
create_slide() {
    local input_img=$1
    local output_img=$2
    local duration=$3
    
    # Scale to 1280x720 and add black bars if needed (cinematic aspect)
    ffmpeg -y -i "$input_img" -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2 black" "$output_img" 2>/dev/null
}

# Function to create zoom effect frames
create_zoom_frames() {
    local input_img=$1
    local output_prefix=$2
    local num_frames=$3
    
    # Create frames with varying zoom levels
    for i in $(seq 1 $num_frames); do
        zoom=$(echo "1.0 + ($i * 0.1)" | bc)
        ffmpeg -y -i "$input_img" -vf "scale=1280:-1,zoompan=z='$zoom':d=1:s=1280x720" -vframes 1 "${output_prefix}_frame_${i}.jpg" 2>/dev/null || true
    done
}

FRAME_DIR="$TEMP_DIR/frames"
mkdir -p "$FRAME_DIR"

FRAME_NUM=0

# Scene 1: Location establishing shot
echo "🎬 Creating Scene 1: Location establishing shot"
if [ -f "${LOCATION_IMAGES[0]}" ]; then
    create_slide "${LOCATION_IMAGES[0]}" "$FRAME_DIR/slide_000.jpg"
    # Hold for 3 seconds (30fps = 90 frames of same image)
    for i in {1..90}; do
        cp "$FRAME_DIR/slide_000.jpg" "$FRAME_DIR/frame_$(printf "%04d" $FRAME_NUM).jpg"
        ((FRAME_NUM++))
    done
fi

# Scene 2: Hero entrance with zoom
echo "🎬 Creating Scene 2: Hero entrance"
if [ -f "${HERO_IMAGES[0]}" ]; then
    # Simple fade-in effect using color overlay
    ffmpeg -y -f lavfi -i color=c=black:s=1280x720:d=1 -i "${HERO_IMAGES[0]}" -filter_complex "[1]scale=1280:720[img];[0][img]overlay=0:0:format=auto:alpha=0.0-1.0" "$FRAME_DIR/hero_entrance.mp4" 2>/dev/null || true
    
    # Extract frames
    ffmpeg -y -i "${HERO_IMAGES[0]}" -vf "scale=1280:720" "$FRAME_DIR/slide_001.jpg" 2>/dev/null || true
    
    if [ -f "$FRAME_DIR/slide_001.jpg" ]; then
        # Fade in over 30 frames
        for i in {1..30}; do
            alpha=$(echo "scale=2; $i / 30" | bc)
            ffmpeg -y -f lavfi -i "color=c=white:s=1280x720:d=0.033" -i "$FRAME_DIR/slide_001.jpg" -filter_complex "[1][0]blend=all_mode=multiply:repeat_last=1:c0_opacity=$alpha[out]" -map "[out]" "$FRAME_DIR/frame_$(printf "%04d" $FRAME_NUM).jpg" 2>/dev/null || cp "$FRAME_DIR/slide_001.jpg" "$FRAME_DIR/frame_$(printf "%04d" $FRAME_NUM).jpg"
            ((FRAME_NUM++))
        done
        # Hold for 60 frames
        for i in {1..60}; do
            cp "$FRAME_DIR/slide_001.jpg" "$FRAME_DIR/frame_$(printf "%04d" $FRAME_NUM).jpg"
            ((FRAME_NUM++))
        done
    fi
fi

# Scene 3: Action shot
echo "🎬 Creating Scene 3: Action sequence"
if [ -f "${HERO_IMAGES[1]}" ]; then
    ffmpeg -y -i "${HERO_IMAGES[1]}" -vf "scale=1280:720" "$FRAME_DIR/slide_002.jpg" 2>/dev/null || true
    if [ -f "$FRAME_DIR/slide_002.jpg" ]; then
        for i in {1..90}; do
            cp "$FRAME_DIR/slide_002.jpg" "$FRAME_DIR/frame_$(printf "%04d" $FRAME_NUM).jpg"
            ((FRAME_NUM++))
        done
    fi
fi

# Scene 4: Villain reveal
echo "🎬 Creating Scene 4: Villain reveal"
if [ -f "${VILLAIN_IMAGES[0]}" ]; then
    ffmpeg -y -i "${VILLAIN_IMAGES[0]}" -vf "scale=1280:720" "$FRAME_DIR/slide_003.jpg" 2>/dev/null || true
    if [ -f "$FRAME_DIR/slide_003.jpg" ]; then
        for i in {1..120}; do
            cp "$FRAME_DIR/slide_003.jpg" "$FRAME_DIR/frame_$(printf "%04d" $FRAME_NUM).jpg"
            ((FRAME_NUM++))
        done
    fi
fi

# Scene 5: Final confrontation location
echo "🎬 Creating Scene 5: Final confrontation"
if [ -f "${LOCATION_IMAGES[1]}" ]; then
    ffmpeg -y -i "${LOCATION_IMAGES[1]}" -vf "scale=1280:720" "$FRAME_DIR/slide_004.jpg" 2>/dev/null || true
    if [ -f "$FRAME_DIR/slide_004.jpg" ]; then
        for i in {1..150}; do
            cp "$FRAME_DIR/slide_004.jpg" "$FRAME_DIR/frame_$(printf "%04d" $FRAME_NUM).jpg"
            ((FRAME_NUM++))
        done
    fi
fi

echo "📊 Generated $FRAME_NUM frames"

# Create video from frames
echo "🎬 Assembling video..."
ffmpeg -y -framerate 30 -i "$FRAME_DIR/frame_%04d.jpg" -c:v libx264 -pix_fmt yuv420p -crf 23 "$OUTPUT_DIR/$OUTPUT_NAME" 2>/dev/null

# Cleanup
rm -rf "$TEMP_DIR"

if [ -f "$OUTPUT_DIR/$OUTPUT_NAME" ]; then
    echo "✅ Success! Video created: $OUTPUT_DIR/$OUTPUT_NAME"
    ls -lh "$OUTPUT_DIR/$OUTPUT_NAME"
else
    echo "❌ Video creation failed"
    exit 1
fi