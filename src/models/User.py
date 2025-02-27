import uuid

class User():
    def __init__(self, name:str):
        print("user init")
        self.id:str = str(uuid.uuid4()) 
        self.name:str = name

    def __str__(self):
        return f"User(id: {self.id}, name: {self.name})"

