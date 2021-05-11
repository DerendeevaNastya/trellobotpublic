import trello


class TrelloClient:
    def __init__(self, key, token, boardId):
        self.boardId = boardId
        self.client = trello.TrelloApi(key, token=token)

    def get_all_trello_cards(self):
        cards = self.client.boards.get_card(self.boardId)
        return cards

    def archive_card(self, card_id):
        self.client.cards.update_closed(card_id, True)

    def due_complete_card(self, card_id):
        self.client.cards.update_dueComplete(card_id, True)

    def due_card(self, card_id, new_due):
        self.client.cards.update_due(card_id, new_due)
