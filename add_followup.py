import json
import uuid

file_path = "c:/Users/Cyber System/Desktop/clinic aotumation/n8n_project/n8n_workflow.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 1. Update JS code in "Compute Days & Build Messages"
for node in data.get("nodes", []):
    if node["name"] == "Compute Days & Build Messages":
        new_js = """const now = new Date();
const todayStr = now.toISOString().split('T')[0];
const startOfToday = new Date(todayStr + "T00:00:00.000Z");

const items = [];
for (const item of $input.all()) {
  const appointmentStr = item.json.Appointment;
  if (!appointmentStr) continue;

  const appointDate = new Date(appointmentStr + "T00:00:00.000Z");
  if (isNaN(appointDate.getTime())) continue;

  const diffTime = appointDate.getTime() - startOfToday.getTime();
  const daysUntil = Math.round(diffTime / (1000 * 60 * 60 * 24)); // منفی به معنی گذشتن از عمل است

  let reminderType = null;
  if (daysUntil === 20) reminderType = 'reminder_20days';
  else if (daysUntil === 2) reminderType = 'reminder_2days';
  else if (daysUntil === 1) reminderType = 'reminder_night_before';
  else if (daysUntil === 0) reminderType = 'reminder_surgery_day';
  else if (daysUntil === -3) reminderType = 'followup_day3';
  else if (daysUntil === -7) reminderType = 'followup_day7';
  else continue;

  const p = item.json;
  const name = p.Name || '';
  const age = parseInt(p.Age) || null;

  const smoker = (p.Smoker || '').toString().toLowerCase() === 'yes' || p.Smoker === 'دارد' || p.Smoker === 'بله';
  const diabetes = (p.Diabetes || '').toString().toLowerCase() === 'yes' || p.Diabetes === 'دارد' || p.Diabetes === 'بله';
  const allergies = p.Allergies || '';

  let extraWarnings = '';
  if (smoker) extraWarnings += '\\n🚭 شما سابقه مصرف دخانیات ثبت کرده‌اید. لطفا حداقل ۲ هفته قبل از عمل مصرف دخانیات را متوقف کنید.';
  if (diabetes) extraWarnings += '\\n🩸 با توجه به دیابت، حتما قند خون خود را کنترل کرده و روز عمل داروهای قند خود را همراه داشته باشید.';
  if (age !== null && age >= 65) extraWarnings += '\\n👴👵 با توجه به سن شما، تاییدیه قلب و عروق (اکو) الزامی است.';
  if (allergies && allergies !== 'ندارد' && allergies !== 'خیر') extraWarnings += `\\n⚠️ هشدار حساسیت: در پرونده شما حساسیت به "${allergies}" ثبت شده است. حتما پیش از عمل به پزشک یادآوری کنید.`;

  let header, body;
  if (reminderType === 'reminder_20days') {
    header = '🔔 <b>۲۰ روز مانده به عمل</b>\\n\\n' + name + ' عزیز، ۲۰ روز تا تاریخ عمل شما زمان باقیست.';
    body = '\\n📌 <b>وظایف شما:</b>\\n- لطفا آزمایشات قبل از عمل را در اسرع وقت انجام دهید تا در صورت وجود مشکل، فرصت درمان باشد.' + extraWarnings;
  } else if (reminderType === 'reminder_2days') {
    header = '🔔 <b>۲ روز مانده به عمل</b>\\n\\n' + name + ' عزیز، تنها ۲ روز تا عمل شما باقیست.';
    body = '\\n📌 <b>لطفا توجه کنید:</b>\\n- مصرف داروهای رقیق‌کننده خون را متوقف کنید.\\n- در صورت داشتن علائم سرماخوردگی فورا به کلینیک اطلاع دهید.' + extraWarnings;
  } else if (reminderType === 'reminder_night_before') {
    header = '🔔 <b>شب قبل از عمل</b>\\n\\n' + name + ' عزیز، فردا روز عمل شماست.';
    body = '\\n- لطفا از ساعت ۱۲ امشب <b>ناشتا</b> باشید (حتی آب ننوشید).\\n- مدارک پزشکی، جواب آزمایشات و کارت شناسایی را آماده کنید.\\n- شام سبک میل کنید و استراحت کافی داشته باشید.' + extraWarnings;
  } else if (reminderType === 'reminder_surgery_day') {
    header = '🔔 <b>روز عمل</b>\\n\\n' + name + ' عزیز، امروز منتظر شما هستیم!';
    body = '\\n- لطفا با یک همراه مراجعه کنید.\\n- هیچ‌گونه زیورآلات همراه نداشته باشید.\\n- در زمان تعیین شده در کلینیک حضور یابید.' + extraWarnings;
  } else if (reminderType === 'followup_day3') {
    header = '🩺 <b>پیگیری روز سوم پس از عمل</b>\\n\\n' + name + ' عزیز، امیدواریم حالتان خوب باشد.';
    body = '\\nلطفا به ما اطلاع دهید وضعیت درد شما چگونه است؟ (از ۱ تا ۱۰ به درد خود چه نمره‌ای می‌دهید؟ در همین صفحه ارسال کنید)\\n\\nدر صورت وجود خونریزی یا ورم غیرطبیعی، حتما یک عکس واضح از ناحیه عمل در همین چت ارسال کنید تا پزشک به صورت مستقیم وضعیت شما را بررسی کند.';
  } else if (reminderType === 'followup_day7') {
    header = '🩺 <b>پیگیری روز هفتم پس از عمل</b>\\n\\n' + name + ' عزیز، یک هفته از عمل شما گذشت.';
    body = '\\nوقت آن رسیده که روند نقاهت شما بررسی شود.\\nلطفا یک عکس واضح از ناحیه عمل بفرستید تا روند بهبودی توسط کلینیک تایید شود.\\nآیا متوجه علائم غیرطبیعی یا عفونت شده‌اید؟';
  }

  items.push({
    json: {
      Telegram_ID: p.Telegram_ID,
      Name: name,
      daysUntil,
      reminderType,
      customMessage: header + body
    }
  });
}
return items;
"""
        node["parameters"]["jsCode"] = new_js

# 2. Update switch node
switch_node_name = "Route by Reminder Type"
for node in data.get("nodes", []):
    if node["name"] == switch_node_name:
        node["parameters"]["rules"]["values"].append({
            "conditions": {
                "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 3},
                "conditions": [{"id": str(uuid.uuid4()), "leftValue": "={{$json.reminderType}}", "rightValue": "followup_day3", "operator": {"type": "string", "operation": "equals"}}],
                "combinator": "and"
            },
            "renameOutput": True,
            "outputKey": "Day 3"
        })
        node["parameters"]["rules"]["values"].append({
            "conditions": {
                "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 3},
                "conditions": [{"id": str(uuid.uuid4()), "leftValue": "={{$json.reminderType}}", "rightValue": "followup_day7", "operator": {"type": "string", "operation": "equals"}}],
                "combinator": "and"
            },
            "renameOutput": True,
            "outputKey": "Day 7"
        })

# 3. Add Telegram nodes for Followup
telegram_nodes = [
    {
      "parameters": {
        "chatId": "={{ $json.Telegram_ID }}",
        "text": "={{ $json.customMessage }}",
        "replyMarkup": "inlineKeyboard",
        "inlineKeyboard": {
          "rows": [
            {"row": {"buttons": [{"text": "درد خفیف (۱-۳)", "additionalFields": {"callback_data": "pain_low"}}, {"text": "درد متوسط (۴-۶)", "additionalFields": {"callback_data": "pain_mid"}}]}},
            {"row": {"buttons": [{"text": "درد شدید! (۷-۱۰)", "additionalFields": {"callback_data": "pain_high"}}]}}
          ]
        },
        "additionalFields": {"parse_mode": "HTML"}
      },
      "name": "SendFollowUp3",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1,
      "position": [800, -200],
      "id": str(uuid.uuid4()),
      "credentials": {"telegramApi": {"id": "vXlmVUHJDbuCCLw6", "name": "Telegram account 2"}}
    },
    {
      "parameters": {
        "chatId": "={{ $json.Telegram_ID }}",
        "text": "={{ $json.customMessage }}",
        "additionalFields": {"parse_mode": "HTML"}
      },
      "name": "SendFollowUp7",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1,
      "position": [1000, -200],
      "id": str(uuid.uuid4()),
      "credentials": {"telegramApi": {"id": "vXlmVUHJDbuCCLw6", "name": "Telegram account 2"}}
    },
    {
      "parameters": {
        "chatId": "191750790",
        "text": "=💬 پیامی از بیمار خارج از دستور ربات دریافت شد!\n\nآیدی: {{$json.message.from.id}}\nمتن:\n{{$json.message.text || 'بدون متن (شاید عکس ارسال شده)'}}",
        "additionalFields": {}
      },
      "name": "Forward To Admin",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1,
      "position": [112, 650],
      "id": str(uuid.uuid4()),
      "credentials": {"telegramApi": {"id": "vXlmVUHJDbuCCLw6", "name": "Telegram account 2"}}
    }
]
data["nodes"].extend(telegram_nodes)

# 4. Update connections
if "Route by Reminder Type" in data["connections"]:
    data["connections"]["Route by Reminder Type"]["main"][0].append({"node": "SendFollowUp3", "type": "main", "index": 0})
    data["connections"]["Route by Reminder Type"]["main"][0].append({"node": "SendFollowUp7", "type": "main", "index": 0})
    # Fix indices for switch node outputs since they are listed out sequentially
    conns = data["connections"]["Route by Reminder Type"]["main"]
    while len(conns) < 6:
        conns.append([])
    conns[4].append({"node": "SendFollowUp3", "type": "main", "index": 0})
    conns[5].append({"node": "SendFollowUp7", "type": "main", "index": 0})

# 5. Fix unmet logic from Telegram Trigger -> IF /start
if "IF /start" in data["connections"]:
    # The false branch of "/start" condition -> forward to admin
    while len(data["connections"]["IF /start"]["main"]) < 2:
        data["connections"]["IF /start"]["main"].append([])
    data["connections"]["IF /start"]["main"][1].append({"node": "Forward To Admin", "type": "main", "index": 0})

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Added Follow-up successfully!")
