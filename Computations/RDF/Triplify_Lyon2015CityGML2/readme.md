## Pre-requisites
 - [install docker](https://docs.docker.com/engine/install/)
 - [install Python3.8](https://www.python.org/)
 - virtualenv:
```
pip install virtualenv 
```

## Installing dependencies

Create a python virtual environment and activate it

```bash
$ virtualenv -p python venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt
```

## Running the triplifier workflow

From the same python virtual environment run the workflow

```bash
(venv)$ python run_citygml2_lyon_workflow.py
```

Note that the workflow configuration can be customized in `./demo_setup_citygml2_lyon_workflow.py`