# Contributing to Django CRM Project

First off, thank you for considering contributing to Django CRM Project! It's people like you that make it such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if possible

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python style guide
* Include screenshots in your pull request whenever possible
* End files with a newline
* Avoid platform-dependent code

## Development Process

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Run the tests
5. Push to your fork
6. Submit a Pull Request

### Setting Up Development Environment

```bash
# Clone your fork
git clone git@github.com:your-username/django-crm-project.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up pre-commit hooks
pre-commit install

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest path/to/test_file.py

# Run with coverage report
pytest --cov=crm_project
```

### Code Style

This project uses:
* Black for code formatting
* isort for import sorting
* flake8 for style guide enforcement
* mypy for type checking

Before submitting a pull request, please ensure your code passes all style checks:

```bash
# Format code
black .
isort .

# Check style
flake8
mypy .
```

## Documentation

* Use docstrings for all public modules, functions, classes, and methods
* Follow the Google Python Style Guide for docstrings
* Keep the README.md up to date
* Update CHANGELOG.md for notable changes

## Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
    * 🎨 `:art:` when improving the format/structure of the code
    * 🐛 `:bug:` when fixing a bug
    * ✨ `:sparkles:` when adding a new feature
    * 📝 `:memo:` when writing docs
    * 🔧 `:wrench:` when updating configuration files
    * ⚡️ `:zap:` when improving performance
    * 🔒 `:lock:` when dealing with security
    * ♻️ `:recycle:` when refactoring code
    * 🔥 `:fire:` when removing code or files
    * ✅ `:white_check_mark:` when adding tests

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed
* `question` - Further information is requested
* `wontfix` - This will not be worked on

## Recognition

Contributors will be recognized in the project's README.md and CONTRIBUTORS.md files.

Thank you for contributing to Django CRM Project!