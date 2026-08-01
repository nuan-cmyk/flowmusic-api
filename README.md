# Flow Music API Client

Unofficial Python client for [Flow Music](https://www.flowmusic.app).
Generate breakcore, lo-fi, pop, and more using their AI engine!

## Installation

```bash
pip install -r requirements.txt
# or
pip install flowmusic-api
```

## Quick Start

```python
from flowmusic import FlowMusicClient

# Find your token in the browser network tab (Authorization: Bearer <token>)
client = FlowMusicClient("eyJhb...")

# Check credits
print("Credits:", client.billing.get_total_credits())

# Generate a song
clips = client.generation.generate_music("high-energy breakcore with chaotic amen breaks")
for clip in clips:
    print(f"Title: {clip.title}")
    print(f"Audio URL: {clip.audio_url}")
```

## Features
- **Authentication**: JWT token based
- **Billing**: Get balance history and calculate total credits
- **Personalize**: Access user stats (scores, level)
- **Generation**: Full support for asynchronous song generation and status polling via SSE
