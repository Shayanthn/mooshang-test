import re

with open(r"c:\Users\Cyber System\Desktop\clinic aotumation\admin.html", 'r', encoding='utf-8') as f:
    text = f.read()

# Add national ID under age
text = text.replace(
    '<p class="font-bold text-red-600 text-lg" id="modal-user-age">...</p>',
    '<p class="font-bold text-red-600 text-lg" id="modal-user-age">...</p>\n                        <p class="font-bold text-gray-600 text-sm mt-1">کد ملی: <span id="modal-user-national-id" class="font-mono">...</span></p>'
)

# Add address inside the info grid
allergies_section = """                            <div class="bg-gray-50 rounded p-3">
                                <span class="text-xs text-gray-500 block mb-1">حساسیت‌ها</span>
                                <span id="modal-user-allergies" class="text-sm font-medium text-red-600">پاسخ</span>
                            </div>"""

new_sections = """                            <div class="bg-gray-50 rounded p-3">
                                <span class="text-xs text-gray-500 block mb-1">حساسیت‌ها</span>
                                <span id="modal-user-allergies" class="text-sm font-medium text-red-600">پاسخ</span>
                            </div>
                            <div class="bg-gray-50 rounded p-3">
                                <span class="text-xs text-gray-500 block mb-1">الکل</span>
                                <span id="modal-user-alcohol" class="text-sm font-medium">پاسخ</span>
                            </div>
                            <div class="bg-gray-50 rounded p-3">
                                <span class="text-xs text-gray-500 block mb-1">مواد مخدر</span>
                                <span id="modal-user-drugs" class="text-sm font-medium">پاسخ</span>
                            </div>
                            <div class="bg-gray-50 rounded p-3 col-span-2">
                                <span class="text-xs text-gray-500 block mb-1">داروهای مصرفی</span>
                                <span id="modal-user-medications" class="text-sm font-medium text-blue-600">پاسخ</span>
                            </div>
                            <div class="bg-gray-50 rounded p-3 col-span-2">
                                <span class="text-xs text-gray-500 block mb-1">آدرس</span>
                                <span id="modal-user-address" class="text-sm font-medium">پاسخ</span>
                            </div>"""

text = text.replace(allergies_section, new_sections)

with open(r"c:\Users\Cyber System\Desktop\clinic aotumation\admin.html", 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated admin.html")
