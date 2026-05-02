#!/bin/bash
# Multi-Character Scene with Props
# Nomark + Ally vs Villain

OUTPUT="/home/openclaw/.openclaw/workspace/comic_series/assets/output"
LOCATIONS="/home/openclaw/.openclaw/workspace/comic_series/assets/locations"
CHAR_NOMARK="/home/openclaw/.openclaw/workspace/comic_series/assets/characters/nomark/parts_detailed"
CHAR_VILLAIN="/home/openclaw/.openclaw/workspace/comic_series/assets/characters/villain/parts_detailed"
CHAR_ALLY="/home/openclaw/.openclaw/workspace/comic_series/assets/characters/ally/parts_detailed"

mkdir -p "$OUTPUT/team_scene"
rm -f "$OUTPUT/team_scene"/*.png

echo "=== TEAM SCENE ==="

BACKGROUND="$LOCATIONS/futuristic_street_night.jpg"

# Scene setup: Nomark and Ally on left, Villain on right
LINE1="NOMARK: We together will stop you."
LINE2="ALLY: You've gone too far."
LINE3="VILLAIN: Two against one? I'm still untouchable."
LINE4="NOMARK: Not today."

LINES=("$LINE1" "$LINE2" "$LINE3" "$LINE4")
FRAME_DELAY=36

for frame in $(seq 0 143); do
    frame_num=$(printf "%04d" $frame)
    
    line_idx=$((frame / FRAME_DELAY))
    if [ $line_idx -ge 4 ]; then line_idx=3; fi
    
    DIALOGUE="${LINES[$line_idx]}"
    
    # Positions
    nomark_x=120
    ally_x=200
    villain_x=420
    
    ffmpeg -y -f lavfi -i "color=c=#101018:s=640x360" \
           -loop 1 -i "$BACKGROUND" \
           -i "$CHAR_VILLAIN/torso.png" \
           -i "$CHAR_VILLAIN/head.png" \
           -i "$CHAR_ALLY/torso.png" \
           -i "$CHAR_ALLY/head.png" \
           -i "$CHAR_NOMARK/torso.png" \
           -i "$CHAR_NOMARK/head.png" \
           -filter_complex "
               [0:v][1:v]overlay=0:0[bg];
               [bg][2:v]overlay=$villain_x:100[vil_t];
               [vil_t][3:v]overlay=$((villain_x+35)):50[vil];
               [vil][4:v]overlay=$ally_x:100[ally_t];
               [ally_t][5:v]overlay=$((ally_x+35)):50[ally];
               [ally][6:v]overlay=$nomark_x:100[nom_t];
               [nom_t][7:v]overlay=$((nomark_x+35)):50,
               drawtext=text='$DIALOGUE':fontcolor=white:fontsize=18:x=(w-text_w)/2:y=320:shadowcolor=black:shadowx=2:shadowy=2
           " -frames:v 1 "$OUTPUT/team_scene/frame_$frame_num.png" 2>/dev/null
    
    if [ $((frame % 24)) -eq 0 ]; then
        echo "  Frame $frame"
    fi
done

echo "Rendering..."
ffmpeg -framerate 12 -i "$OUTPUT/team_scene/frame_%04d.png" \
       -c:v libx264 -pix_fmt yuv420p -vf scale=640:360 \
       -t 16 "$OUTPUT/team_scene.mp4" -y 2>&1 | tail -3

echo "Result:"
ls -lh "$OUTPUT/team_scene.mp4"