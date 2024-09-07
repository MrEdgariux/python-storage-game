from classes.saugyklos import Inventory, NAS
from classes.klaidos import SaveVersionDismatch, SaveFileDecryptionError
from uuid import uuid4
from os import makedirs
from classes.encryptions import WindowsHelloEncryptor

current_save_version = "1.0.0"
current_game_version = "2.0.0"

class Vartotojas():
    def __init__(self):
        self.save_id = str(uuid4())
        self.money = 0
        self.gold = 0
        self.game_version = current_game_version
        self.inventory = Inventory()
        self.serveriai = NAS()

    def add_money(self, amount):
        self.money += amount

    def add_gold(self, amount):
        self.gold += amount

    def save(self):
        data = {
            "save_id": self.save_id,
            "save_version": current_save_version,
            "game_version": self.game_version,
            "money": self.money,
            "gold": self.gold,
            "inventory": self.inventory.__dict__(),
            "serveriai": self.serveriai.__dict__()
        }

        makedirs("saves", exist_ok=True)
        
        WindowsHelloEncryptor.encrypt_save(data, f"saves/{self.save_id}.dat")
        
    def load(self, file_path):
        try:
            data = WindowsHelloEncryptor.decrypt_save(file_path)
        except Exception as e:
            raise SaveFileDecryptionError(e)

        if "save_id" not in data:
            raise ValueError("Neteisingas save failas")
        elif "inventory" not in data or "serveriai" not in data:
            raise ValueError("Sugadintas išsaugotas failas. Trūksta reikiamų duomenų")
        elif "save_version" not in data or data["save_version"] != current_save_version:
            raise SaveVersionDismatch("Sugadintas išsaugotas failas. Netinkama versija")
        elif "game_version" not in data or data["game_version"] != current_game_version:
            print("[WARNING] Ši išsaugota versija gali būti neveikianti su naujesnėmis versijomis!")
        self.save_id = data["save_id"]
        self.save_version = data["save_version"]
        if "game_version" in data:
            self.game_version = data["game_version"]
        else:
            self.game_version = current_game_version
        self.money = data["money"]
        self.gold = data["gold"]
        self.inventory = self.inventory.from_dict(data["inventory"])
        self.serveriai = self.serveriai.from_dict(data["serveriai"])