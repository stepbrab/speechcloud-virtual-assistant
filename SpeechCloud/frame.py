class CalendarEventFrame:
    def __init__(self):
        self.event_type = None
        self.date_day = None
        self.date_month = None
        self.date_year = None
        self.time_start = None
        self.time_end = None
        self.complete = False
        
class ShoppingListFrame:
    def __init__(self):
        self.items = []
        self.complete = False
        
class ShoppingItemFrame:
    def __init__(self):
        self.name = None
        self.amount = None
        self.complete = False
        