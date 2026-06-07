#!/usr/bin/env python3
"""10-1_mermaid_render.py — Mermaid (.mmd) → PNG előrenderelő a MARP prezihez.

A MARP nem rendereli a Mermaidot natívan (kódként kerül a PPTX-be), ezért a
prezi diagramjait előre PNG-vé alakítjuk. A render a mermaid-cli (mmdc) +
egy headless Chromium párossal történik.

Bemenet: egy mappa `.mmd` fájlokkal (alapért. `<week>/4_wip_outputs/_prezi_assets/`).
Kimenet: ugyanott `.png` fájlok, fájlnév-egyezéssel (navigator.mmd -> navigator.png).

Környezeti előfeltételek (lásd project_status B-15):
  1. headless Chromium:  npx puppeteer browsers install chrome-headless-shell
  2. mermaid-cli (böngésző-letöltés nélkül):
       $env:PUPPETEER_SKIP_DOWNLOAD="true"; npm install @mermaid-js/mermaid-cli
  3. puppeteer-config JSON (executablePath FORWARD-slash úttal + ["--no-sandbox"])

Felülírható env-változók:
  MMDC_CLI    – a mermaid-cli `cli.js` teljes útja
  PPTR_CFG    – a puppeteer-config JSON útja
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_CLI = REPO / "test_outputs" / "_tools" / "node_modules" / "@mermaid-js" / "mermaid-cli" / "src" / "cli.js"


def find_chromium() -> str | None:
    """Megkeresi a használható headless Chromiumot (puppeteer cache vagy Edge)."""
    cache = Path.home() / ".cache" / "puppeteer" / "chrome-headless-shell"
    if cache.is_dir():
        hits = list(cache.glob("*/*/chrome-headless-shell.exe")) + list(cache.glob("*/*/chrome-headless-shell"))
        if hits:
            return str(hits[0]).replace("\\", "/")
    for edge in [
        r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
        r"C:/Program Files/Microsoft/Edge/Application/msedge.exe",
        "/usr/bin/google-chrome",
    ]:
        if Path(edge).exists():
            return edge
    return None


def ensure_config(week_dir: Path) -> Path:
    """Puppeteer-config előállítása (ha nincs PPTR_CFG env)."""
    env_cfg = os.environ.get("PPTR_CFG")
    if env_cfg:
        return Path(env_cfg)
    chromium = find_chromium()
    if not chromium:
        sys.exit("HIBA: nem található headless Chromium. Telepítsd: "
                 "npx puppeteer browsers install chrome-headless-shell")
    cfg = week_dir / "4_wip_outputs" / "_prezi_assets" / "_pptcfg.json"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(json.dumps({"executablePath": chromium, "args": ["--no-sandbox"]}),
                   encoding="utf-8")
    return cfg


def main() -> int:
    ap = argparse.ArgumentParser(description="Mermaid .mmd -> PNG a MARP prezihez")
    ap.add_argument("--week-dir", required=True, help="Heti mappa, pl. test_outputs/atg/1_het")
    ap.add_argument("--scale", default="2", help="Felbontás-szorzó (alap: 2)")
    ap.add_argument("--bg", default="white", help="Háttér (alap: white; 'transparent' is lehet)")
    args = ap.parse_args()

    week = Path(args.week_dir)
    assets = week / "4_wip_outputs" / "_prezi_assets"
    if not assets.is_dir():
        sys.exit(f"HIBA: nincs ilyen mappa: {assets}")

    cli = Path(os.environ.get("MMDC_CLI", DEFAULT_CLI))
    if not cli.exists():
        sys.exit(f"HIBA: mermaid-cli nem található: {cli}\n"
                 "Telepítsd (böngésző-letöltés nélkül): "
                 'PUPPETEER_SKIP_DOWNLOAD=true npm install @mermaid-js/mermaid-cli')
    node = shutil.which("node")
    if not node:
        sys.exit("HIBA: 'node' nincs a PATH-ban.")

    cfg = ensure_config(week)
    mmd_files = sorted(assets.glob("*.mmd"))
    if not mmd_files:
        print(f"[10-1] Nincs .mmd a mappában: {assets}")
        return 0

    ok = 0
    for mmd in mmd_files:
        png = mmd.with_suffix(".png")
        cmd = [node, str(cli), "-i", str(mmd), "-o", str(png),
               "-p", str(cfg), "-b", args.bg, "-s", args.scale]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and png.exists():
            print(f"[10-1] OK  {mmd.name} -> {png.name} ({png.stat().st_size} B)")
            ok += 1
        else:
            print(f"[10-1] HIBA {mmd.name}: {res.stderr.strip() or res.stdout.strip()}")
    print(f"[10-1] Kész: {ok}/{len(mmd_files)} diagram renderelve -> {assets}")
    return 0 if ok == len(mmd_files) else 1


if __name__ == "__main__":
    raise SystemExit(main())
