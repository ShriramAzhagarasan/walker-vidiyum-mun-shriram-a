#!/usr/bin/env python3
"""Content hash of the game source shown in the film (build_id).

Method: for every file under <repo>/godot/ except the .godot/ editor cache,
sorted by POSIX relative path, hash the line  "<relpath>\\0<sha256(file)>\\n";
the SHA-256 of that concatenation is the build_id. Deterministic across
machines and independent of git. Usage: python3 source_snapshot.py <repo> [--list]
"""
import hashlib, sys
from pathlib import Path

def snapshot(repo):
    root = Path(repo).resolve() / 'godot'
    files = sorted(p for p in root.rglob('*') if p.is_file() and '.godot' not in p.relative_to(root).parts)
    rows = [(p.relative_to(root).as_posix(), hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
    digest = hashlib.sha256(''.join(f'{r}\0{h}\n' for r, h in rows).encode()).hexdigest()
    return digest, rows

if __name__ == '__main__':
    d, rows = snapshot(sys.argv[1] if len(sys.argv) > 1 else '.')
    if '--list' in sys.argv:
        for r, h in rows: print(h, 'godot/' + r)
    print(d)
