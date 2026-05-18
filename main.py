import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد السجلات لمراقبة العمليات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- [ الإعدادات الخاصة بك ] ---
TELEGRAM_TOKEN = "ضع_توكن_البوت_الخاص_بك_هنا"

# البيانات المستخرجة من الصورة الخاصة بك
RAPIDAPI_KEY = "c854ebec5fmsh3575a0169dc7e91p1a002djsndffbdcb0fc10"
RAPIDAPI_HOST = "breachdirectory.p.rapidapi.com"
BREACH_API_URL = "https://breachdirectory.p.rapidapi.com/"

DEVELOPER_RIGHTS = "المطور: ༺ 𒆜فتى قريش𒆜 ༻⁩\nتليجرام: @ADULF07"

# رسالة الترحيب /start
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

# استقبال البيانات وفحصها عبر الـ API
async def handle_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    
    # رسالة انتظار متحركة واحترافية
    status_message = await update.message.reply_text("🔍 جاري الفحص والتحقق من قواعد البيانات العالمية، انتظر لحظة...")
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
        "Content-Type": "application/json"
    }
    
    # الإعدادات المأخوذة من الكود الخاص بك func=auto
    params = {
        "func": "auto",
        "term": query
    }
    
    try:
        response = requests.get(BREACH_API_URL, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            
            # فحص إذا كانت هناك نتائج تسريب (إذا كانت الاستجابة قائمة تحتوي على تسريبات)
            if isinstance(result, list) and len(result) > 0:
                response_text = f"🚨 **تنبيه أمني عاجل! تم العثور على تسريبات لـ ({query}):**\n\n"
                
                for index, breach in enumerate(result, 1):
                    # استخراج البيانات بناءً على هيكلة RapidAPI لـ BreachDirectory
                    source = breach.get("sources", ["غير معروف"])[0] if breach.get("sources") else "غير معروف"
                    has_password = "نعم 🔑" if breach.get("password") or breach.get("sha1") else "لا 🔒"
                    
                    response_text += f"{index}️⃣ **مصدر التسريب:** {source}\n🔹 **كشف كلمة المرور:** {has_password}\n\n"
                
                response_text += "💡 *نصيحة:* يرجى تغيير كلمات المرور المرتبطة بهذا الحساب فوراً وتفعيل التحقق بخطوتين."
            
            # في حال كانت النتيجة فارغة أو تفيد بعدم وجود خروقات
            elif isinstance(result, dict) and result.get("success") == False:
                response_text = f"❌ **خطأ:** {result.get('message', 'لم تنجح العملية')}"
            else:
                response_text = f"✅ **الحساب آمن!** لم يتم العثور على أي بيانات مسربة مرتبطة بـ ({query}) في قواعد البيانات المتوفرة حالياً."
                
        elif response.status_code == 403 or response.status_code == 401:
            response_text = "❌ انتهت صلاحية مفتاح الـ API أو تم تجاوزه، يرجى مراجعة المطور."
        else:
            response_text = f"⚠️ حدث خطأ في الاتصال بالسيرفر الرئيسي (Status Code: {response.status_code})."
            
    except Exception as e:
        response_text = "❌ حدث خطأ غير متوقع أثناء معالجة البيانات."
        logging.error(f"Error occurred: {e}")

    # إرسال النتيجة النهائية مع حقوقك وثوقيتك
    final_text = f"{response_text}\n\n---\n{DEVELOPER_RIGHTS}"
    await status_message.edit_text(final_text, parse_mode="Markdown")

# تشغيل البوت
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_check))
    
    print("🚀 البوت الخاص بـ فتى قريش يعمل الآن بنجاح...")
    app.run_polling()

if __name__ == "__main__":
    main()