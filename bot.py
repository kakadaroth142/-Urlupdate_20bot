#!/usr/bin/env python3
import os, asyncio, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import yt_dlp
from config import BOT_TOKEN, DOWNLOAD_FOLDER

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

async def download_video(url, res="720"):
    try:
        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
        opts = {
            'format': f'best[height<={res}]/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'quiet': False,
        }
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=True))
            return {'ok': True, 'title': info.get('title', 'video'), 'file': ydl.prepare_filename(info)}
    except Exception as e:
        return {'ok': False, 'error': str(e)}

async def start(u, c):
    await u.message.reply_text(
        "🎬 <b>Bot ទាញយក Urlupdate25</b>\n\n📥 ផ្ញើ URL មកខ្ញុំ\n\n/help - ជំនួយបន្ថែម",
        parse_mode='HTML'
    )

async def help_cmd(u, c):
    await u.message.reply_text(
        "📋 <b>របៀបប្រើ</b>\n\n• 480p - ល្បឿនលឿន ⚡\n• 720p - គុណភាព ⭐\n• 1080p - ខ្ពស់ 🎥\n\n👤 ទាក់ទង @KAKADAROTHKH01",
        parse_mode='HTML'
    )

async def handle_msg(u, c):
    url = u.message.text.strip()
    if not url.startswith('http'):
        await u.message.reply_text("❌ សូមផ្ញើ URL ត្រឹមត្រូវ")
        return
    c.user_data['url'] = url
    kb = [
        [InlineKeyboardButton("480p ⚡", callback_data="480"), InlineKeyboardButton("720p ⭐", callback_data="720")],
        [InlineKeyboardButton("1080p 🎥", callback_data="1080")]
    ]
    await u.message.reply_text("📐 ជ្រើសរើស Resolution:", reply_markup=InlineKeyboardMarkup(kb))

async def btn(u, c):
    q = u.callback_query
    await q.answer()
    res = q.data
    url = c.user_data.get('url')
    if not url:
        await q.edit_message_text("❌ URL ត្រូវផ្ញើម្តងទៀត")
        return
    await q.edit_message_text("⏳ កំពុងទាញយក...")
    result = await download_video(url, res)
    if result['ok']:
        try:
            await q.message.reply_video(video=open(result['file'], 'rb'), caption=result['title'])
            os.remove(result['file'])
        except Exception as e:
            await q.message.reply_text(f"❌ បញ្ហាផ្ញើ file: {e}")
    else:
        await q.message.reply_text(f"❌ Platform នេះមិនគាំទ្រ!\n\nសូមប្រើ Link ពី YouTube, TikTok, Facebook, Instagram, Twitter។\n\n👤 ទាក់ទង: @KAKADAROTHKH01")

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    application.add_handler(CallbackQueryHandler(btn))
    application.run_polling()

if __name__ == "__main__":
    run_bot()
