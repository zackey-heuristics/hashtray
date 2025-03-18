# SETUP FOR DEVELOPMENT
```shell
python -m pip ./.venv/
source .venv/bin/activate
pip install pipenv
pipenv install
pipenv shell
```

# EXECUTE
```shell
python -m hashtray.cli
python -m hashtray.hashtray_json_output
```

# PIPX
```
pipx install . --force
pipx git+https://github.com/zackey-heuristics/hashtray
```