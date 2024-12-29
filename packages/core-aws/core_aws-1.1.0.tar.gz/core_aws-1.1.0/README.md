# core-aws
_______________________________________________________________________________

This project/library contains common elements related to AWS services...

## Execution Environment

### Install libraries
```commandline
pip install --upgrade pip 
pip install virtualenv
```

### Create the Python Virtual Environment.
```commandline
virtualenv --python=python3.11 .venv
```

### Activate the Virtual Environment.
```commandline
source .venv/bin/activate
```

### Install required libraries.
```commandline
pip install .
```

### Check tests and coverage...
```commandline
python manager.py run-tests
python manager.py run-coverage
```
