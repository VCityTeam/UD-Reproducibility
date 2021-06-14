## Developers

### Linting the python source
In order to apply the coding style
```
$ virtualenv -p python3 venv
$ source venv/bin/activate
(venv) pip install -r requirements.tx
```
The manual application of pylint is done with
```
(venv) pylint python_setup.py
```

### For direnv users
```
ln -s .envrc.tpl .envrc
$ direnv allow
(venv)
```
