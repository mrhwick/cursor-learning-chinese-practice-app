# Getting started (macOS)

This repo is designed to be learned **with Cursor**.

If you’re totally new, read `docs/ABSOLUTE_BEGINNER.md` first.

## Step 0: Open the repo in Cursor

If you already have the repo folder on your computer:
- Open Cursor
- File → Open Folder…
- Choose the `learning-to-code` folder

If you need to download it from GitHub later, ask your instructor for the link and use either:\n
- GitHub Desktop (easiest), or\n
- `git clone` (more advanced)

## Step 1: Install prerequisites (tools)

You need 2 tools installed:
- **Node.js** (for the web app tooling)
- **Python** (for the API server)

### Option A (recommended): install with Homebrew

Homebrew is an app installer for macOS.

1) Install Homebrew by following the instructions on [Homebrew](https://brew.sh).

2) Install Node and Python:

```bash
brew install node@20 python@3.11
```

3) Confirm they installed:

```bash
node -v
python3 --version
```

You should see something like Node 20+ and Python 3.11+.

## Step 2: Install web dependencies (first time)

Open the Terminal in Cursor (View → Terminal).

Run:

```bash
cd apps/web
npm install
```

## Step 3: Install API dependencies (first time)

This uses a Python **virtual environment** (“venv”) so the project’s packages don’t mix with anything else.

Run:

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e ".[dev]"
```

## Step 4: Run the app

From the repo root (top-level folder), run:

```bash
./scripts/dev.sh
```

What “success” looks like:
- You see 2 servers start (web + api) in the terminal.
- You can open `http://localhost:5173` in your browser.

## Tests (API)

```bash
./scripts/test_api.sh
```

## Cursor workflow (recommended)

For each lesson:
- open the lesson file in `lessons/`
- add the whole file to Cursor chat context
- tell the agent: “Follow the Agent Contract”
- implement tasks in small steps; run after each step

