"""Check the complete static scenario matrix without third-party dependencies."""
from pathlib import Path
import hashlib
import json
root = Path(__file__).resolve().parents[1]
temperatures = [-10, -5, -2, -1, 0, 1, 2, 5, 10]
precipitations = [-1000, -750, -500, -250, 0, 250, 500, 750, 1000]
manifest = json.loads((root / 'assets/maps/manifest.json').read_text())
records = {item['file']: item for item in manifest['maps']}
assert len(records) == 81
hashes = set()
for temperature in temperatures:
    for precipitation in precipitations:
        path = root / f'assets/maps/t{temperature}_p{precipitation}.webp'
        data = path.read_bytes()
        assert data[:4] == b'RIFF' and data[8:12] == b'WEBP', path
        digest = hashlib.sha256(data).hexdigest()
        assert digest == records[path.name]['sha256'], f'Hash mismatch: {path}'
        hashes.add(digest)
assert len(hashes) == 81, f'Expected 81 distinct maps, found {len(hashes)}'
for name in ['index.html', 'app.js', 'styles.css', 'assets/vendor/bootstrap.min.css']:
    assert (root / name).is_file(), name
print('All 81 distinct scenario maps and static files are present.')
