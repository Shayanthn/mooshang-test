// Initialize Telegram Web App
const tg = window.Telegram?.WebApp;
let currentUserId = null;

// API Configuration - Updated directly to n8n Webhook
const API_BASE_URL = 'https://mooshang.app.n8n.cloud/webhook/clinic-form-submit';

// Setup Telegram Web App
if (tg) {
    tg.ready();
    tg.expand();
    tg.setHeaderColor('#667eea');
    
    console.log('✅ Telegram Web App Initialized');
    console.log('📊 User Info:', {
        id: tg.initData,
        is_bot: tg.isBot || false,
        is_expansion_allowed: tg.isExpanded
    });
}

// ========================================
// 🧪 TEST MODE FUNCTIONS
// ========================================

async function startTestMode() {
    const testUserId = document.getElementById('test-user-id').value;
    console.log('🧪 Starting test mode with user:', testUserId);
    
    // داده‌های تست
    const testData = {
        user_id: testUserId,
        firstName: 'محمد',
        lastName: 'رضایی',
        phone: '09151234567',
        smoker: 'no',
        diabetes: 'no'
    };
    
    console.log('📤 Sending test data...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/form/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(testData)
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            console.log('✅ Test data saved successfully!');
            console.log('📊 Response:', result);
            
            // فرم را پر کنید
            document.getElementById('first-name').value = testData.firstName;
            document.getElementById('last-name').value = testData.lastName;
            document.getElementById('phone').value = testData.phone;
            document.getElementById('smoker').value = testData.smoker;
            document.getElementById('diabetes').value = testData.diabetes;
            document.getElementById('chat-id').value = testUserId;
            
            // فعال کردن دکمه
            document.querySelector('.submit-btn').disabled = false;
            document.querySelector('.submit-btn').title = 'برای ثبت اطلاعات کلیک کنید';
            document.querySelector('.submit-info').textContent = '✅ تست محلی شروع شد! اطلاعات ذخیره شد.';
            document.querySelector('.submit-info').style.background = '#d1fae5';
            document.querySelector('.submit-info').style.borderColor = '#10b981';
            document.querySelector('.submit-info').style.color = '#065f46';
            
            alert('✅ تست موفق!\n\nاطلاعات ذخیره شد!\n\nشناسه: ' + testUserId);
        } else {
            console.error('❌ Error:', result);
            alert('❌ خطا: ' + result.message);
        }
    } catch (error) {
        console.error('❌ Connection error:', error);
        alert('❌ خطا در اتصال: ' + error.message);
    }
}

async function resetTestData() {
    if (confirm('آیا مطمئن هستید؟ تمام داده‌های تست حذف خواهند شد.')) {
        console.log('🔄 Resetting test data...');
        
        // فرم را خالی کنید
        document.getElementById('clinic-form').reset();
        document.getElementById('chat-id').value = '';
        
        // دکمه را غیرفعال کنید
        document.querySelector('.submit-btn').disabled = true;
        document.querySelector('.submit-info').textContent = '⚠️ برای شروع تست، دکمه "🚀 شروع تست محلی" را فشار دهید.';
        document.querySelector('.submit-info').style.background = '#fef3c7';
        document.querySelector('.submit-info').style.borderColor = '#f59e0b';
        document.querySelector('.submit-info').style.color = '#92400e';
        
        console.log('✅ Test data reset!');
        alert('✅ داده‌های تست حذف شد.');
    }
}

// Get parameters from URL or Telegram
function getUserIdFromParams() {
    // بررسی URL parameters
    const params = new URLSearchParams(window.location.search);
    const urlUserId = params.get('user_id');
    
    if (urlUserId) {
        return urlUserId;
    }
    
    // بررسی Local Storage (از قبل ذخیره شده)
    return localStorage.getItem('clinic_user_id');
}

// Get chat ID from Telegram
function getChatIdFromTelegram() {
    if (tg && tg.initDataUnsafe?.user?.id) {
        return tg.initDataUnsafe.user.id;
    }
    return null;
}

// Initialize on page load
window.addEventListener('load', async () => {
    // دریافت شناسه کاربر
    currentUserId = getUserIdFromParams();
    
    if (currentUserId) {
        console.log('📌 User ID:', currentUserId);
        localStorage.setItem('clinic_user_id', currentUserId);
        
        // نمایش شناسه در صفحه
        const chatIdInput = document.getElementById('chat-id');
        if (chatIdInput) {
            chatIdInput.value = currentUserId;
            chatIdInput.disabled = true;
        }
        
        // تایید کاربر
        await validateUser(currentUserId);
    } else {
        showErrorMessage('❌ شناسه کاربری یافت نشد. لطفاً از تلگرام دسترسی حاصل کنید.');
        console.error('User ID not found');
    }
});

// تایید کاربر (بدون نیاز به سرور در حالت n8n، مستقیم تایید می‌شود)
async function validateUser(userId) {
    console.log('✅ User validated locally for n8n:', userId);
    document.querySelector('.submit-btn').disabled = false;
    document.querySelector('.submit-btn').title = 'برای ثبت اطلاعات کلیک کنید';
    document.querySelector('.submit-info').textContent = '✅ شناسه کاربر تایید شد. می‌توانید اطلاعات خود را ثبت کنید.';
    document.querySelector('.submit-info').style.background = '#d1fae5';
    document.querySelector('.submit-info').style.borderColor = '#10b981';
    document.querySelector('.submit-info').style.color = '#065f46';
}

// ارسال داده‌های فرم به n8n Webhook
async function submitFormToServer(formData) {
    try {
        const response = await fetch(API_BASE_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUserId || 'web-user',
                ...formData
            })
        });
        
        // n8n returns standard JSON based on our Respond to Webhook node
        const data = await response.json();
        
        if (data.status === 'success' || response.ok) {
            console.log('✅ Data submitted to n8n:', data);
            return true;
        } else {
            showErrorMessage(`❌ خطا در ثبت اطلاعات`);
            return false;
        }
    } catch (error) {
        console.error('Submission error:', error);
        showErrorMessage('❌ خطا در اتصال به سرور (n8n).');
        return false;
    }
}

// Form submission handler
document.getElementById('clinic-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Check if button is disabled
    const submitBtn = document.querySelector('.submit-btn');
    if (submitBtn.disabled) {
        showErrorMessage('⚠️ شناسه کاربری معتبر نیست. لطفاً از تلگرام دسترسی حاصل کنید.');
        return;
    }

    // Validate form
    if (!validateForm()) {
        showErrorMessage('❌ لطفاً تمام فیلدهای ضروری را پر کنید');
        return;
    }

    // Collect form data
    const formData = {
        firstName: document.getElementById('first-name').value.trim(),
        lastName: document.getElementById('last-name').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        smoker: document.getElementById('smoker').value,
        diabetes: document.getElementById('diabetes').value,
        timestamp: new Date().toISOString(),
        source: 'telegram_web_app'
    };

    // ارسال داده‌ها به سرور
    const success = await submitFormToServer(formData);
    
    if (success) {
        // Show success message
        showSuccessMessage();

        // 1. تغییر دکمه در رابط کاربری
        document.querySelector('.submit-btn').style.display = 'none';
        const backBtn = document.getElementById('back-btn');
        backBtn.style.display = 'flex';
        document.querySelector('.submit-info').textContent = '✅ اطلاعات شما با موفقیت ثبت شد!';

        // 2. ارسال پیام موفقیت‌آمیز به ربات و بستن مینی‌اپ
        if (tg) {
            // ساخت یک پیام از خلاصه اطلاعات برای ربات
            const successSummary = {
                action: "form_submitted",
                firstName: formData.firstName,
                lastName: formData.lastName,
                phone: formData.phone
            };
            
            setTimeout(() => {
                tg.sendData(JSON.stringify(successSummary));
            }, 1000);
        }
        
        console.log('✅ Data submitted:', formData);
    }
});

// مدیریت دکمه بازگشت دستی
document.getElementById('back-btn').addEventListener('click', function() {
    if (tg) {
        tg.close();
    }
});

// دکمه بازگشت
document.addEventListener('DOMContentLoaded', function() {
    const backBtn = document.getElementById('back-btn');
    if (backBtn) {
        backBtn.addEventListener('click', function() {
            // بازگشت به ربات
            if (tg && tg.close) {
                tg.close();
            } else {
                // اگر تلگرام نیست، پیام نشان دهید
                alert('✅ اطلاعات شما دریافت شد!\n\nبه ربات بازگردید.');
                location.href = 'index.html';
            }
        });
    }
});

// Form validation
function validateForm() {
    const firstName = document.getElementById('first-name').value.trim();
    const lastName = document.getElementById('last-name').value.trim();
    const phone = document.getElementById('phone').value.trim();

    if (!firstName || !lastName || !phone) {
        return false;
    }

    // Validate phone number
    if (!/^[\d\s\-\+()]{10,}$/.test(phone)) {
        showErrorMessage('❌ شماره تماس معتبر نیست');
        return false;
    }

    return true;
}

// Save data to file
function saveDataToFile(data) {
    const jsonData = JSON.stringify(data, null, 2);
    console.log('💾 Data saved locally:', jsonData);

    // TODO: Send to server when available
    // fetch('/api/save-patient', { 
    //     method: 'POST', 
    //     headers: { 'Content-Type': 'application/json' },
    //     body: jsonData 
    // });
}

// Send data to Telegram bot
function sendDataToBot(data) {
    if (tg?.sendData) {
        try {
            tg.sendData(JSON.stringify(data));
            console.log('📤 Data sent to Telegram bot');
        } catch (error) {
            console.error('Error sending data to bot:', error);
        }
    }
}

// Show success message
function showSuccessMessage() {
    const successMessage = document.getElementById('success-message');
    successMessage.classList.add('show');

    // Vibrate if supported
    if (navigator.vibrate) {
        navigator.vibrate([100, 50, 100]);
    }

    // Show Telegram Alert if available
    if (tg?.showAlert) {
        tg.showAlert('✅ اطلاعات شما با موفقیت ثبت شد!');
    }

    // Auto-hide after 4 seconds
    setTimeout(() => {
        successMessage.classList.remove('show');
    }, 4000);
}

// Show error message
function showErrorMessage(message) {
    console.warn('❌ Error:', message);
    
    // Show Telegram Alert if available
    if (tg?.showAlert) {
        tg.showAlert(message);
    } else {
        alert(message);
    }
}

// Add input focus effects
document.querySelectorAll('input, select').forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });

    input.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
    });

    // Add real-time validation for phone
    if (input.type === 'tel') {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^\d\-\+() ]/g, '');
        });
    }
});

// Add smooth scrolling for form sections
document.querySelectorAll('.section-title').forEach(title => {
    title.addEventListener('click', function() {
        const section = this.closest('.form-section');
        if (section) {
            section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Handle main button (if in Telegram)
if (tg?.MainButton) {
    tg.MainButton.text = 'ارسال اطلاعات';
    tg.MainButton.show();
    tg.MainButton.onClick(() => {
        document.getElementById('clinic-form').dispatchEvent(new Event('submit'));
    });
}

// Log when page loads
console.log('✅ Form ready for input');
console.log('🔗 Telegram Web App:', !!tg);
