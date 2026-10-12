#!/bin/bash
#
# Stop and remove the sacramental records background service installed by
# install-macos.sh. Your records (the database file) are NOT touched.
#
#     cd sacraments
#     bash deploy/uninstall-macos.sh
#
set -euo pipefail

LABEL="com.parish.sacraments"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

launchctl unload "$PLIST" 2>/dev/null || true
rm -f "$PLIST"

echo "Stopped and removed: $LABEL"
echo "Your records were left untouched."
echo "To also stop remote access, run: tailscale serve reset"
