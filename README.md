# content-select Downloader

This script can download PDFs from https://content-select.com and merge them to one PDF.

```
usage: download.py [-h] --url URL [--output OUTPUT]

optional arguments:
  -h, --help       show this help message and exit
  --url URL        Url to the PDF on https://content-select.com/
  --output OUTPUT  Name of the resulting PDF.
```

The URL must be of the form: https://content-select.com/media/moz_viewer/5c84e9c9-292c-4c4c-bfcf-646eb0dd2d03/

Example usage:

```
./download.py --url https://content-select.com/media/moz_viewer/5c84e9c9-292c-4c4c-bfcf-646eb0dd2d03/language:de --output Jugend.pdf
```

## Setup

Install `virtualenv`:
```
pip3 install virtualenv
```

Create a virtual environment:
```
virtualenv venv
```

Activate the virtual environment:
```
source venv/bin/activate
```

Install dependencies:
```
pip3 install -r requirements.txt
```

Download PDF:
```
./download.py --url https://content-select.com/media/moz_viewer/5c84e9c9-292c-4c4c-bfcf-646eb0dd2d03/language:de --output Jugend.pdf
```

Deactivate the virtual environment:
```
deactivate
```
