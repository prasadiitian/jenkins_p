properties([
    parameters([
        [$class: 'FileParameterDefinition', name: 'INPUT_FILE', description: 'Upload a CSV/TXT file to validate (2 numeric columns: a,b).'],
    ]),
])

pipeline {
    agent any

    environment {
        PYTHONPATH = 'src'
    }

    options {
        timestamps()
    }

    stages {
        stage('Install + Test') {
            steps {
                script {
                    def inputPath = ((env.INPUT_FILE ?: params.INPUT_FILE) ?: '').toString().trim()
                    if (!inputPath) {
                        echo "INPUT_FILE not provided. Falling back to sample_input.csv."
                        echo "Tip: use 'Build with Parameters' to upload INPUT_FILE."
                        inputPath = 'sample_input.csv'
                        currentBuild.result = 'UNSTABLE'
                    }

                    env.VALIDATION_INPUT = inputPath
                    echo "Using input file: ${env.VALIDATION_INPUT}"

                    if (isUnix()) {
                        sh '''
                            set -eu
                            python -m pip install --upgrade pip
                            python -m pip install -r requirements.txt
                            mkdir -p reports
                            # Validate uploaded file (Jenkins file parameter is saved in workspace as INPUT_FILE)
                            python -m jenkins_practice.validate --input "$VALIDATION_INPUT" --outdir reports

                            # Pytest: JUnit + HTML report + capture console output
                            python -m pytest --junitxml=reports/junit.xml --html=reports/pytest_report.html --self-contained-html > reports/pytest_output.txt
                        '''
                    } else {
                        bat "python -m pip install --upgrade pip"
                        bat "python -m pip install -r requirements.txt"
                        bat "if not exist reports mkdir reports"
                        // Validate uploaded file (Jenkins file parameter is saved in workspace as INPUT_FILE)
                        bat "python -m jenkins_practice.validate --input \"%VALIDATION_INPUT%\" --outdir reports"

                        // Pytest: JUnit + HTML report + capture console output
                        bat "python -m pytest --junitxml=reports\\junit.xml --html=reports\\pytest_report.html --self-contained-html > reports\\pytest_output.txt"
                    }
                }
            }
        }
    }

    post {
        always {
            junit testResults: 'reports/junit.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'reports/*.*', fingerprint: true, allowEmptyArchive: true
        }
    }
}
