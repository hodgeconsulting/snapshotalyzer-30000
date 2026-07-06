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

## Running

```
pip install flask
cd sacraments
python3 app.py
```

Then open <http://localhost:5000>. On first use, fill in **Parish
Settings** — that information appears on every certificate.

Records are stored in `sacraments.db` (SQLite) next to `app.py`; set
the `SACRAMENTS_DB` environment variable to store it elsewhere. Back up
that single file (or use the CSV export) to preserve your records.

## Customizing

Field lists, register columns, and certificate titles are defined
declaratively in `config.py` — the forms, detail pages, register
printouts, and CSV export all follow from those definitions. The
certificate wording lives in `templates/certificate_*.html`.
