from telethon import TelegramClient, events

# Foydalanuvchi ma'lumotlari
api_id = 28256212
api_hash = "78b3e30e93d912fe1350b54bc88b5c31"
phone_number = "+998912000754"
target_group_id = -4650300446  # Nusxa ko‘chirish uchun guruh ID'si

# TelegramClient yaratish
client = TelegramClient("azamjon_vipe", api_id, api_hash)

trigger_words = [
	"odam", "1 ta", "2 ta", "3 ta", "4 ta", "kishi", "bola", "kshi", "ayol", "ayollar",
	"1ta", "poshta", "2ta", "4ta", "3ta", "pochta", "1", "2", "3", "4",
	"одам", "1 та", "2 та", "3 та", "4 та", "киши", "бола", "кши", "аёл", "аёллар",
	"1та", "пошта", "2та", "4та", "3та", "почта",
	"bitta", "ikkita", "uchta", "tortta", "torta", "ikta",
	"битта", "иккита", "учта", "тўртта", "торта", "икта"
]

block_words = ["olamiz", "kam", "yuramiz", ]
ignore_words = ["your user id:", "current chat id:"]

@client.on(events.NewMessage)
async def handler(event):
	if event.chat_id > 0:  # Shaxsiy chat bo‘lsa, qaytamiz
		return
	
	if event.out:  # Agar bot o‘zi yuborgan xabar bo‘lsa, qaytamiz
		return
	
	text = getattr(event.message, "text", "").lower().strip()
	if not text:
		return  # Xabar bo‘lmasa, qaytamiz
	
	# Agar xabar ignore_words ichida bo‘lsa, yubormaymiz
	if any(word in text for word in ignore_words):
		return
	
	sender = await event.get_sender()
	chat = await event.get_chat()
	
	if event.chat_id == target_group_id:
		return  # Xabar allaqachon nusxa ko‘chiriladigan guruhdan bo‘lsa, yana yubormaymiz
	
	user_id = sender.id
	user_link = f"tg://user?id={user_id}"
	
	# Telefon raqami tekshirish
	phone_number = f"+{getattr(sender, 'phone', 'Telefon raqami yopilgan')}"
	
	# Guruh nomi va username
	chat_title = getattr(chat, "title", "Guruh nomi yo'q")
	chat_username = f"https://t.me/{chat.username}" if getattr(chat, "username", None) else chat_title
	
	# Agar trigger so‘zlari bo‘lsa va block_words so‘zlari bo‘lmasa
	if any(word in text for word in trigger_words) and not any(block in text for block in block_words):
		formatted_message = (f"👋 Tog'ala yangi buyurtma !\n"
		                     f"<b>👥 Guruhdan :</b> <a href='{chat_username}'>@Azimjon Vip</a>\n"
		                     f"<b>👤 Murojat uchun :</b> <a href='{user_link}'>Profil</a>\n"
		                     f"<b>📞 Telefon raqami:</b> {phone_number}\n\n"
		                     f"✉️ <b>Xabar:</b> {event.message.text} \n\n🤲 Oq yol yaxhsi yetvolila :) \n Olinga bosa 🤝 Bosib qoyila ")
		
		await client.send_message(target_group_id, formatted_message, parse_mode='html')
		print(f"[{event.chat_id}] Xabar nusxalandi:", event.message.text)
	else:
		print(f"[{event.chat_id}] Xabar cheklangan:", event.message.text)

async def main():
	await client.start(phone_number)
	print("Userbot ishga tushdi...")
	await client.run_until_disconnected()

client.loop.run_until_complete(main())
