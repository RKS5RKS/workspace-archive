#!/bin/bash
# Character Asset Generator using FFmpeg
# Creates basic character shapes using FFmpeg filters

ASSETS="/home/openclaw/.openclaw/workspace/comic_series/assets"
OUTPUT_DIR="$ASSETS/characters"

# Colors (hex)
SKIN_COLOR="#ffccb1" # Light Peach
SHIRT_BLUE="#3264c8"
SHIRT_RED="#801010"
SHIRT_GREEN="#329650"
PANTS_DARK="#283250" # Dark Navy
PANTS_BLACK="#141414"
HAIR_COLOR="#28190f" # Dark Brown
LIP_COLOR="#b46464"

# Function to create asset part
# Parameters:
# $1: character name (nomark, villain, ally)
# $2: part name (head, torso, etc.)
# $3: ffmpeg command string for the part
# $4: output file name (e.g., head.png)
create_part() {
    local name=$1
    local part_name=$2
    local ffmpeg_command_string=$3
    local output_filename=$4
    local output_dir="$OUTPUT_DIR/$name/parts_detailed"
    
    mkdir -p "$output_dir"
    
    echo "Creating $part_name for $name..."
    # Execute the FFmpeg command
    eval "$ffmpeg_command_string -update 1 -frames:v 1 \"$output_dir/$output_filename\" -y 2>/dev/null"
    
    if [ $? -eq 0 ]; then
        echo "  Created $output_dir/$output_filename"
    else
        echo "  ERROR creating $output_dir/$output_filename"
    fi
}

# Head - using solid color with drawbox for features
# Removed 'r' option as it's not supported in this FFmpeg version.
create_head() {
    local name=$1
    ffmpeg_cmd="ffmpeg -f lavfi -i \"color=c=$SKIN_COLOR:s=150x180:d=1\" -vf \
        \"drawbox=x=25:y=10:w=100:h=130:color=$SKIN_COLOR:fill=1,\
         drawcircle=75:55:35:color=$SKIN_COLOR:fill=1,\
         drawbox=x=40:y=50:w=25:h=20:color=white:fill=1,\
         drawcircle=52:58:7:color=black:fill=1,\
         drawbox=x=85:y=50:w=25:h=20:color=white:fill=1,\
         drawcircle=97:58:7:color=black:fill=1,\
         drawbox=x=50:y=40:w=50:h=20:color=$HAIR_COLOR:fill=1,\
         drawbox=x=62:y=110:w=25:h=20:color=$LIP_COLOR:fill=1\""
    create_part "$name" "head" "$ffmpeg_cmd" "head.png"
}

# Torso
# Removed 'r' option. Added simple neck/collar line.
create_torso() {
    local name=$1
    local color=$2
    ffmpeg_cmd="ffmpeg -f lavfi -i \"color=c=$color:s=150x200:d=1\" -vf \
        \"drawbox=x=30:y=0:w=90:h=180:color=$color:fill=1,\
         drawbox=x=30:y=170:w=90:h=10:color=#cccccc:fill=1, \
         drawbox=x=60:y=140:w=30:h=50:color=$SKIN_COLOR:fill=1\""
    create_part "$name" "torso" "$ffmpeg_cmd" "torso.png"
}

# Arm (generic, will be mirrored/placed)
# Removed 'r' option. Adjusted dimensions and positions for square edges.
create_arm() {
    local name=$1
    local color=$2
    local side=$3 # left or right
    local arm_width=35
    local arm_height=110
    local shoulder_y=0
    local elbow_y=$((arm_height / 2))
    local hand_y=$(($elbow_y + arm_height / 2))
    
    local x_offset=0
    local base_color=$color
    local skin_color=$SKIN_COLOR
    
    local cmd_args=""
    
    if [ "$side" = "left" ]; then
        x_offset=30 # Position relative to torso origin
        cmd_args="drawbox=x=$x_offset:y=$shoulder_y:w=$arm_width:h=$elbow_y:color=$base_color:fill=1,\
                  drawbox=x=$x_offset:y=$elbow_y:w=$((arm_width)):h=$((arm_height - elbow_y)):color=$skin_color:fill=1,\
                  drawbox=x=$((x_offset + 5)):y=$hand_y:w=$((arm_width - 10)):h=30:color=$skin_color:fill=1"
    else # right
        x_offset=85 # Position relative to torso origin
        cmd_args="drawbox=x=$x_offset:y=$shoulder_y:w=$arm_width:h=$elbow_y:color=$base_color:fill=1,\
                  drawbox=x=$((x_offset + 5)):y=$elbow_y:w=$((arm_width)):h=$((arm_height - elbow_y)):color=$skin_color:fill=1,\
                  drawbox=x=$((x_offset + 5)):y=$hand_y:w=$((arm_width - 10)):h=30:color=$skin_color:fill=1"
    fi

    ffmpeg_cmd="ffmpeg -f lavfi -i \"color=c=$base_color:s=150x200:d=1\" -vf \"$cmd_args\""
    create_part "$name" "arm_$side" "$ffmpeg_cmd" "${side}_arm.png"
}

# Leg (generic, will be placed)
# Removed 'r' option. Adjusted dimensions and positions for square edges.
create_leg() {
    local name=$1
    local color=$2
    local pants_color=$PANTS_DARK
    local leg_width=35
    local leg_height=140
    local thigh_y=0
    local knee_y=$((leg_height / 2))
    local foot_y=$(($knee_y + leg_height / 2))
    
    local x_offset=0
    
    ffmpeg_cmd="ffmpeg -f lavfi -i \"color=c=$pants_color:s=80x200:d=1\" -vf \
        \"drawbox=x=$x_offset:y=$thigh_y:w=$leg_width:h=$knee_y:color=$pants_color:fill=1,\
         drawbox=x=$x_offset:y=$knee_y:w=$((leg_width)):h=$((leg_height - knee_y)):color=$pants_color:fill=1,\
         drawbox=x=$((x_offset + 5)):y=$foot_y:w=$((leg_width - 5)):h=40:color=#1e1e1e:fill=1\""
    create_part "$name" "leg" "$ffmpeg_cmd" "leg.png"
}

echo "Generating character assets with FFmpeg..."
echo ""

# Nomark (blue shirt, dark pants)
create_head "nomark"
create_torso "nomark" "$SHIRT_BLUE"
create_arm "nomark" "$SHIRT_BLUE" "left"
create_arm "nomark" "$SHIRT_BLUE" "right"
create_leg "nomark" "$PANTS_DARK"

# Villain (red shirt, black pants)
create_head "villain"
create_torso "villain" "$SHIRT_RED"
create_arm "villain" "$SHIRT_RED" "left"
create_arm "villain" "$SHIRT_RED" "right"
create_leg "villain" "$PANTS_BLACK"

# Ally (green shirt, gray pants)
create_head "ally"
create_torso "ally" "$SHIRT_GREEN"
create_arm "ally" "$SHIRT_GREEN" "left"
create_arm "ally" "$SHIRT_GREEN" "right"
create_leg "ally" "#32323c"

echo ""
echo "Done!"