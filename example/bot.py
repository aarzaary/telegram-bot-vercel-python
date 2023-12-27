import telebot
from flask import Flask, request
import os
import json

TOKEN = 'YOUR_BOT_TOKEN'
AUTHORIZED_USER = 'hax5x'
FILES_JSON = 'files.json'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: message.from_user.username == AUTHORIZED_USER)
def handle_authorized_user(message):
    if message.text.startswith('-'):
        # إذا كان المستخدم أراد إيقاف التشغيل
        stop_command(message.text[1:])
    elif message.text.startswith('+'):
        # إذا كان المستخدم أراد بدء التشغيل
        start_command(message.text[1:])
    else:
        bot.reply_to(message, "لم يتم فهم الأمر. يرجى استخدام '+' أو '-'.")

def stop_command(filename):
    try:
        # قراءة ملف JSON
        with open(FILES_JSON, 'r') as file:
            data = json.load(file)
            files = data['files']

        # التحقق من أن الملف الحالي هو الملف الذي يعمل
        for file in files:
            if file['name'] == filename and file['status'] == 'running':
                # إيقاف التشغيل
                os.system(f'pkill -f {filename}')

                # تحديث حالة الملف
                file['status'] = 'stopped'

                # حفظ التغييرات في ملف JSON
                with open(FILES_JSON, 'w') as file:
                    json.dump(data, file, indent=2)
                bot.reply_to(message, f"تم إيقاف تشغيل الملف: {filename}.")
                return

        bot.reply_to(message, f"الملف {filename} ليس الملف الذي يعمل حاليًا.")

    except FileNotFoundError:
        bot.reply_to(message, f"الملف {filename} غير موجود في قاعدة البيانات.")

def start_command(filename):
    try:
        # قراءة ملف JSON
        with open(FILES_JSON, 'r') as file:
            data = json.load(file)
            files = data['files']

        # التحقق من أن لا يوجد ملف يعمل حاليًا
        for file in files:
            if file['status'] == 'stopped':
                # بدء التشغيل
                os.system(f'python {filename} &')

                # تحديث حالة الملف
                file['status'] = 'running'

                # حفظ التغييرات في ملف JSON
                with open(FILES_JSON, 'w') as file:
                    json.dump(data, file, indent=2)
                bot.reply_to(message, f"تم بدء تشغيل الملف: {filename}.")
                return

        bot.reply_to(message, "جميع الملفات تعمل حاليًا. يرجى إيقاف تشغيل ملف آخر أولاً.")

    except FileNotFoundError:
        bot.reply_to(message, f"الملف {filename} غير موجود في قاعدة البيانات.")

# باقي الكود كما هو

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
