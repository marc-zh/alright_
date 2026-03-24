# CI/CD Schulaufgaben - Comprehensive Plan

## Project Analysis

**Project Type:** Python-based Polymarket Trading Bot
**Repository:** https://github.com/marc-zh/alright_
**Language:** Python 3.x
**Test Framework:** pytest (already configured)
**Current State:**
- ✅ pytest configured (pytest.ini)
- ✅ Existing unit tests in tests/ directory
- ✅ pytest-asyncio, pytest-cov installed
- ❌ No GitHub Actions workflows
- ❌ No CI/CD pipeline
- ❌ No code formatting/linting tools

**Key Adaptation:** Since this is a pure Python backend project (no frontend), tasks will be adapted accordingly.

---

## AUFGABE 1 – LU03.A01: Formatter & Linter in GitHub Actions

**Python Equivalent:**
- **Formatter:** Black (Python code formatter)
- **Linter:** Flake8 (Python linter)
- **Type Checker:** mypy (optional, for static type checking)

### Implementation Plan:

1. **Update requirements.txt** - Add dev dependencies:
   ```txt
   black>=23.0.0
   flake8>=6.0.0
   mypy>=1.0.0
   ```

2. **Create configuration files:**
   - `.flake8` - Flake8 configuration
   - `pyproject.toml` - Black configuration

3. **Create GitHub Actions workflow:**
   - File: `.github/workflows/python_job.yml`
   - Steps:
     - Checkout code
     - Set up Python 3.10+
     - Install dependencies
     - Run Black check
     - Run Flake8 check
     - Run mypy (optional)
     - Run existing tests

4. **Commit message:** `feat: add formatter and linter to CI/CD [LU03.A01]`

---

## AUFGABE 2 – LU04.A01: Jenkins-Pipeline erstellen

**Python Adaptation:**

### Jenkinsfile Structure:

```groovy
pipeline {
  agent any
  environment {
    PROJECT_NAME = "alright_"
    BRANCH_NAME = "main"
    REPO_URL = "https://github.com/marc-zh/${PROJECT_NAME}.git"
    SONAR_SCANNER_OPTS = "-Xmx512m"
  }
  stages {
    stage('Checkout') {
      steps {
        git branch: BRANCH_NAME, url: REPO_URL
      }
    }
    stage('Setup Python') {
      steps {
        sh 'python3 -m venv venv'
        sh '. venv/bin/activate'
        sh 'pip install -r requirements.txt'
      }
    }
    stage('Run Tests') {
      steps {
        sh 'pytest tests/ -v --cov=src'
      }
    }
    stage('SonarQube Analysis') {
      steps {
        sh """
          sonar-scanner \
          -Dsonar.projectKey=${PROJECT_NAME} \
          -Dsonar.sources=src \
          -Dsonar.language=py
        """
      }
    }
  }
}
```

5. **Commit message:** `feat: add Jenkins pipeline [LU04.A01]`

---

## AUFGABE 3 – LU04.A02: SonarQube Issue beheben

**Potential Issues to Fix:**

1. **Unused imports** - Check for unused imports in source files
2. **Missing error handling** - Add proper exception handling
3. **TODO comments** - Remove or address TODO/FIXME comments
4. **Code complexity** - Simplify complex functions
5. **Missing docstrings** - Add docstrings to functions/classes

### Implementation Plan:

1. **Analyze existing code** for common SonarQube issues
2. **Fix at least 1 critical issue** (e.g., unused import, missing error handling)
3. **Document the fix** with comments
4. **Commit message:** `fix: resolve SonarQube code quality issues [LU04.A02]`

---

## AUFGABE 4 – LU05.A01: Frontend Unit-Testing

**Adaptation:** Since there's no frontend, create a simple CLI interface as the "frontend" component.

### Implementation Plan:

1. **Create CLI module:** `src/cli.py`
   - Simple command-line interface for the bot
   - Functions to display market data, place orders, etc.

2. **Add CLI tests:** `tests/test_cli.py`
   - Test CLI argument parsing
   - Test CLI output formatting
   - Use Arrange, Act, Assert pattern

3. **Update GitHub Actions** to run CLI tests

4. **Commit message:** `feat: add CLI interface and unit tests [LU05.A01]`

---

## AUFGABE 5 – LU05.A02: Backend Unit-Testing ergänzen

**Python Backend Tests:**

### Implementation Plan:

1. **Add new test file:** `tests/test_integration_utils.py`
   - Test integration between utils and bot modules
   - Test error scenarios
   - Use Arrange, Act, Assert pattern

2. **Enhance existing tests:**
   - Add edge case tests to existing test files
   - Add async tests for WebSocket client
   - Add coverage for untested functions

3. **Update GitHub Actions** to run all tests with coverage

4. **Commit message:** `feat: add backend unit tests [LU05.A02]`

---

## AUFGABE 6 – LU06.A02: Integration-Tests & Testing Doubles

**Python Test Doubles:**

### Implementation Plan:

1. **Create test doubles directory:** `tests/doubles/`

2. **Create test double classes:**
   - `tests/doubles/ConfigFake.py` - Fake configuration for testing
   - `tests/doubles/ApiClientStub.py` - Stub API responses
   - `tests/doubles/WebSocketMock.py` - Mock WebSocket client

3. **Create integration tests:** `tests/test_integration_bot.py`
   - Test bot initialization with fake config
   - Test order placement with stubbed API
   - Test WebSocket handling with mocked connection

4. **Structure:**
   ```python
   # tests/doubles/ConfigFake.py
   class ConfigFake:
       def __init__(self):
           self.safe_address = "0x123..."
           self.builder_api_key = "test_key"

   # tests/test_integration_bot.py
   from tests.doubles.ConfigFake import ConfigFake

   def test_bot_initialization():
       # Arrange
       fake_config = ConfigFake()
       # Act
       bot = TradingBot(config=fake_config, private_key="0x...")
       # Assert
       assert bot.is_initialized() == True
   ```

5. **Commit message:** `feat: add integration tests with test doubles [LU06.A02]`

---

## Summary of Changes

### Files to Create:
1. `.github/workflows/python_job.yml` - GitHub Actions workflow
2. `Jenkinsfile` - Jenkins pipeline
3. `.flake8` - Flake8 configuration
4. `pyproject.toml` - Black configuration
5. `src/cli.py` - CLI interface (frontend replacement)
6. `tests/test_cli.py` - CLI tests
7. `tests/test_integration_utils.py` - Additional backend tests
8. `tests/test_integration_bot.py` - Integration tests
9. `tests/doubles/ConfigFake.py` - Test double
10. `tests/doubles/ApiClientStub.py` - Test double
11. `tests/doubles/WebSocketMock.py` - Test double

### Files to Modify:
1. `requirements.txt` - Add dev dependencies
2. Existing test files - Fix SonarQube issues

### Commits:
1. `feat: add formatter and linter to CI/CD [LU03.A01]`
2. `feat: add Jenkins pipeline [LU04.A01]`
3. `fix: resolve SonarQube code quality issues [LU04.A02]`
4. `feat: add CLI interface and unit tests [LU05.A01]`
5. `feat: add backend unit tests [LU05.A02]`
6. `feat: add integration tests with test doubles [LU06.A02]`

---

## Next Steps

Ready to proceed with implementation? Each task will be completed sequentially with proper commits and verification that the GitHub Actions pipeline passes.
