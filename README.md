# AntiTrapLens

An OSINT + UX watchdog that scans websites for manipulative design patterns ("dark patterns") like hidden cookie banners, pre-ticked checkboxes, forced opt-ins, and misleading CTAs.

## Features
- Crawl websites using headless browser (Playwright)
- Detect common dark patterns with rule-based heuristics
- Generate reports in JSON/Markdown
- CLI interface for easy use

## Installation
1. Clone the repo: `git clone https://github.com/ahsan1o/AntiTrapLens.git`
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Install Playwright browsers: `playwright install`

## Usage
Run the basic crawler:
```
python main.py https://example.com
```

## Project Structure
- `antitraplens/` - Main package
  - `cli.py` - Command-line interface
  - `scraper/` - Web scraping logic
  - `detector/` - Dark pattern detection rules
  - `reporter/` - Report generation
- `tests/` - Unit tests
- `docs/` - Documentation
- `scripts/` - Setup scripts

## Phases
- Phase 1: Basic setup and crawler (current)
- Phase 2: Enhanced scraper
- Phase 3: Detection engine
- Phase 4: Report generator
- Phase 5: UI/CLI polish
- Phase 6: Advanced features (AI, web UI)

## Contributing
Feel free to open issues or PRs!