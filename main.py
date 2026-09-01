# main.py
import os
import re
import json
import imaplib
import email
import asyncio
from email.header import decode_header
from pathlib import Path
from datetime import datetime

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BotCommand,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# =========================
# Secrets / Env Vars
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
GMAIL_LABEL = os.getenv("GMAIL_LABEL", "TO_BOT")

GIFT_CHANNEL_ID = os.getenv("GIFT_CHANNEL_ID")
# رابط واتساب موحّد لزرّي «شراء إيميل» و «الدعم»
SUPPORT_WHATSAPP_URL = "https://wa.me/966500900942"
STORE_GROUP_URL = os.getenv("STORE_GROUP_URL", "https://chat.whatsapp.com/KM6wCSUCjGY6yI5oN4LJnQ")

ADMIN_ID = os.getenv("ADMIN_ID", "331753565")

COPYRIGHT = "© DDXSTORE"

# صورة/GIF القائمة (تُدمج معها الأزرار)
MENU_GIF = Path("assets/menu.gif")
_MENU_FILE_ID = None  # كاش لمعرّف الملف بعد أول إرسال

DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)
GIFT_STATE_FILE = DATA_DIR / "gift_state.json"

USERS_FILE = DATA_DIR / "users.json"

BACKUP_DIR = Path("./backups")
BACKUP_DIR.mkdir(exist_ok=True)

WELCOME_TEXT = (
    "👋 أهلًا بك في متجر DDXSTORE\n\n"
    "اختر من القائمة 👇\n"
    f"—\n{COPYRIGHT}"
)

# =========================
# Backup Helpers
# =========================
def _create_backup() -> None:
    try:
        if USERS_FILE.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = BACKUP_DIR / f"users_backup_{timestamp}.json"
            content = USERS_FILE.read_text(encoding="utf-8")
            backup_file.write_text(content, encoding="utf-8")
            latest_backup = BACKUP_DIR / "users_latest.json"
            latest_backup.write_text(content, encoding="utf-8")
            backups = sorted(BACKUP_DIR.glob("users_backup_*.json"))
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    old_backup.unlink()
    except Exception as e:
        print(f"⚠️ خطأ في إنشاء النسخة الاحتياطية: {e}")


async def _async_send_backup(app: Application) -> None:
    try:
        if not (USERS_FILE.exists() and ADMIN_ID):
            return
        users = _users_load()
        count = len(users)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = (
            f"📊 نسخة احتياطية\n"
            f"⏰ الوقت: {timestamp}\n"
            f"👥 عدد المشتركين: {count}\n"
            f"—\n{COPYRIGHT}"
        )
        with open(USERS_FILE, "rb") as fp:
            await app.bot.send_document(
                chat_id=int(ADMIN_ID),
                document=fp,
                filename=f"users_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                caption=message,
            )
    except Exception as e:
        print(f"⚠️ خطأ في إرسال النسخة للأدمن: {e}")

# =========================
# Users Helpers
# =========================
def _users_load() -> set[int]:
    if USERS_FILE.exists():
        try:
            data = json.loads(USERS_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return set(int(x) for x in data)
        except Exception as e:
            print(f"⚠️ خطأ في قراءة الملف الأساسي: {e}")

    latest_backup = BACKUP_DIR / "users_latest.json"
    if latest_backup.exists():
        try:
            data = json.loads(latest_backup.read_text(encoding="utf-8"))
            if isinstance(data, list):
                print("✅ تم الاسترجاع من النسخة الاحتياطية")
                users = set(int(x) for x in data)
                _users_save(users)
                return users
        except Exception as e:
            print(f"⚠️ خطأ في قراءة النسخة الاحتياطية: {e}")

    return set()


def _users_save(users: set[int]) -> None:
    try:
        USERS_FILE.write_text(
            json.dumps(sorted(list(users)), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        _create_backup()
    except Exception as e:
        print(f"⚠️ خطأ في حفظ الملف: {e}")


def register_user(user_id: int) -> None:
    users = _users_load()
    if user_id not in users:
        users.add(user_id)
        _users_save(users)


def get_users_count() -> int:
    return len(_users_load())


def is_admin(user_id) -> bool:
    try:
        return int(user_id) == int(ADMIN_ID)
    except Exception:
        return False

# =========================
# Inline Keyboards (merged with the menu GIF)
# =========================
def main_menu_inline(is_admin_user: bool = False) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton("📩 الحصول على الكود", callback_data="get_code")],
        [
            InlineKeyboardButton("🎁 الهدية", callback_data="gift"),
            InlineKeyboardButton("🛒 شراء إيميل", url=SUPPORT_WHATSAPP_URL),
        ],
        [
            InlineKeyboardButton("👨‍💻 الدعم", url=SUPPORT_WHATSAPP_URL),
            InlineKeyboardButton("📢 قروب المتجر", url=STORE_GROUP_URL),
        ],
    ]
    if is_admin_user:
        rows.append([InlineKeyboardButton("🛠 لوحة الأدمن", callback_data="admin_panel")])
    return InlineKeyboardMarkup(rows)


def admin_menu_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 الإحصائيات", callback_data="adm_stats")],
        [
            InlineKeyboardButton("📣 بث رسالة", callback_data="adm_broadcast"),
            InlineKeyboardButton("💾 نسخة احتياطية", callback_data="adm_backup"),
        ],
        [
            InlineKeyboardButton("👥 المشتركون", callback_data="adm_users"),
            InlineKeyboardButton("🪪 معلوماتي", callback_data="adm_me"),
        ],
        [InlineKeyboardButton("🏠 الرئيسية", callback_data="home")],
    ])

# =========================
# Gmail Helpers (IMAP)
# =========================
def _decode_header_value(v: str) -> str:
    if not v:
        return ""
    parts = decode_header(v)
    out = []
    for text, enc in parts:
        if isinstance(text, bytes):
            try:
                out.append(text.decode(enc or "utf-8", errors="ignore"))
            except Exception:
                out.append(text.decode("utf-8", errors="ignore"))
        else:
            out.append(text)
    return "".join(out).strip()


def _extract_text_from_email(msg: email.message.Message) -> str:
    text_parts = []
    html_parts = []

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition") or "")
            if "attachment" in disp.lower():
                continue
            payload = part.get_payload(decode=True)
            if not payload:
                continue
            charset = part.get_content_charset() or "utf-8"
            try:
                decoded = payload.decode(charset, errors="ignore")
            except Exception:
                decoded = payload.decode("utf-8", errors="ignore")
            if ctype == "text/plain":
                text_parts.append(decoded)
            elif ctype == "text/html":
                html_parts.append(decoded)
    else:
        ctype = msg.get_content_type()
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            try:
                decoded = payload.decode(charset, errors="ignore")
            except Exception:
                decoded = payload.decode("utf-8", errors="ignore")
            if ctype == "text/plain":
                text_parts.append(decoded)
            elif ctype == "text/html":
                html_parts.append(decoded)

    if text_parts:
        return "\n".join(text_parts).strip()

    if html_parts:
        html = "\n".join(html_parts)
        html = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", html)
        html = re.sub(r"(?s)<.*?>", " ", html)
        html = html.replace("&nbsp;", " ").replace("&amp;", "&")
        html = re.sub(r"\s+", " ", html).strip()
        return html

    return ""


def _clean_text_keep_code_only(raw: str) -> str:
    if not raw:
        return ""
    raw = re.sub(r"https?://\S+", " ", raw)
    raw = re.sub(r"\s+", " ", raw).strip()
    m = re.search(r"\b(\d{4,8})\b", raw)
    if m:
        return m.group(1)
    return raw[:200].strip()


def fetch_latest_code_from_label() -> str:
    if not (GMAIL_USER and GMAIL_APP_PASSWORD):
        return "❌ ناقص إعدادات Gmail في Secrets (GMAIL_USER / GMAIL_APP_PASSWORD)."

    label = GMAIL_LABEL or "TO_BOT"
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        status, _ = imap.select(f'"{label}"', readonly=True)
        if status != "OK":
            imap.logout()
            return f"❌ ما قدرت أفتح الليبل: {label}"
        status, data = imap.search(None, "ALL")
        if status != "OK" or not data or not data[0]:
            imap.logout()
            return "❌ ما فيه رسائل داخل الليبل."
        ids = data[0].split()
        latest_id = ids[-1]
        status, msg_data = imap.fetch(latest_id, "(RFC822)")
        if status != "OK" or not msg_data:
            imap.logout()
            return "❌ ما قدرت أقرأ آخر رسالة."
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        body = _extract_text_from_email(msg)
        code = _clean_text_keep_code_only(body)
        imap.logout()
        if not code:
            return "❌ ما لقيت كود واضح."
        return f"✅ الكود: {code}\n—\n{COPYRIGHT}"
    except Exception as e:
        return f"❌ خطأ: {e}"

# =========================
# Gift Channel Helpers
# =========================
def _gift_state_load() -> dict:
    if GIFT_STATE_FILE.exists():
        try:
            return json.loads(GIFT_STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _gift_state_save(state: dict) -> None:
    GIFT_STATE_FILE.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")


def get_gift_channel_id_int() -> int | None:
    if not GIFT_CHANNEL_ID:
        return None
    try:
        return int(GIFT_CHANNEL_ID.strip())
    except Exception:
        return None


async def _send_gift(chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    channel_id = get_gift_channel_id_int()
    if not channel_id:
        await context.bot.send_message(chat_id, "❌ GIFT_CHANNEL_ID غير مضبوط في Secrets.")
        return
    state = _gift_state_load()
    msg_id = state.get("message_id")
    if not msg_id:
        await context.bot.send_message(
            chat_id,
            "🎁 ما فيه هدية محفوظة للحين.\n"
            "ارسل رسالة في قناة الهدايا عشان تتسجل تلقائياً.",
        )
        return
    try:
        await context.bot.copy_message(chat_id=chat_id, from_chat_id=channel_id, message_id=int(msg_id))
        await context.bot.send_message(chat_id, "—\n" + COPYRIGHT)
    except Exception:
        gift_text = state.get("text") or "🎁"
        await context.bot.send_message(chat_id, f"{gift_text}\n—\n{COPYRIGHT}")

# =========================
# Menu sender (GIF + inline buttons merged)
# =========================
async def send_main_menu(chat_id: int, context: ContextTypes.DEFAULT_TYPE, is_admin_user: bool):
    global _MENU_FILE_ID
    markup = main_menu_inline(is_admin_user)
    try:
        if _MENU_FILE_ID:
            await context.bot.send_animation(
                chat_id=chat_id, animation=_MENU_FILE_ID,
                caption=WELCOME_TEXT, reply_markup=markup,
            )
        elif MENU_GIF.exists():
            with open(MENU_GIF, "rb") as f:
                msg = await context.bot.send_animation(
                    chat_id=chat_id, animation=f,
                    caption=WELCOME_TEXT, reply_markup=markup,
                )
            if msg.animation:
                _MENU_FILE_ID = msg.animation.file_id
        else:
            await context.bot.send_message(chat_id, WELCOME_TEXT, reply_markup=markup)
    except Exception:
        await context.bot.send_message(chat_id, WELCOME_TEXT, reply_markup=markup)

# =========================
# Telegram Handlers
# =========================
async def set_commands(app: Application) -> None:
    commands = [
        BotCommand("start", "تشغيل القائمة"),
        BotCommand("code", "جلب آخر كود"),
        BotCommand("gift", "عرض الهدية"),
        BotCommand("support", "التواصل مع الدعم"),
        BotCommand("users", "عدد المشتركين (أدمن)"),
        BotCommand("broadcast", "بث رسالة للجميع (أدمن)"),
        BotCommand("backup", "إرسال نسخة احتياطية (أدمن)"),
        BotCommand("me", "اختبار (يعرض ID والإعدادات)"),
    ]
    try:
        await app.bot.set_my_commands(commands)
    except Exception:
        pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = update.effective_user.id if update.effective_user else None
    if uid:
        register_user(uid)
    await send_main_menu(update.effective_chat.id, context, is_admin(uid) if uid else False)


async def cmd_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = await asyncio.to_thread(fetch_latest_code_from_label)
    await update.message.reply_text(msg)


async def cmd_gift(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _send_gift(update.effective_chat.id, context)


async def cmd_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👨‍💻 للتواصل أو الشراء اضغط الزر:",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("💬 فتح واتساب", url=SUPPORT_WHATSAPP_URL)]]
        ),
    )


async def cmd_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = update.effective_user.id if update.effective_user else None
    await update.message.reply_text(
        f"Your ID: {uid}\nADMIN_ID: {ADMIN_ID}\n"
        f"IsAdmin: {is_admin(uid) if uid else False}\nUsersCount: {get_users_count()}"
    )


async def cmd_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ هذا الأمر للأدمن فقط.")
        return
    await update.message.reply_text(f"👥 عدد المشتركين: {get_users_count()}\n—\n{COPYRIGHT}")


async def cmd_backup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ هذا الأمر للأدمن فقط.")
        return
    try:
        if not USERS_FILE.exists():
            await update.message.reply_text("❌ ملف المشتركين غير موجود.")
            return
        count = get_users_count()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = (
            f"📊 نسخة احتياطية يدوية\n"
            f"⏰ الوقت: {timestamp}\n"
            f"👥 عدد المشتركين: {count}\n"
            f"—\n{COPYRIGHT}"
        )
        with open(USERS_FILE, "rb") as fp:
            await update.message.reply_document(
                document=fp,
                filename=f"users_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                caption=message,
            )
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}")


async def cmd_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ هذا الأمر للأدمن فقط.")
        return

    users = _users_load()
    if not users:
        await update.message.reply_text("ما فيه مشتركين محفوظين للحين.")
        return

    sent = 0
    failed = 0

    if update.message and update.message.reply_to_message:
        src = update.message.reply_to_message
        await update.message.reply_text("📣 جاري البث للجميع...")
        for uid in users:
            try:
                await context.bot.copy_message(chat_id=uid, from_chat_id=src.chat_id, message_id=src.message_id)
                sent += 1
            except Exception:
                failed += 1
            await asyncio.sleep(0.05)
        await update.message.reply_text(f"✅ تم البث\nوصلت: {sent}\nفشل: {failed}")
        return

    if not context.args:
        await update.message.reply_text(
            "استخدم البث بطريقتين:\n"
            "1) ارسل أي رسالة/صورة ثم رد عليها بـ /broadcast\n"
            "2) /broadcast نص الرسالة"
        )
        return

    text = " ".join(context.args)
    await update.message.reply_text("📣 جاري البث للجميع...")
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=text)
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)
    await update.message.reply_text(f"✅ تم البث\nوصلت: {sent}\nفشل: {failed}")


async def channel_post_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    channel_id = get_gift_channel_id_int()
    if not channel_id:
        return
    post = update.channel_post
    if not post or post.chat.id != channel_id:
        return
    state = {"message_id": post.message_id, "text": post.text or post.caption or ""}
    _gift_state_save(state)


# =========================
# Inline Buttons Router (callbacks)
# =========================
async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    if not q:
        return
    await q.answer()
    data = q.data or ""
    uid = q.from_user.id if q.from_user else None
    chat_id = q.message.chat_id if q.message else None

    async def _edit_caption(text: str, markup: InlineKeyboardMarkup):
        try:
            await q.edit_message_caption(caption=text, reply_markup=markup)
        except Exception:
            try:
                await q.edit_message_text(text, reply_markup=markup)
            except Exception:
                await context.bot.send_message(chat_id, text, reply_markup=markup)

    # ---- تنقّل ----
    if data == "home":
        await _edit_caption(WELCOME_TEXT, main_menu_inline(is_admin(uid) if uid else False))
        return

    if data == "get_code":
        await q.answer("⏳ جاري جلب الكود...")
        code = await asyncio.to_thread(fetch_latest_code_from_label)
        await context.bot.send_message(chat_id, code)
        return

    if data == "gift":
        await _send_gift(chat_id, context)
        return

    # ---- لوحة الأدمن ----
    if data == "admin_panel" or data.startswith("adm_"):
        if not uid or not is_admin(uid):
            await q.answer("❌ هذا الأمر للأدمن فقط.", show_alert=True)
            return

        if data == "admin_panel":
            await _edit_caption("🛠 لوحة التحكم:", admin_menu_inline())
            return

        if data in ("adm_stats", "adm_users"):
            await _edit_caption(
                f"👥 عدد المشتركين: {get_users_count()}\n—\n{COPYRIGHT}",
                admin_menu_inline(),
            )
            return

        if data == "adm_backup":
            await q.answer("💾 جاري الإرسال...")
            if USERS_FILE.exists():
                await _async_send_backup(context.application)
                await context.bot.send_message(chat_id, "✅ تم إرسال النسخة الاحتياطية لك.")
            else:
                await context.bot.send_message(chat_id, "❌ ملف المشتركين غير موجود.")
            return

        if data == "adm_broadcast":
            await _edit_caption(
                "📣 البث للجميع:\n"
                "• أرسل: /broadcast نص الرسالة\n"
                "• أو رد على أي رسالة/صورة بـ /broadcast",
                admin_menu_inline(),
            )
            return

        if data == "adm_me":
            await _edit_caption(
                f"Your ID: {uid}\nADMIN_ID: {ADMIN_ID}\n"
                f"IsAdmin: {is_admin(uid)}\nUsersCount: {get_users_count()}",
                admin_menu_inline(),
            )
            return


async def fallback_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """أي رسالة نصية عادية -> أعرض القائمة (مدمجة مع الـ GIF)."""
    if not update.message:
        return
    uid = update.effective_user.id if update.effective_user else None
    await send_main_menu(update.effective_chat.id, context, is_admin(uid) if uid else False)

# =========================
# Main
# =========================
def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing in Secrets")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("code", cmd_code))
    app.add_handler(CommandHandler("gift", cmd_gift))
    app.add_handler(CommandHandler("support", cmd_support))
    app.add_handler(CommandHandler("users", cmd_users))
    app.add_handler(CommandHandler("broadcast", cmd_broadcast))
    app.add_handler(CommandHandler("backup", cmd_backup))
    app.add_handler(CommandHandler("me", cmd_me))

    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, channel_post_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_text))

    app.post_init = set_commands

    print("✅ البوت يعمل الآن — قائمة Inline مدمجة مع الـ GIF!")
    print(f"📁 مجلد البيانات: {DATA_DIR.absolute()}")
    print(f"💾 مجلد النسخ الاحتياطية: {BACKUP_DIR.absolute()}")

    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
