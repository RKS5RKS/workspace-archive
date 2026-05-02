# Coding Expert Reference (v2)

A quick‑reference guide with ready‑to‑copy snippets for everyday development tasks. All examples are **self‑contained** and can be run as‑is (you may need to install a few libraries).

---

## 1. Python Automation

### 1.1 Running shell commands
```python
import subprocess

# Simple command
result = subprocess.run(["ls", "-l"], capture_output=True, text=True)
print(result.stdout)

# With error handling
try:
    out = subprocess.check_output(["git", "status"], text=True)
    print(out)
except subprocess.CalledProcessError as e:
    print("Command failed:", e)
```

### 1.2 Scheduling recurring jobs (using `schedule`)
```python
import schedule
import time

def job():
    print("Running periodic task…")

# Run every 5 minutes
schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```
*Install with:* `pip install schedule`

### 1.3 File/Folder utilities (Pathlib)
```python
from pathlib import Path

# Create a folder if it doesn't exist
Path("logs").mkdir(exist_ok=True)

# List all Python files recursively
for py_file in Path(".").rglob("*.py"):
    print(py_file)
```

### 1.4 Simple automation with `pyautogui`
```python
import pyautogui, time

# Give you 3 seconds to focus the target window
time.sleep(3)

# Move mouse to (100, 200) and click
pyautogui.moveTo(100, 200, duration=0.5)
pyautogui.click()

# Type a phrase and hit Enter
pyautogui.write("Hello, world!", interval=0.05)
pyautogui.press('enter')
```
*Install with:* `pip install pyautogui`

---

## 2. JavaScript / Node.js

### 2.1 Reading & writing files (`fs`)
```js
const fs = require('fs').promises;

// Write a file
async function writeFile() {
  await fs.writeFile('example.txt', 'Hello from Node.js!');
}

// Read a file
async function readFile() {
  const data = await fs.readFile('example.txt', 'utf8');
  console.log(data);
}

writeFile().then(readFile);
```

### 2.2 Spawning child processes
```js
const { exec } = require('child_process');

exec('git rev-parse HEAD', (error, stdout, stderr) => {
  if (error) {
    console.error(`exec error: ${error}`);
    return;
  }
  console.log(`Current commit: ${stdout.trim()}`);
});
```

### 2.3 HTTP requests with `axios`
```js
const axios = require('axios');

(async () => {
  try {
    const res = await axios.get('https://api.github.com/repos/nodejs/node');
    console.log('Stars:', res.data.stargazers_count);
  } catch (err) {
    console.error(err);
  }
})();
```
*Install with:* `npm install axios`

### 2.4 Web automation with **Puppeteer**
```js
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('https://news.ycombinator.com');

  // Grab the titles of the front page
  const titles = await page.$$eval('.storylink', els => els.map(e => e.textContent));
  console.log(titles);

  await browser.close();
})();
```
*Install with:* `npm install puppeteer`

---

## 3. Bash Scripts

### 3.1 Basic script template
```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Example: print the current git branch
branch=$(git rev-parse --abbrev-ref HEAD)
echo "On branch: $branch"
```
Make it executable: `chmod +x script.sh`

### 3.2 Loop over files
```bash
#!/usr/bin/env bash
for file in *.log; do
  echo "Processing $file"
  grep -i "error" "$file" | wc -l
done
```

### 3.3 Using `curl` for quick API calls
```bash
#!/usr/bin/env bash
API="https://api.github.com/repos/owner/repo/releases/latest"
curl -s "$API" | jq -r '.tag_name'
```
*Requires `jq` for JSON parsing (`sudo apt-get install jq`).*

---

## 4. API Integrations

### 4.1 Python – `requests`
```python
import requests

url = "https://jsonplaceholder.typicode.com/posts"
payload = {"title": "foo", "body": "bar", "userId": 1}

resp = requests.post(url, json=payload)
print(resp.status_code)
print(resp.json())
```
*Install with:* `pip install requests`

### 4.2 Node.js – `node-fetch`
```js
const fetch = require('node-fetch');

(async () => {
  const res = await fetch('https://jsonplaceholder.typicode.com/posts/1');
  const data = await res.json();
  console.log(data);
})();
```
*Install with:* `npm install node-fetch@2` (v2 works with CommonJS).

### 4.3 Handling OAuth2 (Python example using `requests_oauthlib`)
```python
from requests_oauthlib import OAuth2Session

client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
auth_base = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

# Redirect user to auth_base + ?client_id=...&scope=repo
# After redirect back, capture `code` query param
code = 'CODE_FROM_CALLBACK'

oauth = OAuth2Session(client_id, redirect_uri='http://localhost/')
token = oauth.fetch_token(token_url, client_secret=client_secret, code=code)
print(token)
```
*Install:* `pip install requests_oauthlib`

---

## 5. Web Scraping

### 5.1 Python – BeautifulSoup
```python
import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

for title in soup.select('.storylink'):
    print(title.get_text())
```
*Install:* `pip install beautifulsoup4 requests`

### 5.2 Python – Scrapy (quick spider)
```python
# file: hackernews_spider.py
import scrapy

class HackerNewsSpider(scrapy.Spider):
    name = "hn"
    start_urls = ["https://news.ycombinator.com/"]

    def parse(self, response):
        for sel in response.css('.athing'):
            yield {
                'title': sel.css('.storylink::text').get(),
                'url': sel.css('.storylink::attr(href)').get()
            }
```
Run with: `scrapy runspider hackernews_spider.py -o hn.json`
*Install:* `pip install scrapy`

### 5.3 Node.js – Cheerio (jQuery‑style parsing)
```js
const fetch = require('node-fetch');
const cheerio = require('cheerio');

(async () => {
  const html = await fetch('https://news.ycombinator.com').then(r => r.text());
  const $ = cheerio.load(html);
  $('.storylink').each((i, el) => {
    console.log($(el).text());
  });
})();
```
*Install:* `npm install node-fetch@2 cheerio`

---

## 6. Git Commands Cheat‑Sheet

| Action | Command |
|--------|---------|
| Clone a repo | `git clone https://github.com/user/repo.git` |
| Create and switch to a new branch | `git checkout -b feature/foo` |
| Stage all changes | `git add .` |
| Commit with message | `git commit -m "Your message"` |
| Push current branch | `git push origin HEAD` |
| Rebase onto master | `git fetch && git rebase origin/master` |
| Stash changes | `git stash` |
| Apply latest stash | `git stash pop` |
| View log with graph | `git log --oneline --graph --decorate --all` |
| Amend last commit (keep message) | `git commit --amend --no-edit` |
| Reset file to HEAD | `git checkout -- path/to/file` |

---

## 7. Common Dev Tools

### 7.1 Docker – simple Dockerfile
```dockerfile
# Use official Python image
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "main.py"]
```
Build & run:
```bash
docker build -t myapp .
docker run --rm -p 8000:8000 myapp
```

### 7.2 Virtual Environments (Python)
```bash
# Create
python -m venv .venv
# Activate (Linux/macOS)
source .venv/bin/activate
# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
# Install deps
pip install -r requirements.txt
```

### 7.3 npm scripts (package.json)
```json
{
  "name": "my-tool",
  "version": "1.0.0",
  "scripts": {
    "start": "node index.js",
    "test": "jest",
    "lint": "eslint .",
    "build": "npm run lint && npm run test"
  }
}
```
Run with `npm run build`.

### 7.4 Linters / Formatters
- **Python:** `black`, `flake8`
  ```bash
  pip install black flake8
  black .
  flake8 .
  ```
- **JavaScript/Node:** `eslint`, `prettier`
  ```bash
  npm install --save-dev eslint prettier
  npx eslint . --fix
  npx prettier --write .
  ```

### 7.5 Continuous Integration (GitHub Actions) – simple workflow
```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest
```
Place in `.github/workflows/ci.yml`.

---

## 8. Quick Tips
- **Shebangs:** Use `#!/usr/bin/env python3` or `#!/usr/bin/env bash` for portable scripts.
- **Error handling:** In Bash, `set -euo pipefail` prevents silent failures.
- **Logging:** In Python, the built‑in `logging` module is preferable over `print` for larger projects.
- **Cross‑platform paths:** Use `pathlib` (Python) or `path` module (`path.join`) in Node.
- **Avoid hard‑coded secrets:** Store them in environment variables or `.env` files and load via `python‑dotenv` or `dotenv` (Node).

---

*Happy coding! 🎉*
