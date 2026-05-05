// admin.js

// === آدرس وب‌هوک‌های n8n شما باید اینجا قرار گیرد ===
const N8N_WEBHOOK_BASE = 'https://mooshang.app.n8n.cloud/webhook'; 
// ====================================================

let allUsersData = {};
let isLoggedIn = false;

// Login Logic
function handleLogin(e) {
    e.preventDefault();
    const pass = document.getElementById('login-pass').value;
    
    const btn = document.getElementById('login-btn');
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    btn.disabled = true;

    // در اینجا فقط پسورد چک می‌شود
    // پسورد دیفالت: 1234
    setTimeout(() => {
        if (pass === 'Amoo@shayan') {
            document.getElementById('login-modal').classList.add('hidden');
            isLoggedIn = true;
            showSection('dashboard');
            showToast('با موفقیت وارد شدید', 'success');
        } else {
            showToast('رمز عبور اشتباه است', 'error');
            btn.innerHTML = 'ورود به سیستم';
            btn.disabled = false;
        }
    }, 800);
}

// Navigation UI Controller
function showSection(sectionId) {
    if (!isLoggedIn) return;

    // Hide all sections
    ['dashboard', 'users', 'add-user'].forEach(id => {
        document.getElementById(`section-${id}`).classList.remove('block');
        document.getElementById(`section-${id}`).classList.add('hidden');
        document.getElementById(`nav-${id}`).classList.remove('nav-active');
    });

    // Show selected section
    const targetSection = document.getElementById(`section-${sectionId}`);
    targetSection.classList.remove('hidden');
    targetSection.classList.add('block');
    document.getElementById(`nav-${sectionId}`).classList.add('nav-active');

    // Fetch new data if needed
    if (sectionId === 'dashboard') {
        fetchUsers(true); 
    } else if (sectionId === 'users') {
        fetchUsers();
    }
}

// Init
document.addEventListener('DOMContentLoaded', () => {
    // Show login by default
});

function refreshData() {
    showToast('در حال بروزرسانی اطلاعات...', 'info');
    fetchUsers(false);
}

// محاسبه آمار بر اساس اطلاعات موجود
function calculateDashboardStats(usersData) {
    const usersArray = Array.isArray(usersData) ? usersData : Object.values(usersData || {});
    const totalUsers = usersArray.length;
    const completedForms = usersArray.filter(u => u.first_name && u.phone).length;
    const diabetics = usersArray.filter(u => u.diabetes === 'yes' || u.diabetes === 'بلی').length;
    const smokers = usersArray.filter(u => u.smoker === 'yes' || u.smoker === 'بلی').length;

    document.getElementById('stat-total').innerText = totalUsers;
    document.getElementById('stat-completed').innerText = completedForms;
    document.getElementById('stat-diabetic').innerText = diabetics;
    document.getElementById('stat-smoker').innerText = smokers;
}

// Fetch Users List از n8n
async function fetchUsers(isRecentOnly = false) {
    try {
        const response = await fetch(`${N8N_WEBHOOK_BASE}/admin-get-users`);
        const json = await response.json();
        
        if (json.status === 'success') {
            allUsersData = json.data;
            calculateDashboardStats(json.data);
            populateTables(json.data, isRecentOnly);
        }
    } catch (e) {
        console.error("Failed fetching users", e);
        showToast('ارتباط با سرور برقرار نشد.', 'error');
    }
}

// Render data into tables
function populateTables(usersObj, isRecentOnly) {
    // Convert object to array for sorting
    let usersArray = Object.values(usersObj);
    usersArray.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));

    // Dashboard Recent Table
    if (isRecentOnly || document.getElementById('section-dashboard').classList.contains('block')) {
        const tbodyRecent = document.getElementById('recent-users-table');
        if (tbodyRecent) {
            tbodyRecent.innerHTML = '';
            const recent = usersArray.slice(0, 5); // Get last 5
            
            if (recent.length === 0) {
                tbodyRecent.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-gray-500">هیچ کاربری ثبت نشده است.</td></tr>';
            }

            recent.forEach(u => {
                const tr = document.createElement('tr');
                
                let highRiskAlert = '';
                if (parseInt(u.age) >= 65 || (u.surgeries && u.surgeries.toLowerCase() !== 'خیر' && u.surgeries !== 'no')) {
                    highRiskAlert = '<span class="text-red-500 ml-1"><i class="fas fa-exclamation-triangle"></i></span>';
                }

                tr.innerHTML = `
                    <td class="px-6 py-4">
                        <div class="flex items-center">
                            <div class="h-8 w-8 rounded bg-indigo-100 flex items-center justify-center text-indigo-600 ml-3">
                                ${u.first_name ? u.first_name.charAt(0) : '<i class="fas fa-user"></i>'}
                            </div>
                            <div>
                                <div class="font-medium text-gray-800">${highRiskAlert}${u.first_name || 'تلگرام'} ${u.last_name || 'کاربر'}</div>
                                <div class="text-xs text-gray-400">ID: ${u.user_id ? String(u.user_id).substring(0,6) : '-'}</div>
                            </div>
                        </div>
                    </td>
                    <td class="px-6 py-4 font-medium text-gray-700">${u.phone || '<span class="text-red-400 text-xs">ثبت نشده</span>'}</td>
                    <td class="px-6 py-4 text-gray-500 text-xs">${u.is_manual ? 'منشی' : 'ربات تلگرام'}</td>
                    <td class="px-6 py-4">
                        ${getHealthBadges(u.smoker, u.diabetes)}
                    </td>
                `;
                tbodyRecent.appendChild(tr);
            });
        }
    }

    // All Users Table (Only update if needed or not limited to recent)
    if (!isRecentOnly) {
        const tbodyAll = document.getElementById('all-users-table');
        if (tbodyAll) {
            tbodyAll.innerHTML = '';

            if (usersArray.length === 0) {
                tbodyAll.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-gray-500">بانک اطلاعاتی خالی است.</td></tr>';
                return;
            }

            usersArray.forEach(u => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-gray-50 transition cursor-pointer user-row";
                tr.dataset.name = `${u.first_name || ''} ${u.last_name || ''}`.toLowerCase();
                tr.dataset.phone = u.phone || '';
                
                let date = u.created_at ? new Date(u.created_at) : new Date();
                let dateStr = isNaN(date.getTime()) ? '-' : date.toLocaleDateString('fa-IR');
                
                let highRiskAlert = '';
                if (parseInt(u.age) >= 65 || (u.surgeries && u.surgeries.toLowerCase() !== 'خیر' && u.surgeries !== 'no')) {
                    highRiskAlert = '<span class="text-red-500 ml-1" title="نیاز به تایید پزشک (سن بالا یا سابقه بیماری)"><i class="fas fa-exclamation-triangle"></i></span>';
                }

                tr.innerHTML = `
                    <td class="px-6 py-4 text-xs font-mono text-indigo-600">${u.user_id || '-'}</td>
                    <td class="px-6 py-4 font-medium text-gray-800">${highRiskAlert}${u.first_name || ''} ${u.last_name || 'بدون نام'} <span class="text-xs text-gray-400">(${u.age ? u.age + ' سال' : '?'})</span></td>
                    <td class="px-6 py-4 font-medium text-gray-600">${u.phone || '-'}</td>
                    <td class="px-6 py-4 text-xs">${getHealthBadges(u.smoker, u.diabetes)}</td>
                    <td class="px-6 py-4 text-gray-500 text-xs">${dateStr}</td>
                    <td class="px-6 py-4 flex gap-2">
                        <button onclick="openUserModal('${u.user_id}')" class="text-indigo-500 hover:text-indigo-700 text-sm p-1 focus:outline-none ml-2" title="مشاهده و ویرایش">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button onclick="deleteUser('${u.user_id}')" class="text-red-500 hover:text-red-700 text-sm p-1 focus:outline-none" title="حذف بیمار">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </td>
                `;
                tbodyAll.appendChild(tr);
            });
        }
    }
}

function getHealthBadges(smoker, diabetes) {
    let badges = '';
    
    // Normalize both 'yes' (API) and 'بلی' (Persian manual)
    const IS_YES = (v) => v === 'yes' || v === 'بلی';
    const IS_NO = (v) => v === 'no' || v === 'خیر';

    if (IS_YES(smoker)) {
        badges += `<span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800 ml-1 mb-1">سیگاری</span>`;
    } else if (IS_NO(smoker)) {
        badges += `<span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800 ml-1 mb-1">غیرسیگاری</span>`;
    }
    
    if (IS_YES(diabetes)) {
        badges += `<span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800 ml-1 mb-1">دیابت</span>`;
    } else if (IS_NO(diabetes)) {
        badges += `<span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800 ml-1 mb-1">بدون دیابت</span>`;
    }
    
    if (!badges) return '<span class="text-gray-300">در انتظار آپدیت</span>';
    return badges;
}

// Add Manual User
async function submitNewUser(e) {
    e.preventDefault();
    
    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin ml-2"></i> در حال ذخیره...';
    submitBtn.disabled = true;

    const reqData = {
        firstName: document.getElementById('add-fname').value,
        lastName: document.getElementById('add-lname').value,
        age: parseInt(document.getElementById('add-age').value) || 0,
        phone: document.getElementById('add-phone').value,
        smoker: document.getElementById('add-smoker').value,
        diabetes: document.getElementById('add-diabetes').value,
        allergies: document.getElementById('add-allergies').value,
        surgeries: document.getElementById('add-surgeries').value,
        user_id: "MANUAL_" + Date.now() // Generating a manual ID for n8n to process
    };

    try {
        const response = await fetch(`${N8N_WEBHOOK_BASE}/clinic-form-submit`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(reqData)
        });
        const res = await response.json();
        
        if (res.status === 'success') {
            document.getElementById('admin-add-form').reset();
            showToast('بیمار جدید با موفقیت در سیستم ثبت شد.');
            showSection('users');
            fetchUsers(); // refresh data
        } else {
            showToast('خطا در ثبت کاربر: ' + res.message, 'error');
        }
    } catch (err) {
        showToast('خطای شبکه در ثبت کاربر.', 'error');
    } finally {
        submitBtn.innerHTML = '<i class="fas fa-save ml-2"></i> ذخیره اطلاعات';
        submitBtn.disabled = false;
    }
}

// Delete User
async function deleteUser(userId) {
    if(!confirm('آیا از حذف این بیمار اطمینان دارید؟ اطلاعات قابل بازگشت نیست.')) return;
    
    try {
        const response = await fetch(`${API_URL}/api/admin/users/${userId}`, {
            method: 'DELETE'
        });
        const res = await response.json();
        
        if (res.status === 'success') {
            showToast('بیمار حذف شد.', 'success');
            fetchUsers();
        } else {
            showToast('خطا در حذف کاربر.', 'error');
        }
    } catch (err) {
        showToast('خطای شبکه.', 'error');
    }
}

// Toast
function showToast(msg, type='success') {
    const t = document.getElementById('toast');
    document.getElementById('toast-msg').innerText = msg;
    
    t.className = `fixed bottom-4 right-4 transform translate-y-0 opacity-100 px-6 py-3 rounded-lg shadow-lg flex items-center transition-all duration-300 z-50 flex-row-reverse text-white`;
    
    if (type === 'error') {
        t.classList.add('bg-red-500');
    } else if (type === 'info') {
        t.classList.add('bg-blue-500');
    } else {
        t.classList.add('bg-green-500');
    }
    
    setTimeout(() => {
        t.classList.replace('translate-y-0', 'translate-y-20');
        t.classList.replace('opacity-100', 'opacity-0');
    }, 4000);
}

// Search / Filter
function filterTable() {
    let input = document.getElementById('search-input').value.toLowerCase();
    let rows = document.querySelectorAll('.user-row');
    
    rows.forEach(row => {
        let name = row.dataset.name;
        let phone = row.dataset.phone;
        if (name.includes(input) || phone.includes(input)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

// ---- Modal / Popup Logic ---- //
function openUserModal(userId) {
    const userArray = Object.values(allUsersData);
    const user = userArray.find(u => String(u.user_id) === String(userId));
    if (!user) return;

    // Populate Data
    document.getElementById('modal-user-id').value = user.user_id;
    document.getElementById('modal-user-name').innerText = `${user.first_name || ''} ${user.last_name || 'بدون نام'}`;
    
    const phoneElement = document.getElementById('modal-user-phone');
    if (user.phone) {
        phoneElement.innerText = user.phone;
        phoneElement.classList.replace('text-red-400', 'text-gray-800');
        document.getElementById('modal-call-btn').href = `tel:${user.phone}`;
        document.getElementById('modal-call-btn').classList.remove('hidden');
    } else {
        phoneElement.innerText = 'ثبت نشده';
        phoneElement.classList.replace('text-gray-800', 'text-red-400');
        document.getElementById('modal-call-btn').classList.add('hidden');
    }

    document.getElementById('modal-user-smoker').innerText = user.smoker === 'yes' ? 'سیگاری (بله)' : 'غیرسیگاری (خیر)';
    document.getElementById('modal-user-diabetes').innerText = user.diabetes === 'yes' ? 'دارد (بله)' : 'ندارد (خیر)';
    document.getElementById('modal-user-age').innerText = user.age ? user.age : 'نامشخص';
    document.getElementById('modal-user-allergies').innerText = user.allergies ? user.allergies : 'نامشخص';
    document.getElementById('modal-user-surgeries').innerText = user.surgeries ? user.surgeries : 'نامشخص';
    
    document.getElementById('modal-appointment').value = user.appointment || '';
    document.getElementById('modal-notes').value = user.notes || '';

    // Show modal
    document.getElementById('user-modal').classList.remove('hidden');
    
    // Initialize Datepicker AFTER modal is visible so it can calculate offsets
    setTimeout(() => {
        if(typeof $ !== 'undefined') {
            $('#modal-appointment').persianDatepicker({
                format: 'YYYY/MM/DD ساعت HH:mm',
                timePicker: {
                    enabled: true,
                    meridiem: { enabled: true }
                },
                toolbox: { calendarSwitch: { enabled: false } },
                initialValue: false, // Prevents overwriting what we just set via vanilla JS
                autoClose: true
            });
            // Re-apply the value in case datepicker wiped it
            document.getElementById('modal-appointment').value = user.appointment || '';
        }
    }, 100);
}

function closeModal() {
    document.getElementById('user-modal').classList.add('hidden');
}

async function saveUserDetails(e) {
    e.preventDefault();
    const btn = document.getElementById('modal-save-btn');
    btn.innerHTML = '<i class="fas fa-spinner fa-spin ml-2"></i> در حال ذخیره...';
    btn.disabled = true;

    const userId = document.getElementById('modal-user-id').value;
    const appointment = document.getElementById('modal-appointment').value;
    const notes = document.getElementById('modal-notes').value;

    try {
        // Send to Webhook
        const response = await fetch(`${N8N_WEBHOOK_BASE}/admin-update-user`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: Number(userId),
                appointment: appointment,
                notes: notes
            })
        });
        
        let res = {};
        try { res = await response.json(); } catch(e) {}
        
        if (response.ok || res.status === 'success') {
            showToast('اطلاعات با موفقیت بروزرسانی شد.');
            closeModal();
            fetchUsers(true); // reload dashboard exactly
        } else {
            showToast('خطا در بروزرسانی اطلاعات', 'error');
        }
    } catch (error) {
        showToast('خطای ارتباط با سرور', 'error');
        console.error(error);
    } finally {
        btn.innerHTML = '<i class="fas fa-check ml-2"></i> ذخیره تغییرات';
        btn.disabled = false;
    }
}
