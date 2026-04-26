#!/usr/bin/env python3
"""
Mariachi Scores Folder Reorganizer
===================================
Dry-run by default.  Pass --execute to actually make changes.

What it does
------------
1. PROMOTE  — subfolders of mariachi_partituras become top-level song folders
2. FLATTEN  — files buried in subfolders of any song folder are moved up to
              the song folder itself (one level only)
3. CONVERT  — jpg/jpeg/tif/tiff/png files are converted to PDF via ImageMagick
4. ARCHIVE  — txt/mus/sib/enc/mid/wma/doc/docx/rtf/rar/zip/dat/onetoc2 files
              move to _archive/<song>/ for later review
5. DEDUPE   — if a filename collision occurs, compare SHA-256 hashes:
                • identical   → skip the source (already have it)
                • different   → rename source with a suffix before moving

Folders/files at depth 1 that are already flat are never touched.
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCORES_ROOT = Path("/var/www/mariachiesencia/scores")
ARCHIVE_DIR = SCORES_ROOT / "_archive"

# Files to archive for manual review (not useful in the portal)
ARCHIVE_EXTS = {".txt", ".mus", ".sib", ".enc", ".mid",
                ".wma", ".doc", ".docx", ".rtf", ".rar",
                ".zip", ".dat", ".onetoc2", ".db", ".html", ".m4a"}

# Images that should be converted to PDF
CONVERT_EXTS = {".jpg", ".jpeg", ".tif", ".tiff", ".png"}

# Audio to keep as-is
KEEP_EXTS = {".mp3", ".wav", ".ogg", ".flac"}

# The special folder whose subfolders should become top-level song folders
PROMOTE_PARENT = "mariachi_partituras"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_dest(dest: Path) -> Path:
    """If dest already exists, append _2, _3, etc. to the stem."""
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    i = 2
    while True:
        candidate = dest.with_name(f"{stem}_{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1


class Reorganizer:
    def __init__(self, dry_run: bool):
        self.dry_run = dry_run
        self.actions = []        # list of (tag, msg) for summary
        self.skipped = []
        self.errors  = []

    def log(self, tag: str, msg: str):
        color = {
            "PROMOTE": "\033[36m",   # cyan
            "MOVE":    "\033[32m",   # green
            "CONVERT": "\033[33m",   # yellow
            "ARCHIVE": "\033[34m",   # blue
            "SKIP":    "\033[90m",   # grey
            "DUPE":    "\033[35m",   # magenta
            "ERROR":   "\033[31m",   # red
        }.get(tag, "")
        reset = "\033[0m"
        prefix = "[DRY-RUN] " if self.dry_run else ""
        print(f"{color}[{tag}]{reset} {prefix}{msg}")
        self.actions.append((tag, msg))

    # ------------------------------------------------------------------ #

    def run(self):
        if not SCORES_ROOT.exists():
            print(f"ERROR: {SCORES_ROOT} does not exist.", file=sys.stderr)
            sys.exit(1)

        if not self.dry_run:
            ARCHIVE_DIR.mkdir(exist_ok=True)

        # Step 1: Promote mariachi_partituras subfolders
        self._promote_partituras()

        # Step 2: Flatten all song folders
        self._flatten_all()

        # Print summary
        self._summary()

    # ------------------------------------------------------------------ #

    def _promote_partituras(self):
        """
        Move /scores/mariachi_partituras/<Song>/* → /scores/<Song>/
        then delete the empty mariachi_partituras folder.
        """
        partitura_path = SCORES_ROOT / PROMOTE_PARENT
        if not partitura_path.exists():
            return

        print(f"\n{'='*60}")
        print(f"PHASE 1: Promoting subfolders of '{PROMOTE_PARENT}'")
        print(f"{'='*60}")

        for sub in sorted(partitura_path.iterdir()):
            if not sub.is_dir():
                # files directly in mariachi_partituras — move to root
                self._move_file(sub, SCORES_ROOT / sub.name)
                continue

            dest_song_dir = SCORES_ROOT / sub.name
            self.log("PROMOTE", f"{sub.relative_to(SCORES_ROOT)}  →  {dest_song_dir.relative_to(SCORES_ROOT)}/")

            if not self.dry_run:
                dest_song_dir.mkdir(exist_ok=True)

            # Move all files from the subfolder up
            for f in sorted(sub.rglob("*")):
                if f.is_file():
                    rel = f.relative_to(sub)
                    dest = dest_song_dir / rel.name   # flatten one level
                    self._move_file(f, dest)

            if not self.dry_run:
                try:
                    sub.rmdir()
                except OSError:
                    pass  # not empty — leave it

        if not self.dry_run:
            try:
                partitura_path.rmdir()
            except OSError:
                pass

    # ------------------------------------------------------------------ #

    def _flatten_all(self):
        """
        For every song folder, move files from any subfolders up to the song
        folder, convert images, and archive non-portal files.
        """
        print(f"\n{'='*60}")
        print(f"PHASE 2: Flatten, convert, and archive")
        print(f"{'='*60}")

        for song_dir in sorted(SCORES_ROOT.iterdir()):
            if not song_dir.is_dir():
                continue
            if song_dir.name.startswith("_"):
                continue   # skip _archive etc.
            if song_dir.name == "special-events":
                continue   # skip — will be handled separately later

            has_subfolders = any(p.is_dir() for p in song_dir.iterdir())
            if not has_subfolders:
                # Still scan for images / archive files at depth-1
                for f in sorted(song_dir.iterdir()):
                    if f.is_file():
                        self._process_file(f, song_dir)
                continue

            # Has subfolders — flatten
            print(f"\n  [{song_dir.name}]")
            for item in sorted(song_dir.rglob("*")):
                if item.is_file():
                    self._process_file(item, song_dir)

            # Remove now-empty subfolders (bottom-up)
            if not self.dry_run:
                for sub in sorted(song_dir.rglob("*"), reverse=True):
                    if sub.is_dir():
                        try:
                            sub.rmdir()
                        except OSError:
                            pass

    # ------------------------------------------------------------------ #

    def _process_file(self, src: Path, song_dir: Path):
        ext = src.suffix.lower()
        dest_name = src.name
        dest = song_dir / dest_name

        # File is already in the song folder root — just check if it needs converting/archiving
        already_flat = (src.parent == song_dir)

        if ext in ARCHIVE_EXTS:
            archive_dest = ARCHIVE_DIR / song_dir.name / src.name
            if already_flat:
                self.log("ARCHIVE", f"{src.relative_to(SCORES_ROOT)}  →  _archive/{song_dir.name}/{src.name}")
                if not self.dry_run:
                    archive_dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(archive_dest))
            else:
                self.log("ARCHIVE", f"{src.relative_to(SCORES_ROOT)}  →  _archive/{song_dir.name}/{src.name}")
                if not self.dry_run:
                    archive_dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(archive_dest))
            return

        if ext in CONVERT_EXTS:
            pdf_name = src.stem + ".pdf"
            pdf_dest = song_dir / pdf_name
            self.log("CONVERT", f"{src.relative_to(SCORES_ROOT)}  →  {song_dir.name}/{pdf_name}")
            if not self.dry_run:
                self._convert_to_pdf(src, pdf_dest)
                src.unlink(missing_ok=True)
            return

        # Regular file (pdf, mp3, etc.) — move up if not already flat
        if already_flat:
            return   # nothing to do

        self._move_file(src, dest)

    # ------------------------------------------------------------------ #

    def _move_file(self, src: Path, dest: Path):
        if dest.exists():
            src_hash  = sha256(src)
            dest_hash = sha256(dest)
            if src_hash == dest_hash:
                self.log("DUPE", f"IDENTICAL hash — skipping  {src.relative_to(SCORES_ROOT)}")
                return
            else:
                new_dest = safe_dest(dest)
                self.log("MOVE", f"{src.relative_to(SCORES_ROOT)}  →  {new_dest.relative_to(SCORES_ROOT)}  [renamed: hash differs]")
                if not self.dry_run:
                    shutil.move(str(src), str(new_dest))
        else:
            self.log("MOVE", f"{src.relative_to(SCORES_ROOT)}  →  {dest.relative_to(SCORES_ROOT)}")
            if not self.dry_run:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dest))

    # ------------------------------------------------------------------ #

    def _convert_to_pdf(self, src: Path, dest: Path):
        if dest.exists():
            self.log("SKIP", f"PDF already exists: {dest.name}")
            return
        result = subprocess.run(
            ["convert", "-density", "150", str(src), str(dest)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            self.log("ERROR", f"convert failed for {src.name}: {result.stderr.strip()}")

    # ------------------------------------------------------------------ #

    def _summary(self):
        counts = {}
        for tag, _ in self.actions:
            counts[tag] = counts.get(tag, 0) + 1

        print(f"\n{'='*60}")
        print("SUMMARY" + (" (DRY RUN — nothing changed)" if self.dry_run else " (EXECUTED)"))
        print(f"{'='*60}")
        for tag, n in sorted(counts.items()):
            print(f"  {tag:<10} {n:>5}")
        print(f"  {'TOTAL':<10} {len(self.actions):>5}")
        if self.dry_run:
            print("\n  Re-run with --execute to apply all changes.")


# ------------------------------------------------------------------ #

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reorganize mariachi scores folder")
    parser.add_argument("--execute", action="store_true",
                        help="Actually make changes (default is dry-run)")
    args = parser.parse_args()

    r = Reorganizer(dry_run=not args.execute)
    r.run()
