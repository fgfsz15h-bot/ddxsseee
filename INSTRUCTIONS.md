# تعليمات نقل البوت من Replit إلى GitHub و Railway

## ✅ تم إعداد المشروع بالكامل!

جميع الملفات جاهزة للرفع على GitHub والنشر على Railway.

---

## 📁 الملفات المُعدة

| الملف | الوصف |
|-------|--------|
| `main.py` | الكود الأساسي للبوت |
| `requirements.txt` | المكتبات المطلوبة |
| `Procfile` | ملف تشغيل Railway |
| `runtime.txt` | إصدار Python |
| `.env.example` | مثال للمتغيرات البيئية |
| `.gitignore` | ملفات يتم تجاهلها في Git |
| `README.md` | وصف المشروع |
| `QUICKSTART.md` | دليل البدء السريع |
| `RAILWAY_DEPLOYMENT.md` | دليل النشر المفصل |

---

## 🚀 الخطوات التالية

### الخطوة 1: رفع المشروع على GitHub

#### أ) إنشاء مستودع جديد على GitHub

1. افتح [github.com](https://github.com)
2. اضغط على **+** في الأعلى ← **New repository**
3. أدخل اسم المستودع (مثل: `telegram-bot`)
4. اختر **Private** إذا أردت أن يكون خاص
5. **لا تضف** README أو .gitignore أو License (موجودين بالفعل)
6. اضغط **Create repository**

#### ب) رفع الملفات

بعد إنشاء المستودع، ستظهر لك تعليمات. استخدم هذه الأوامر:

```bash
cd telegram-bot
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

**مهم:** استبدل `YOUR_USERNAME` باسم المستخدم الخاص بك و `YOUR_REPO_NAME` باسم المستودع.

**إذا طلب منك تسجيل الدخول:**
- Username: اسم المستخدم في GitHub
- Password: استخدم **Personal Access Token** وليس كلمة المرور العادية
  - أنشئ Token من: Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
  - اختر scope: `repo`

---

### الخطوة 2: النشر على Railway

#### أ) إنشاء حساب

1. افتح [railway.app](https://railway.app)
2. اضغط **Login**
3. اختر **Login with GitHub**
4. اسمح لـ Railway بالوصول

#### ب) إنشاء مشروع جديد

1. اضغط **New Project**
2. اختر **Deploy from GitHub repo**
3. اختر المستودع الذي رفعته للتو
4. انتظر حتى يتم قراءة المشروع

#### ج) إضافة المتغيرات البيئية

**هذه الخطوة الأهم!** بدون المتغيرات البيئية، البوت لن يعمل.

1. في صفحة المشروع، اضغط على تبويب **Variables**
2. أضف المتغيرات التالية واحدة تلو الأخرى:

```
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_password
GMAIL_LABEL=TO_BOT
GIFT_CHANNEL_ID=-1001234567890
SUPPORT_WHATSAPP_URL=https://wa.me/966503560199
ADMIN_ID=331753565
```

**استبدل القيم بقيمك الخاصة!**

---

## 🔑 كيف تحصل على المتغيرات

### 1. BOT_TOKEN

1. افتح [@BotFather](https://t.me/BotFather) في تيليجرام
2. أرسل `/newbot`
3. أدخل اسم البوت (مثل: DDXSTORE Bot)
4. أدخل username للبوت (يجب أن ينتهي بـ `bot` مثل: `ddxstore_bot`)
5. انسخ التوكن الذي سيظهر (شكله: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. GMAIL_USER

بريدك الإلكتروني الكامل (مثل: `yourname@gmail.com`)

### 3. GMAIL_APP_PASSWORD

**مهم:** ليست كلمة مرور Gmail العادية!

1. افتح [myaccount.google.com/security](https://myaccount.google.com/security)
2. فعّل **2-Step Verification** إذا لم يكن مفعلاً
3. ارجع لصفحة الأمان
4. ابحث عن **App passwords** (كلمات مرور التطبيقات)
5. اختر:
   - App: **Mail**
   - Device: **Other** (أدخل: Telegram Bot)
6. اضغط **Generate**
7. انسخ كلمة المرور المكونة من 16 حرف (مثل: `abcd efgh ijkl mnop`)
8. **احذف المسافات** عند إدخالها في Railway: `abcdefghijklmnop`

### 4. GMAIL_LABEL

1. افتح [Gmail](https://mail.google.com)
2. من القائمة الجانبية، اضغط **More** ثم **Create new label**
3. أدخل الاسم: `TO_BOT` (أو أي اسم تريده)
4. اضغط **Create**

**إعداد Filter (اختياري لكن مهم):**

1. اضغط على أيقونة البحث في الأعلى
2. أدخل شروط البحث (مثل: من مرسل معين)
3. اضغط **Create filter**
4. اختر **Apply the label:** ← `TO_BOT`
5. اضغط **Create filter**

الآن كل رسالة تطابق الشروط ستذهب تلقائياً لـ Label `TO_BOT`

### 5. GIFT_CHANNEL_ID

1. أنشئ قناة جديدة في تيليجرام (أو استخدم قناة موجودة)
2. أضف البوت كـ **Administrator** في القناة
3. أرسل أي رسالة في القناة
4. افتح المتصفح واذهب لهذا الرابط (استبدل `YOUR_BOT_TOKEN`):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
5. ابحث في النص عن `"chat":{"id":-100`
6. انسخ الرقم الكامل (مثل: `-1001234567890`)

**مثال:**
```json
"chat": {
  "id": -1001234567890,
  "title": "My Channel",
  "type": "channel"
}
```
انسخ: `-1001234567890`

### 6. SUPPORT_WHATSAPP_URL

رابط واتساب للدعم. الشكل:
```
https://wa.me/966503560199
```

استبدل الرقم برقمك (بدون `+` أو `00`)

### 7. ADMIN_ID

معرفك الشخصي في تيليجرام:

1. افتح [@userinfobot](https://t.me/userinfobot)
2. اضغط `/start`
3. سيرسل لك معلوماتك
4. انسخ رقم **Id** (مثل: `331753565`)

---

## ✅ التحقق من التشغيل

بعد إضافة جميع المتغيرات:

1. في Railway، اذهب لتبويب **Deployments**
2. يجب أن ترى **Success** باللون الأخضر
3. اضغط على **View Logs** لمشاهدة السجلات
4. إذا كان كل شيء صحيح، سترى رسائل تفيد بأن البوت يعمل

**اختبار البوت:**

1. افتح تيليجرام
2. ابحث عن البوت الخاص بك
3. اضغط `/start`
4. يجب أن يرد بالقائمة الرئيسية
5. جرب الأوامر المختلفة

---

## 🛠️ استكشاف الأخطاء

### البوت لا يرد في تيليجرام

**الحلول:**
- تحقق من أن `BOT_TOKEN` صحيح
- افتح Logs في Railway وابحث عن أخطاء
- تأكد من أن Deployment في حالة **Running**

### لا يجلب الأكواد من Gmail

**الحلول:**
- تحقق من `GMAIL_USER` و `GMAIL_APP_PASSWORD`
- تأكد من أن Label `TO_BOT` موجود في Gmail
- تأكد من وجود رسائل داخل Label
- جرب أمر `/code` وشاهد رسالة الخطأ

### أوامر الأدمن لا تعمل

**الحلول:**
- استخدم أمر `/me` في البوت
- تحقق من أن `ADMIN_ID` يطابق معرفك
- تأكد من عدم وجود مسافات في `ADMIN_ID`

### Railway يطلب فلوس

Railway يعطيك **$5 مجاناً** شهرياً للمشاريع الصغيرة. إذا انتهى الرصيد:
- تحقق من استهلاك المشروع
- يمكنك إضافة بطاقة ائتمان للحصول على رصيد إضافي
- أو استخدم منصات أخرى مثل:
  - [Render.com](https://render.com) (مجاني)
  - [Fly.io](https://fly.io) (مجاني)
  - [Heroku](https://heroku.com) (مدفوع)

---

## 📝 الأوامر المتاحة في البوت

| الأمر | الوصف | من يستخدمه |
|-------|--------|------------|
| `/start` | تشغيل البوت وعرض القائمة | الجميع |
| `/code` | جلب آخر كود من Gmail | الجميع |
| `/gift` | عرض الهدية من القناة | الجميع |
| `/support` | رابط التواصل مع الدعم | الجميع |
| `/users` | عرض عدد المشتركين | الأدمن فقط |
| `/broadcast` | بث رسالة لجميع المشتركين | الأدمن فقط |
| `/me` | عرض معلومات المستخدم | الجميع |

### استخدام `/broadcast`

**طريقة 1:** بث نص
```
/broadcast مرحباً بالجميع! هذه رسالة تجريبية
```

**طريقة 2:** بث رسالة/صورة/فيديو
1. أرسل الرسالة/الصورة/الفيديو في البوت
2. اضغط Reply على الرسالة
3. اكتب `/broadcast`

---

## 🔄 تحديث الكود

إذا قمت بتعديل الكود لاحقاً:

```bash
cd telegram-bot
# عدّل الملفات
git add .
git commit -m "وصف التعديل"
git push
```

سيتم إعادة النشر تلقائياً على Railway.

---

## 📞 الدعم

إذا واجهت أي مشكلة:
- راجع ملف [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) للتفاصيل الكاملة
- راجع ملف [QUICKSTART.md](QUICKSTART.md) للخطوات السريعة
- تواصل عبر WhatsApp: [966503560199](https://wa.me/966503560199)

---

**بالتوفيق! 🚀**

© DDXSTORE
