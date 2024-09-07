from classes.saugyklos import Diskas, Inventory
from classes.vartotojo import Vartotojas
from classes.klaidos import NotEnoughMoneyError
class Shop():
    def __init__(self):
        self.inventory = []

    def add_item(self, item):
        if isinstance(item, Diskas):
            self.inventory.append(item)

    def find_disk(self, disk_name):
        for disk in self.inventory:
            if disk.disk_name == disk_name:
                return disk
        raise ValueError("Diskas nerastas parduotuvėje")
    
    def get_disks_by_that_type(self, type):
        disks_by_type = []
        for disk in self.inventory:
            if not isinstance(disk, Diskas):
                print("Netinkamas formatas daiktu wtf")
                continue
            if disk.disk_name.startswith(type):
                disks_by_type.append(disk)
        return disks_by_type
    
    def get_disk_types(self):
        disk_types = []
        for disk in self.inventory:
            if not isinstance(disk, Diskas):
                print("Netinkamas formatas daiktu wtf")
                continue
            disk_type = disk.disk_name.split()[0]
            if disk_type not in disk_types:
                disk_types.append(disk_type)
        return disk_types
        
    def list_items(self):
        for item in self.inventory:
            print(f" - {item.disk_name} - {item.price} €")

    def purchase_disk(self, user, disk_name):
        disk = self.find_disk(disk_name)
        if not isinstance(user, Vartotojas):
            raise ValueError("User turi būti Vartotojas klasės objektas")
        inventorius = user.inventory
        if not isinstance(inventorius, Inventory):
            raise ValueError("Inventorius turi būti Inventory klasės objektas")
        if user.money >= disk.price:
            user.money -= disk.price
            inventorius.add_disk(disk)
        else:
            raise NotEnoughMoneyError("Jūs neturite tiek bapkiu gaidy")