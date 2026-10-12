"""Production runner for always-on deployment (e.g. behind Tailscale).

app.py's built-in `python3 app.py` uses Flask's development server, which
is fine for local use but prints warnings and isn't meant to run for days
at a time. This runner serves the same app with waitress, a small,
robust, pure-Python WSGI server, when it's installed; otherwise it falls
back to the built-in server so the app still starts.

It honors the same environment variables as app.py:
  HOST   - interface to bind (default 127.0.0.1; Tailscale Serve proxies
           to this, so localhost is the right, safest default)
  PORT   - port to listen on (default 5000)
  SACRAMENTS_DB, SACRAMENTS_SECRET_KEY - as in app.py

Run with:  python3 serve.py
"""

import os

from app import app  # importing runs init_db(); the dev-server block does not run


def main():
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 5000))
    try:
        from waitress import serve
    except ImportError:
        print("waitress not installed; using Flask's development server. "
              "For always-on use, install it: python3 -m pip install waitress")
        app.run(host=host, port=port, debug=False)
        return
    print(f"Serving sacramental records on http://{host}:{port} (waitress)")
    serve(app, host=host, port=port, threads=8)


if __name__ == "__main__":
    main()
