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
Use this pattern at the start of posts:
```python
import ee
import pandas as pd
import altair as alt
from IPython.display import Image

# Prefer env var; readers can also hardcode directly if preferred.
PROJECT_ID = os.environ.get("EE_PROJECT_ID", "YOUR_PROJECT_ID")
ee.Initialize(project=PROJECT_ID)
```

For rendering, use the author's actual project. Readers will replace with their own.

## Image Display Guidelines
Use `getThumbURL()` for displaying Earth Engine images in blog posts:
```python
url = image.getThumbURL({
    'region': region,
    'dimensions': 800,
    'format': 'png',
    **vis_params
})
Image(url=url)
```
- Set `dimensions` to 800 for full-width images
- Use PNG format for best quality
- Keep zoom/region appropriate for the content
- This approach works reliably with Quarto rendering and shows readers practical EE code

### Persist Earth Engine images (avoid expiring tokens)
- Always save EE thumbs to local PNGs and display those paths in posts so images stay valid after publish.
- Include a visible setup chunk with a small helper:
    ```python
    from pathlib import Path
    from urllib.request import urlopen

    def save_image(url: str, filename: str) -> Path:
            dest = Path(filename)
            with urlopen(url) as response, open(dest, "wb") as fp:
                    fp.write(response.read())
            return dest
    ```
- Pattern when rendering images:
    ```python
    url = image.getThumbURL({...})
    save_image(url, 'my_image.png')
    Image(url='my_image.png')
    ```
- Keep images in the post folder; Quarto will copy them into `docs/` during render.

## Chart Guidelines
- Use Altair for exploratory charts; inline creation.
- Use width 800 for charts.
- Save Altair charts to PNG for smaller HTML file size: `chart.save('filename.png')`
- Display saved charts with: `Image(url='filename.png')`
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
- Use `getThumbURL()` for Earth Engine image visualization to ensure reliable Quarto rendering.

## Reusable Patterns
### Annual Composite Example
```python
collection = ee.ImageCollection('LANDSAT/COMPOSITES/C02/T1_L2_ANNUAL').filterDate('2023-01-01','2024-01-01')
image = collection.first()
region = ee.Geometry.Rectangle([5.9, 45.8, 10.5, 47.8])
vis = {'bands':['red','green','blue'], 'min':0, 'max':0.3}

url = image.getThumbURL({
    'region': region,
    'dimensions': 800,
    'format': 'png',
    **vis
})
Image(url=url)
```
### NDVI Time Series (8-Day)
```python
point = ee.Geometry.Point([-121.5, 38.5])
collection = ee.ImageCollection('LANDSAT/COMPOSITES/C02/T1_L2_8DAY_NDVI') \
    .filterDate('2023-01-01', '2024-01-01')

def extract_ndvi(img):
    date = img.date().format("YYYY-MM-dd")
    ndvi = img.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point,
        scale=30
    ).get('NDVI')
    return ee.Feature(None, {'date': date, 'ndvi': ndvi})

timeseries = collection.map(extract_ndvi).getInfo()
rows = [f['properties'] for f in timeseries['features']]
df = pd.DataFrame(rows)
df['date'] = pd.to_datetime(df['date'])

chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X('date:T', title='Date'),
    y=alt.Y('ndvi:Q', title='NDVI'),
    tooltip=['date:T', alt.Tooltip('ndvi:Q', format='.3f')]
).properties(
    width=800,
    height=300
)
chart.save('ndvi_chart.png', scale_factor=2.0)
Image(url='ndvi_chart.png')
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
