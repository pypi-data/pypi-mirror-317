# DDownloader
- DDownloader is a Python library to download HLS and DASH manifests and decrypt media files.

# Features
- Download HLS streams using N_m3u8DL-RE.
- Download DASH manifests and segments.
- Decrypt media files using mp4decrypt.

# Installation
Use the package manager pip to install DDownloader.
```pip install DDownloader```

# Usage

- Download DASH content using the library:

```python
from DDownloader.dash_downloader import DASH

dash_downloader = DASH()
dash_downloader.manifest_url = "https://example.com/path/to/manifest.mpd"  # Set your DASH manifest URL
dash_downloader.output_name = "output.mp4"  # Set desired output name
dash_downloader.decryption_key = "12345:678910"  # Set decryption key if needed
dash_downloader.dash_downloader()
```

- Download HLS content using the library:
```python
from DDownloader.hls_downloader import HLS

hls_downloader = HLS()
hls_downloader.manifest_url = "https://example.com/path/to/manifest.m3u8"  # Set your HLS manifest URL
hls_downloader.output_name = "output.mp4"  # Set desired output name
hls_downloader.decryption_key = "12345:678910"  # Set decryption key if needed
hls_downloader.hls_downloader()  # Call the downloader method
```

# THIS PROJECT STILL IN DEVELOPMENT
