#!/bin/bash
# Auto-backup script for OpenClaw workspace
# Runs hourly - backs up ALL workspace files

cd /home/openclaw/.openclaw/workspace || exit 1

# Define what to backup (everything needed)
BACKUP_ITEMS="MEMORY.md memory/ press/ sponsors/ collab/ AGENTS.md USER.md IDENTITY.md SOUL.md TOOLS.md HEARTBEAT.md"

cd /home/openclaw/.openclaw/workspace/heyronbackup || exit 1

# Copy all workspace files
for item in $BACKUP_ITEMS; do
    cp -r /home/openclaw/.openclaw/workspace/$item . 2>/dev/null
done

# Add and commit
git add -A
git commit -m "Auto-backup $(date +%Y-%m-%d\ %H:%M)" 2>/dev/null

# Push
git push origin main 2>/dev/null

echo "Backup complete: $(date)"