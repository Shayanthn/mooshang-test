
import json

try:
    with open('admin.js', 'r', encoding='utf-8') as f: content = f.read()
    content = content.replace('http://localhost:5678/webhook/admin-get-users', 'https://mooshang.app.n8n.cloud/webhook/admin-get-users')
    content = content.replace('http://localhost:5678/webhook/admin-update-user', 'https://mooshang.app.n8n.cloud/webhook/admin-update-user')
    with open('admin.js', 'w', encoding='utf-8') as f: f.write(content)
except Exception as e:
    print('admin.js error:', e)

try:
    with open('script.js', 'r', encoding='utf-8') as f: content = f.read()
    content = content.replace('http://localhost:5678/webhook/clinic-form-submit', 'https://mooshang.app.n8n.cloud/webhook/clinic-form-submit')
    with open('script.js', 'w', encoding='utf-8') as f: f.write(content)
except Exception as e:
    print('script.js error:', e)

try:
    with open('n8n_project/n8n_workflow.json', 'r', encoding='utf-8') as f: content = f.read()
    content = content.replace('https://shayanthn.github.io/clinic_assistance/index.html', 'https://shayanthn.github.io/mooshang-test/index.html')
    with open('n8n_project/n8n_workflow.json', 'w', encoding='utf-8') as f: f.write(content)
except Exception as e:
    print('n8n_project json error:', e)

try:
    with open('n8n_workflow.json', 'r', encoding='utf-8') as f: content = f.read()
    content = content.replace('https://shayanthn.github.io/clinic_assistance/index.html', 'https://shayanthn.github.io/mooshang-test/index.html')
    with open('n8n_workflow.json', 'w', encoding='utf-8') as f: f.write(content)
except Exception as e:
    pass

print('Done')

