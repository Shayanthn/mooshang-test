import codecs

with open(r"c:\Users\Cyber System\Desktop\clinic aotumation\admin.js", "r", encoding="utf-8") as f:
    text = f.read()

# Add the new elements into `openUserModal`
new_js = """    document.getElementById('modal-user-surgeries').innerText = user.surgeries || 'نامشخص';

    // New Fields
    document.getElementById('modal-user-national-id').innerText = user.national_id || 'ثبت نشده';
    document.getElementById('modal-user-address').innerText = user.address || 'ثبت نشده';
    document.getElementById('modal-user-alcohol').innerText = user.alcohol === 'yes' ? 'بله' : 'خیر';
    document.getElementById('modal-user-drugs').innerText = user.drugs === 'yes' ? 'بله' : 'خیر';
    document.getElementById('modal-user-medications').innerText = user.medications || 'بدون مصرف دارو';
"""

text = text.replace(
    "    document.getElementById('modal-user-surgeries').innerText = user.surgeries ? user.surgeries : 'نامشخص';",
    new_js
)

with open(r"c:\Users\Cyber System\Desktop\clinic aotumation\admin.js", "w", encoding="utf-8") as f:
    f.write(text)

print("admin.js UI updated")
