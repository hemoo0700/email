import logging
import requests
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- إعداد Flask للتهرب من شروط الاستضافة المجانية ---
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Bot is running!"

def run_flask():
    # تشغيل سيرفر وهمي على المنفذ 8080
    app_flask.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- إعدادات البوت الأساسية ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_TOKEN = "8426090796:AAEyPqECETpS-x7oMtv3qusyYQ_6_jv5gTc"
RAPIDAPI_KEY = "c854ebec5fmsh3575a0169dc7e91p1a002djsndffbdcb0fc10"
RAPIDAPI_HOST = "breachdirectory.p.rapidapi.com"
BREACH_API_URL = "https://breachdirectory.p.rapidapi.com/"

DEVELOPER_RIGHTS = "المطور: ༺ 𒆜فتى قريش𒆜 ༻⁩\nتليجرام: @ADULF07"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"🙋‍♂️ أهلاً بك يا {user_name} في بوت فحص التسريبات الأمنية الاحترافي.\n\n"
        "🔒 يمكنك فحص الإيميلات، أسماء المستخدمين، أو النطاقات للتأكد من سلامتها من الاختراقات.\n\n"
        "📥 **أرسل الآن الهدف المراد فحصه** (مثال: email@example.com)\n\n"
        "---"
    )
    keyboard = [[InlineKeyboardButton("💬 تواصل مع المطور", url="https://t.me/ADULF07")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"{welcome_text}\n\n{DEVELOPER_RIGHTS}", reply_markup=reply_markup, parse_mode="Markdown")

async def handle_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    status_message = await update.message.reply_text("🔍 جاري الفحص والتحقق من قواعد البيانات العالمية، انتظر لحظة...")
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
        "Content-Type": "application/json"
    }
    params = {"func": "auto", "term": query}
    
    try:
        response = requests.get(BREACH_API_URL, headers=headers, params=params, timeout=15)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                response_text = f"🚨 **تنبيه أمني عاجل! تم العثور على تسريبات لـ ({query}):**\n\n"
                for index, breach in enumerate(result, 1):
                    source = breach.get("sources", ["غير معروف"])[0] if breach.get("sources") else "غير معروف"
                    has_password = "نعم 🔑" if breach.get("password") or breach.get("sha1") else "لا 🔒"
                    response_text += f"{index}️⃣ **مصدر التسريب:** {source}\n🔹 **كشف كلمة المرور:** {has_password}\n\n"
                response_text += "💡 *نصيحة:* يرجى تغيير كلمات المرور وتفعيل التحقق بخطوتين."
            elif isinstance(result, dict) and result.get("success") == False:
                response_text = f"❌ **خطأ:** {result.get('message', 'لم تنجح العملية')}"
            else:
                response_text = f"✅ **الحساب آمن!** لم يتم العثور على أي بيانات مسربة مرتبطة بـ ({query})."
        else:
            response_text = f"⚠️ حدث خطأ في الاتصال (Status Code: {response.status_code})."
    except Exception as e:
        response_text = "❌ حدث خطأ غير متوقع أثناء معالجة البيانات."
    
    final_text = f"{response_text}\n\n---\n{DEVELOPER_RIGHTS}"
    await status_message.edit_text(final_text, parse_mode="Markdown")

def main():
    # تشغيل السيرفر الوهمي في الخلفية لحماية البوت من الإغلاق
    keep_alive()
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_check))
    
    print("🚀 البوت الخاص بـ فتى قريش يعمل الآن بنجاح...")
    app.run_polling()

if __name__ == "__main__":
    main()
