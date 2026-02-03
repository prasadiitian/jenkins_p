# pytest + Jenkins practice

This is a tiny Python project with a few unit tests using `pytest`.

## Run locally (Windows / Linux / macOS)

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
pytest
```

## Jenkins

This repo includes a `Jenkinsfile` for a simple Pipeline job:

- Checks out the repo
- Installs Python deps
- Runs `pytest` and publishes a JUnit test report

Create a **Pipeline** job in Jenkins, point it at this Git repo, and set **Pipeline script from SCM**.
