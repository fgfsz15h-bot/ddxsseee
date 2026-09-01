# دليل النشر على Railway

هذا الدليل يشرح خطوات نشر البوت على Railway بالتفصيل.

## الخطوات

### 1. رفع المشروع على GitHub

أولاً، يجب رفع المشروع على GitHub:

```bash
# في مجلد المشروع
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

**ملاحظة:** استبدل `YOUR_USERNAME` و `YOUR_REPO_NAME` باسم المستخدم واسم المستودع الخاص بك.

### 2. إنشاء حساب على Railway

1. افتح [Railway.app](https://railway.app)
2. اضغط "Login" في الأعلى
3. سجل دخول باستخدام حساب GitHub الخاص بك
4. اسمح لـ Railway بالوصول لحسابك

### 3. إنشاء مشروع جديد

1. بعد تسجيل الدخول، اضغط "New Project"
2. اختر "Deploy from GitHub repo"
3. اختر المستودع الذي رفعت عليه البوت
4. سيبدأ Railway بقراءة المشروع تلقائياً

### 4. إضافة المتغيرات البيئية

هذه الخطوة **مهمة جداً**:

1. في صفحة المشروع، اضغط على تبويب "Variables"
2. أضف المتغيرات التالية واحدة تلو الأخرى:

```
BOT_TOKEN = التوكن من @BotFather
GMAIL_USER = بريدك الإلكتروني الكامل
GMAIL_APP_PASSWORD = كلمة مرور التطبيق (16 حرف)
GMAIL_LABEL = TO_BOT
GIFT_CHANNEL_ID = معرف القناة (مثل: -1001234567890)
SUPPORT_WHATSAPP_URL = https://wa.me/966503560199
ADMIN_ID = معرف المستخدم الخاص بك في تيليجرام
```

### 5. التحقق من النشر

1. بعد إضافة المتغيرات، اضغط "Deploy" إذا لم يبدأ تلقائياً
2. انتظر حتى يكتمل النشر (سترى "Success" باللون الأخضر)
3. اذهب لتبويب "Logs" لمشاهدة سجلات التشغيل
4. إذا كان كل شيء صحيح، سترى رسالة تفيد بأن البوت يعمل

### 6. اختبار البوت

1. افتح تيليجرام
2. ابحث عن البوت الخاص بك
3. اضغط `/start`
4. جرب الأوامر المختلفة

## الحصول على المتغيرات المطلوبة

### BOT_TOKEN

1. افتح [@BotFather](https://t.me/BotFather) في تيليجرام
2. أرسل `/newbot`
3. اتبع التعليمات لإنشاء بوت جديد
4. انسخ التوكن الذي سيعطيك إياه

### GMAIL_APP_PASSWORD

1. افتح [Google Account Security](https://myaccount.google.com/security)
2. فعّل "2-Step Verification" إذا لم يكن مفعلاً
3. ارجع لصفحة الأمان
4. ابحث عن "App passwords" واضغط عليها
5. اختر "Mail" و "Other device"
6. أدخل اسم (مثل: TelegramBot)
7. انسخ كلمة المرور المكونة من 16 حرف (بدون مسافات)

### GMAIL_LABEL

1. افتح [Gmail](https://mail.google.com)
2. من القائمة الجانبية، اضغط "Create new label"
3. أدخل اسم `TO_BOT` (أو أي اسم تريده)
4. أنشئ Filter لتحويل الرسائل المطلوبة لهذا Label تلقائياً:
   - اضغط على أيقونة البحث
   - اضغط "Create filter"
   - حدد الشروط (مثل: من مرسل معين)
   - اختر "Apply label" واختر `TO_BOT`
   - اضغط "Create filter"

### GIFT_CHANNEL_ID

1. أنشئ قناة في تيليجرام
2. أضف البوت كـ Admin في القناة
3. أرسل رسالة في القناة
4. افتح الرابط التالي في المتصفح (استبدل `BOT_TOKEN` بتوكن البوت):
   ```
   https://api.telegram.org/botBOT_TOKEN/getUpdates
   ```
5. ابحث عن `"chat":{"id":-100xxxxxxxxxx`
6. انسخ الرقم الكامل (يبدأ بـ `-100`)

### ADMIN_ID

1. افتح [@userinfobot](https://t.me/userinfobot) في تيليجرام
2. اضغط `/start`
3. سيعطيك معرفك (رقم مثل: 331753565)
4. انسخ هذا الرقم

## استكشاف الأخطاء

### البوت لا يرد

- تحقق من أن `BOT_TOKEN` صحيح
- تحقق من سجلات Railway (Logs)
- تأكد من أن المشروع في حالة "Running"

### لا يجلب الأكواد من Gmail

- تحقق من `GMAIL_USER` و `GMAIL_APP_PASSWORD`
- تأكد من أن Label موجود في Gmail
- تأكد من وجود رسائل في Label

### أوامر الأدمن لا تعمل

- تحقق من `ADMIN_ID` صحيح
- استخدم أمر `/me` للتحقق من المعرف

## إعادة النشر

إذا قمت بتعديل الكود:

```bash
git add .
git commit -m "وصف التعديل"
git push
```

سيتم إعادة النشر تلقائياً على Railway.

## إيقاف المشروع

إذا أردت إيقاف البوت مؤقتاً:
1. افتح المشروع في Railway
2. اضغط على Settings
3. اضغط "Pause Deployment"

---

© DDXSTORE
