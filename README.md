```bash
# python and venv
pyenv local 3.11.7
pyenv exec python -m venv .venv
source .venv/bin/activate
# poetry
pip install -U pip setuptools
pip install poetry # 2.2.1
poetry init
# streamlit
poetry add streamlit # 1.50.0
streamlit run your_script.py [-- script args]
```
