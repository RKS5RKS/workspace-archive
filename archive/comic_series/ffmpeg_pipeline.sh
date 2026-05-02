#!/bin/bash
# Complete FFmpeg-based Animation Pipeline
# No external dependencies beyond FFmpeg

ASSETS="/home/openclaw/.openclaw/workspace/comic_series/assets"
OUTPUT_DIR="$ASSETS/output"
CHAR_DIR="$ASSETS/characters"
LOC_DIR="$ASSETS/locations"

mkdir -p "$OUTPUT_DIR"

echo "=== FFmpeg Animation Pipeline ==="
echo ""

# Function to create a character frame using FFmpeg
create_character_frame() {
    local name=$1
    local color=$2
    local output=$3
    
    # Create a simple character using FFmpeg filters
    # Head (circle), body (rectangle), legs
    ffmpeg -f lavfi -i "color=c=$color:s=200x400:d=1" \
           -vf "drawbox=x=50:y=50:w=100:h=100:r=50:color=$color:fill=1,\
                drawbox=x=50:y=150:w=100:h=150:r=10:color=$color:fill=1,\
                drawbox=x=50:y=300:w=30:h=100:r=5:color=dark$color:fill=1,\
                drawbox=x=120:y=300:w=30:h=100:r=5:color=dark$color:fill=1" \
           -update 1 -frames:v 1 "$output" -y 2>/dev/null
}

# Function to create a background
create_background() {
    local name=$1
    local color=$2
    local output=$3
    
    ffmpeg -f lavfi -i "color=c=$color:s=1280x720:d=1" \
           -update 1 -frames:v 1 "$output" -y 2>/dev/null
}

# Function to composite character onto background
composite_scene() {
    local bg=$1
    local char=$2
    local pos_x=$3
    local pos_y=$4
    local output=$5
    
    ffmpeg -i "$bg" -i "$char" \
           -filter_complex "[0:v][1:v] overlay=$pos_x:$pos_y" \
           -update 1 -frames:v 1 "$output" -y 2>/dev/null
}

# Function to create animation from frames
create_animation() {
    local frame_pattern=$1
    local output=$2
    local duration=$3
    local fps=$4
    
    ffmpeg -framerate $fps -i "$frame_pattern" \
           -c:v libx264 -t $duration -pix_fmt yuv420p \
           "$output" -y 2>/dev/null
}

echo "Step 1: Creating backgrounds..."
mkdir -p "$LOC_DIR"

# Create different location backgrounds
create_background "alley_night" "#0a0a15" "$LOC_DIR/alley_night.png"
create_background "rooftop" "#1a1a2e" "$LOC_DIR/rooftop.png"  
create_background "street" "#2a2a3e" "$LOC_DIR/street.png"

echo "Step 2: Creating character assets..."
mkdir -p "$CHAR_DIR/nomark/parts_detailed"
mkdir -p "$CHAR_DIR/villain/parts_detailed"
mkdir -p "$CHAR_DIR/ally/parts_detailed"

# Nomark - blue
create_character_frame "nomark" "#3264c8" "$CHAR_DIR/nomark/parts_detailed/standing.png"
# Villain - red
create_character_frame "villain" "#801010" "$CHAR_DIR/villain/parts_detailed/standing.png"
# Ally - green
create_character_frame "ally" "#329650" "$CHAR_DIR/ally/parts_detailed/standing.png"

echo "Step 3: Creating scene frames..."
mkdir -p "$OUTPUT_DIR/frames"

# Create 10 frames of animation
for i in $(seq 0 9); do
    frame_num=$(printf "%03d" $i)
    
    # Simple animation - slightly move the character
    offset=$((i * 5))
    
    ffmpeg -i "$LOC_DIR/alley_night.png" -i "$CHAR_DIR/nomark/parts_detailed/standing.png" \
           -filter_complex "[0:v][1:v] overlay=$((540 + offset)):250" \
           -frames:v 1 "$OUTPUT_DIR/frames/scene_$frame_num.png" -y 2>/dev/null
    
    echo "  Created frame $frame_num"
done

echo "Step 4: Rendering animation video..."

# Create video from frames
ffmpeg -framerate 10 -i "$OUTPUT_DIR/frames/scene_%03d.png" \
       -c:v libx264 -pix_fmt yuv420p -vf "scale=1280:720" \
       "$OUTPUT_DIR/animation_pipeline_test.mp4" -y 2>/dev/null

echo ""
echo "=== Pipeline Complete ==="
echo "Output: $OUTPUT_DIR/animation_pipeline_test.mp4"

if [ -f "$OUTPUT_DIR/animation_pipeline_test.mp4" ]; then
    ls -lh "$OUTPUT_DIR/animation_pipeline_test.mp4"
    
    # Verify
    duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_DIR/animation_pipeline_test.mp4" 2>/dev/null)
    echo "Duration: ${duration}s"
else
    echo "ERROR: Output file not created"
fi