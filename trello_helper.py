from trello_card import TrelloCard


class MessageData:
    def __init__(self, text, params):
        self.text = text
        self.params = params


class TrelloHelper:
    def __init__(self, trello_client):
        self.client = trello_client

    def get_messages_for_chat(self):
        all_cards = self.client.get_all_trello_cards()
        all_cards = [TrelloCard(card) for card in all_cards]

        deadline = get_cards_with_deadline(all_cards)
        notice = get_cards_with_notification(all_cards)

        messages = []
        for card in notice:
            messages.append(get_message_for_telegram_notification(card))
        for card in deadline:
            messages.append(get_message_for_telegram_deadline(card))
        return messages


def get_message_for_telegram_notification(card):
    text = "Напоминание: " + str(card.due) + "\n" + card.name
    params = {}
    return MessageData(text, params)


def get_message_for_telegram_deadline(card):
    text = "Сегодня!\n" + card.name
    params = {
            "inline_keyboard": [[
            {
                "text": "done",
                "callback_data": f"done {card.id}"
            },
            {
                "text": "tomorrow",
                "callback_data": f"tomorrow {card.id}"
            }]
        ]}
    return MessageData(text, params)


def get_cards_with_notification(cards):
    cards_note = []
    for card in cards:
        if card.is_notification_today():
            cards_note.append(card)
    return cards_note


def get_cards_with_deadline(cards):
    cards_deadline = []
    for card in cards:
        if card.is_deadline_today():
            cards_deadline.append(card)
    return cards_deadline
