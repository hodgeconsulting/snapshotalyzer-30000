#!/bin/bash
#
# Install the sacramental records app as an always-on background service
# on macOS, so it keeps running (and restarts after reboots or crashes)
# and is ready for remote access via Tailscale. Run it once, on the Mac
# that will act as the server:
#
#     cd sacraments
#     bash deploy/install-macos.sh
#
# Re-run it any time to apply changes (e.g. after a git pull). Uninstall
# with deploy/uninstall-macos.sh. See deploy/REMOTE_ACCESS.md for the full
# walkthrough including Tailscale.
#
set -euo pipefail

LABEL="com.parish.sacraments"
DEPLOY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(cd "$DEPLOY_DIR/.." && pwd)"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

# Use the project's virtualenv Python if it exists, else the system one.
if [ -x "$APP_DIR/venv/bin/python3" ]; then
  PYTHON="$APP_DIR/venv/bin/python3"
else
  PYTHON="$(command -v python3)"
fi

# Make sure the chosen Python can import the server dependencies.
if ! "$PYTHON" -c "import flask" 2>/dev/null; then
  echo "ERROR: Flask isn't installed for $PYTHON"
  echo "Install dependencies first, e.g.:"
  echo "    $PYTHON -m pip install -r \"$APP_DIR/requirements.txt\""
  exit 1
fi

# Database location. Defaults to iCloud Drive so records are backed up;
# override by exporting SACRAMENTS_DB before running this script.
DB_PATH="${SACRAMENTS_DB:-$HOME/Library/Mobile Documents/com~apple~CloudDocs/SacramentalRecords/sacraments.db}"
mkdir -p "$(dirname "$DB_PATH")"

PORT="${PORT:-5000}"

# A stable random secret key (signs session/flash cookies). Generated once
# and reused across reinstalls so logins/cookies survive restarts.
SECRET_FILE="$APP_DIR/.secret_key"
if [ ! -f "$SECRET_FILE" ]; then
  "$PYTHON" -c "import secrets; print(secrets.token_hex(32))" > "$SECRET_FILE"
  chmod 600 "$SECRET_FILE"
fi
SECRET="$(cat "$SECRET_FILE")"

LOG="$HOME/Library/Logs/sacraments.log"
mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"

cat > "$PLIST" <<PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON</string>
    <string>$APP_DIR/serve.py</string>
  </array>
  <key>WorkingDirectory</key><string>$APP_DIR</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>HOST</key><string>127.0.0.1</string>
    <key>PORT</key><string>$PORT</string>
    <key>FLASK_DEBUG</key><string>0</string>
    <key>SACRAMENTS_DB</key><string>$DB_PATH</string>
    <key>SACRAMENTS_SECRET_KEY</key><string>$SECRET</string>
  </dict>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
</dict>
</plist>
PLIST_EOF

# (Re)load the service.
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

echo "Installed and started: $LABEL"
echo "  Python:   $PYTHON"
echo "  App dir:  $APP_DIR"
echo "  Database: $DB_PATH"
echo "  Logs:     $LOG"
echo "  Local:    http://127.0.0.1:$PORT"
echo
echo "Next, expose it privately to your own devices with Tailscale:"
echo "    tailscale serve --bg $PORT"
echo "then open the https://<machine>.<tailnet>.ts.net URL it prints."
echo "Full guide: deploy/REMOTE_ACCESS.md"
