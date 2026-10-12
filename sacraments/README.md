# Parish Sacramental Records

A small, self-contained web application for keeping the sacramental
records of a parish of the Orthodox Church in America, and for printing
certificates and register pages for permanent filing in physical
binders.

## Registers

Four registers are maintained:

| Register | Certificate produced |
|---|---|
| Baptisms & Chrismations | Certificate of Baptism and Chrismation |
| Receptions into the Church (by Holy Chrismation or Confession of Faith) | Certificate of Reception into the Orthodox Church |
| Marriages | Certificate of Marriage |
| Funerals & Burials | Certificate of Christian Burial |

Every record carries a register reference (Entry No., Volume, Page) so
the electronic record always points back to its place in the physical
register book. Entry numbers are suggested automatically in sequence.

## Features

- Entry forms tailored to each sacrament (sponsors/godparents, name in
  religion, former confession and mode of reception, witnesses, civil
  license, place of interment, etc.)
- Parish settings (parish name, diocese, rector, address) merged onto
  every certificate and printed register page
- Print-ready certificates: US letter, decorative border, signature and
  seal block, and an "extract from the register" line — print from the
  browser at 100% scale and file in a binder
- Batch printing: a "Print All Certificates" page renders every
  certificate in a register, one per page, for printing a whole binder
  in a single pass
- Printable ledger-style register pages per sacrament
- Search across each register
- CSV export of each register for backup

## Prerequisites

- **Python 3.8 or newer.** Check with `python3 --version`. macOS ships
  with Python 3; on Windows, install it from <https://www.python.org>
  and tick "Add Python to PATH".
- **Flask**, which is not part of Python's standard library and must be
  installed once (see below).

## Running

The recommended way — a virtual environment keeps this app's Flask
install separate from the rest of your system and avoids permission
errors:

```
cd sacraments
python3 -m venv venv          # create the environment (first time only)
source venv/bin/activate       # macOS / Linux
# venv\Scripts\activate        # Windows PowerShell / cmd
pip install -r requirements.txt
python3 app.py
```

You'll see `(venv)` at the start of your prompt while the environment is
active. In future sessions just re-run the `activate` line, then
`python3 app.py` — you do not need to reinstall.

Simplest possible way (no virtual environment):

```
cd sacraments
python3 -m pip install flask
python3 app.py
```

Then open <http://localhost:5000>. On first use, fill in **Parish
Settings** — that information appears on every certificate.

To stop the app, press `Ctrl+C` in the terminal.

## Troubleshooting

**`ModuleNotFoundError: No module named 'flask'`**
Flask isn't installed for the Python interpreter that's running the app.
Install it into the *same* interpreter:

```
python3 -m pip install flask
```

Using `python3 -m pip` (rather than a bare `pip`) guarantees the install
goes to the same Python that runs `python3 app.py` — a mismatched
`python`/`pip` is the most common cause of this error. If you set up the
virtual environment above, make sure it is activated (you see `(venv)` in
your prompt) before running the app.

**`error: externally-managed-environment`** when installing Flask
Newer macOS (Homebrew) and Linux Pythons block installing into the
system Python. Use the virtual-environment steps above — that is the
clean fix. (As a last resort, `python3 -m pip install --user flask`
also works.)

**`command not found: python3`**
Python 3 isn't installed or isn't on your PATH. Install it from
<https://www.python.org>. On some Windows setups the command is `python`
instead of `python3`.

**`Address already in use` / port 5000 is taken**
Another program (on macOS, sometimes AirPlay Receiver) is using port
5000. Run the app on a different port:

```
PORT=5001 python3 app.py          # macOS / Linux
```

then open <http://localhost:5001>. On Windows PowerShell use
`$env:PORT=5001; python3 app.py`.

Records are stored in `sacraments.db` (SQLite) next to `app.py`; set
the `SACRAMENTS_DB` environment variable to store it elsewhere. Back up
that single file (or use the CSV export) to preserve your records.

## Using it from an iPad (or iPhone / another computer)

The app is a normal web page, so any device with a browser can use it —
including an iPad — as long as it can reach the computer that is running
the app. The recommended setup is to **run the app on a Mac (or other
computer) and open it in Safari on the iPad over your local Wi-Fi.** The
records stay on that computer; nothing goes to the cloud.

By default the app only answers requests from the computer it runs on.
To let other devices on your network reach it, start it with
`HOST=0.0.0.0`:

```
cd sacraments
HOST=0.0.0.0 python3 app.py
```

Then find that computer's local network address and open it on the iPad.

1. **On the Mac, find its LAN IP address:**
   ```
   ipconfig getifaddr en0        # Wi-Fi; try en1 if that is blank
   ```
   You'll get something like `192.168.1.50`.
2. **On the iPad**, make sure it's on the **same Wi-Fi network**, open
   Safari, and go to:
   ```
   http://192.168.1.50:5000
   ```
   (substitute your Mac's address). In Safari you can tap **Share → Add
   to Home Screen** to get an app-like icon that opens straight to it.

Printing works from the iPad too: use Safari's **Share → Print** (AirPrint)
for certificates and register pages.

Notes and cautions:

- **The Mac must be on and running the app** for the iPad to reach it.
  The iPad is only displaying the page; the Mac does the work and holds
  the data.
- **Keep it to your home/parish Wi-Fi.** `HOST=0.0.0.0` exposes the app
  to everyone on that network with no password, so don't do this on
  public or shared Wi-Fi. For safety the app automatically turns its
  developer debugger **off** whenever it is served to the network.
- **This is a local-network setup, not internet access.** Reaching it
  from outside your building would mean exposing the app publicly, which
  this simple app isn't built to do securely — tell me if you need that
  and we'll design it properly (authentication, HTTPS, etc.).

### Running natively on the iPad (advanced, usually not worth it)

It is technically possible to run the Python server on the iPad itself
using a terminal app such as **a-Shell** (free, App Store):
`pip install flask`, then `python app.py`, then open
`http://localhost:5000` in Safari. It works but is slow and fiddly, and
your records would live only inside that app's sandbox. The Mac-plus-Safari
approach above is simpler and keeps your data in one place.

## Storing your records in iCloud (macOS)

Because the database location is just the `SACRAMENTS_DB` environment
variable, you can keep the file in iCloud Drive so it is backed up
offsite and available across your Macs.

**1. Stop the app first** (`Ctrl+C`). Never move the database while it
is in use.

**2. Move the file into iCloud Drive:**

```
mkdir -p ~/Library/Mobile\ Documents/com~apple~CloudDocs/SacramentalRecords
mv ~/snapshotalyzer-30000/sacraments/sacraments.db \
   ~/Library/Mobile\ Documents/com~apple~CloudDocs/SacramentalRecords/
```

(iCloud Drive lives at `~/Library/Mobile Documents/com~apple~CloudDocs/`.
In Finder it appears as **iCloud Drive → SacramentalRecords**.)

**3. Point the app at the iCloud copy permanently** by adding the
variable to your shell profile, so every terminal uses it:

```
echo 'export SACRAMENTS_DB="$HOME/Library/Mobile Documents/com~apple~CloudDocs/SacramentalRecords/sacraments.db"' >> ~/.zshrc
source ~/.zshrc
```

After that, a plain `python3 app.py` uses the iCloud database. (For a
one-off run without editing your profile, prefix the command instead:
`SACRAMENTS_DB="$HOME/Library/Mobile Documents/com~apple~CloudDocs/SacramentalRecords/sacraments.db" python3 app.py`.)

### Important cautions

iCloud is a *file sync* service, not a live-database server, so:

- **Run the app on only one Mac at a time.** Two Macs writing the same
  database mid-sync can corrupt it or lose records. iCloud is safe as a
  single-machine store plus offsite backup — not as a way to run the app
  on two computers at once.
- **Quit the app before switching machines**, and wait for iCloud to
  finish uploading (the cloud icon by the file in Finder shows sync
  status) before opening it on the other Mac.
- **Prevent iCloud from evicting the file.** When disk is low, iCloud may
  move the file to the cloud only. Right-click the SacramentalRecords
  folder in Finder → **Keep Downloaded**. If the app ever can't find the
  database, click the download (cloud) icon on the file in Finder.
- **Still export CSV backups** (the Export CSV button). A synced `.db`
  protects against a dead drive; a CSV protects against the database file
  itself being damaged.
- **If you ever copy the database by hand**, also copy any
  `sacraments.db-wal` / `sacraments.db-shm` sidecar files that exist
  next to it. Always quitting the app before it syncs avoids this
  entirely.

## Customizing

Field lists, register columns, and certificate titles are defined
declaratively in `config.py` — the forms, detail pages, register
printouts, and CSV export all follow from those definitions. The
certificate wording lives in `templates/certificate_*.html`.
