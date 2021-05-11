from trello_client import TrelloClient
from trello_helper import TrelloHelper
from telegram_client import TelegramClient
from telegram_helper import TelegramHelper
from datetime import datetime, date


def get_settings(file_name):
    settings = {}
    f = open(f"settings/{file_name}", 'r')
    try:
        line = f.readline().rstrip("\n")
        while line:
            name, value = line.split("=")
            settings[name] = value
            line = f.readline().rstrip("\n")
        return settings
    finally:
        f.close()
        return settings


def update_last_update(setting_name):
    new_date = date.today()
    with open("last_update") as last:
        settings = last.readlines()

    for i in range(len(settings)):
        if setting_name in settings[i]:
            settings[i] = setting_name + "=" + new_date.strftime("%Y-%m-%d") + "\n"

    with open("last_update", "w") as last:
        last.writelines(settings)


def get_last(setting_name):
    with open("last_update") as last:
        settings = last.readlines()

    for i in range(len(settings)):
        if setting_name in settings[i]:
            str_date = settings[i].split("=")[-1].rstrip("\n")
            last_datetime = datetime.strptime(str_date, "%Y-%m-%d")
            return last_datetime.date()


def main():
    print("Start trellolo bot")

    print("Start to read settings from tg file")
    telegram = get_settings("telegram")
    print("End to read settings from tg file")

    print("Start to read settings from trello file")
    trello = get_settings("trello")
    print("End to read settings from trello file")

    trello_client = TrelloClient(trello["KEY"], trello["TOKEN"], trello["BOARD_ID"])
    trello_helper = TrelloHelper(trello_client)
    telegram_client = TelegramClient(telegram["TOKEN"], telegram["CHAT_ID"])
    telegram_helper = TelegramHelper(telegram_client)

    while True:
        print(f"Start to get updates from chat")
        updates = telegram_helper.get_updated_cards()
        print(f"Count of updated cards is {len(updates)}")
        print(f"update: {updates[0].card_id} status: {updates[0].status}")

        telegram_messages = trello_helper.get_messages_for_chat()
        print(f"Count of new messages is {len(telegram_messages)}")
        telegram_helper.send_all_messages(telegram_messages)
        print(f"Messages was send in chat")

        break


if __name__ == '__main__':
    main()
