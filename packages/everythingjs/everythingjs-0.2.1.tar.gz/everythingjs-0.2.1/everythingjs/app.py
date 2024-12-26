import os
import json
import requests
import re
import tempfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import argparse
from urllib.parse import urlparse, urlunparse
import threading
from tqdm import tqdm
import jsbeautifier


# Define the list of keywords to ignore
# Define the list of keywords to ignore
nopelist = [
    "node_modules", "jquery", "bootstrap", "react", "vue", "angular", "favicon.ico", "logo", "style.css", 
    "font-awesome", "materialize", "semantic-ui", "tailwindcss", "bulma", "d3", "chart.js", "three.js", 
    "vuex", "express", "axios", "jquery.min.js", "moment.js", "underscore", "lodash", "jquery-ui", 
    "angular.min.js", "react-dom", "redux", "chartist.js", "anime.min.js", "highcharts", "leaflet", 
    "pdf.js", "fullcalendar", "webfontloader", "swiper", "slick.js", "datatables", "webfonts", "react-scripts", 
    "vue-router", "vite", "webpack", "electron", "socket.io", "codemirror", "angularjs", "firebase", "swagger", 
    "typescript", "p5.js", "ckeditor", "codemirror.js", "recharts", "bluebird", "lodash.min.js", "sweetalert2", 
    "polyfils", "runtime", "bootstrap", "google-analytics", 
    "application/json", "application/x-www-form-urlencoded", "json2.js", "querystring", "axios.min.js", 
    "ajax", "formdata", "jsonschema", "jsonlint", "json5", "csrf", "jQuery.ajax", "superagent", 
    "body-parser", "urlencoded", "csrf-token", "express-session", "content-type", "fetch", "protobuf", 
    "formidable", "postman", "swagger-ui", "rest-client", "swagger-axios", "graphql", "apollo-client", 
    "react-query", "jsonapi", "json-patch", "urlencoded-form", "url-search-params", "graphql-tag", 
    "vue-resource", "graphql-request", "restful-api", "jsonwebtoken", "fetch-jsonp", "reqwest", "lodash-es", 
    "jsonwebtoken", "graphene", "axios-jsonp", "postman-collection", 
    "application/xml", "text/xml", "text/html", "text/plain", "multipart/form-data", "image/jpeg", 
    "image/png", "image/gif", "audio/mpeg", "audio/ogg", "video/mp4", "video/webm", "text/css", 
    "application/pdf", "application/octet-stream", "image/svg+xml", "application/javascript", 
    "application/ld+json", "text/javascript", "application/x-www-form-urlencoded", ".dtd", "google.com", "application/javascript", "text/css", "w3.org", "www.thymeleaf.org", "application/javascrip", "toastr.min.js", "spin.min.js" "./" ,"DD/MM/YYYY"
]



links_regex = "\b(?:https?|wss?):\/\/(?:[a-zA-Z0-9-]+\.)+(?:com|org|net|io|gov|edu|info|biz|co|us|uk|in|dev|xyz|tech|ai|me)(?::\d+)?(?:\/[^\s?#]*)?(?:\?[^\s#]*)?(?:#[^\s]*)?|\b(?:[a-zA-Z0-9-]+\.)+(?:com|org|net|io|gov|edu|info|biz|co|us|uk|in|dev|xyz|tech|ai|me)\b"
links_regex = r"https?://(?:s3\.amazonaws\.com|storage\.googleapis\.com|blob\.core\.windows\.net|cdn\.cloudfront\.net)[\\w\\-\\./]*"
links_regex = {
    "s3": r"https?://(?:[\w\-]+\.)?s3(?:[\.-][\w\-]+)?\.amazonaws\.com[\w\-\./]*",
    "gcs": r"https?://(?:[\w\-]+\.)?storage\.googleapis\.com[\w\-\./]*",
    "azure_blob": r"https?://[\w\-]+\.blob\.core\.windows\.net[\w\-\./]*",
    "cloudfront": r"https?://[\w\-]+\.cloudfront\.net[\w\-\./]*"
}

def find_matches(content):
    regex_patterns = {
        "s3": r"https?://(?:[\w\-]+\.)?s3(?:[\.-][\w\-]+)?\.amazonaws\.com[\w\-\./]*",
        "gcs": r"https?://(?:[\w\-]+\.)?storage\.googleapis\.com[\w\-\./]*",
        "azure_blob": r"https?://[\w\-]+\.blob\.core\.windows\.net[\w\-\./]*",
        "cloudfront": r"https?://[\w\-]+\.cloudfront\.net[\w\-\./]*"
    }

    all_matches = {}
    for key, regex in regex_patterns.items():
        matches = re.findall(regex, content)
        all_matches[key] = matches

    return all_matches

def find_xss_sinks(js_content):
    """Find potential XSS sinks in minified JavaScript content with line numbers."""
    xss_sink_pattern = re.compile(
        r"(?:document\.write|document\.writeln|innerHTML|outerHTML|eval|setTimeout|setInterval|Function|"
        r"location\.href|location\.assign|location\.replace|window\.open|execCommand)\s*\("
    )

    lines = js_content.splitlines()
    matches_with_lines = []

    for line_number, line in enumerate(lines, start=1):
        matches = xss_sink_pattern.findall(line)
        if matches:
            for match in matches:
                matches_with_lines.append((line_number, match))

    sorted_matches = list(set(matches_with_lines))
    return sorted_matches

# Regex pattern to match JavaScript file URLs and other patterns
regex_str = r"""
  (?:"|')                               # Start newline delimiter
  (
    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
    |
    ((?:/|\.\./|\./)                    # Start with /,../,./
    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
    [^"'><,;|()]{1,})                   # Rest of the characters can't be
    |
    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
    [a-zA-Z0-9_\-/.]{1,}                # Resource name
    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
    |
    ([a-zA-Z0-9_\-/]{1,}/               # REST API (no extension) with /
    [a-zA-Z0-9_\-/]{3,}                 # Proper REST endpoints usually have 3+ chars
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
    |
    ([a-zA-Z0-9_\-/]{1,}                 # filename
    \.(?:php|asp|aspx|jsp|json|
         action|html|js|txt|xml)        # . + extension
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
  )
  (?:"|')                               # End newline delimiter
"""

# Function to check if any keyword in nopelist is present in the JS URL
def is_nopelist(js_url):
    return any(keyword in js_url.lower() for keyword in nopelist)

def fetch_js_links(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=3)
        response.raise_for_status()
        
        # Explicitly checking if content is non-empty before parsing
        if response.text.strip():
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            return None  # Return None if the response body is empty

        js_links = set()
        
        # Extract script tags with src attribute
        for script in soup.find_all('script', src=True):
            js_url = script['src']
            # Convert relative URL to absolute URL using urljoin
            full_url = urljoin(url, js_url)

            # Ignore URLs that match any keyword in the nopelist
            if not is_nopelist(full_url):
                js_links.add(full_url)
        
        # Return only if there are JS links found
        return (url, list(js_links)) if js_links else None
    except requests.RequestException as e:
        #print(f"Error fetching URL {url}: {e}")
        return None


# Load regex patterns from secrets.regex file
def load_regex_patterns(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Validate if the regex pattern is valid
def validate_regex(pattern):
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False

def apply_regex_patterns_to_text(file_path, text_data):
    patterns = load_regex_patterns(file_path)
    matches = []
    lock = threading.Lock()

    def apply_pattern(entry):
        nonlocal matches
        name = entry.get("name")
        regex = entry.get("regex")

        # Only apply valid patterns
        if validate_regex(regex):
            compiled_regex = re.compile(regex)
            matches_found = compiled_regex.findall(text_data)
            if matches_found:
                joined_matches = " ".join(
                    " ".join(match) if isinstance(match, tuple) else match
                    for match in matches_found
                )
                with lock:
                    matches.append({"name": name, "matches": joined_matches})

    threads = []
    for entry in patterns:
        thread = threading.Thread(target=apply_pattern, args=(entry,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return matches


def run_flask_app(filename):
    import json
    import os
    from flask import Flask, render_template, request, jsonify

    app = Flask(__name__)

    with open(filename, 'r') as file:
        data = json.load(file)

    @app.route('/')
    def hello_world():
        return render_template('template.html', data=data)

    @app.route('/filesearch')
    def file_search():
        keyword = request.args.get('keyword', '')
        lines_param = request.args.get('lines', 5)

        # Validate the 'lines' parameter
        try:
            lines_count = int(lines_param)
        except ValueError:
            return jsonify({"error": "'lines' must be an integer"}), 400

        if not keyword:
            return jsonify({"error": "Keyword is required"}), 400

        results = []

        # Iterate through all files in the data
        for entry in data:
            js_url = entry.get("endpoints", {}).get("js_url", {}).get("filename")
            if not js_url or not os.path.isfile(js_url):
                continue

            # Read the file and search for the keyword
            with open(js_url, 'r') as js_file:
                lines = js_file.readlines()

            for i, line in enumerate(lines):
                if keyword in line:
                    # Get the specified number of lines before and after the match
                    snippet_start = max(0, i - lines_count)
                    snippet_end = min(len(lines), i + lines_count + 1)
                    snippet = ''.join(lines[snippet_start:snippet_end])

                    results.append({
                        "filename": js_url,
                        "codesnippet": snippet.strip()
                    })
                    break  # Stop searching in the current file after a match

        return jsonify(results)

    app.run(debug=False, use_reloader=False)


def get_hostname_filename(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    # Use the path to avoid including the query string and fragment
    filename = os.path.basename(parsed_url.path)
    hostname_filename = f"{hostname}_{filename}"
    return hostname_filename
    
def fetch_js_and_apply_regex(js_url, headers, save_js, secrets_file):
    if secrets_file:
        file_path_secrets = secrets_file[0]
    else:
        file_path_secrets = "secrets.regex"
    try:
        # Download the JS file to a temporary location
        response = requests.get(js_url, headers=headers, timeout=3)
        response.raise_for_status()

        # Use temporary file to store the JS content
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            temp_file.write(response.text)
            temp_file_path = temp_file.name
        
        # Apply regex to the content of the JS file
        with open(temp_file_path, 'r', encoding='utf-8') as file:
            js_filename = get_hostname_filename(js_url)
            js_content = file.read()
            beautified_js = jsbeautifier.beautify(js_content)
            js_details = {}
            if save_js:
                os.makedirs(save_js, exist_ok=True)
                open(save_js+"/"+js_filename, 'a').write(beautified_js)
                js_details = {
                    'js_url': js_url,
                    'filename':  save_js+"/"+js_filename
                }
            regex_matches = re.findall(regex_str, beautified_js, re.VERBOSE)
            matches = apply_regex_patterns_to_text(file_path_secrets, js_content)
            links_matches = find_matches(js_content)
            dom_sinks = find_xss_sinks(js_content)
            #print(links_matches)
        # Clean up temp file after reading
        os.remove(temp_file_path)

        # Check if .map file exists and has a 200 status code
        parsed_url = urlparse(js_url)
        map_url = urlunparse(parsed_url._replace(query="")) + ".map"
        map_status = False
        try:
            map_response = requests.head(map_url, headers=headers, timeout=3)
            if map_response.status_code == 200:
                map_status = True
        except requests.RequestException:
            map_status = False

        # Filter out empty matches
        filtered_matches = [match[0] for match in regex_matches if match[0].strip() and not any(keyword in match[0] for keyword in nopelist)]
        filtered_matches = list(set(filtered_matches))

        # Return filtered matches, secrets, links, and .map status
        return {
            "endpoints": filtered_matches,
            "secrets": matches,
            "links": links_matches,
            "mapping": map_status,
            "dom_sinks": dom_sinks,
            "js_url": js_details
        }
    
    except requests.RequestException as e:
        #print(f"Error fetching JS URL {js_url}: {e}")
        return []


def process_urls(urls, headers, secrets_file, save_js, verbose=False):
    results = []
    with ThreadPoolExecutor() as executor:
        # Submit tasks and store futures
        futures = {executor.submit(fetch_js_links, url, headers): url for url in urls}
        
        if verbose:
            # Create a progress bar for processing URLs
            for future in tqdm(futures.keys(), desc="Processing URLs", total=len(futures)):
                result = future.result()  # Call result() on the future object
                if result:
                    url, js_links = result

                    # For each JS link, fetch and apply regex
                    for js_link in js_links:
                        regex_matches = fetch_js_and_apply_regex(js_link, headers, save_js, secrets_file)
                        if regex_matches:
                            results.append({
                                "input": url,
                                "jslink": js_link,
                                "endpoints": regex_matches
                            })
                    
                    #print(f"Processed: {url} - Found {len(js_links)} JS links and {len(results)} links with matches.")
        else:
            # If verbose is False, just process the URLs without a progress bar
            for future in futures:
                result = future.result()  # Call result() on the future object
                if result:
                    url, js_links = result

                    # For each JS link, fetch and apply regex
                    for js_link in js_links:
                        regex_matches = fetch_js_and_apply_regex(js_link, headers, save_js, secrets_file)
                        if regex_matches:
                            results.append({
                                "input": url,
                                "jslink": js_link,
                                "endpoints": regex_matches
                            })
    return results

def load_urls(input_source):
    if input_source.startswith("http://") or input_source.startswith("https://"):
        return [input_source]
    else:
        with open(input_source, 'r') as file:
            return [line.strip() for line in file.readlines()]

def parse_headers(header_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    for header in header_list:
        try:
            key, value = header.split(':', 1)
            headers[key.strip()] = value.strip()
        except ValueError:
            print(f"Invalid header format: {header}")
    return headers

def print_js_banner():
    ascii_art = r"""
    ______                      __  __    _                 __    
   / ____/   _____  _______  __/ /_/ /_  (_)___  ____ _    / /____
  / __/ | | / / _ \/ ___/ / / / __/ __ \/ / __ \/ __ `/_  / / ___/
 / /___ | |/ /  __/ /  / /_/ / /_/ / / / / / / / /_/ / /_/ (__  ) 
/_____/ |___/\___/_/   \__, /\__/_/ /_/_/_/ /_/\__, /\____/____/  
                      /____/                  /____/              
    """
    tagline = "You are running Everything about JS for Secrets | Endpoints | DOM Sinks "
    print(ascii_art)
    print(tagline)



def main():
    print_js_banner()
    parser = argparse.ArgumentParser(description="Extract JS links from a URL or a list of URLs")
    parser.add_argument('-i', '--input', required=False, help="URL or file containing URLs")
    parser.add_argument('-f', '--server', required=False, help="provide output to launch web server")
    parser.add_argument('-o', '--output', help="Output JSON file to save results (optional, prints to CLI if not specified)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose logging")
    parser.add_argument('-H', '--header', action='append', help="Add custom header (can be used multiple times)")
    parser.add_argument('-s', '--secrets_file', action='append', help="add your secrets.regex file containing compatible secrets file")
    parser.add_argument('-sjs', '--save_js', help="save js files to specific location.")
    args = parser.parse_args()

    if args.server:
        filename = args.server
        run_flask_app(filename)
        exit(0)
    
    if not args.input:
        print("[+] args required, run `everythingjs -h`")
        exit(0)

    # Load URLs from input
    urls = load_urls(args.input)
    if args.verbose:
        print(f"Loaded {len(urls)} URL(s) from input.")
    

    # Parse custom headers, including defaults
    headers = parse_headers(args.header if args.header else [])
    if args.verbose:
        print(f"[+] Running in verbose mode")

    # Process URLs and extract JS links
    results = process_urls(urls, headers, args.secrets_file, args.save_js, verbose=args.verbose)

    # If output file is specified, write results to it; otherwise, print to CLI
    if args.output:
        with open(args.output, 'w') as out_file:
            json.dump(results, out_file, indent=2)
        if args.verbose:
            print(f"Results saved to {args.output}")
    else:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
