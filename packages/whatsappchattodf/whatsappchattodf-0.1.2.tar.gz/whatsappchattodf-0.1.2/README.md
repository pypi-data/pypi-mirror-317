# WhatsappChatToDF

`WhatsappChatToDF` is a Python library that converts WhatsApp chat logs into a pandas DataFrame for analysis.

### Directory Structure
```bash
WhatsappChatToDF/
|__ whatsappchattodf/
│   |__ __init__.py
│   |__ whatsappchattodf.py
│
|__ tests/
│   |__ __init__.py
│   |__ test_whatsappchattodf.py
│
|__ LICENSE
|__ README.md
|__ setup.py
|__ pyproject.toml
```

### Build and Publish in PyPI
1. Install dependencies
```bash
pip install setuptools wheel twine
```
2. Build the package
```bash
python setup.py sdist bdist_wheel
```
3. Upload to PyPI (need an account + token)
```bash
twine upload dist/*
```

## Installation

```bash
pip install whatsappchattodf
```

```python
from whatsappchattodf import WhatsappChatToDF

chat_to_df = WhatsappChatToDF("path_to_whatsapp_chat.txt")
df = chat_to_df.run()
print(df)
```