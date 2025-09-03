# AntiTrapLens

An advanced OSINT + UX watchdog that scans websites for manipulative design patterns ("dark patterns") using AI-powered detection.

## Features
- **Comprehensive Crawling**: Headless browser extraction of HTML, CSS, JS, popups, forms, and more.
- **Depth Crawling**: Follow internal links up to specified depth.
- **AI-Powered Detection**: 14+ rule-based heuristics + NLP analysis for misleading text.
- **Scoring System**: Rate websites 0-100 with grades (A-F) based on darkness level.
- **Multi-Format Reports**: JSON, Markdown, or console output.
- **Extensive Rules**: Detects pre-ticked checkboxes, hidden costs, fake reviews, subscription traps, accessibility issues, and more.

## Installation
1. Clone: `git clone https://github.com/ahsan1o/AntiTrapLens.git`
2. Virtual env: `python -m venv venv && source venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Playwright: `playwright install`
5. SpaCy model: `python -m spacy download en_core_web_sm`

## Usage
```bash
# Basic scan
python main.py https://example.com/

# Depth crawl with markdown report
python main.py https://example.com/ --depth 2 --report-format markdown --report-file report.md

# Console report
python main.py https://example.com/ --report-format console
```

## Project Structure
- `antitraplens/`
  - `cli.py` - CLI with options
  - `scraper/` - Web crawling logic
  - `detector/` - 14+ detection rules + NLP + scoring
  - `reporter/` - JSON/Markdown/console reports
- `tests/` - Unit tests
- `docs/` - Documentation
- `scripts/` - Setup scripts
- `reports/` - Output files

## Detection Rules
- Pre-ticked checkboxes
- Hidden unsubscribe links
- Overloaded consent banners
- Misleading buttons (with NLP)
- Forced popups/modals
- Countdown timers
- Endless scroll
- Hidden costs
- Fake reviews
- Subscription traps
- Privacy policy issues
- Aggressive ads
- Data collection
- Accessibility issues

## Scoring
- **0-19**: A (Clean)
- **20-39**: B (Minor issues)
- **40-59**: C (Moderate)
- **60-79**: D (High)
- **80+**: F (Very dark)

## Contributing
Open issues/PRs. Add more rules or improve NLP!