# Coding Expert Quick Reference Guide

A handy cheat‑sheet of the most useful patterns, best‑practices, and ready‑to‑copy snippets for everyday development tasks. Feel free to copy‑paste and adapt.

---

## 1️⃣ Python
### a) Virtual environments (venv)
```bash
python3 -m venv .venv          # create
source .venv/bin/activate      # activate (Linux/macOS)
# .venv\Scripts\activate      # Windows PowerShell
pip install --upgrade pip
```
### b) Common project layout
```
my_project/
├─ src/               # package code
│   └─ __init__.py
├─ tests/             # pytest tests
│   └─ test_example.py
├─ requirements.txt   # pinned deps
├─ pyproject.toml    # build config (optional)
└─ README.md
```
### c) Script starter (CLI with argparse)
```python
#!/usr/bin/env python3
import argparse

def main(args: argparse.Namespace) -> int:
    print(f"Hello {args.name}!")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demo script")
    parser.add_argument("--name", default="World", help="Name to greet")
    args = parser.parse_args()
    raise SystemExit(main(args))
```
### d) HTTP requests (requests)
```python
import requests
resp = requests.get('https://api.example.com/data', timeout=10)
resp.raise_for_status()
print(resp.json())
```
### e) Async HTTP (httpx)
```python
import httpx, asyncio
async def fetch():
    async with httpx.AsyncClient() as client:
        r = await client.get('https://api.example.com')
        r.raise_for_status()
        print(r.json())
asyncio.run(fetch())
```
### f) Data classes (Python 3.10+)
```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class User:
    id: int
    name: str
    tags: List[str] = None
    active: bool = True
```
### g) FastAPI starter
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    tags: list[str] = []

@app.get('/')
async def root():
    return {"msg": "👋"}

@app.post('/items/')
async def create_item(item: Item):
    return item
```
### h) Flask minimal app
```python
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"msg": "hello"})

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
```
### i) Logging best practice
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)
log.info('started')
```
### j) Context manager for temporary files
```python
import tempfile
with tempfile.NamedTemporaryFile(delete=False) as tf:
    tf.write(b'hello')
    path = tf.name
# path can be used after block
```

---

## 2️⃣ JavaScript / TypeScript
### a) Node.js project init
```bash
npm init -y                # creates package.json
npm i express              # install deps
npm i -D typescript @types/node @types/express   # dev deps for TS
npx tsc --init             # tsconfig.json
```
### b) Simple Express server (TS)
```ts
import express, { Request, Response } from 'express';
const app = express();
app.use(express.json());

app.get('/', (req: Request, res: Response) => {
  res.json({ msg: '👋' });
});

app.post('/echo', (req: Request, res: Response) => {
  res.json(req.body);
});

app.listen(3000, () => console.log('Listening on 3000'));
```
### c) Async/await fetch (node >=18 or with node-fetch)
```ts
const response = await fetch('https://api.example.com/users');
if (!response.ok) throw new Error('Network error');
const data = await response.json();
console.log(data);
```
### d) Type definitions for API payloads
```ts
interface User {
  id: number;
  name: string;
  email?: string;
}
```
### e) React functional component with hooks
```tsx
import React, { useState, useEffect } from 'react';

export const Counter = () => {
  const [count, setCount] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setCount(c => c + 1), 1000);
    return () => clearInterval(id);
  }, []);
  return <div>Count: {count}</div>;
};
```
### f) React fetch with error handling
```tsx
const [data, setData] = useState<User[] | null>(null);
const [error, setError] = useState<string | null>(null);
useEffect(() => {
  fetch('/api/users')
    .then(r => r.ok ? r.json() : Promise.reject(r.statusText))
    .then(setData)
    .catch(setError);
}, []);
```
### g) Vite + React quick start (TS)
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app && npm install && npm run dev
```
### h) Next.js API route (TS)
```ts
// pages/api/hello.ts
import type { NextApiRequest, NextApiResponse } from 'next';
export default function handler(req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({ message: 'Hello from Next.js' });
}
```
### i) ESLint + Prettier config (basic)
```json
// .eslintrc.json
{
  "env": {"browser": true, "es2021": true},
  "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended", "prettier"],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "rules": {}
}
```
### j) npm scripts for lint & format
```json
// package.json (scripts section)
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "lint": "eslint src --ext .ts,.tsx",
  "format": "prettier --write ."
}
```

---

## 3️⃣ Bash / Shell Scripting
### a) Shebang & safe flags
```bash
#!/usr/bin/env bash
set -euo pipefail   # exit on error, undefined var, and pipeline failures
IFS=$'\n\t'        # sane field splitting
```
### b) Argument parsing with `getopts`
```bash
while getopts ":f:o:" opt; do
  case $opt in
    f) FILE="$OPTARG";;
    o) OUT="$OPTARG";;
    \?) echo "Invalid option -$OPTARG" >&2; exit 1;;
  esac
done
shift $((OPTIND-1))
```
### c) Loop over files safely
```bash
for f in ./*.log; do
  [[ -e "$f" ]] || continue   # handle no matches
  echo "Processing $f"
done
```
### d) Using `jq` for JSON
```bash
curl -s https://api.github.com/repos/openai/gpt-4 | jq '.full_name, .stargazers_count'
```
### e) One‑liner to replace text in many files
```bash
grep -rl 'foo' ./src | xargs sed -i '' 's/foo/bar/g'
```
### f) Parallel execution with GNU `parallel`
```bash
parallel -j4 myscript.sh ::: 1 2 3 4 5
```
### g) Temp dir and cleanup
```bash
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT
# use $TMPDIR
```
### h) Exporting environment variables from a file
```bash
set -a; source .env; set +a   # automatically export all vars
```

---

## 4️⃣ HTML / CSS
### a) Boilerplate (HTML5)
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Document</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <main id="app"></main>
</body>
</html>
```
### b) Simple CSS reset (modern)
```css
/* modern-css-reset */
*, *::before, *::after {margin:0;padding:0;box-sizing:border-box;}
html,body {height:100%;}
```
### c) Flexbox centering helper
```css
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}
```
### d) Responsive grid (CSS Grid)
```css
.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}
```
### e) Dark‑mode toggle (CSS variable)
```css
:root {--bg:#fff;--text:#111;}
@media (prefers-color-scheme: dark) {
  :root {--bg:#111;--text:#eee;}
}
body {background:var(--bg);color:var(--text);}
```
### f) Simple button with hover transition
```css
button {
  background:#0069d9; color:#fff; border:none; padding:.5rem 1rem;
  cursor:pointer; transition:background .2s ease;
}
button:hover {background:#0053a6;}
```

---

## 5️⃣ Git Workflows
### a) Typical feature branch flow
```
# create branch from main
git checkout -b feature/my‑feature main
# work, commit frequently
git add . && git commit -m "feat: add something"
# keep up‑to‑date
git fetch origin && git rebase origin/main
# push and open PR
git push -u origin feature/my‑feature
```
### b) Amend last commit (no push yet)
```bash
git commit --amend -m "new message"
```
### c) Squash merge via CLI
```bash
git checkout main
git pull
git merge --squash feature/my-feature
git commit -m "feat: concise description"
```
### d) Rewriting history safely (interactive rebase)
```bash
git rebase -i HEAD~4   # mark commits as pick / squash / edit
```
### e) Stashing uncommitted work
```bash
git stash push -m "WIP: work on X"
# later
git stash pop
```
### f) Submodule add (e.g., common library)
```bash
git submodule add https://github.com/user/lib.git libs/lib
git submodule update --init --recursive
```

---

## 6️⃣ Common Frameworks
### a) React – Context API (TS)
```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

type Theme = 'light' | 'dark';
interface ThemeCtx {theme: Theme; toggle: () => void;}
const ThemeContext = createContext<ThemeCtx | undefined>(undefined);
export const ThemeProvider = ({children}: {children: ReactNode}) => {
  const [theme, setTheme] = useState<Theme>('light');
  const toggle = () => setTheme(t => (t==='light'?'dark':'light'));
  return <ThemeContext.Provider value={{theme, toggle}}>{children}</ThemeContext.Provider>;
};
export const useTheme = () => useContext(ThemeContext)!;
```
### b) Flask – Blueprint pattern
```python
# app/__init__.py
from flask import Flask
from .api import api_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix='/api')
    return app

# app/api.py
from flask import Blueprint, jsonify
api_bp = Blueprint('api', __name__)
@api_bp.get('/ping')
def ping():
    return jsonify({'msg':'pong'})
```
### c) FastAPI – Dependency injection
```python
from fastapi import Depends, FastAPI, HTTPException
app = FastAPI()

def get_token(header: str = Header(...)):
    if header != 'secret':
        raise HTTPException(status_code=401)
    return header

@app.get('/secure')
async def secure(token: str = Depends(get_token)):
    return {'ok': True}
```
### d) React Testing Library (TS)
```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';

test('increments count', async () => {
  render(<Counter />);
  await userEvent.click(screen.getByText(/count:/i));
  expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
});
```
### e) Pytest fixture for temporary DB
```python
import pytest, sqlite3

@pytest.fixture
def db_conn(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(db_file)
    yield conn
    conn.close()
```

---

## 7️⃣ API Integration
### a) OpenAPI client generation (quick)
```bash
pip install openapi-python-client
openapi-python-client generate --url https://api.example.com/openapi.json
```
### b) OAuth2 client credentials flow (requests)
```python
import requests
token_resp = requests.post(
    'https://auth.example.com/oauth2/token',
    data={'grant_type': 'client_credentials'},
    auth=('client_id', 'client_secret')
)
access_token = token_resp.json()['access_token']
api_resp = requests.get('https://api.example.com/resource', headers={'Authorization': f'Bearer {access_token}'})
print(api_resp.json())
```
### c) Retry with backoff (httpx + tenacity)
```python
from tenacity import retry, wait_exponential, stop_after_attempt
import httpx

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
def get_data():
    r = httpx.get('https://unstable.api/')
    r.raise_for_status()
    return r.json()
```
### d) GraphQL query (gql library)
```python
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
transport = RequestsHTTPTransport(url='https://api.spacex.land/graphql/')
client = Client(transport=transport, fetch_schema_from_transport=True)
query = gql('''{ launchesPast(limit: 3) { mission_name launch_date_utc } }''')
result = client.execute(query)
print(result)
```

---

## 8️⃣ Web Scraping
### a) Requests + BeautifulSoup
```python
import requests, bs4
html = requests.get('https://news.ycombinator.com/').text
soup = bs4.BeautifulSoup(html, 'html.parser')
for a in soup.select('a.storylink'):
    print(a.text, a['href'])
```
### b) Headless Chrome with Playwright (async)
```python
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://example.com')
        title = await page.title()
        print('Title:', title)
        await browser.close()

asyncio.run(run())
```
### c) Random user‑agent rotation
```python
import random, requests
UA_LIST = [
    'Mozilla/5.0 ...',
    'Chrome/118.0 ...',
    # add more
]
headers = {'User-Agent': random.choice(UA_LIST)}
resp = requests.get('https://httpbin.org/headers', headers=headers)
print(resp.json())
```
### d) Respect robots.txt (reppy)
```python
from reppy.robots import Robots
robots = Robots.fetch('https://example.com/robots.txt')
if robots.allowed('https://example.com/page', '*'):
    # safe to scrape
    pass
```

---

## 9️⃣ Automation Scripts
### a) Cron entry (Linux) – run every day at 2 am
```
0 2 * * * /usr/bin/python3 /path/to/script.py >> /var/log/myjob.log 2>&1
```
### b) GitHub Actions – simple CI for Node.js
```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run lint
      - run: npm test
```
### c) Dockerfile for Python app (production)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry && poetry install --only main
COPY . .
CMD ["python", "-m", "myapp"]
```
### d) Bash wrapper to sync a directory with rsync (dry‑run first)
```bash
#!/usr/bin/env bash
set -euo pipefail
SRC="/home/user/projects/"
DEST="user@remote:/backup/projects/"
rsync -avzn --delete "$SRC" "$DEST"   # -n = dry run
# remove -n after confirming output
```
### e) Simple CI/CD with GitLab CI – build & deploy Docker image
```yaml
stages:
  - build
  - deploy

build:
  stage: build
  image: docker:latest
  services: [docker:dind]
  script:
    - docker build -t registry.example.com/app:$CI_COMMIT_SHA .
    - docker push registry.example.com/app:$CI_COMMIT_SHA

deploy:
  stage: deploy
  script:
    - echo "Deploy to k8s or server…"
  only:
    - main
```

---

## 📚 How to Use This Guide
- **Copy‑paste** the snippet you need.
- Adjust paths, names, and config values for your project.
- Keep this file in version control (`git add collab/coding_expert_reference.md`).
- When a new technology emerges, prepend a new section – the file is meant to grow.

*Happy coding!*