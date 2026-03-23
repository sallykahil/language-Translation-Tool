
import argostranslate.package

# We want offline translation between these languages.
LANGS = ["en", "ar", "fr"]
DESIRED = [
    ("en", "ar"),
    ("en", "fr"),
    ("ar", "en"),
    ("ar", "fr"),
    ("fr", "en"),
    ("fr", "ar"),
]


def find_direct_package(available, from_code: str, to_code: str):
    return next(
        (p for p in available if p.from_code == from_code and p.to_code == to_code),
        None,
    )


def find_chain(available_pairs_set, src: str, dst: str):
    """Return a chain of length 2 (direct) or 3 (pivot) or None."""
    if (src, dst) in available_pairs_set:
        return [src, dst]

    # Pivot through one of the supported languages.
    for pivot in LANGS:
        if pivot == src or pivot == dst:
            continue
        if (src, pivot) in available_pairs_set and (pivot, dst) in available_pairs_set:
            return [src, pivot, dst]

    return None


argostranslate.package.update_package_index()
available = argostranslate.package.get_available_packages()

# Keep only language pairs we care about, to make debugging easier.
available_pairs = [
    (p.from_code, p.to_code)
    for p in available
    if p.from_code in LANGS and p.to_code in LANGS
]
available_pairs_set = set(available_pairs)

print("Available offline Argos pairs among en/ar/fr:")
for src, dst in sorted(available_pairs_set):
    print(f"  {src} -> {dst}")

needed_edges = set()
missing = []
for src, dst in DESIRED:
    chain = find_chain(available_pairs_set, src, dst)
    if chain is None:
        missing.append((src, dst))
        continue

    # chain is either [src, dst] or [src, pivot, dst]
    if len(chain) == 2:
        needed_edges.add((chain[0], chain[1]))
    else:
        needed_edges.add((chain[0], chain[1]))
        needed_edges.add((chain[1], chain[2]))

if missing:
    print("\nMissing conversions (no direct or 1-pivot path found):")
    for src, dst in missing:
        print(f"  {src} -> {dst}")
    print("\nStopping download because at least one conversion cannot be satisfied with 1 pivot.")
    raise SystemExit(1)

print("\nDownloading required model edges:")
for src, dst in sorted(needed_edges):
    pkg = find_direct_package(available, src, dst)
    if pkg is None:
        # Shouldn't happen because we built available_pairs_set from available.
        raise RuntimeError(f"Internal error: package not found for {src} -> {dst}")
    print(f"  Downloading {src} -> {dst}")
    argostranslate.package.install_from_path(pkg.download())

print("\nDone. Offline translation should work now.")