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
import traceback
import hashlib
import time
from datetime import datetime
import sqlite3
from flask import Flask, render_template
from flask_socketio import SocketIO

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

def get_distinct_inputs():
    home_dir = os.path.expanduser("~")
    folder_path = os.path.join(home_dir, ".everythingjs")
    db_path = os.path.join(folder_path, "scan_results.db")
    distinct_values = []

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT input FROM scan_results")
        distinct_values = [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

    return distinct_values

def create_db_with_data():
    # Get the home directory and create the '.everythingjs' folder
    home_dir = os.path.expanduser("~")
    folder_path = os.path.join(home_dir, ".everythingjs")
    os.makedirs(folder_path, exist_ok=True)

    # Define the SQLite database path
    db_path = os.path.join(folder_path, "scan_results.db")

    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the scan_results table with created_at and updated_at
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_results (
            input TEXT,
            jslink TEXT,
            endpoints TEXT,
            secrets TEXT,
            links TEXT,
            mapping BOOLEAN,
            dom_sinks TEXT,
            js_url TEXT,
            md5_hash TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')

    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    # Commit and close the connection
    conn.commit()
    conn.close()

    #print(f"Database created at: {db_path}")


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

def create_app(interval_seconds=5):
    from flask import Flask, render_template
    from flask_socketio import SocketIO
    import random
    import sqlite3
    import time
    from threading import Thread

    # Initialize Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Initialize Flask-SocketIO
    socketio = SocketIO(app)

    # List of random messages
    messages = [
        "System is stable.",
        "Warning: High CPU usage.",
        "Error: Connection lost.",
        "Service restarted successfully.",
        "Alert: Disk space low.",
        "All systems operational.",
    ]

    def fetch_distinct_inputs():
        db_path = os.path.join(os.path.expanduser("~"), ".everythingjs", "scan_results.db")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT input FROM scan_results")
            results = cursor.fetchall()
            return [row[0] for row in results]  # Extracting the input value from each tuple
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def emit_random_message():
        """Emit a random message at the specified interval."""
        while True:
            urls = fetch_distinct_inputs()
            headers = {}
            socketio.emit('new_message', {'message': f'found {len(urls)} urls to process, scan started..' })
            #jdata = process_urls(urls, headers, False, False, False, verbose=False)
            message = random.choice(messages)
            socketio.emit('new_message', {'message': message})
            time.sleep(interval_seconds)

    @app.route('/')
    def index():
        """Serve the monitor page."""
        return render_template('monitor.html')

    # Start the background thread to emit messages
    Thread(target=emit_random_message, daemon=True).start()

    return app, socketio



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

        # Calculate MD5 hash of the JS content
        with open(temp_file_path, 'rb') as temp_file_binary:
            file_content = temp_file_binary.read()
            md5_hash = hashlib.md5(file_content).hexdigest()

        # Apply regex to the content of the JS file
        with open(temp_file_path, 'r', encoding='utf-8') as file:
            js_filename = get_hostname_filename(js_url)
            js_content = file.read()
            try:
                beautified_js = jsbeautifier.beautify(js_content)
            except:
                beautified_js = ""
            js_details = {}

            if save_js:
                os.makedirs(save_js, exist_ok=True)
                with open(f"{save_js}/{js_filename}", 'w', encoding='utf-8') as js_file:
                    js_file.write(beautified_js)
                js_details = {
                    'js_url': js_url,
                    'filename': f"{save_js}/{js_filename}"
                }

            regex_matches = re.findall(regex_str, beautified_js, re.VERBOSE)
            matches = apply_regex_patterns_to_text(file_path_secrets, js_content)
            links_matches = find_matches(js_content)
            dom_sinks = find_xss_sinks(js_content)

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

        # Get the current timestamp
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Return filtered matches, secrets, links, .map status, MD5 hash, and timestamp
        return {
            "endpoints": filtered_matches,
            "secrets": matches,
            "links": links_matches,
            "mapping": map_status,
            "dom_sinks": dom_sinks,
            "js_url": js_details,
            "md5_hash": md5_hash,
            "timestamp": current_timestamp  # Include the timestamp
        }

    except requests.RequestException as e:
        # Log or handle the exception as needed
        return []

def initialize_database():
    home_dir = os.path.expanduser("~")
    folder_path = os.path.join(home_dir, ".everythingjs")
    os.makedirs(folder_path, exist_ok=True)

    db_path = os.path.join(folder_path, "scan_results.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_results (
            input TEXT,
            jslink TEXT PRIMARY KEY,
            endpoints TEXT,
            secrets TEXT,
            links TEXT,
            mapping INTEGER,
            dom_sinks TEXT,
            js_url TEXT,
            md5_hash TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    return conn, cursor, db_path

def process_scan_results(data_list):
    initialize_database()
    home_dir = os.path.expanduser("~")
    folder_path = os.path.join(home_dir, ".everythingjs")
    os.makedirs(folder_path, exist_ok=True)
    db_path = os.path.join(folder_path, "scan_results.db")

    inserted_items = []
    updated_items = []

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO scan_results (input, jslink, endpoints, secrets, links, mapping, dom_sinks, js_url, md5_hash, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        update_query = """
            UPDATE scan_results
            SET endpoints = ?, secrets = ?, links = ?, mapping = ?, dom_sinks = ?, js_url = ?, md5_hash = ?, updated_at = ?
            WHERE jslink = ?
        """
        select_query = "SELECT * FROM scan_results WHERE jslink = ?"

        for data in data_list:
            input_url = data.get("input", "")
            jslink = data.get("jslink", "")
            endpoints = json.dumps(data.get("endpoints", {}).get("endpoints", []))
            secrets = json.dumps(data.get("endpoints", {}).get("secrets", []))
            links = json.dumps(data.get("endpoints", {}).get("links", {}))
            mapping = data.get("endpoints", {}).get("mapping", False)
            dom_sinks = json.dumps(data.get("endpoints", {}).get("dom_sinks", []))
            js_url = json.dumps(data.get("endpoints", {}).get("js_url", {}))
            md5_hash = data.get("endpoints", {}).get("md5_hash", "")
            timestamp = data.get("endpoints", {}).get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("SELECT md5_hash FROM scan_results WHERE jslink = ?", (jslink,))
            existing_row = cursor.fetchone()

            if existing_row:
                existing_md5 = existing_row[0]
                if existing_md5 != md5_hash:
                    cursor.execute(update_query, (endpoints, secrets, links, mapping, dom_sinks, js_url, md5_hash, updated_at, jslink))
                    conn.commit()  # Ensure changes are saved before fetching updated details
                    cursor.execute(select_query, (jslink,))
                    updated_record = cursor.fetchone()
                    updated_items.append({
                        "input": updated_record[0],
                        "jslink": updated_record[1],
                        "endpoints": json.loads(updated_record[2]),
                        "secrets": json.loads(updated_record[3]),
                        "links": json.loads(updated_record[4]),
                        "mapping": updated_record[5],
                        "dom_sinks": json.loads(updated_record[6]),
                        "js_url": json.loads(updated_record[7]),
                        "md5_hash": updated_record[8],
                        "created_at": updated_record[9],
                        "updated_at": updated_record[10],
                        "status": "updated"
                    })
            else:
                cursor.execute(insert_query, (input_url, jslink, endpoints, secrets, links, mapping, dom_sinks, js_url, md5_hash, timestamp, updated_at))
                inserted_items.append({
                    "input": input_url,
                    "jslink": jslink,
                    "endpoints": json.loads(endpoints),
                    "secrets": json.loads(secrets),
                    "links": json.loads(links),
                    "mapping": mapping,
                    "dom_sinks": json.loads(dom_sinks),
                    "js_url": json.loads(js_url),
                    "md5_hash": md5_hash,
                    "created_at": timestamp,
                    "status": "inserted"
                })

        conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    finally:
        conn.close()

    return {"inserted": inserted_items, "updated": updated_items}


def process_urls(urls, headers, secrets_file, save_js, save_db, verbose=False):
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
        if save_db:
            #print("upserting data...")
            changes_results = process_scan_results(results)
    return results, changes_results

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
 / /___ | |/ /  __/ /  / /_/ / /_/ / / / / / / /_/ / /_/ ( /__  ) 
/_____/ |___/\___/_/   \__, /\__/_/ /_/_/_/ /_/\__, /\____/____/  
                      /____/                  /____/              
    """
    tagline = "You are running Everything about JS for Secrets | Endpoints | DOM Sinks"
    x_handle = "================>X @le4rner <================"
    print(ascii_art)
    print(tagline)
    print(x_handle)

def post_to_ui(message_dict):
    # Check if both 'inserted' and 'updated' are empty
    if not message_dict['inserted'] and not message_dict['updated']:
        print("No new or updated entries to display.")
        return None  # Return None to indicate no message was displayed

    # Display inserted messages
    for item in message_dict['inserted']:
        formatted_message = (
            f"🚨 *JS Discovered: {item['input']}* 🚨\n"
            f"JS Link: {item['jslink']}\n"
            f"MD5 Hash: {item['md5_hash']}\n"
            "Endpoints:\n"
            ""
        )
        formatted_message += "\n".join(item['endpoints'])
        formatted_message += ""
        
        print("\n" + "="*50)
        print(formatted_message)
        print("="*50 + "\n")

    # Display updated messages
    for item in message_dict['updated']:
        formatted_message = (
            f"⚠️ *Javascript Updated: {item['input']}* ⚠️\n"
            f"JS Link: {item['jslink']}\n"
            f"MD5 Hash: {item['md5_hash']}"
        )
        
        print("\n" + "="*50)
        print(formatted_message)
        print("="*50 + "\n")

import json
import requests

def post_to_slack(webhook_url, message_dict):
    # Check if both 'inserted' and 'updated' are empty
    if not message_dict['inserted'] and not message_dict['updated']:
        print("No new or updated entries to send.")
        return None  # Return None to indicate no message was sent
    
    headers = {'Content-Type': 'application/json'}
    
    # Send inserted messages
    for item in message_dict['inserted']:
        if item['endpoints']:  # Only proceed if the endpoint list is not empty
            formatted_message = (
                f"🚨 *JS Discovered: {item['input']}* 🚨\n"
                f"JS Link: {item['jslink']}\n"
                f"MD5 Hash: `{item['md5_hash']}`\n"
                "Endpoints:\n"
                "```"
            )
            formatted_message += "\n".join(item['endpoints'])
            formatted_message += "```"
            
            payload = {"text": formatted_message}
            response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                pass
                #print(f"Inserted message for {item['input']} posted successfully!")
            else:
                pass
                #print(f"Failed to post inserted message for {item['input']}. Status Code: {response.status_code}, Response: {response.text}")
    
    # Send updated messages
    for item in message_dict['updated']:
        if item['endpoints']:  # Only proceed if the endpoint list is not empty
            formatted_message = (
                f"⚠️ *Javascript Updated: {item['input']}* ⚠️\n"
                f"JS Link: {item['jslink']}\n"
                f"MD5 Hash: `{item['md5_hash']}`\n"
                "Endpoints:\n"
                "```"
            )
            formatted_message += "\n".join(item['endpoints'])
            formatted_message += "```"
            
            payload = {"text": formatted_message}
            response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                pass
                #print(f"Updated message for {item['input']} posted successfully!")
            else:
                pass
                #print(f"Failed to post updated message for {item['input']}. Status Code: {response.status_code}, Response: {response.text}")


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Extract JS links from a URL or a list of URLs")
    parser.add_argument('-i', '--input', required=False, help="URL or file containing URLs")
    parser.add_argument('-db', '--from_db', action='store_true', required=False, help="consume input from db, past results")
    parser.add_argument('-f', '--server', required=False, help="Provide output to launch web server")
    parser.add_argument('-o', '--output', help="Output JSON file to save results (optional, prints to CLI if not specified)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose logging")
    parser.add_argument('-H', '--header', action='append', help="Add custom header (can be used multiple times)")
    parser.add_argument('-s', '--secrets_file', action='append', help="Add your secrets.regex file containing compatible secrets file")
    parser.add_argument('-sjs', '--save_js', help="Save JS files to specific location.")
    parser.add_argument('-store', '--save_db', action='store_true', default=True, help="Save contents to database in ~/.everythingjs/scan_results.db")
    parser.add_argument('-m', '--monitor', help="Monitor the process at specified intervals (e.g., 2s, 2m, 1d, 4w)")
    parser.add_argument('-slack', '--slack_webhook', help="Pass the slack webhook url where you want to post the message updates")
    parser.add_argument('-j', '--jsonl', action='store_true', help="print output in jsonl format in stdout")
    parser.add_argument('-silent', '--silent', action='store_true', help="dont print anything except output")
    
    args = parser.parse_args()

    if not args.silent:
        print_js_banner()
    create_db_with_data()

    if args.server:
        filename = args.server
        run_flask_app(filename)
        exit(0)
    
    if args.input or args.from_db:
        pass
    else:
        print("[+] args required, run `everythingjs -h`")
        exit(0)

    # Load URLs from input
    if args.from_db:
        urls = get_distinct_inputs()
    elif args.input:
        urls = load_urls(args.input)
    else:
        print("[+] args required, run `everythingjs -h`")
    if args.verbose:
        print(f"Loaded {len(urls)} URL(s) from input.")
    
    # Parse custom headers, including defaults
    headers = parse_headers(args.header if args.header else [])
    if args.verbose:
        print(f"[+] Running in verbose mode")

    # Process URLs and extract JS links
    results, changed_results = process_urls(urls, headers, args.secrets_file, args.save_js, True, verbose=args.verbose)
    if args.slack_webhook:
        post_to_slack(args.slack_webhook, changed_results)
    elif args.jsonl:
        for item in changed_results['updated']:
            print(json.dumps(item))
        for item in changed_results['inserted']:
            print(json.dumps(item))
    else:
        post_to_ui(changed_results)

    # If output file is specified, write results to it; otherwise, print to CLI
    if args.output and not args.monitor:
        with open(args.output, 'w') as out_file:
            json.dump(results, out_file, indent=2)
        if args.verbose:
            print(f"Results saved to {args.output}")
    else:
        pass

    # Process URLs based on the --monitor flag
    
    if args.monitor is not None:
        print(f"Monitoring javascript changes every {args.monitor}")
        interval = parse_interval(args.monitor)
        print(f"Monitoring {len(urls)} urls")
        while True:
            time.sleep(interval)
            if args.verbose:
                print(f"Re-running process after {args.monitor}...")
            results, changed_results = process_urls(urls, headers, args.secrets_file, args.save_js, True, verbose=args.verbose)
            if args.slack_webhook:
                post_to_slack(args.slack_webhook, changed_results)
            else:
                post_to_ui(changed_results)
            if args.output:
                with open(args.output, 'w') as out_file:
                    json.dump(results, out_file, indent=2)
                if args.verbose:
                    print(f"Results saved to {args.output}")
            else:
                pass
                #print(json.dumps(results, indent=2))


def parse_interval(interval):
    """Parse the interval string and return the time in seconds."""
    time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800}
    
    unit = interval[-1]
    if unit not in time_units:
        raise ValueError(f"Invalid time unit in {interval}. Must be one of {', '.join(time_units.keys())}.")
    
    value = int(interval[:-1])
    return value * time_units[unit]

if __name__ == "__main__":
    main()