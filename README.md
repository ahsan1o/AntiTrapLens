<div align="center">

# 🔍 AntiTrapLens

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-12%20Passed-brightgreen.svg)](tests/)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)]()
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)

*An advanced OSINT + UX watchdog that scans websites for manipulative design patterns ("dark patterns") using AI-powered detection.*

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-documentation) • [🔧 Installation](#-installation) • [📊 Demo](#-demo)

---

## ✨ What is AntiTrapLens?

🕵️‍♂️ **AntiTrapLens** is your digital detective that uncovers hidden manipulation tactics on websites. Using cutting-edge AI and web scraping technology, it detects "dark patterns" - those sneaky design tricks that trick users into unwanted actions.

### 🎯 Key Highlights
- **🤖 AI-Powered Detection**: 18+ sophisticated rules with enhanced pattern descriptions and user impact analysis
- **🌐 Advanced Crawling**: Headless browser that bypasses anti-bot protections with realistic browser fingerprints
- **🍪 Comprehensive Cookie Analysis**: Detects hidden cookies, third-party tracking, and privacy implications with detailed explanations
- **🖼️ Smart Image Classification**: Categorizes websites (e-commerce, social media, adult, etc.) using image analysis
- **📈 Intelligent Scoring**: Grades websites A-F based on darkness level with detailed breakdowns
- **🎨 Enhanced HTML Reports**: Modern reports with separated dark patterns and tracking analysis, detailed descriptions, and user impact explanations
- **⚡ Fast & Reliable**: Optimized for speed with robust error handling and retry logic
- **🏗️ Modular Architecture**: Clean, maintainable codebase with separate concerns

## 🚀 Quick Start

Get started in 3 simple steps:

```bash
# 1. Clone the repo
git clone https://github.com/ahsan1o/AntiTrapLens.git
cd AntiTrapLens

# 2. Setup environment
python -m venv venv && source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Run your first scan
python main.py https://example.com --verbose
```

**That's it!** You'll get a detailed analysis in seconds. 🎉

### 🎮 Try the Demo
Want to see it in action immediately? Run our interactive demo:

```bash
python demo.py
```

This will scan a sample website and show you the full output!

## 📊 Demo

### Sample Output
```
╭─────────────────────────────────────╮
│ AntiTrapLens - Dark Pattern Scanner │
╰─────────────────────────────────────╮
  Analyzing pages...
HTML report saved to reports/amazon_scan.html
         Scan Summary          
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Metric              ┃ Value ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Pages Scanned       │ 1     │
│ Dark Patterns Found │ 7     │
│ Scan Depth          │ 1     │
└─────────────────────┴───────┘

Top Findings:
• endless_scroll (low): Potential endless scroll or auto-load detected.
• privacy_buried (low): Privacy policy might be buried in long page.
• aggressive_ads (medium): Aggressive ads or overlays detected.
• cookie_consent_banner (low): Cookie consent banner detected - review what data sharing is allowed.
• third_party_tracking (high): Third-party tracking detected from 30 domains
... and 2 more.
```

### HTML Report Features
- 🎨 **Modern Design**: Clean white/black color scheme with visual depth
- 📊 **Separated Analysis**: Distinct sections for dark patterns vs cookies/tracking
- 🔍 **Enhanced Descriptions**: Each pattern includes detailed explanations and user impact
- 🏷️ **Website Categorization**: Prominent display of website category (E-commerce, Social Media, etc.)
- � **Interactive Cards**: Varied heights and hover effects with pattern descriptions
- 🎯 **Educational Content**: "What this means" and "How it affects you" explanations
- 📱 **Responsive**: Works perfectly on mobile and desktop
- 🎯 **Visual Hierarchy**: Clear information architecture with organized sections

## 🔧 Installation

### Prerequisites
- Python 3.8+
- Git
- Internet connection for dependencies

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ahsan1o/AntiTrapLens.git
   cd AntiTrapLens
   ```

2. **Create virtual environment**
   ```bash
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

5. **Download SpaCy model (optional, for enhanced NLP)**
   ```bash
   python -m spacy download en_core_web_sm
   ```

6. **Verify installation**
   ```bash
   python main.py --version
   ```

### Dependencies Overview
- **Core**: `playwright`, `beautifulsoup4`, `rich`
- **Analysis**: `spacy` (optional), `dataclasses`
- **Development**: `pytest`, `black`, `flake8`

## 📖 Usage

### Basic Commands

```bash
# Simple website scan
python main.py https://example.com

# Deep crawl with HTML report
python main.py https://example.com --depth 2 --report-format html --report-file analysis.html

# Verbose mode with progress
python main.py https://example.com --verbose --depth 2

# Custom output location
python main.py https://example.com --output my_scan.json --report-format json
```

### Advanced Options

| Option | Description | Default |
|--------|-------------|---------|
| `--depth` | Crawling depth (1-5) | 1 |
| `--max-pages` | Maximum pages to crawl | 10 |
| `--timeout` | Page load timeout (ms) | 30000 |
| `--report-format` | Output format (json/markdown/html/console) | json |
| `--report-file` | Output file for report | auto-generated |
| `--verbose` | Show detailed progress | false |
| `--version` | Show version information | - |

### Example: Complete Analysis

```bash
python main.py https://suspicious-site.com \
  --depth 2 \
  --max-pages 20 \
  --report-format html \
  --report-file analysis.html \
  --verbose
```

This will:
- 🔍 Crawl 2 levels deep (up to 20 pages)
- 🤖 Analyze each page for dark patterns
- 🍪 Perform comprehensive cookie analysis
- 🖼️ Classify content using image analysis
- 📊 Generate an interactive HTML report
- 📝 Show detailed progress in terminal

## 🏗️ Project Structure

```
AntiTrapLens/
├── 📁 antitraplens/          # Main package
│   ├── core/                 # Core functionality 🧠
│   │   ├── __init__.py
│   │   ├── config.py         # Configuration management
│   │   └── types.py          # Data type definitions
│   ├── crawler/              # Web crawling module 🕷️
│   │   ├── __init__.py
│   │   ├── playwright_crawler.py # Advanced crawler with anti-bot
│   │   ├── base.py           # Base crawler interface
│   │   └── data_extractor.py # HTML data extraction
│   ├── detector/             # Detection engine 🎯
│   │   ├── __init__.py
│   │   ├── engine.py         # Main detection orchestrator
│   │   ├── base.py           # Base detector interface
│   │   └── rules/            # Detection rules
│   │       ├── __init__.py
│   │       ├── dark_patterns.py # Dark pattern rules
│   │       └── cookie_analysis.py # Cookie analysis rules
│   ├── analyzer/             # Content analysis 📊
│   │   ├── __init__.py
│   │   ├── cookie_analyzer.py # Cookie privacy analysis
│   │   ├── image_analyzer.py # Image content analysis
│   │   └── content_analyzer.py # Combined content analysis
│   ├── reporter/             # Report generation 📊
│   │   ├── __init__.py
│   │   ├── base.py           # Base reporter interface
│   │   ├── html_reporter.py  # Premium HTML reports
│   │   ├── json_reporter.py  # JSON output
│   │   ├── markdown_reporter.py # Markdown reports
│   │   └── console_reporter.py # Terminal output
│   ├── cli.py               # Command-line interface 🖥️
│   └── utils/                # Utility functions 🛠️
│       └── __init__.py
├── 📁 tests/                 # Unit tests (12 tests) 🧪
│   ├── __init__.py
│   ├── test_detector.py
│   ├── test_reporter.py
│   └── test_scraper.py
├── 📁 reports/               # Generated reports 📁
├── 📁 docs/                  # Documentation 📚
├── 📁 scripts/               # Utility scripts
├── main.py                  # Entry point 🚀
├── demo.py                  # Quick demo script 🎮
├── requirements.txt         # Dependencies 📦
├── requirements-dev.txt     # Dev dependencies 🔧
├── CONTRIBUTING.md          # Contribution guide 🤝
├── LICENSE                  # MIT License 📄
├── README.md               # This file 📖
└── .gitignore
```

## 🎯 Detection Rules

AntiTrapLens detects **18+ types** of dark patterns with detailed explanations:

### 🚨 High Severity Dark Patterns
- ❌ **Pre-ticked checkboxes** - Can lead to unwanted subscriptions, emails, or data sharing
- 🎭 **Misleading buttons** - May cause accidental agreements to terms or purchases
- ⏰ **Countdown timers** - Pressures you into making hasty decisions
- 💰 **Hidden costs** - Forces you to pay more than advertised
- 🔒 **Subscription traps** - Can result in unwanted recurring charges

### 🍪 High Severity Tracking Issues  
- 📊 **Third-party tracking** - Your browsing data is shared with multiple companies
- 🍪 **Excessive cookies** - Enables extensive tracking across the web
- � **Tracking scripts** - Can track clicks, scrolling, and behavioral data

### ⚠️ Medium Severity
- 📰 **Fake reviews** - Misleads your purchasing decisions
- 📢 **Aggressive ads** - Degrades browsing experience
- 🎪 **Forced popups** - Interrupts your browsing experience

### ℹ️ Low Severity
- 🔄 **Endless scroll** - Designed to keep you on site longer, potentially addictive
- ♿ **Accessibility issues** - Excludes users with disabilities
- 📊 **Data collection** - Compromises your privacy
- 🍪 **Cookie consent banners** - May trick you into accepting more tracking
- 📧 **Hidden unsubscribe** - Makes it hard to stop unwanted communications
- 🏗️ **Overloaded consent** - Tricks you into agreeing to more data collection

## 📈 Scoring System

We grade websites based on detected patterns:

| Score Range | Grade | Description | Color |
|-------------|-------|-------------|-------|
| 0-19 | **A** | 🟢 Clean | Green |
| 20-39 | **B** | 🟡 Minor Issues | Yellow |
| 40-59 | **C** | 🟠 Moderate | Orange |
| 60-79 | **D** | 🔴 High | Red |
| 80+ | **F** | ⚫ Very Dark | Black |

## 🎯 Use Cases

AntiTrapLens is perfect for:

### 🔍 **Digital Privacy Advocates**
- Audit websites for user manipulation tactics
- Generate comprehensive reports for consumer protection agencies
- Monitor e-commerce sites for dark patterns and privacy violations

### 🏢 **UX Researchers & Designers**
- Analyze competitor websites for UX best practices
- Identify problematic design patterns and accessibility issues
- Benchmark websites against ethical design standards

### 🛡️ **Security Professionals**
- Detect phishing attempts and scam websites
- Monitor for data collection violations and tracking abuse
- Assess website trustworthiness and security posture

### 📊 **Data Scientists & Analysts**
- Study prevalence of dark patterns across industries
- Analyze user manipulation trends and patterns
- Generate insights for regulatory bodies and research

### 🎓 **Students & Educators**
- Learn about ethical web design and dark patterns
- Study real-world UX manipulation techniques
- Teach digital literacy and consumer awareness

### 💼 **Business Owners & Marketers**
- Ensure your website follows ethical design practices
- Avoid legal issues with consumer protection laws
- Build trust with transparent user experiences
- Optimize conversion funnels ethically

### 🌐 **Web Developers & QA Teams**
- Test websites for unintended dark patterns
- Improve user experience and accessibility
- Stay compliant with emerging UX regulations
- Perform automated quality assurance

### 🏛️ **Regulatory Bodies & NGOs**
- Monitor websites for compliance with consumer protection laws
- Generate evidence for legal proceedings
- Support consumer advocacy initiatives
- Track industry-wide dark pattern trends

## 🧪 Testing

Run our comprehensive test suite:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=antitraplens

# Run specific test file
pytest tests/test_detector.py -v
```

**Current Status**: ✅ **12/12 tests passing**

## 🤝 Contributing

We love contributions! Here's how you can help:

### Ways to Contribute
- 🐛 **Report bugs** - Open an issue
- 💡 **Suggest features** - Start a discussion
- 🔧 **Code contributions** - Submit a PR
- 📚 **Improve docs** - Update README or docs
- 🧪 **Add tests** - Increase test coverage

### Development Setup
```bash
git clone https://github.com/ahsan1o/AntiTrapLens.git
cd AntiTrapLens
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

### Guidelines
- Follow PEP 8 style
- Add tests for new features
- Update documentation
- Use meaningful commit messages

## 📋 Roadmap

### ✅ **Current Version (v1.0.0)**
- **Enhanced Reporting**: Separated dark patterns and tracking analysis with detailed user impact explanations
- **Modular Architecture**: Clean separation of concerns with improved data flow
- **Advanced Detection**: 18+ dark pattern rules with comprehensive descriptions
- **Enhanced HTML Reports**: Modern design with separated sections and educational content
- **Comprehensive Analysis**: Cookie, image, and content analysis with user impact focus
- **Robust CLI**: Full-featured command-line interface with multiple output formats
- **Configuration Management**: Centralized settings with improved error handling
- **Type Safety**: Full type annotations with enhanced data structures

### 🚀 **Upcoming Features**
- [ ] **Browser Extension** - Chrome/Firefox extension for real-time detection
- [ ] **API Integration** - REST API for third-party integrations
- [ ] **Database Storage** - Persistent scan history and analytics
- [ ] **Real-time Monitoring** - Continuous website watching
- [ ] **Machine Learning** - Advanced pattern recognition with ML models
- [ ] **Multi-language Support** - International websites and localization
- [ ] **Batch Processing** - Scan multiple websites simultaneously
- [ ] **Export Options** - PDF reports and data visualization
- [ ] **Plugin System** - Extensible detection rules
- [ ] **Web Dashboard** - Web-based interface for analysis

### 📊 **Version History**
- **v1.0.0** - Complete modular rewrite with premium HTML reports
- **v0.9.0** - Beta with testing framework and basic functionality
- **v0.8.0** - Alpha with core detection capabilities

## 🛠️ Technologies Used

AntiTrapLens is built with modern, battle-tested technologies:

### Core Technologies
- **🐍 Python 3.8+** - Fast, reliable, and widely adopted
- **🎭 Playwright** - Next-gen browser automation by Microsoft
- **🧠 SpaCy** - Industrial-strength NLP processing
- **🍜 BeautifulSoup** - Robust HTML parsing
- **📊 dataclasses** - Clean data structure definitions
- **🎨 Rich** - Beautiful terminal output
- **🔧 argparse** - Command-line argument parsing

### Architecture
- **🏗️ Modular Design** - Separated concerns with clear interfaces
- **📦 Abstract Base Classes** - Extensible plugin architecture
- **⚙️ Configuration Management** - Centralized settings with nested configs
- **🔄 Context Managers** - Proper resource management
- **📝 Type Hints** - Full type annotation for better code quality

### Development Tools
- **🧪 pytest** - Comprehensive testing framework
- **📦 pip** - Python package management
- **🐙 Git** - Version control
- **📝 Black** - Code formatting
- **🔍 flake8** - Code linting

### Why These Technologies?
- **Performance**: Optimized for speed and memory efficiency
- **Reliability**: Mature libraries with active maintenance
- **Security**: Safe dependencies with no known vulnerabilities
- **Scalability**: Designed to handle large-scale web crawling
- **Extensibility**: Easy to add new detection rules and features
- **Maintainability**: Clean, modular architecture for long-term development

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Playwright** - For headless browser automation
- **SpaCy** - For natural language processing
- **BeautifulSoup** - For HTML parsing
- **Rich** - For beautiful terminal output

## 📞 Contact

**Ahsan Malik**
- 📧 Email: [ahsanmalik919@gmail.com](mailto:ahsanmalik919@gmail.com)
- 🐙 GitHub: [@ahsan1o](https://github.com/ahsan1o)
- 💼 LinkedIn: [LinkedIn](https://linkedin.com/in/ahsan1o)


---

<div align="center">

**Made with ❤️ by [Ahsan Malik](https://github.com/ahsan1o)**

⭐ **Star this repo if you found it useful!**

[⬆️ Back to Top](#-antitraplens)

---

## 🎉 Recent Updates

### v1.0.0 - Enhanced Reporting & User Education
- 🏗️ **Enhanced Architecture**: Improved data flow with separated dark patterns and tracking analysis
- 🎨 **Educational Reports**: Detailed explanations of what each pattern means and how it affects users
- 🤖 **Enhanced Detection**: 18+ sophisticated dark pattern rules with comprehensive descriptions
- 🍪 **Advanced Cookie Analysis**: Separated tracking analysis with detailed privacy impact explanations
- 🏷️ **Website Categorization**: Prominent category display (E-commerce, Social Media, etc.)
- ⚡ **Improved Performance**: Optimized reporting with better error handling and data organization
- 📱 **Better UX**: Clear separation between manipulative design and tracking issues
- 🧪 **Enhanced Testing**: Comprehensive test suite with improved pattern classification

*AntiTrapLens now provides educational insights helping users understand the impact of dark patterns and tracking on their digital privacy!*

</div>