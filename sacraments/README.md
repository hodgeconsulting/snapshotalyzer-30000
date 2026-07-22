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

## Customizing

Field lists, register columns, and certificate titles are defined
declaratively in `config.py` — the forms, detail pages, register
printouts, and CSV export all follow from those definitions. The
certificate wording lives in `templates/certificate_*.html`.
