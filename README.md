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

</div>

## ✨ What is AntiTrapLens?

🕵️‍♂️ **AntiTrapLens** is your digital detective that uncovers hidden manipulation tactics on websites. Using cutting-edge AI and web scraping technology, it detects "dark patterns" - those sneaky design tricks that trick users into unwanted actions.

### 🎯 Key Highlights
- **🤖 AI-Powered Detection**: 14+ sophisticated rules with NLP analysis
- **🌐 Comprehensive Crawling**: Headless browser that bypasses anti-bot protections
- **📈 Smart Scoring**: Grades websites A-F based on darkness level
- **🎨 Beautiful Reports**: Interactive HTML reports with modern UI
- **⚡ Fast & Reliable**: Optimized for speed with robust error handling

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
Scanning https://example.com with depth 1, timeout 30000ms
  Analyzing pages for dark patterns...
JSON report saved to reports/scan_result.json
         Scan Summary
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Metric              ┃ Value ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Pages Scanned       │ 1     │
│ Dark Patterns Found │ 0     │
│ Scan Depth          │ 1     │
└─────────────────────┴───────┘
No dark patterns detected!
```

### HTML Report Preview
![HTML Report](https://via.placeholder.com/800x400/4CAF50/FFFFFF?text=Interactive+HTML+Report+Preview)

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

5. **Download SpaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

6. **Verify installation**
   ```bash
   python main.py --version
   ```

## 📖 Usage

### Basic Commands

```bash
# Simple website scan
python main.py https://example.com

# Deep crawl with HTML report
python main.py https://example.com --depth 3 --report-format html

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
| `--verbose` | Show detailed progress | false |
| `--output` | Output file path | reports/scan_result.json |

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
- 📊 Generate an interactive HTML report
- 📝 Show detailed progress in terminal

## 🏗️ Project Structure

```
AntiTrapLens/
├── 📁 antitraplens/          # Main package
│   ├── cli.py               # Command-line interface 🖥️
│   ├── scraper/             # Web crawling module 🕷️
│   │   ├── crawler.py       # Core crawler with anti-bot
│   │   └── __init__.py
│   ├── detector/            # Detection engine 🧠
│   │   ├── rules.py         # 14+ detection rules + NLP
│   │   └── __init__.py
│   └── reporter/            # Report generation 📊
│       ├── generator.py     # Multi-format report generator
│       └── __init__.py
├── 📁 tests/                 # Unit tests (12 tests) 🧪
│   ├── test_scraper.py
│   ├── test_detector.py
│   └── test_reporter.py
├── 📁 reports/               # Generated reports 📁
├── 📁 docs/                  # Documentation 📚
├── 📁 .github/               # GitHub templates 🤝
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

AntiTrapLens detects **14+ types** of dark patterns:

### 🚨 High Severity
- ❌ **Pre-ticked checkboxes** - Sneaky opt-ins
- 🎭 **Misleading buttons** - NLP detects confusing text
- ⏰ **Countdown timers** - Fake urgency
- 💰 **Hidden costs** - Surprise fees

### ⚠️ Medium Severity
- 📧 **Subscription traps** - Hard to unsubscribe
- 📰 **Fake reviews** - Manufactured testimonials
- 🔒 **Privacy policy issues** - Data collection without consent
- 📢 **Aggressive ads** - Intrusive advertising

### ℹ️ Low Severity
- 🔄 **Endless scroll** - Infinite content loading
- ♿ **Accessibility issues** - Poor UX design
- 📊 **Data collection** - Excessive tracking
- 🎪 **Forced popups** - Modal abuse

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
- Generate reports for consumer protection agencies
- Monitor e-commerce sites for dark patterns

### 🏢 **UX Researchers & Designers**
- Analyze competitor websites for UX best practices
- Identify problematic design patterns
- Benchmark websites against ethical standards

### 🛡️ **Security Professionals**
- Detect phishing attempts and scam websites
- Monitor for data collection violations
- Assess website trustworthiness

### 📊 **Data Scientists & Analysts**
- Study prevalence of dark patterns across industries
- Analyze user manipulation trends
- Generate insights for regulatory bodies

### 🎓 **Students & Educators**
- Learn about ethical web design
- Study real-world UX manipulation techniques
- Teach digital literacy and consumer awareness

### 💼 **Business Owners**
- Ensure your website follows ethical design practices
- Avoid legal issues with consumer protection laws
- Build trust with transparent user experiences

### 🌐 **Web Developers**
- Test your websites for unintended dark patterns
- Improve user experience and conversion ethics
- Stay compliant with emerging UX regulations

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

### 🚀 Upcoming Features
- [ ] **Browser Extension** - Chrome/Firefox extension
- [ ] **API Integration** - REST API for integrations
- [ ] **Database Storage** - Persistent scan history
- [ ] **Real-time Monitoring** - Continuous website watching
- [ ] **Machine Learning** - Advanced pattern recognition
- [ ] **Multi-language Support** - International websites

### 📊 Version History
- **v1.0.0** - Initial release with core features
- **v0.9.0** - Beta with testing framework
- **v0.8.0** - Alpha with basic functionality

## 🛠️ Technologies Used

AntiTrapLens is built with modern, battle-tested technologies:

### Core Technologies
- **🐍 Python 3.8+** - Fast, reliable, and widely adopted
- **🎭 Playwright** - Next-gen browser automation by Microsoft
- **🧠 SpaCy** - Industrial-strength NLP processing
- **🍜 BeautifulSoup** - Robust HTML parsing
- **📊 scikit-learn** - Machine learning capabilities
- **🎨 Rich** - Beautiful terminal output

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

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Playwright** - For headless browser automation
- **SpaCy** - For natural language processing
- **BeautifulSoup** - For HTML parsing
- **Rich** - For beautiful terminal output

## 📞 Contact

**Ahsan Malik**
- 📧 Email: [your-email@example.com](mailto:ahsanmalik919@gmail.com)
- 🐙 GitHub: [@ahsan1o](https://github.com/ahsan1o)
- 💼 LinkedIn: [Your LinkedIn](https://linkedin.com/in/ahsan1o)


---

<div align="center">

**Made with ❤️ by [Ahsan Malik](https://github.com/ahsan1o)**

⭐ **Star this repo if you found it useful!**

[⬆️ Back to Top](#-antitraplens)

</div>