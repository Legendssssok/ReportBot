import json
import os
import subprocess
from pathlib import Path
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from pyrogram.errors import MessageIdInvalid
from info import Config, Txt


config_path = Path("config.json")


async def Report_Function(No, message_ids):

    message = No
    print(No, message_ids)
    # Run a shell command and capture its output
    process = subprocess.Popen(
        ["python", f"reportmsg.py",
            f"{message}", f"{message_ids}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Use communicate() to interact with the process
    stdout, stderr = process.communicate()

    # Get the return code
    return_code = process.wait()

    # Check the return code to see if the command was successful
    if return_code == 0:
        # Print the output of the command
        print("Command output:")
        print(stdout)
        return [stdout, True]

    else:
        # Print the error message if the command failed
        print("Command failed with error:")
        print(stderr)
        return f"<b>Something Went Wrong Kindly Check your Inputs Whether You Have Filled Correctly or Not !</b>\n\n <code> {stderr} </code> \n ERROR"


async def CHOICE_OPTION(bot, msg, number):

    if not config_path.exists():
        return await msg.reply_text(text="**You don't have any config first make the config then you'll able to report**\n\n Use /make_config", reply_to_message_id=msg.id, reply_markup=ReplyKeyboardRemove())

    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)

    try:
        if Path('report.txt').exists():
            await msg.reply_text(text="**Already One Process is Ongoing Please Wait Until it's Finished ⏳**", reply_to_message_id=msg.id)
        message_ids = await bot.ask(text=Txt.MSG_REPORT_FORMAT, chat_id=msg.chat.id, filters=filters.text, timeout=200, reply_markup=ReplyKeyboardRemove())
        no_of_reports = await bot.ask(text=Txt.SEND_NO_OF_REPORT_MSG.format(config['Target']), chat_id=msg.chat.id, filters=filters.text, timeout=30)
    except:
        await bot.send_message(msg.from_user.id, "Error!!\n\nRequest timed out.\nRestart by using /msgreport", reply_markup=ReplyKeyboardRemove())
        return
    ms = await bot.send_message(chat_id=msg.chat.id, text=f"**Please Wait**\n\n Have Patience ⏳", reply_to_message_id=msg.id, reply_markup=ReplyKeyboardRemove())
    if str(no_of_reports.text).isnumeric():

        try:
            i = 0
            while i < int(no_of_reports.text):
                result = await Report_Function(number, message_ids.text)

                if result[1]:
                    # Assuming output is a bytes object
                    output_bytes = result[0]
                    # Decode bytes to string and replace "\r\n" with newlines
                    output_string = output_bytes.decode(
                        'utf-8').replace('\r\n', '\n')

                    with open('report.txt', 'a+') as file:
                        file.write(output_string)

                    i += 1
                    continue

                else:
                    await bot.send_message(chat_id=msg.chat.id, text=f"{result}", reply_to_message_id=msg.id)
        except Exception as e:
            print('Error on line {}'.format(
                sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            return await msg.reply_text(text=f"**{e}**\n\n ERROR !")

    else:
        await msg.reply_text(text='**Please Enter Valid Integer Number !**\n\n Try Again :- /report')
        return

    await ms.delete()
    await msg.reply_text(text=f"Bot Successfully Reported To @{config['Target']} ✅\n\n{no_of_reports.text} Times")
    file = open('report.txt', 'a')
    file.write(
        f"\n\n@{config['Target']} Channel or Group is Reported {no_of_reports.text} Times ✅")
    file.close()
    await bot.send_document(chat_id=msg.chat.id, document='report.txt', reply_to_message_id=msg.id)
    os.remove('report.txt')


@Client.on_message(filters.private & filters.user(Config.SUDO) & filters.command('msgreport'))
async def handle_report(bot: Client, cmd: Message):
    
    CHOICE = [
        [("A_1"), ("A_2")], [("A_3"), ("A_4")], [("A_5"), ("A_6")], [("A_7"), ("A_8")], [("A_9"), ("A_0")]
    ]

    await bot.send_message(chat_id=cmd.from_user.id, text=Txt.REPORT_CHOICE, reply_to_message_id=cmd.id, reply_markup=ReplyKeyboardMarkup(CHOICE, resize_keyboard=True))


@Client.on_message(filters.regex("A_1"))
async def one(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 1)


@Client.on_message(filters.regex("A_2"))
async def two(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 2)


@Client.on_message(filters.regex("A_3"))
async def three(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 3)


@Client.on_message(filters.regex("A_4"))
async def four(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 4)


@Client.on_message(filters.regex("A_5"))
async def five(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 5)


@Client.on_message(filters.regex("A_6"))
async def six(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 6)


@Client.on_message(filters.regex("A_7"))
async def seven(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 7)


@Client.on_message(filters.regex("A_8"))
async def eight(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 8)


@Client.on_message(filters.regex("A_9"))
async def nine(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 9)


@Client.on_message(filters.regex("A_0"))
async def ten(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 10)


