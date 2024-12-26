
# EverythingJS

## Overview

**EverythingJS** is a CLI tool for extracting JavaScript links from URLs or web pages, applying custom regex patterns to those JS files, and organizing the results in a structured JSON format. It’s designed for efficiency, with features like multi-threading, filtering irrelevant links, and customizable headers.

## Installation

Install EverythingJS via pip:

```bash
pip install everythingjs
```

## Features

- Extracts JavaScript links from a URL or a list of URLs.
- Converts relative links to absolute URLs.
- Applies a regex pattern to each JavaScript file, extracting relevant matches.
- Filters irrelevant JavaScript links using a predefined `nopelist`.
- Supports custom headers for HTTP requests.
- Outputs results in JSON format, tagged to respective JS links.
- Multi-threaded for fast processing.

## Usage

### Command-Line Arguments

```
usage: everythingjs [-h] -i INPUT [-o OUTPUT] [-v] [-H HEADER]

Extract JS links from a URL or list of URLs and apply regex to them.

optional arguments:
  -h, --help            Show this help message and exit.
  -i INPUT, --input INPUT
                        URL or file containing URLs.
  -o OUTPUT, --output OUTPUT
                        Output JSON file to save results (optional, prints to CLI if not specified).
  -v, --verbose         Enable verbose logging.
  -H HEADER, --header HEADER
                        Add custom header (can be used multiple times).
```

### Example Usage

#### 1. Extract JavaScript links from a single URL:

```bash
everythingjs -i https://example.com
```

#### 2. Extract JavaScript links from a file of URLs:

```bash
everythingjs -i urls.txt
```

#### 3. Save the output to a JSON file:

```bash
everythingjs -i https://example.com -o results.json
```

#### 4. Enable verbose logging:

```bash
everythingjs -i https://example.com -v
```

#### 5. Add custom headers:

```bash
everythingjs -i https://example.com -H "User-Agent: CustomAgent" -H "Authorization: Bearer TOKEN"
```

## Output

- Outputs JSON in the format:

```json
{
  "https://example.com": {
    "js_links": [
      "https://example.com/static/script1.js",
      "https://example.com/static/script2.js"
    ],
    "regex_matches": {
      "https://example.com/static/script1.js": ["match1", "match2"],
      "https://example.com/static/script2.js": ["match3"]
    }
  }
}
```
- Domains without JavaScript links are excluded from the output.

## License

MIT License
