# دليل البدء السريع

## الخطوات الأساسية لتشغيل البوت

### 1️⃣ رفع المشروع على GitHub

```bash
# افتح Terminal أو Command Prompt
cd telegram-bot

# إنشاء مستودع جديد على GitHub من الموقع
# ثم نفذ الأوامر التالية:

git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

**مهم:** استبدل `YOUR_USERNAME` و `YOUR_REPO_NAME` بمعلوماتك الخاصة.

---

### 2️⃣ النشر على Railway

1. افتح [railway.app](https://railway.app)
2. سجل دخول بحساب GitHub
3. اضغط **New Project**
4. اختر **Deploy from GitHub repo**
5. اختر المستودع الذي رفعته

---

### 3️⃣ إضافة المتغيرات البيئية

في صفحة المشروع على Railway، اذهب لـ **Variables** وأضف:

| المتغير | القيمة | كيف تحصل عليه |
|---------|--------|---------------|
| `BOT_TOKEN` | `123456:ABCdef...` | من [@BotFather](https://t.me/BotFather) |
| `GMAIL_USER` | `yourname@gmail.com` | بريدك الإلكتروني |
| `GMAIL_APP_PASSWORD` | `abcd efgh ijkl mnop` | من [Google App Passwords](https://myaccount.google.com/apppasswords) |
| `GMAIL_LABEL` | `TO_BOT` | اسم Label في Gmail |
| `GIFT_CHANNEL_ID` | `-1001234567890` | معرف قناة تيليجرام |
| `SUPPORT_WHATSAPP_URL` | `https://wa.me/966503560199` | رابط واتساب |
| `ADMIN_ID` | `331753565` | من [@userinfobot](https://t.me/userinfobot) |

---

### 4️⃣ اختبار البوت

1. افتح البوت في تيليجرام
2. اضغط `/start`
3. جرب الأزرار والأوامر

---

## الحصول على المتغيرات بسرعة

### 🤖 BOT_TOKEN

1. [@BotFather](https://t.me/BotFather) → `/newbot`
2. اتبع التعليمات
3. انسخ التوكن

### 📧 GMAIL_APP_PASSWORD

1. [Google Security](https://myaccount.google.com/security) → فعّل "2-Step Verification"
2. [App Passwords](https://myaccount.google.com/apppasswords)
3. اختر Mail → Other → أدخل اسم
4. انسخ كلمة المرور (16 حرف)

### 🏷️ GMAIL_LABEL

1. افتح Gmail
2. Create new label → `TO_BOT`
3. أنشئ Filter لتحويل الرسائل لهذا Label

### 📢 GIFT_CHANNEL_ID

1. أنشئ قناة في تيليجرام
2. أضف البوت كـ Admin
3. أرسل رسالة في القناة
4. افتح: `https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates`
5. ابحث عن `"chat":{"id":-100...`
6. انسخ الرقم الكامل

### 👤 ADMIN_ID

1. [@userinfobot](https://t.me/userinfobot) → `/start`
2. انسخ الرقم

---

## الأوامر المتاحة

| الأمر | الوصف | من يستخدمه |
|-------|--------|------------|
| `/start` | تشغيل البوت | الجميع |
| `/code` | جلب آخر كود | الجميع |
| `/gift` | عرض الهدية | الجميع |
| `/support` | التواصل مع الدعم | الجميع |
| `/users` | عدد المشتركين | الأدمن فقط |
| `/broadcast` | بث رسالة | الأدمن فقط |
| `/me` | معلومات المستخدم | الجميع |

---

## حل المشاكل الشائعة

### ❌ البوت لا يرد
- تحقق من `BOT_TOKEN`
- افتح Logs في Railway

### ❌ لا يجلب الأكواد
- تحقق من `GMAIL_USER` و `GMAIL_APP_PASSWORD`
- تأكد من وجود Label في Gmail
- تأكد من وجود رسائل في Label

### ❌ أوامر الأدمن لا تعمل
- استخدم `/me` للتحقق من `ADMIN_ID`

---

**للمزيد من التفاصيل:** اقرأ [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

© DDXSTORE
