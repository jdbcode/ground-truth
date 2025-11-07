# Ground Truth Blog Agent Instructions

These guidelines help an AI agent draft new short "b-side" posts for the Ground Truth blog.

## Purpose & Tone
- Short, discovery-oriented notes (500–900 words typical).
- Conversational, pragmatic, not overly polished; prioritize usefulness.
- Emphasize Earth Engine, geospatial analysis, Python workflows, Google Cloud, public geospatial datasets.
- When announcing datasets: include collection ID, a minimal usage snippet, and 1–2 suggested applications.

## Standard Post Structure
1. Title (succinct, action or insight oriented)
2. 1–2 sentence hook/summary.
3. Minimal context (what/why).
4. One or more concise examples (image, chart, or stat table).
5. Optional: small troubleshooting tip or gotcha.
6. Links (dataset, docs, code repo, related post).
7. Closing nudge ("Try it", "Explore variants", etc.).

## Earth Engine Initialization (Python)
Use this standard pattern in the first hidden setup chunk:
```python
import ee
try:
    ee.Initialize()
except Exception:
    ee.Authenticate()
    ee.Initialize()
```
Avoid printing auth URLs unless necessary; keep the chunk `#| echo: false` when rendering.

## Helper Import
Always load helpers:
```python
from scripts.ee_helpers import display_ee_image, composite_info
```

## Image Display Guidelines
Use `display_ee_image(image, region, vis, title="...", width=650)`.
- Default width: 650px (fits inside content column).
- Prefer region bounding boxes (`ee.Geometry.Rectangle`) or polygons with minimal extent.
- Provide `vis` dict with explicit `min`/`max` or bands + palette.
- Avoid very large palettes; 3–10 colors typical.

## Chart Guidelines
- Use Altair for exploratory charts; inline creation.
- Keep chart width ≤ 650.
- Titles concise; axes labeled.
- For time series: convert FeatureCollection to client-side list carefully (limit temporal range).

## Dataset Announcement Checklist
When introducing a dataset:
- Collection ID
- Spatial/temporal coverage summary
- Key bands / properties
- One usage code snippet
- Attribution / source link

## Code Chunk Conventions
- Hide setup/auth chunks: `#| echo: false`
- Show analysis chunks: `#| echo: true`
- Suppress messages unless relevant: `#| message: false`
- If a chunk produces an image or chart only: `#| echo: false` but keep narrative around it.

## Image Sizing / Responsiveness
- All static PNGs must fit container; rely on Quarto CSS (`img { max-width: 100%; height: auto; }`).
- Avoid base64 or giant inline arrays; prefer static server-side rendering in the chunk.

## Reusable Patterns
### Annual Composite Example
```python
collection = ee.ImageCollection('LANDSAT/COMPOSITES/C02/T1_L2_ANNUAL').filterDate('2023-01-01','2024-01-01')
image = collection.first()
region = ee.Geometry.Rectangle([5.9, 45.8, 10.5, 47.8])
vis = {'bands':['red','green','blue'], 'min':0, 'max':0.3}
display_ee_image(image, region, vis, title='2023 Annual Composite Switzerland')
```
### NDVI Time Series (8-Day)
```python
point = ee.Geometry.Point([-121.5, 38.5])
collection_ndvi = ee.ImageCollection('LANDSAT/COMPOSITES/C02/T1_L2_8DAY_NDVI').filterDate('2023-01-01','2024-01-01')
# Extract small time series
features = []
for img in collection_ndvi.toList(collection_ndvi.size()).getInfo():
    date = ee.Date(img['properties']['system:time_start']).format('YYYY-MM-dd').getInfo()
    ndvi = img['properties'].get('NDVI')
    features.append({'date': date, 'ndvi': ndvi})
import pandas as pd, altair as alt
import datetime
for f in features: f['date'] = pd.to_datetime(f['date'])
df = pd.DataFrame(features)
chart = alt.Chart(df).mark_line(point=True).encode(x='date:T', y='ndvi:Q').properties(title='8-Day NDVI (2023)')
chart
```
(Agent: ensure performance; for large collections, reduce temporal range.)

## Writing Style Reminders
- Prefer active voice ("We load", "This composite shows")
- Use short paragraphs (2–4 sentences).
- Avoid marketing fluff; precise technical wording.
- Link dataset IDs with backticks.

## Quality Checklist Before Finish
- No overflowing images.
- All code executes under current environment.
- Title and first sentence compelling.
- At least one visual (image or chart).
- Links validated.

## Out of Scope
- Deep multi-thousand word tutorials.
- Complex multi-stage ETL pipelines (link out instead).

## Final Output
One `index.qmd` file in `posts/YYYY-MM-DD-slug/` using the template.
