class Memory:

    def __init__(self):
        self.history = []

    def add(self, key, value):
        self.history.append({key: value})

    def get_context(self):
        return self.history