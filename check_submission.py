"""
Self-check of your M1 coursework submission.  Run it in your submission folder,
with your CRSid in place of ab123:

    python check_submission.py ab123

It runs step1.py to step4.py one after the other from a clean start (each with a time
limit of 30 minutes), collects the "row <id>: <value>" lines they print, compares them
with the Value column of your results_table.xlsx, checks the SEED and the three CSV
files (looked for anywhere below the folder, for instance in outputs/), lists every file
of the folder with its SHA-256 (taken with Windows line endings read as Unix ones), and
writes all of it to check_ab123.txt.  Hand that file in with the rest.

The check marks nothing.  It tells you whether your scripts run on their own, and it
lets the markers verify that the files they received are the files you checked.  Needs
only Python 3.8 or later; the results table is read when openpyxl is installed (it is
when pandas can read Excel files), and skipped with a note otherwise
"""
import hashlib
import importlib.metadata
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

STEPS      = ("step1.py", "step2.py", "step3.py", "step4.py")
CSV_FILES  = ("test_predictions_linear.csv", "test_predictions_network.csv", "suspect_labels.csv")
LABELS     = {"active payload", "dead payload", "rocket body", "fragment"}
PACKAGES   = ("numpy", "scipy", "pandas", "scikit-learn", "matplotlib", "torch", "openpyxl")
TIME_LIMIT = 1800                                   # seconds per script
SKIP_DIRS  = {"__pycache__", ".git", ".ipynb_checkpoints", "data"}
SEED       = 0                                      # the seed the handout prescribes for every script


def sha256(path):
    """
    The SHA-256 of a file's content, with Windows line endings (CRLF) read as Unix ones (LF)
    """
    # git may store a text file with LF although it has CRLF on your disk: both must give one hash
    # shortcut: the file is read whole, upgrade to reading in blocks if a folder holds files of gigabytes
    content = Path(path).read_bytes().replace(b"\r\n", b"\n")
    digest = hashlib.sha256(content).hexdigest()
    return digest


def run_script(name, folder):
    """
    Run one script with a clean interpreter; return (status, seconds, rows, error tail)
    """
    started = time.time()
    try:
        run = subprocess.run([sys.executable, name], cwd=folder, capture_output=True, text=True, timeout=TIME_LIMIT)
    except subprocess.TimeoutExpired:
        result = ("TIMEOUT", TIME_LIMIT, {}, f"stopped after {TIME_LIMIT} s")
        return result
    rows = dict(re.findall(r"^row (\S+):\s*(.*?)\s*$", run.stdout, flags=re.M))
    status = "ok" if run.returncode == 0 else f"FAILED (exit {run.returncode})"
    tail = "" if run.returncode == 0 else "\n".join(run.stderr.strip().splitlines()[-12:])
    result = (status, time.time() - started, rows, tail)
    return result


def seed_in(path):
    """
    What the script sets SEED to, beside the seed of the handout: "ok", the other value, or no SEED found
    """
    text = path.read_text(errors="replace")
    # the first line of the script that starts with "SEED =", without its comment
    found = re.search(r"^SEED\s*=\s*([^#\n]*)", text, flags=re.M)
    if not found:
        verdict = "no SEED found"
        return verdict
    value = found.group(1).strip()
    verdict = "ok" if value == str(SEED) else f"SEED = {value}, expected {SEED}"
    return verdict


def find(folder, name):
    """
    The file of that name nearest the top of the folder, or None
    """
    found = [p for p in folder.rglob(name) if not set(p.relative_to(folder).parts[:-1]) & SKIP_DIRS]
    nearest = min(found, key=lambda p: (len(p.parts), str(p))) if found else None
    return nearest


def table_values(folder):
    """
    Row id -> Value of results_table.xlsx, or None when it cannot be read
    """
    try:
        from openpyxl import load_workbook
    except ImportError:
        values = None
        return values
    path = find(folder, "results_table.xlsx")
    if path is None:
        values = {}
        return values
    sheet = load_workbook(path, data_only=True)["Results"]
    values = {str(r[0]).strip(): ("" if r[4] is None else str(r[4]).strip()) for r in list(sheet.iter_rows(values_only=True))[1:] if r[0]}
    return values


def same(printed, table):
    """
    A printed value and a table cell agree: equal to three significant figures, or as text
    """
    try:
        # numbers: equal once both are rounded to three significant figures
        agree = f"{float(printed):.3g}" == f"{float(table):.3g}"
    except ValueError:
        agree = printed.strip().lower() == table.strip().lower()
    return agree


def csv_summary(path):
    """
    One line about a hand-in CSV file: its number of rows, its header, and any label not in the learning set
    """
    if path is None:
        summary = "missing"
        return summary
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    header = lines[0].strip() if lines else ""
    labels = {line.split(",", 1)[1].strip() for line in lines[1:] if "," in line}
    odd = sorted(labels - LABELS)
    summary = (f"{len(lines) - 1} rows; header {'ok' if header == 'object_id,predicted_class' else repr(header)}"
               + (f"; labels not in the learning set: {odd}" if odd else ""))
    return summary


def main(argv):
    """
    Run the four scripts, compare their rows with the results table, check the SEED and the CSV
    files, list the files with their SHA-256, and write check_<CRSid>.txt
    """
    if len(argv) != 2 or not re.fullmatch(r"[a-z]+[0-9]+", argv[1]):
        sys.exit("usage: python check_submission.py <CRSid>, e.g. python check_submission.py ab123")
    crsid, folder = argv[1], Path.cwd()
    out = [f"M1 coursework 2026-27, self-check of {crsid}", f"folder: {folder.name}", f"run: {time.strftime('%Y-%m-%d %H:%M:%S')}",
           f"python: {platform.python_version()} on {platform.platform()}", f"expected SEED: {SEED}"]
    for package in PACKAGES:
        try:
            out.append(f"{package}: {importlib.metadata.version(package)}")
        except importlib.metadata.PackageNotFoundError:
            out.append(f"{package}: not installed")

    out.append("## scripts")
    printed = {}
    for name in STEPS:
        if not (folder / name).exists():
            out.append(f"{name}: missing")
            continue
        status, seconds, rows, tail = run_script(name, folder)
        printed.update(rows)
        out.append(f"{name}: {status}; {seconds:.0f} s; {len(rows)} rows printed; SEED {seed_in(folder / name)}")
        out.extend("    " + line for line in tail.splitlines())
        print(out[-1 - len(tail.splitlines())])

    out.append("## rows (printed by the scripts | results_table.xlsx)")
    table = table_values(folder)
    if table is None:
        out.append("results_table.xlsx not read: openpyxl is not installed")
    elif not table:
        out.append("results_table.xlsx missing")
    else:
        out.append(f"CRSid: {table.get('CRSid', '')} | expected {crsid} | {'ok' if table.get('CRSid', '') == crsid else 'DIFFERS'}")
        for row_id in [k for k in table if k != "CRSid"]:
            value, cell = printed.get(row_id), table[row_id]
            verdict = ("ok" if cell.lower() in ("not attempted", "not obtained") else "empty cell" if cell == "" else
                       "not printed" if value is None else "ok" if same(value, cell) else "DIFFERS")
            out.append(f"{row_id}: {value if value is not None else '-'} | {cell if cell else '-'} | {verdict}")
        unknown = sorted(set(printed) - set(table))
        if unknown:
            out.append(f"printed but not in the table: {unknown}")

    out.append("## csv files")
    out.extend(f"{name}: {csv_summary(find(folder, name))}" for name in CSV_FILES)

    out.append("## files (sha256, bytes, path)")
    for path in sorted(p for p in folder.rglob("*") if p.is_file()):
        relative = path.relative_to(folder)
        if set(relative.parts[:-1]) & SKIP_DIRS or path.name.startswith(".") or path.name == f"check_{crsid}.txt":
            continue
        out.append(f"{sha256(path)}  {path.stat().st_size:>10d}  {relative.as_posix()}")

    body = "\n".join(out) + "\n"
    report = folder / f"check_{crsid}.txt"
    report.write_text(body + f"certificate: {hashlib.sha256(body.encode()).hexdigest()}\n", encoding="utf-8")
    problems = [line for line in out if "FAILED" in line or "TIMEOUT" in line or "DIFFERS" in line or "missing" in line]
    print(f"wrote {report.name}; {len(problems)} line(s) to look at" + (":\n  " + "\n  ".join(problems) if problems else ""))


if __name__ == "__main__":
    main(sys.argv)
