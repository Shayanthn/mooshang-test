import json
import uuid

file_path = "c:/Users/Cyber System/Desktop/clinic aotumation/n8n_project/n8n_workflow.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 1. Create the HTTP Request node to call our Local AI
http_ai_node = {
  "parameters": {
    "method": "POST",
    "url": "http://host.docker.internal:5001/ask-ai",
    "sendBody": True,
    "specifyBody": "json",
    "jsonBody": "={ \"message\": \"{{$json.message.text}}\", \"user_id\": \"{{$json.message.from.id}}\" }",
    "options": {}
  },
  "name": "Ask AI FAQ",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.1,
  "position": [112, 850],
  "id": str(uuid.uuid4())
}

# 2. Create the Telegram node to send AI reply to the user
telegram_ai_reply_node = {
  "parameters": {
    "chatId": "={{ $('Telegram Trigger').first().json.message.from.id }}",
    "text": "={{ $json.reply }}",
    "additionalFields": {
      "parse_mode": "HTML"
    }
  },
  "name": "Send AI Reply to Patient",
  "type": "n8n-nodes-base.telegram",
  "typeVersion": 1,
  "position": [320, 850],
  "id": str(uuid.uuid4()),
  "credentials": {
    "telegramApi": {
      "id": "vXlmVUHJDbuCCLw6",
      "name": "Telegram account 2"
    }
  }
}

# Add nodes
data["nodes"].append(http_ai_node)
data["nodes"].append(telegram_ai_reply_node)

# 3. Add connections
# From "Forward To Admin" to "Ask AI FAQ"
if "Forward To Admin" not in data["connections"]:
    data["connections"]["Forward To Admin"] = {"main": [[]]}

data["connections"]["Forward To Admin"]["main"][0].append({
    "node": "Ask AI FAQ",
    "type": "main",
    "index": 0
})

# From "Ask AI FAQ" to "Send AI Reply to Patient"
data["connections"]["Ask AI FAQ"] = {
    "main": [
        [
            {
                "node": "Send AI Reply to Patient",
                "type": "main",
                "index": 0
            }
        ]
    ]
}

# Update URL to 127.0.0.1 if n8n is running directly on Windows
for n in data["nodes"]:
    if n["name"] == "Ask AI FAQ":
        n["parameters"]["url"] = "http://127.0.0.1:5001/ask-ai"

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("AI Nodes connected successfully!")
