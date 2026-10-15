"""Export original scenario images. Requires playwright and Pillow.

Install: pip install playwright Pillow && playwright install chromium
Run from the repository root: python scripts/export_maps.py
The original Shiny service must be reachable when refreshing the maps.
"""
from pathlib import Path
import base64
import hashlib
import io
import json
from datetime import date
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://veg-model.shinyapps.io/shinyapp/'
TEMPERATURES = [0, -10, -5, -2, -1, 1, 2, 5, 10]
PRECIPITATIONS = [0, -1000, -750, -500, -250, 250, 500, 750, 1000]

def main():
    records = []
    destination = ROOT / 'assets/maps'
    destination.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
        page.goto(SOURCE, wait_until='domcontentloaded', timeout=90000)
        page.wait_for_function("document.querySelector('#vegmap img')?.src.startsWith('data:image/png')", timeout=90000)
        page.wait_for_function("!document.documentElement.classList.contains('shiny-busy')", timeout=90000)
        for temperature in TEMPERATURES:
            for precipitation in PRECIPITATIONS:
                expected = f'{temperature} °C | {precipitation} mm'
                if page.locator('#scenario_text').inner_text() != expected:
                    page.evaluate("""window.__updates = 0;
                        window.__observer?.disconnect();
                        window.__observer = new MutationObserver(() => window.__updates++);
                        window.__observer.observe(document.querySelector('#vegmap'),
                            {subtree:true, childList:true, attributes:true});""")
                    page.locator(f'input[name=temp][value="{temperature}"]').check()
                    page.locator(f'input[name=prec][value="{precipitation}"]').check()
                    page.wait_for_function("expected => document.querySelector('#scenario_text').textContent === expected", arg=expected, timeout=90000)
                    page.wait_for_function("window.__updates > 0 && !document.documentElement.classList.contains('shiny-busy')", timeout=90000)
                source = page.locator('#vegmap img').get_attribute('src')
                assert source.startswith('data:image/png;base64,')
                png = base64.b64decode(source.split(',', 1)[1])
                image = Image.open(io.BytesIO(png)).convert('RGB')
                target = destination / f't{temperature}_p{precipitation}.webp'
                image.save(target, lossless=True, method=6)
                with Image.open(target) as restored:
                    assert image.tobytes() == restored.convert('RGB').tobytes()
                records.append({'file': target.name, 'source_sha256': hashlib.sha256(png).hexdigest(),
                                'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
                                'width': image.width, 'height': image.height, 'bytes': target.stat().st_size})
                print(expected, flush=True)
        browser.close()
    (destination / 'manifest.json').write_text(json.dumps({
        'source': SOURCE, 'exported': str(date.today()),
        'encoding': 'lossless WebP, pixel-identical to exported PNG', 'maps': records,
    }, indent=2) + '\n')

if __name__ == '__main__':
    main()
