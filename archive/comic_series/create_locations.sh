#!/bin/bash
# Scene Location Generator
# Creates background images for different locations

OUTPUT="/home/openclaw/.openclaw/workspace/comic_series/assets/locations"
mkdir -p "$OUTPUT"

echo "Creating location backgrounds..."

# Location 1: Alley at Night
ffmpeg -f lavfi -i "color=c=#0a0a15:s=640x360" \
       -vf "drawbox=x=0:y=280:w=640:h=80:color=#1a1a25:fill=1,\
            drawbox=x=500:y=150:w=80:h=200:color=#151520:fill=1,\
            drawbox=x=50:y=200:w=60:h=150:color=#12121a:fill=1,\
            drawbox=x=150:y=250:w=40:h=40:color=#ffcc00:fill=1" \
       -frames:v 1 "$OUTPUT/alley_night.png" -y 2>/dev/null
echo "  alley_night.png"

# Location 2: Rooftop
ffmpeg -f lavfi -i "color=c=#1a1a2e:s=640x360" \
       -vf "drawbox=x=0:y=280:w=640:h=80:color=#0f0f1a:fill=1,\
            drawbox=x=100:y=200:w=150:h=100:color=#252535:fill=1,\
            drawbox=x=400:y=180:w=180:h=120:color=#202030:fill=1,\
            drawcircle=550:80:40:color=#ffffff:fill=1,\
            drawbox=x=0:y=0:w=50:h=360:color=#0a0a15:fill=1" \
       -frames:v 1 "$OUTPUT/rooftop.png" -y 2>/dev/null
echo "  rooftop.png"

# Location 3: Street
ffmpeg -f lavfi -i "color=c=#1f1f2f:s=640x360" \
       -vf "drawbox=x=0:y=290:w=640:h=70:color=#2a2a3a:fill=1,\
            drawbox=x=80:y=150:w=100:h=200:color=#15151f:fill=1,\
            drawbox=x=450:y=180:w=120:h=180:color=#181825:fill=1,\
            drawbox=x=200:y=220:w=30:h=30:color=#ffcc00:fill=1,\
            drawbox=x=350:y=210:w=25:h=25:color=#ffcc00:fill=1,\
            drawbox=x=0:y=120:w=60:h=360:color=#101018:fill=1" \
       -frames:v 1 "$OUTPUT/street.png" -y 2>/dev/null
echo "  street.png"

# Location 4: Warehouse Interior
ffmpeg -f lavfi -i "color=c=#15151f:s=640x360" \
       -vf "drawbox=x=0:y=0:w=640:h=50:color=#0a0a10:fill=1,\
            drawbox=x=0:y=0:w=50:h=360:color=#0a0a10:fill=1,\
            drawbox=x=590:y=0:w=50:h=360:color=#0a0a10:fill=1,\
            drawbox=x=100:y=100:w=80:h=150:color=#252530:fill=1,\
            drawbox=x=450:y=80:w=100:h=180:color=#202028:fill=1,\
            drawbox=x=250:y=200:w=120:h=80:color=#303040:fill=1" \
       -frames:v 1 "$OUTPUT/warehouse.png" -y 2>/dev/null
echo "  warehouse.png"

# Location 5: Subway Station
ffmpeg -f lavfi -i "color=c=#252530:s=640x360" \
       -vf "drawbox=x=0:y=300:w=640:h=60:color=#1a1a25:fill=1,\
            drawbox=x=80:y=150:w=100:h=200:color=#1f1f28:fill=1,\
            drawbox=x=450:y=180:w=120:h=180:color=#181820:fill=1,\
            drawbox=x=200:y=100:w=40:h=100:color=#ffcc00:fill=1,\
            drawbox=x=220:y=100:w=40:h=100:color=#ffaa00:fill=1,\
            drawbox=x=0:y=0:w=640:h=30:color=#101015:fill=1" \
       -frames:v 1 "$OUTPUT/subway.png" -y 2>/dev/null
echo "  subway.png"

echo ""
echo "Done! Created 5 location backgrounds"
ls -la "$OUTPUT"