from datetime import datetime, date, timedelta


class CardDescSettings:
    def __init__(self, desc):
        rows = desc.split("\n")
        self.rows = rows

    def get_period(self):
        row_period = None
        for row in self.rows:
            if "Period" in row:
                row_period = row
                break

        if row_period is None:
            return None

        str_period = row_period.split()[-1]
        time_value = str_period[-1]
        count = int(str_period[:-1])

        if time_value == "y":
            return timedelta(days=365)
        if time_value == "w":
            return timedelta(days=7 * count)
        if time_value == "d":
            return timedelta(days=count)
        return None


class TrelloCard:
    def __init__(self, data):
        self.data = data

        self.name = self.data["name"]
        self.id = self.data["id"]
        self.datetime_format = "%Y-%m-%dT%H:%M:%S.000Z"
        self.due_reminder = None
        self.due = None
        self.period = None
        if "dueReminder" in self.data:
            self.due_reminder = self.data["dueReminder"]
        if "due" in self.data and self.data["due"] is not None:
            due = self.data["due"]
            self.due = datetime.strptime(due, self.datetime_format)
        if "desc" in self.data:
            self.period = CardDescSettings(self.data["desc"]).get_period()

    def is_notification_today(self):
        if self.due_reminder is None or self.due is None:
            return False

        today_end = date.today()
        notification_datetime = self.due - timedelta(minutes=self.due_reminder)
        notification_date = date(year=notification_datetime.year, month=notification_datetime.month, day=notification_datetime.day)
        if today_end == notification_date:
            return True
        return False

    def get_next_due(self):
        if self.due is None or self.period is None:
            return None

        new_due = self.due + self.period
        if self.period == timedelta(days=365):
            new_due = self.due
        return new_due.strftime(self.datetime_format)

    def is_deadline_today(self):
        if self.due is None:
            return False

        today_date = date.today()
        due_date = date(year=self.due.year, month=self.due.month, day=self.due.day)
        if today_date == due_date:
            return True
        return False
