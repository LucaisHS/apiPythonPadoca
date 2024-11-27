class DateFormatterDTO:
    def __init__(self, min_age, max_age, count):
        self.min_age = min_age
        self.max_age = max_age
        self.count = count

    def to_dict(self):
        return {
            'minAge': self.min_age,
            'maxAge': self.max_age,
            'userCount': self.count
        }