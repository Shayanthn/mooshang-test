import json

file_path = "c:/Users/Cyber System/Desktop/clinic aotumation/n8n_project/n8n_workflow.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for node in data.get("nodes", []):
    if node["name"] == "CRM: General Instructions":
        node["parameters"]["text"] = "👤 نام بیمار: {{$node[\"Webhook (Update User)\"].json[\"body\"][\"firstName\"]}}\n📅 وقت تعیین شده برای شما: {{$node[\"Webhook (Update User)\"].json[\"body\"][\"appointment\"]}}\n\n🔔 دستورالعمل‌های عمومی قبل از عمل:\n- حتما آزمایشات قبل از عمل را انجام دهید.\n- هزینه عمل طبق تعرفه با شما هماهنگ خواهد شد.\n\nآزمایشات لازم:\nCBC, HBS Ag, HCV, HIV, Pt, Ptt, INR, FBS\n(لطفا جواب آزمایشات را روز عمل همراه داشته باشید)."
    
    elif node["name"] == "IF: High Risk (Age/Surgery)":
        if "conditions" in node["parameters"] and "conditions" in node["parameters"]["conditions"]:
            for cond in node["parameters"]["conditions"]["conditions"]:
                if cond["id"] == "c2":
                    cond["rightValue"] = "ندارد"
    
    elif node["name"] == "CRM: High Risk Warning":
        node["parameters"]["text"] = "⚠️ هشدار ریسک بالا:\nبا توجه به سن یا سوابق جراحی، لطفا قبل از عمل علاوه بر آزمایشات روتین، تاییدیه پزشک متخصص قلب و عروق (اکو و نوار قلب) را نیز دریافت کنید."
    
    elif node["name"] == "IF: Allergies":
        if "conditions" in node["parameters"] and "conditions" in node["parameters"]["conditions"]:
            for cond in node["parameters"]["conditions"]["conditions"]:
                if cond["id"] == "c3":
                    cond["rightValue"] = "ندارد"
                
    elif node["name"] == "CRM: Allergies Alert":
        node["parameters"]["text"] = "⚠️ هشدار حساسیت دارویی:\nشما در فرم ثبت‌نام به حساسیت دارویی/غذایی اشاره کرده‌اید. لطفا روز عمل، پزشک و پرستار کلینیک را مستقیماً در جریان نوع حساسیت خود قرار دهید."
        
    elif node["name"] == "Compute Days & Build Messages":
        node["parameters"]["jsCode"] = """const now = new Date();
const todayStr = now.toISOString().split('T')[0];
const startOfToday = new Date(todayStr + "T00:00:00.000Z");

const items = [];
for (const item of $input.all()) {
  const appointmentStr = item.json.Appointment;
  if (!appointmentStr) continue;

  const appointDate = new Date(appointmentStr + "T00:00:00.000Z");
  if (isNaN(appointDate.getTime())) continue;

  const diffTime = appointDate.getTime() - startOfToday.getTime();
  const daysUntil = Math.round(diffTime / (1000 * 60 * 60 * 24));

  let reminderType = null;
  if (daysUntil === 20) reminderType = 'reminder_20days';
  else if (daysUntil === 2) reminderType = 'reminder_2days';
  else if (daysUntil === 1) reminderType = 'reminder_night_before';
  else if (daysUntil === 0) reminderType = 'reminder_surgery_day';
  else continue;

  const p = item.json;
  const name = p.Name || '';
  const age = parseInt(p.Age) || null;

  const smoker = (p.Smoker || '').toString().toLowerCase() === 'yes' || p.Smoker === 'دارد' || p.Smoker === 'بله';
  const diabetes = (p.Diabetes || '').toString().toLowerCase() === 'yes' || p.Diabetes === 'دارد' || p.Diabetes === 'بله';
  const allergies = p.Allergies || '';
  const surgeries = p.Surgeries || '';

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
    body = '\\n- لطفا با یک همراه (راننده) مراجعه کنید.\\n- هیچ‌گونه زیورآلات همراه نداشته باشید.\\n- در زمان تعیین شده در کلینیک حضور یابید.' + extraWarnings;
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

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("JSON successfully fixed!")
