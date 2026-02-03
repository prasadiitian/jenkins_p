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
                    def originalName = (env.INPUT_FILE ?: '').toString().trim()
                    echo "Debug: env.INPUT_FILE='${originalName}'"

                    // Some Jenkins setups store file parameters under WORKSPACE@tmp.
                    // Try to materialize it into the workspace as INPUT_FILE.
                    if (isUnix()) {
                        sh '''
                            set +e
                            if [ -f "$WORKSPACE@tmp/INPUT_FILE" ] && [ ! -f "INPUT_FILE" ]; then
                              cp "$WORKSPACE@tmp/INPUT_FILE" "INPUT_FILE"
                            fi
                            if [ -n "${INPUT_FILE:-}" ] && [ -f "$WORKSPACE@tmp/${INPUT_FILE}" ] && [ ! -f "${INPUT_FILE}" ]; then
                              cp "$WORKSPACE@tmp/${INPUT_FILE}" "${INPUT_FILE}"
                            fi
                            set -e
                        '''
                    } else {
                        bat "@echo off"
                        bat "if exist \"%WORKSPACE%@tmp\\INPUT_FILE\" if not exist INPUT_FILE copy /y \"%WORKSPACE%@tmp\\INPUT_FILE\" INPUT_FILE >nul"
                        bat "if not \"%INPUT_FILE%\"==\"\" if exist \"%WORKSPACE%@tmp\\%INPUT_FILE%\" if not exist \"%INPUT_FILE%\" copy /y \"%WORKSPACE%@tmp\\%INPUT_FILE%\" \"%INPUT_FILE%\" >nul"
                        bat "echo Debug: dir workspace root"
                        bat "dir /a /b"
                        bat "echo Debug: dir workspace@tmp"
                        bat "if exist \"%WORKSPACE%@tmp\" dir /a /b \"%WORKSPACE%@tmp\""
                    }

                    // Resolve which path we should validate.
                    def candidates = []
                    if (originalName) {
                        candidates << originalName
                    }
                    candidates << 'INPUT_FILE'
                    candidates << 'sample_input.csv'

                    def found = candidates.find { p -> fileExists(p) }
                    if (!found) {
                        error("Unable to locate input file in workspace. Tried: ${candidates.join(', ')}")
                    }

                    if (found == 'sample_input.csv') {
                        echo "Using sample_input.csv (no usable upload found)."
                        currentBuild.result = 'UNSTABLE'
                    }

                    env.VALIDATION_INPUT = found
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
