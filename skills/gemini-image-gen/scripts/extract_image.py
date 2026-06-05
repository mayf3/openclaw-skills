#!/usr/bin/env python3
"""Extract a generated image from Gemini via CDP Canvas-to-base64 trick.

Usage:
    python3 extract_image.py <tab_id> <output_path> [--cdp-port 9222]

Reads the first <img> with a blob: src on the page, draws it to a canvas,
exports as PNG base64, and writes the decoded bytes to <output_path>.
"""
import argparse
import base64
import json
import os
import sys
import urllib.request

CDP_HOST = "127.0.0.1"

# ---------- CDP helpers (minimal, no websockets dependency) ----------

def _ws_url(tab_id: str, port: int) -> str:
    """Get the debugger websocket URL for a tab."""
    tabs = json.loads(urllib.request.urlopen(f"http://{CDP_HOST}:{port}/json/list").read())
    for t in tabs:
        if t["id"] == tab_id:
            return t["webSocketDebuggerUrl"]
    raise SystemExit(f"Tab {tab_id!r} not found")


def _cdp_send(ws, method: str, params: dict | None = None):
    """Send a CDP command and return the result."""
    import importlib
    ws_mod = importlib.import_module("websockets.sync.client")
    ws_cls = ws_mod.connect

    url = ws
    conn = None
    # we open a fresh ws per call for simplicity
    import uuid
    msg_id = uuid.uuid4().int % (2**53)
    payload = {"id": msg_id, "method": method, "params": params or {}}
    # Actually we need to reuse — let's use the approach from cdp_exec.py
    # Re-use the existing cdp_exec helper instead
    raise RuntimeError("Use cdp_exec.py eval instead")


def cdp_eval_http(tab_id: str, expr: str, port: int = 9222, await_promise: bool = False) -> str:
    """Evaluate JS via CDP using the shared brave-browser-agent cdp_exec.py."""
    import subprocess
    # Use the shared brave-browser-agent's cdp_exec.py (port 9222)
    brave_agent_dir = os.path.expanduser("brave-browser-agent/scripts")
    cdp_script = os.path.join(brave_agent_dir, "cdp_exec.py")
    cmd = [
        sys.executable,
        cdp_script,
        "--port", str(port),
        "eval", tab_id, expr,
    ]
    if await_promise:
        cmd.append("--await-promise")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        raise RuntimeError(f"cdp_exec failed: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser(description="Extract generated image from Gemini tab")
    ap.add_argument("tab_id", help="CDP tab ID of the Gemini page")
    ap.add_argument("output_path", help="Where to save the PNG file")
    ap.add_argument("--cdp-port", type=int, default=9222)
    args = ap.parse_args()

    port = args.cdp_port
    tab = args.tab_id
    out = args.output_path

    # 1. Find the LAST blob: image (most recent generation) to avoid stale cache
    js_find = """
    (function() {
        var imgs = document.querySelectorAll('img');
        for (var i = imgs.length - 1; i >= 0; i--) {
            if (imgs[i].src && imgs[i].src.startsWith('blob:') && imgs[i].naturalWidth > 100) {
                return JSON.stringify({idx: i, src: imgs[i].src.substring(0, 60), w: imgs[i].naturalWidth, h: imgs[i].naturalHeight, direction: 'last'});
            }
        }
        return 'NOT_FOUND';
    })()
    """
    info = cdp_eval_http(tab, js_find, port)
    if info == "NOT_FOUND":
        raise SystemExit("No blob image found on the page. The image may not be ready yet.")

    print(f"Found image: {info}")

    # 2. Draw to canvas and store base64 in window._imgb64
    js_canvas = """
    (function() {
        var imgs = document.querySelectorAll('img');
        var img = null;
        // Pick the LAST blob: image (most recent generation) to avoid stale cache
        for (var i = imgs.length - 1; i >= 0; i--) {
            if (imgs[i].src && imgs[i].src.startsWith('blob:') && imgs[i].naturalWidth > 100) {
                img = imgs[i]; break;
            }
        }
        if (!img) return 'NO_IMG';
        var c = document.createElement('canvas');
        c.width = img.naturalWidth; c.height = img.naturalHeight;
        c.getContext('2d').drawImage(img, 0, 0);
        window._imgb64 = c.toDataURL('image/png').split(',')[1];
        return 'OK:' + window._imgb64.length;
    })()
    """
    result = cdp_eval_http(tab, js_canvas, port, await_promise=True)
    print(f"Canvas export: {result}")
    if not result.startswith("OK:"):
        raise SystemExit(f"Canvas export failed: {result}")

    total_len = int(result.split(":")[1])

    # 3. Read base64 in chunks
    chunk_size = 50000
    parts = []
    offset = 0
    while offset < total_len:
        end = min(offset + chunk_size, total_len)
        js_chunk = f"window._imgb64.substring({offset},{end})"
        chunk = cdp_eval_http(tab, js_chunk, port)
        parts.append(chunk)
        offset = end

    img_data = base64.b64decode("".join(parts))

    # 4. Write file
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "wb") as f:
        f.write(img_data)
    print(f"Saved {len(img_data)} bytes to {out}")


if __name__ == "__main__":
    main()
