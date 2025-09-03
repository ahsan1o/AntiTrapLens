# Contributing to AntiTrapLens

Thank you for your interest in contributing to AntiTrapLens! 🎉 We welcome contributions from everyone.

## Ways to Contribute

### 🐛 Report Bugs
- Use the [GitHub Issues](https://github.com/ahsan1o/AntiTrapLens/issues) page
- Include detailed steps to reproduce
- Add screenshots if applicable
- Specify your environment (OS, Python version, etc.)

### 💡 Suggest Features
- Start a [GitHub Discussion](https://github.com/ahsan1o/AntiTrapLens/discussions)
- Describe the problem you're trying to solve
- Explain why this feature would be useful

### 🔧 Code Contributions
- Fork the repository
- Create a feature branch
- Make your changes
- Add tests
- Submit a Pull Request

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment tool (venv)

### Setup Steps

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AntiTrapLens.git
   cd AntiTrapLens
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Install Playwright**
   ```bash
   playwright install
   ```

5. **Download SpaCy Model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Development Workflow

### 1. Choose an Issue
- Check [open issues](https://github.com/ahsan1o/AntiTrapLens/issues)
- Comment on the issue to indicate you're working on it
- Wait for maintainer approval

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# OR
git checkout -b fix/issue-number-description
```

### 3. Make Changes
- Follow PEP 8 style guidelines
- Write clear, concise commit messages
- Add docstrings to new functions
- Update documentation if needed

### 4. Add Tests
- Write unit tests for new features
- Ensure all existing tests pass
- Aim for high test coverage

### 5. Test Your Changes
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=antitraplens --cov-report=html

# Run specific tests
pytest tests/test_detector.py -v
```

### 6. Update Documentation
- Update README.md if needed
- Add docstrings to new code
- Update any relevant documentation

### 7. Commit and Push
```bash
git add .
git commit -m "feat: add new detection rule for XYZ"
git push origin feature/your-feature-name
```

### 8. Create Pull Request
- Go to your fork on GitHub
- Click "New Pull Request"
- Fill out the PR template
- Wait for review

## Coding Guidelines

### Python Style
- Follow [PEP 8](https://pep8.org/)
- Use type hints where possible
- Maximum line length: 88 characters
- Use descriptive variable names

### Commit Messages
Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

### Testing
- Write tests for all new features
- Maintain >80% code coverage
- Test edge cases
- Use descriptive test names

## Project Structure

```
antitraplens/
├── cli.py              # CLI interface
├── scraper/            # Web scraping logic
├── detector/           # Detection rules and scoring
└── reporter/           # Report generation
```

## Adding New Detection Rules

1. Add your rule to `antitraplens/detector/rules.py`
2. Implement the detection logic
3. Add appropriate severity level
4. Write unit tests in `tests/test_detector.py`
5. Update documentation

## Questions?

Feel free to:
- Open a [GitHub Discussion](https://github.com/ahsan1o/AntiTrapLens/discussions)
- Join our [Discord server](https://discord.gg/antitraplens) (if available)
- Email the maintainers

## Recognition

Contributors will be:
- Listed in the README.md
- Added to the project's contributor graph
- Recognized in release notes

Thank you for contributing to AntiTrapLens! 🚀
