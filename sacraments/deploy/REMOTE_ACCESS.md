# Remote Access (private, via Tailscale)

This guide sets up secure remote access to your sacramental records so
you can use the app from your iPad, phone, or laptop **anywhere with an
internet connection** — while keeping all the records on your Mac and off
the public internet.

## How it works

```
  Your iPad / phone / laptop                      Your Mac (always on)
  (anywhere with internet)                        at the parish or home
 ┌────────────────────────┐                      ┌──────────────────────────┐
 │ Safari                 │   encrypted, private  │ Tailscale → the app       │
 │ https://<mac>.<net>    │◄───── Tailscale ─────►│  (HTTPS)        :5000      │
 │        .ts.net         │  only YOUR devices    │ records: sacraments.db     │
 └────────────────────────┘                      └──────────────────────────┘
```

- **Tailscale** is a free service that builds a private, encrypted
  network ("tailnet") between *your own devices only*. Nothing is exposed
  to the public internet.
- **Tailscale is the login.** A device can only join your tailnet after
  you sign in with your account (Apple/Google/Microsoft/etc.) and approve
  it. That is why the app itself doesn't need its own password for a
  single user.
- **The records never leave the Mac.** Your devices just display pages
  served by the Mac. The database stays in one place.
- **Real HTTPS, no domain needed.** Tailscale Serve gives the Mac a
  address like `https://macmini.tailxxxx.ts.net` with a valid
  certificate, so Safari shows the lock icon and no warnings.

## One-time setup

### 1. Install Tailscale on the Mac (the server)

- Download from <https://tailscale.com/download/mac> (or `brew install
  --cask tailscale`), open it, and **sign in**. Pick a personal account;
  the free plan is plenty for this.
- After signing in, note the Mac's tailnet name. In the Tailscale menu
  bar icon, or at <https://login.tailscale.com/admin/machines>, you'll
  see a name like `macmini` and a full address like
  `macmini.tailXXXX.ts.net`.
- In the admin console, make sure **MagicDNS** and **HTTPS
  certificates** are enabled (Settings → "Features"/"DNS"). These let
  Tailscale Serve issue the HTTPS address. They're on by default for new
  tailnets.

### 2. Make the app run always-on

From the `sacraments` folder on the Mac (after installing dependencies —
see the main README):

```
cd sacraments
python3 -m pip install -r requirements.txt     # includes waitress
bash deploy/install-macos.sh
```

This installs a background service (launchd) that:

- starts the app automatically at login and **restarts it** if it crashes
  or the Mac reboots,
- runs it on a real server (waitress), bound to `127.0.0.1:5000` (local
  only — Tailscale will provide the remote path),
- stores records in your iCloud Drive database by default (override by
  running `SACRAMENTS_DB="/some/path/sacraments.db" bash
  deploy/install-macos.sh`),
- generates a private secret key once and keeps it.

Check it's up: open <http://127.0.0.1:5000> on the Mac. Logs are at
`~/Library/Logs/sacraments.log`.

### 3. Publish it to your tailnet (HTTPS)

```
tailscale serve --bg 5000
```

This proxies `https://<mac>.<tailnet>.ts.net` → the app on port 5000,
reachable **only by devices on your tailnet**. Confirm with:

```
tailscale serve status
```

It prints the exact `https://…ts.net` URL. (If your Tailscale version
uses different wording, `tailscale serve --help` shows the current form;
older versions used `tailscale serve https / 5000`.)

### 4. Add your iPad (and any other device)

- Install **Tailscale** from the App Store on the iPad and **sign in with
  the same account**. Approve the device if prompted.
- In Safari, go to the `https://<mac>.<tailnet>.ts.net` URL from step 3.
- Tap **Share → Add to Home Screen** for an app-like icon that opens
  straight to your records.

That's it. From then on, as long as the Mac is on and the iPad has
internet, you can open the records from anywhere. Printing works through
Safari's **Share → Print** (AirPrint).

## Everyday notes

- **The Mac must stay on and awake.** In System Settings → Energy /
  Lock Screen, set the Mac to not sleep (or to allow network access while
  sleeping). A Mac Mini acting as the server is ideal for this.
- **Only this one Mac should run the app.** It is the single source of
  truth for the records. Don't run `app.py` on another computer against
  the same iCloud database at the same time.
- **Back up regularly** with the Export CSV button, in addition to the
  iCloud copy of the database.

## Managing it

| Task | Command (in the `sacraments` folder on the Mac) |
|---|---|
| See if it's running | `launchctl list \| grep sacraments` |
| View logs | `tail -f ~/Library/Logs/sacraments.log` |
| Restart after a `git pull` | `bash deploy/install-macos.sh` |
| Stop remote publishing | `tailscale serve reset` |
| Stop & remove the service | `bash deploy/uninstall-macos.sh` |

## If you later want to share with others

For just you, Tailscale's device login is the whole security story. If
you later need to give access to a secretary or clergy, two good options:

- **Invite them to your tailnet** (Tailscale supports sharing a single
  machine with specific people) — still no app password needed, and still
  nothing on the public internet.
- If you need people to log in from devices where they *can't* install
  Tailscale, we'd add a proper username/password login to the app and
  (optionally) a public address via Cloudflare. Ask and I'll design it.

## Security summary

- No part of the app is exposed to the public internet; only devices you
  signed in and approved can reach it.
- Traffic is end-to-end encrypted by Tailscale, and HTTPS on top via
  Tailscale Serve.
- Flask's code-executing debugger is force-disabled whenever the app is
  not on localhost, and the service runs it with debug off regardless.
- The session secret key is random, stored with `600` permissions, and
  never committed to git (`.gitignore` excludes `.secret_key`).
