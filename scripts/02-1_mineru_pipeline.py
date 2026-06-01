"""
03_run_mineru_pipeline.py -- MinerU pipeline vizualis folyamatkovetesssel

Feladat: 1_raw_inputs/*.pdf -> 2_clean_inputs/<forrasnev>/ + figure_catalog.json
         Minden notebook (het-mappa) es fajl szamlaloval, MinerU progress-barral.
         Nagy fajloknal a felhasznalo donti el, feldolgozza-e.

Futtatas (tantargy gyokerebol):
    python ../../scripts/03_run_mineru_pipeline.py [--root <tantargy_mappa>] [--warn-mb 20]

Peldak:
    # Claude_play gyokerebol:
    python scripts/03_run_mineru_pipeline.py --root test_outputs/haromhetes_teszt
    # Tantargy mappan belulrol:
    cd test_outputs/haromhetes_teszt && python ../../scripts/03_run_mineru_pipeline.py
"""

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

try:
    from rich.columns import Columns
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import (BarColumn, Progress, SpinnerColumn,
                               TaskProgressColumn, TextColumn,
                               TimeElapsedColumn)
    from rich.rule import Rule
    from rich.table import Table
    from rich.text import Text
    RICH = True
except ImportError:
    RICH = False

# ── Konfiguracio ──────────────────────────────────────────────────────────────
WARN_MB_DEFAULT    = 20    # e felett figyelmeztetes + kerdes (MB)
WARN_PAGES_DEFAULT = 50    # e felett figyelmeztetes + kerdes (oldalszam)
CONDA_ENV          = "mineru"

def build_cmd(backend: str) -> list[str]:
    """Build the MinerU command with the given backend."""
    return ["conda", "run", "-n", CONDA_ENV, "--no-capture-output",
            "mineru", "-p", "{pdf}", "-o", "{out}", "-m", "auto", "-b", backend]

# ── Helper-ek ─────────────────────────────────────────────────────────────────
console = Console() if RICH else None


def human_mb(path: Path) -> float:
    return path.stat().st_size / 1_048_576


def count_pdf_pages(pdf_path: Path) -> int:
    """Gyors oldalszamlales pypdf-fel (fallback: 0)."""
    try:
        import pypdf
        return len(pypdf.PdfReader(str(pdf_path)).pages)
    except Exception:
        return 0


def discover_notebooks(root: Path) -> list[tuple[str, list[Path]]]:
    """
    Visszaadja a het-mappak listajat (notebook_nev, pdf_lista) rendezett sorban.
    Keresi: root/N_*/1_raw_inputs/*.pdf
    """
    notebooks = []
    for week_dir in sorted(root.iterdir()):
        raw = week_dir / "1_raw_inputs"
        if not raw.is_dir():
            continue
        pdfs = sorted(raw.glob("*.pdf"))
        if pdfs:
            notebooks.append((week_dir.name, pdfs))
    return notebooks


def ask_user(prompt: str) -> str:
    """Interaktiv billentyuleutes (i/k/q)."""
    if RICH:
        console.print(prompt, end="")
    else:
        print(prompt, end="", flush=True)
    return input().strip().lower()


def should_process(pdf: Path, warn_mb: float, warn_pages: int, pages: int) -> bool:
    """
    Ha a fajl nagyobb warn_mb MB-nel VAGY tobb mint warn_pages oldal, kerdi a felhasznalot.
    Visszateres: True = feldolgozas, False = kihagyas.
    """
    mb = human_mb(pdf)
    over_mb    = mb >= warn_mb
    over_pages = pages > 0 and pages >= warn_pages

    if not over_mb and not over_pages:
        return True

    reasons = []
    if over_mb:
        reasons.append(f"{mb:.1f} MB")
    if over_pages:
        reasons.append(f"{pages} oldal")
    reason_str = ", ".join(reasons)

    if RICH:
        console.print(
            f"      [yellow]⚠️  Nagy fajl:[/yellow] [bold]{pdf.name}[/bold]"
            f" [dim]({reason_str})[/dim]"
        )
        answer = ask_user(
            "      Feldolgozzuk? "
            "\\[[green]i[/green]]gen / "
            "\\[[red]k[/red]]ihagyas / "
            "\\[[bold]q[/bold]]uit : "
        )
    else:
        print(f"      ⚠️  Nagy fajl: {pdf.name} ({reason_str})")
        answer = ask_user("      Feldolgozzuk? [i]gen / [k]ihagyas / [q]uit : ")

    if answer in ("q", "quit", "exit"):
        if RICH:
            console.print("[bold red]Megszakitva.[/bold red]")
        else:
            print("Megszakitva.")
        sys.exit(0)

    return answer in ("i", "igen", "y", "yes", "")


def run_mineru(pdf: Path, out_dir: Path, pages: int, backend: str = "pipeline") -> bool:
    """
    Futtatja a mineru-t, valosi idejU progress-barral.
    Visszateres: True = siker, False = hiba.
    Log: mineru_run.log a 3_raw_outputs/ mappaban.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_out = pdf.parent.parent / "3_raw_outputs"
    raw_out.mkdir(parents=True, exist_ok=True)
    log_path = raw_out / "mineru_run.log"
    cmd = [
        c.replace("{pdf}", str(pdf)).replace("{out}", str(out_dir))
        for c in build_cmd(backend)
    ]

    # ── Rich progress bar ──────────────────────────────────────────────────
    if RICH:
        with Progress(
            SpinnerColumn(),
            TextColumn("      "),
            BarColumn(bar_width=28),
            TaskProgressColumn(),
            TextColumn("[dim]{task.fields[detail]}[/dim]"),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        ) as prog:
            task = prog.add_task(
                "MinerU",
                total=max(pages, 1),
                detail=f"0/{pages} oldal" if pages else "fut...",
            )

            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True, bufsize=1,
                errors="replace",
            )

            with open(log_path, "a", encoding="utf-8") as log_f:
                log_f.write(f"\n--- {pdf.name} ---\n")
                for line in proc.stdout:
                    log_f.write(line)
                    # tqdm / mineru progress: "XX%|...| N/M [...]"
                    m = re.search(r"(\d+)%\|.*?(\d+)/(\d+)", line)
                    if m:
                        done  = int(m.group(2))
                        total = int(m.group(3))
                        prog.update(
                            task,
                            completed=done,
                            total=max(total, 1),
                            detail=f"{done}/{total} oldal",
                        )
                        continue

                    # mineru soros log: "page_id: N" vagy "INFO - page N"
                    m2 = re.search(r"page[_\s-]*(?:id[:\s]+)?(\d+)", line, re.I)
                    if m2 and pages:
                        done = int(m2.group(1)) + 1
                        prog.update(
                            task,
                            completed=done,
                            detail=f"{done}/{pages} oldal",
                        )

            proc.wait()
            if proc.returncode == 0:
                prog.update(task, completed=max(pages, 1), detail="kesz")

    # ── Fallback: egyszerű szoveg ─────────────────────────────────────────
    else:
        print(f"      [MinerU] {pdf.name} ...", end="", flush=True)
        proc = subprocess.run(cmd, capture_output=True, text=True)
        print(" KESZ" if proc.returncode == 0 else " HIBA")

    return proc.returncode == 0


# ── Fo fuggveny ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="MinerU pipeline vizualis futtatasa")
    parser.add_argument(
        "--root", default=".",
        help="Tantargy gyokermappaja (alapertek: aktualis konyvtar)"
    )
    parser.add_argument(
        "--warn-mb", type=float, default=WARN_MB_DEFAULT,
        help=f"Fajlmeret MB-ben, ami felett kerdez (alapertek: {WARN_MB_DEFAULT})"
    )
    parser.add_argument(
        "--warn-pages", type=int, default=WARN_PAGES_DEFAULT,
        help=f"Oldalszam, ami felett kerdez (alapertek: {WARN_PAGES_DEFAULT})"
    )
    parser.add_argument(
        "--backend", default="pipeline",
        choices=["pipeline", "vlm-transformers", "vlm-sglang"],
        help="MinerU backend (alapertek: pipeline=CPU; vlm-transformers=GPU)"
    )
    parser.add_argument(
        "--yes", action="store_true",
        help="Nagy fajloknal ne kerdezzen, mindet dolgozza fel"
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        sys.exit(f"HIBA: mappa nem talalhato: {root}")

    notebooks = discover_notebooks(root)
    if not notebooks:
        sys.exit(f"HIBA: nincs 1_raw_inputs/*.pdf a {root} alatt.")

    nb_total = len(notebooks)

    if RICH:
        console.print(Rule(f"[bold]MinerU Pipeline[/bold] -- {root.name}"))
        console.print(
            f"[dim]Notebookok: {nb_total} | "
            f"Hatar: {args.warn_mb:.0f} MB / {args.warn_pages} oldal | "
            f"Backend: {args.backend}[/dim]\n"
        )
    else:
        print(f"=== MinerU Pipeline: {root.name} ({nb_total} notebook) "
              f"[{args.backend}] ===\n")

    results = []  # (notebook, fajl, statusz)

    for nb_idx, (nb_name, pdfs) in enumerate(notebooks, 1):
        week_dir  = root / nb_name
        clean_dir = week_dir / "2_clean_inputs"
        pdf_total = len(pdfs)

        if RICH:
            console.print(
                f"[bold cyan][{nb_idx}/{nb_total}][/bold cyan] "
                f"Notebook: [bold]{nb_name}[/bold] "
                f"[dim]({pdf_total} PDF)[/dim]"
            )
        else:
            print(f"[{nb_idx}/{nb_total}] Notebook: {nb_name} ({pdf_total} PDF)")

        for f_idx, pdf in enumerate(pdfs, 1):
            mb     = human_mb(pdf)
            pages  = count_pdf_pages(pdf)
            mb_str = f"{mb:.1f} MB"
            pg_str = f"{pages}p" if pages else "?"

            if RICH:
                console.print(
                    f"  [bold white][{f_idx}/{pdf_total}][/bold white] "
                    f"{pdf.name} [dim]({mb_str}, {pg_str})[/dim]"
                )
            else:
                print(f"  [{f_idx}/{pdf_total}] {pdf.name} ({mb_str}, {pg_str})")

            # Nagy fajl kerdes (kihagyva ha --yes)
            if not args.yes and not should_process(pdf, args.warn_mb, args.warn_pages, pages):
                if RICH:
                    console.print("      [yellow]→ KIHAGYVA[/yellow]")
                else:
                    print("      → KIHAGYVA")
                results.append((nb_name, pdf.name, "KIHAGYVA"))
                continue

            # MinerU futtatasa
            # clean_dir-t adjuk at (nem clean_dir/pdf.stem):
            # MinerU maga hozza letre a <pdf_stem>/ alkonyvtarat belul
            ok = run_mineru(pdf, clean_dir, pages, backend=args.backend)

            if ok:
                if RICH:
                    console.print(f"      [green]✓ {pdf.name}[/green]")
                else:
                    print(f"      ✓ {pdf.name}")
                results.append((nb_name, pdf.name, "OK"))
            else:
                if RICH:
                    console.print(f"      [red]✗ HIBA: {pdf.name}[/red]")
                else:
                    print(f"      ✗ HIBA: {pdf.name}")
                results.append((nb_name, pdf.name, "HIBA"))

        if RICH:
            console.print()

    # ── Osszefoglalo ──────────────────────────────────────────────────────────
    ok_n   = sum(1 for _, _, s in results if s == "OK")
    skip_n = sum(1 for _, _, s in results if s == "KIHAGYVA")
    err_n  = sum(1 for _, _, s in results if s == "HIBA")

    if RICH:
        table = Table(title="Osszefoglalo", show_header=True, header_style="bold")
        table.add_column("Notebook")
        table.add_column("Fajl")
        table.add_column("Statusz")
        for nb, f, s in results:
            color = {"OK": "green", "KIHAGYVA": "yellow", "HIBA": "red"}[s]
            table.add_row(nb, f, Text(s, style=color))
        console.print(table)
        console.print(
            f"\n[green]✓ {ok_n} OK[/green]  "
            f"[yellow]{skip_n} kihagyva[/yellow]  "
            f"[red]{err_n} hiba[/red]"
        )
    else:
        print("\n--- Osszefoglalo ---")
        for nb, f, s in results:
            print(f"  {nb}  {f}  {s}")
        print(f"\n{ok_n} OK  {skip_n} kihagyva  {err_n} hiba")


if __name__ == "__main__":
    main()
       