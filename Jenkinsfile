pipeline {
  agent any

  environment {
    PROJECT_NAME = "alright_"
    BRANCH_NAME = "main"
    REPO_URL = "https://github.com/marc-zh/${PROJECT_NAME}.git"
    SONAR_SCANNER_OPTS = "-Xmx512m"
    NODE_OPTIONS = "--max-old-space-size=384"
  }

  stages {
    stage('Checkout') {
      steps {
        echo "Checking out ${REPO_URL} branch ${BRANCH_NAME}"
        git branch: BRANCH_NAME, url: REPO_URL
      }
    }

    stage('Setup Python') {
      steps {
        echo "Setting up Python environment"
        sh """
          python3 --version
          python3 -m pip install --upgrade pip
          pip install -r requirements.txt
        """
      }
    }

    stage('Code Quality Checks') {
      parallel {
        stage('Black Formatter') {
          steps {
            echo "Running Black formatter check"
            sh "black --check . || exit 1"
          }
        }
        stage('Flake8 Linter') {
          steps {
            echo "Running Flake8 linter check"
            sh "flake8 . || exit 1"
          }
        }
      }
    }

    stage('Run Tests') {
      steps {
        echo "Running pytest with coverage"
        sh """
          pytest tests/ -v \
            --cov=src \
            --cov-report=xml \
            --cov-report=term-missing \
            --junitxml=pytest-report.xml
        """
      }
    }

    stage('SonarQube Analysis') {
      steps {
        echo "Starting SonarQube analysis of ${PROJECT_NAME}"
        sh """
          echo "SONAR_SCANNER_OPTS=$SONAR_SCANNER_OPTS"
          echo "NODE_OPTIONS=$NODE_OPTIONS"
        """
        script {
          def scannerHome = tool 'sonar-scanner'
          withSonarQubeEnv('SonarQube') {
            sh """
              ${scannerHome}/bin/sonar-scanner \
              -Dsonar.projectKey=${PROJECT_NAME} \
              -Dsonar.sources=src \
              -Dsonar.language=py \
              -Dsonar.python.coverage.reportPaths=coverage.xml \
              -Dsonar.python.xunit.reportPath=pytest-report.xml
            """
          }
        }
      }
    }
  }

  post {
    always {
      echo 'Pipeline completed'
    }
    success {
      echo 'Pipeline succeeded!'
    }
    failure {
      echo 'Pipeline failed!'
    }
  }
}
