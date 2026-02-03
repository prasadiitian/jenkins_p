properties([
    parameters([
        [$class: 'FileParameterDefinition', name: 'INPUT_FILE', description: 'Upload a CSV/TXT file to validate (2 numeric columns: a,b).'],
    ]),
])

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
                    if (!params.INPUT_FILE) {
                        error("Missing INPUT_FILE. Use 'Build with Parameters' and upload a file.")
                    }
                    if (isUnix()) {
                        sh '''
                            set -eu
                            python -m pip install --upgrade pip
                            python -m pip install -r requirements.txt
                            mkdir -p reports
                            # Validate uploaded file (Jenkins file parameter is saved in workspace as INPUT_FILE)
                            python -m jenkins_practice.validate --input "${INPUT_FILE}" --outdir reports

                            # Pytest: JUnit + HTML report + capture console output
                            python -m pytest --junitxml=reports/junit.xml --html=reports/pytest_report.html --self-contained-html > reports/pytest_output.txt
                        '''
                    } else {
                        bat "python -m pip install --upgrade pip"
                        bat "python -m pip install -r requirements.txt"
                        bat "if not exist reports mkdir reports"
                        // Validate uploaded file (Jenkins file parameter is saved in workspace as INPUT_FILE)
                        bat "python -m jenkins_practice.validate --input \"%INPUT_FILE%\" --outdir reports"

                        // Pytest: JUnit + HTML report + capture console output
                        bat "python -m pytest --junitxml=reports\\junit.xml --html=reports\\pytest_report.html --self-contained-html > reports\\pytest_output.txt"
                    }
                }
            }
        }
    }

    post {
        always {
            junit 'reports/junit.xml'
            archiveArtifacts artifacts: 'reports/*.*', fingerprint: true
        }
    }
}
