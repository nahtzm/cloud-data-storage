class Plan:
    def __init__(self, name, storage_limit, price):
        self.name = name
        self.storage_limit = storage_limit
        self.price = price

PLANS = {
    "free": Plan("Free", 1024, 0),
    "basic": Plan("Basic", 1024*30, 20000),
    "pro": Plan("Pro", 1024*100, 50000)
}