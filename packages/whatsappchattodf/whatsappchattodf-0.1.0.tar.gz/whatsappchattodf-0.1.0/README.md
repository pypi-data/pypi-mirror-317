# WhatsappChatToDF

`WhatsappChatToDF` is a Python library that converts WhatsApp chat logs into a pandas DataFrame for analysis.

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