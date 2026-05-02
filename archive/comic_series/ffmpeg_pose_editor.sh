#!/bin/bash
# Pose Editor using ffmpeg - cut and reposition body regions
# No AI needed, just image manipulation

BASE_DIR="/home/openclaw/.openclaw/workspace/comic_series"
CHAR_DIR="$BASE_DIR/character_concepts"
OUTPUT_DIR="$BASE_DIR/generated_poses"

mkdir -p "$OUTPUT_DIR"

# Find a character image
CHAR_IMAGE="$CHAR_DIR/hero_01_action.jpg"
if [ ! -f "$CHAR_IMAGE" ]; then
    CHAR_IMAGE=$(ls "$CHAR_DIR"/*.jpg 2>/dev/null | head -1)
fi

if [ -z "$CHAR_IMAGE" ]; then
    echo "No character image found!"
    exit 1
fi

echo "🎭 Using character: $CHAR_IMAGE"

# Get dimensions
WIDTH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$CHAR_IMAGE")
HEIGHT=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$CHAR_IMAGE")
echo "Image size: ${WIDTH}x${HEIGHT}"

# Compute region coordinates using awk for float math
read -r head_x head_y head_w head_h <<< $(awk -v w=$WIDTH -v h=$HEIGHT 'BEGIN {
    printf "%.0f %.0f %.0f %.0f\n", 0.30*w, 0.00*h, 0.40*w, 0.25*h
}')
read -r torso_x torso_y torso_w torso_h <<< $(awk -v w=$WIDTH -v h=$HEIGHT 'BEGIN {
    printf "%.0f %.0f %.0f %.0f\n", 0.25*w, 0.20*h, 0.50*w, 0.35*h
}')
read -r left_arm_x left_arm_y left_arm_w left_arm_h <<< $(awk -v w=$WIDTH -v h=$HEIGHT 'BEGIN {
    printf "%.0f %.0f %.0f %.0f\n", 0.05*w, 0.20*h, 0.20*w, 0.30*h
}')
read -r right_arm_x right_arm_y right_arm_w right_arm_h <<< $(awk -v w=$WIDTH -v h=$HEIGHT 'BEGIN {
    printf "%.0f %.0f %.0f %.0f\n", 0.75*w, 0.20*h, 0.20*w, 0.30*h
}')
read -r left_leg_x left_leg_y left_leg_w left_leg_h <<< $(awk -v w=$WIDTH -v h=$HEIGHT 'BEGIN {
    printf "%.0f %.0f %.0f %.0f\n", 0.30*w, 0.50*h, 0.18*w, 0.50*h
}')
read -r right_leg_x right_leg_y right_leg_w right_leg_h <<< $(awk -v w=$WIDTH -v h=$HEIGHT 'BEGIN {
    printf "%.0f %.0f %.0f %.0f\n", 0.52*w, 0.50*h, 0.18*w, 0.50*h
}')

echo "head: $head_x,$head_y size ${head_w}x${head_h}"
echo "torso: $torso_x,$torso_y size ${torso_w}x${torso_h}"
echo "left_arm: $left_arm_x,$left_arm_y size ${left_arm_w}x${left_arm_h}"
echo "right_arm: $right_arm_x,$right_arm_y size ${right_arm_w}x${right_arm_h}"
echo "left_leg: $left_leg_x,$left_leg_y size ${left_leg_w}x${left_leg_h}"
echo "right_leg: $right_leg_x,$right_leg_y size ${right_leg_w}x${right_leg_h}"

# Extract all regions as temp images if not exist
if [ ! -f "$OUTPUT_DIR/temp_left_arm.png" ]; then
    echo "Extracting body regions..."
    ffmpeg -y -i "$CHAR_IMAGE" -vf "crop=${left_arm_w}:${left_arm_h}:${left_arm_x}:${left_arm_y}" "$OUTPUT_DIR/temp_left_arm.png" 2>/dev/null
    ffmpeg -y -i "$CHAR_IMAGE" -vf "crop=${right_arm_w}:${right_arm_h}:${right_arm_x}:${right_arm_y}" "$OUTPUT_DIR/temp_right_arm.png" 2>/dev/null
    ffmpeg -y -i "$CHAR_IMAGE" -vf "crop=${torso_w}:${torso_h}:${torso_x}:${torso_y}" "$OUTPUT_DIR/temp_torso.png" 2>/dev/null
    ffmpeg -y -i "$CHAR_IMAGE" -vf "crop=${head_w}:${head_h}:${head_x}:${head_y}" "$OUTPUT_DIR/temp_head.png" 2>/dev/null
    ffmpeg -y -i "$CHAR_IMAGE" -vf "crop=${left_leg_w}:${left_leg_h}:${left_leg_x}:${left_leg_y}" "$OUTPUT_DIR/temp_left_leg.png" 2>/dev/null
    ffmpeg -y -i "$CHAR_IMAGE" -vf "crop=${right_leg_w}:${right_leg_h}:${right_leg_x}:${right_leg_y}" "$OUTPUT_DIR/temp_right_leg.png" 2>/dev/null
    echo "Regions extracted"
fi

# Helper function to create a pose
# Args: output_name "left_arm_x,left_arm_y,right_arm_x,right_arm_y"
create_pose() {
    local outname=$1
    local ax1=$2
    local ay1=$3
    local ax2=$4
    local ay2=$5
    
    # Use pattern for output, then rename
    local tmpPattern="${OUTPUT_DIR}/temp_pose_%04d.jpg"
    
    ffmpeg -y -i "$CHAR_IMAGE" \
        -i "$OUTPUT_DIR/temp_left_arm.png" \
        -i "$OUTPUT_DIR/temp_right_arm.png" \
        -filter_complex "
        [0]split[base][bg];
        [bg]crop=${WIDTH}:${HEIGHT}:0:0[clean];
        [1]crop=${left_arm_w}:${left_arm_h}:0:0[armL];
        [2]crop=${right_arm_w}:${right_arm_h}:0:0[armR];
        [clean][armL]overlay=${ax1}:${ay1}[tmp1];
        [tmp1][armR]overlay=${ax2}:${ay2}
        " -frames:v 1 "$tmpPattern" 2>/dev/null
    
    # Rename the generated file
    local generated=$(ls -1 ${OUTPUT_DIR}/temp_pose_*.jpg 2>/dev/null | head -1)
    if [ -n "$generated" ]; then
        mv "$generated" "$OUTPUT_DIR/${outname}.jpg"
        echo "   ✅ ${outname}.jpg"
    else
        echo "   ❌ Failed: ${outname}"
    fi
}

echo ""
echo "Creating poses..."

# Pose 1: Arms raised
create_pose "pose_arms_raised" "$left_arm_x" "$((left_arm_y - 80))" "$right_arm_x" "$((right_arm_y - 80))"

# Pose 2: Arms crossed
create_pose "pose_arms_crossed" "$((left_arm_x + 50))" "$((left_arm_y + 30))" "$((right_arm_x - 50))" "$((right_arm_y + 30))"

# Pose 3: Hands on hips
create_pose "pose_hands_hips" "$((left_arm_x + 60))" "$((left_arm_y + 80))" "$((right_arm_x - 60))" "$((right_arm_y + 80))"

# Pose 4: Legs apart
# For legs, we need to use leg overlays - add extra inputs
# Let's simplify: create leg apart pose using leg region overlay

# Function for leg-based pose
create_leg_pose() {
    local outname=$1
    local lx=$2
    local ly=$3
    local rx=$4
    local ry=$5
    
    local tmpPattern="${OUTPUT_DIR}/temp_pose_%04d.jpg"
    
    ffmpeg -y -i "$CHAR_IMAGE" \
        -i "$OUTPUT_DIR/temp_left_leg.png" \
        -i "$OUTPUT_DIR/temp_right_leg.png" \
        -filter_complex "
        [0]split[base][bg];
        [bg]crop=${WIDTH}:${HEIGHT}:0:0[clean];
        [1]crop=${left_leg_w}:${left_leg_h}:0:0[legL];
        [2]crop=${right_leg_w}:${right_leg_h}:0:0[legR];
        [clean][legL]overlay=${lx}:${ly}[tmp1];
        [tmp1][legR]overlay=${rx}:${ry}
        " -frames:v 1 "$tmpPattern" 2>/dev/null
    
    local generated=$(ls -1 ${OUTPUT_DIR}/temp_pose_*.jpg 2>/dev/null | head -1)
    if [ -n "$generated" ]; then
        mv "$generated" "$OUTPUT_DIR}/${outname}.jpg"
        echo "   ✅ ${outname}.jpg"
    else
        echo "   ❌ Failed: ${outname}"
    fi
}

create_leg_pose "pose_legs_apart" "$((left_leg_x - 40))" "$left_leg_y" "$((right_leg_x + 40))" "$right_leg_y"

echo ""
echo "✅ Generated poses:"
ls -la "$OUTPUT_DIR"/pose_arms*.jpg "$OUTPUT_DIR"/pose_hands*.jpg "$OUTPUT_DIR"/pose_legs*.jpg 2>/dev/null

echo ""
echo "🎉 Done! Check: $OUTPUT_DIR"