import telebot
from telebot import types
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime


cnx = mysql.connector.connect(user='root', password='***********',
                              host='127.0.0.1',
                              database='OnlyfDb')
cursor = cnx.cursor()
bot = telebot.TeleBot("656************************A3lsprNE")
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton('onlyf')
    button2 = types.KeyboardButton("members nude")
  #  button3 = types.KeyboardButton("video")
  #  button4 = types.KeyboardButton("photo")
    markup.row(button)
    markup.row(button2)
   # markup.row(button3,button4)
     #ذخیره اطلاعات کاربر  {
    name = message.from_user.full_name 
    username = message.from_user.username
    user_id = message.from_user.id


    # چک کردن اینکه کاربر در جدول وجود دارد یا نه
    cursor.execute("SELECT * FROM onlyfuser WHERE user_id=%s", (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        # اگر کاربر وجود نداشته باشد، اضافه کنید و زمان اضافه شدن را ذخیره کنید
        join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO onlyfuser (name,username,user_id,join_date) VALUES (%s, %s, %s,%s)", (name,username,user_id ,join_date))
        cnx.commit()
      #ذخیره اطلاعات کاربر  }

    bot.reply_to(message, "خوش اومدید برای شروع روی یکی از دکمه های زیر بزنید  \n Welcome, click on one of the buttons below to start", reply_markup=markup)
@bot.message_handler(func=lambda msg: msg.text == '/********')
def admin_welcome(message):
    b = message
    
    markup = types.ReplyKeyboardMarkup()
    admin_button = types.KeyboardButton('upload onlyf')
    admin_button2 = types.KeyboardButton('uplod members nude')
    back_button = types.KeyboardButton('upload photo')

    markup.row(admin_button)
    markup.row(admin_button2)
    markup.row(back_button)

    bot.send_message(message.chat.id, "ادمین خوش آمدی!", reply_markup=markup)
    
    bot.register_next_step_handler(b ,admin)

    

def admin(message):
    m = message
    aa = m.text

    bot.reply_to(message, "ax bede")

    if m.text == "upload onlyf" :
        bot.send_message(m.chat.id , "عکس و اسم و لینک ارسال کن ") 
        bot.register_next_step_handler(m,get_name,aa)
    if m.text == "uplod members nude" :
         bot.send_message(m.chat.id , "عکس و اسم و لینک ارسال کن ") 
         bot.register_next_step_handler(m,get_name,aa)
    if m.text == "upload photo" :
         bot.send_message(m.chat.id , "عکس و اسم و لینک ارسال کن ") 
         bot.register_next_step_handler(m,get_name,aa)


def get_name(message,aa):
    name = message.text
    if name == "/c":
        admin_welcome(message)
    bot.send_message(message.chat.id, "لطفاً لینک را وارد کنید:")
    bot.register_next_step_handler(message, get_link,aa, name)

def get_link(message,aa, name):
    link = message.text
    if link == "/c":
        admin_welcome(message)

    bot.send_message(message.chat.id, "لطفاً عکس را ارسال کنید:")
    bot.register_next_step_handler(message, get_photo,aa,name,link)

def get_photo(message,aa, name, link):
    photo_link = message.text
    if photo_link == "/c":
        admin_welcome(message)
    else : 

        if aa == "upload onlyf" :
            try:
                    query = "INSERT INTO onlyf (name, link, photo) VALUES (%s, %s, %s)"
                    values = (name, link, photo_link)
                    cursor.execute(query, values)
                    cnx.commit()

                    bot.reply_to(message, "اطلاعات با موفقیت به دیتابیس اضافه شد.")
            except mysql.connector.Error as err:
                    bot.reply_to(message, f"خطا در وارد کردن اطلاعات به دیتابیس: {err}")
        elif aa == "uplod members nude" :
            try:
                    query = "INSERT INTO MembersNude (name, link, photo) VALUES (%s, %s, %s)"
                    values = (name, link, photo_link)
                    cursor.execute(query, values)
                    cnx.commit()

                    bot.reply_to(message, "اطلاعات با موفقیت به دیتابیس اضافه شد.")
            except mysql.connector.Error as err:
                    bot.reply_to(message, f"خطا در وارد کردن اطلاعات به دیتابیس: {err}")
        else :
            bot.reply_to(message, ";dv")

                         





@bot.message_handler(func=lambda msg: True) 
def send_something(message):
    m = message

    if m.text == 'onlyf':
        hide_markup = types.ReplyKeyboardRemove()
        new_markup = types.ReplyKeyboardMarkup()
        new_button1 = types.KeyboardButton('search')
        new_button2 = types.KeyboardButton('show onlyf users')
        new_button3 = types.KeyboardButton('back')

        new_markup.row(new_button1)
        new_markup.row(new_button2)
        new_markup.row(new_button3)

        bot.send_message(m.chat.id, "یکی از دکمه های زیر را انتخاب کنید \n Select one of the buttons below", reply_markup=new_markup)
        bot.register_next_step_handler(m,onlyf)
    if m.text == 'members nude'  :
        hide_markup = types.ReplyKeyboardRemove()
        new_markup = types.ReplyKeyboardMarkup()
        new_button1 = types.KeyboardButton('Show photos')
        new_button2 = types.KeyboardButton('Send Photo')
        new_button3 = types.KeyboardButton('back')
        new_markup.row(new_button1)
        new_markup.row(new_button2)
        new_markup.row(new_button3)
        bot.send_message(m.chat.id, " یکی از دکمه های زیر را انتخاب کنید \n Select one of the buttons below", reply_markup=new_markup)
        bot.register_next_step_handler(m,members_nude)
    #if m.text == 'video':
     #   bot.send_message(m.chat.id, "این بخش هنوز کامل نیست")
   # if m.text == 'photo':
     #   bot.send_message(m.chat.id, "این بخش هنوز کامل نیست") 

def onlyf (message):
    m=message
    if m.text == "search":
        bot.reply_to(message, "Enter the onlyf username you want \n اسم کاربر onlyf که میخوای وارد کن")
        bot.register_next_step_handler(m,onlyf_search)
    elif m.text == "show onlyf users" :
        cursor.execute("SELECT COUNT(*) FROM onlyf")
        total_ids = cursor.fetchone()[0]
    
        bot.send_message(m.chat.id, f"تعداد IDهای موجود در دیتابیس: {total_ids}")
        bot.send_message(m.chat.id, f"یک عدد بین 1 تا {total_ids} انتخاب کنید \n Choose a number between 1 and {total_ids}")
        bot.register_next_step_handler(m,onlyf_users)
    elif m.text == 'back':
        send_welcome(m)
    else :
        bot.register_next_step_handler(message,onlyf)


def members_nude(message):
    m=message
    if m.text =='Show photos':
        cursor.execute("SELECT COUNT(*) FROM MembersNude")
        total_ids = cursor.fetchone()[0]
    
        bot.send_message(m.chat.id, f"تعداد IDهای موجود در دیتابیس: {total_ids}")
        bot.send_message(m.chat.id, f"یک عدد بین 1 تا {total_ids} انتخاب کنید \n Choose a number between 1 and {total_ids}")
        bot.register_next_step_handler(m,members_nude_ph)
    elif m.text == 'Send Photo':
         bot.reply_to(message, "عکس قشنگتو برامون بفرست 😍 \n Send us your beautiful photo 😍")
         bot.register_next_step_handler(m,send_photo)
    elif m.text == 'back':
        send_welcome(m)
    else :
        bot.register_next_step_handler(m,members_nude)
def members_nude_ph(message):
     m = message
     m2 = m.text
     # محاسبه تعداد IDها در دیتابیس
     if m2 == 'back'or m2== '/start':
         send_welcome(m)
     else:
         if m2.isdigit():
             user_id = int(m.text)  # تبدیل ورودی کاربر به یک عدد صحیح
     
             # انجام جستجو بر اساس شناسه کاربر در دیتابیس
             query = "SELECT * FROM MembersNude WHERE id = %s"
             cursor.execute(query, (user_id,))
             result = cursor.fetchone()
     
             if result:
                user_info = f"id: {result[0]}\n"
              #  user_info += f"name: {result[1]}\n"
                user_info += f"{result[2]}\n"
                photo_link = result[3]
                # اضافه کردن سایر اطلاعات کاربر به user_info
                bot.send_photo(message.chat.id, photo_link ,user_info)
                bot.register_next_step_handler(message,members_nude)
     
             else:
                 bot.send_message(m.chat.id, f"کاربر با شناسه {user_id} یافت نشد. \n User with id {user_id} was not found")
                 bot.register_next_step_handler(message,members_nude)
         else:
             bot.send_message(m.chat.id, f"یک عدد بین رنج گفته شده انتخاب کنید \n Choose a number from the given range" )
             bot.register_next_step_handler(message,members_nude_ph)


def send_photo (message):
     m = message
     try:
        # دریافت اطلاعات عکس
        photo_id = message.photo[-1].file_id
        photo_caption = message.caption if message.caption else "بدون توضیحات"
        channel_id = "-1002096338510"
        # ارسال عکس به کانال
        bot.send_photo(channel_id, photo_id, caption=photo_caption)
        bot.reply_to(message, f" عکست ارسال شد")
        bot.register_next_step_handler(m,members_nude)

       
     except Exception as e:
         bot.reply_to(message, f"خطا در پردازش عکس: {e}")
         bot.register_next_step_handler(m,members_nude)



#def onlyf(message):

   
#    if message.text == 'search':
#        bot.register_next_step_handler(message, onlyf_search)

#    if message.text == 'show onlyf users':
#        bot.register_next_step_handler(message, send_username)

#    if message.text == 'back':
#        bot.register_next_step_handler(message, send_username)


def onlyf_search(message):
     user_input = message.text  # مقدار user_input از متن پیام کاربر دریافت می‌شود
    
     bot.reply_to(message, "search:")
     query = "SELECT * FROM onlyf WHERE name LIKE %s"
     cursor.execute(query, ("%" + user_input + "%",))

     # دریافت نتایج
     results = cursor.fetchall()

     if results:
         result_text = "کاربران مشابه:\n"
         for result in results:
             user_id = result[0]  # دریافت شناسه کاربر
             name = result[1]  # دریافت نام کاربری
             onlyf_link = result[2]  # دریافت اطلاعات دیگر کاربر
             only_photo = result[3]

             result_text += f"id: {user_id}\n\n"
             result_text += f"name: {name}\n\n"
             result_text += f"only fans link: {onlyf_link}\n\n"
             bot.send_photo(message.chat.id, only_photo ,result_text)
             result_text = ''
         bot.register_next_step_handler(message,onlyf)
         #bot.send_photo(message.chat.id, image_url ,result_text)
     else:
         bot.reply_to(message, f"کاربر با نام {user_input} پیدا نشد \n  User with name {user_input} not found")
         bot.register_next_step_handler(message,onlyf)

def onlyf_users (message):
    m = message
    m2 = m.text
    # محاسبه تعداد IDها در دیتابیس
    if m2 == 'back'or m2== '/start':
        send_welcome(m)
    else:

        
        if m2.isdigit():
            user_id = int(m.text)  # تبدیل ورودی کاربر به یک عدد صحیح
    
            # انجام جستجو بر اساس شناسه کاربر در دیتابیس
            query = "SELECT * FROM onlyf WHERE id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
    
            if result:
                user_info = f"id: {result[0]}\n"
                user_info += f"name: {result[1]}\n"
                user_info += f"only fans link: {result[2]}\n"
                photo_link = result[3]
                # اضافه کردن سایر اطلاعات کاربر به user_info
                bot.send_photo(message.chat.id, photo_link ,user_info)
                bot.register_next_step_handler(message,onlyf)

            else:
                bot.send_message(m.chat.id, f"کاربر با شناسه {user_id} یافت نشد. \n User with id {user_id} was not found")
                bot.register_next_step_handler(message,onlyf)
        else:
            bot.send_message(m.chat.id, f"یک عدد بین رنج گفته شده انتخاب کنید \n Choose a number from the given range")
            bot.register_next_step_handler(message,onlyf_users)

            


bot.polling()
