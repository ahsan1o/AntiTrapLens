# AntiTrapLens

An advanced OSINT + UX watchdog that scans websites for manipulative design patterns ("dark patterns") using AI-powered detection.

## Features
- **Comprehensive Crawling**: Headless browser extraction of HTML, CSS, JS, popups, forms, and more.
- **Depth Crawling**: Follow internal links up to specified depth.
- **AI-Powered Detection**: 14+ rule-based heuristics + NLP analysis for misleading text.
- **Website Categorization**: Automatically detects site type (e.g., Ecommerce, Adult, Streaming).
- **Scoring System**: Rate websites 0-100 with grades (A-F) based on darkness level.
- **Interactive Reports**: HTML reports with collapsible sections, charts, and modern UI.
- **Multi-Format Reports**: JSON, Markdown, HTML, or console output.
- **Anti-Bot Bypass**: Handles Cloudflare and similar protections.

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

# Depth crawl with interactive HTML report
python main.py https://example.com/ --depth 2 --report-format html --report-file report.html

# Console report
python main.py https://example.com/ --report-format console
```

## Project Structure
```
antitraplens/
├── cli.py              # CLI with options
├── scraper/            # Web crawling logic
│   ├── __init__.py
│   └── crawler.py      # Crawler with anti-bot, categorization
├── detector/           # Detection rules + NLP + scoring
│   ├── __init__.py
│   └── rules.py        # 14+ rules, scoring
└── reporter/           # Report generation
    ├── __init__.py
    └── generator.py    # JSON/Markdown/HTML/console reports
```

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

Developed by **Ahsan Malik** | [GitHub: ahsan1o](https://github.com/ahsan1o)