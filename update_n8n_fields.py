import json

file_path = r"c:/Users/Cyber System/Desktop/clinic aotumation/n8n_project/n8n_workflow.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for node in data.get("nodes", []):
    if node["name"] == "Save to Google Sheets":
        # Add National_ID, Address, Alcohol, Drugs to appended values
        val = dict(node["parameters"]["columns"]["value"])
        val["National_ID"] = "={{$json.body.nationalId}}"
        val["Address"] = "={{$json.body.address}}"
        val["Alcohol"] = "={{$json.body.alcohol}}"
        val["Drugs"] = "={{$json.body.drugs}}"
        
        node["parameters"]["columns"]["value"] = val

    elif node["name"] == "Format Data":
        # Add those fields to the admin JSON response
        js_code = node["parameters"]["jsCode"]
        js_code = js_code.replace(
            "age: item.json.Age,",
            "age: item.json.Age,\n    national_id: item.json.National_ID,\n    address: item.json.Address,\n    alcohol: item.json.Alcohol,\n    drugs: item.json.Drugs,"
        )
        node["parameters"]["jsCode"] = js_code

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated N8N schema for new fields.")
