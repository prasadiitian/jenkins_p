pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install + Test') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            set -eu
                            python -m pip install --upgrade pip
                            python -m pip install -r requirements.txt
                            mkdir -p reports
                            pytest --junitxml=reports/junit.xml
                        '''
                    } else {
                        bat "python -m pip install --upgrade pip"
                        bat "python -m pip install -r requirements.txt"
                        bat "if not exist reports mkdir reports"
                        bat "pytest --junitxml=reports\\junit.xml"
                    }
                }
            }
        }
    }

    post {
        always {
            junit 'reports/junit.xml'
        }
    }
}
