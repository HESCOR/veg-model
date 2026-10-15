# Be a vegetation modeller!

A static port of the [original Shiny application](https://veg-model.shinyapps.io/shinyapp/), preserving its existing layout, labels, controls, colours, and maps.

**[Open the application](https://hescor.github.io/veg-model/)**

The nine temperature changes and nine precipitation changes select 81 original scenario maps. All interaction runs in the browser. There is no R/Shiny server, map API, API key, JavaScript dependency, or build step. Bootstrap 3.4.1 is vendored locally to retain the original styling.

## Map provenance

The 81 PNG map outputs were exported directly from the running original application on 15 October 2026 at a 1440 × 1000 browser viewport and device pixel ratio 1. They were converted to lossless WebP and checked for pixel equality. `assets/maps/manifest.json` records dimensions and source/output SHA-256 hashes.

These are the original model outputs, not a reimplementation or approximation of the scientific model. The underlying model source and input data were not available for this port. Changing the scientific model requires refreshing the exported maps from the original app or obtaining its source. No new scientific attribution or data licence is asserted here; the original authors' rights are retained.

To refresh the maps, install Python packages `playwright` and `Pillow`, install Playwright Chromium, then run `python scripts/export_maps.py`. This contacts the original Shiny service and overwrites the exported map assets.

## Run locally

```sh
python3 -m http.server 4173
```

Open http://localhost:4173/. To check that all 81 scenario maps are present:

```sh
python3 scripts/check.py
```

## Deployment

`.github/workflows/pages.yml` checks the scenario matrix and deploys the static files to GitHub Pages on pushes to `main`. Repository Settings → Pages uses **GitHub Actions** as its source.

Bootstrap is distributed under the MIT licence; see `assets/vendor/bootstrap-LICENSE.txt`.
