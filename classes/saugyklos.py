from classes.failai import Failas
from classes.klaidos import *
from classes.funkcijos import bytes_to_human_readable
from uuid import uuid4
from random import randint

class Inventory():
    def __init__(self):
        self.disks = []
    
    def add_disk(self, disk):
        if isinstance(disk, Diskas):
            disk.disk_id = str(uuid4()) # Generate unique disk id for each disk
            self.disks.append(disk)
        else:
            raise ValueError("Diskas turi būti 'Diskas' klasės objektas")

    def list_disks(self):
        for disk in self.disks:
            print(disk)

    def remove_disk(self, disk):
        if isinstance(disk, Diskas):
            self.disks.remove(disk)
            return
        elif isinstance(disk, str):
            for d in self.disks:
                if d.disk_id == disk:
                    self.disks.remove(d)
                    return
        raise ValueError("Diskas nerastas arba formatas netinkamas")
    
    def format_disk(self, disk):
        if isinstance(disk, Diskas):
            disk.files = []
            disk.used_size = 0
            return
        elif isinstance(disk, str):
            for d in self.disks:
                if d.disk_id == disk:
                    d.files = []
                    d.used_size = 0
                    return
        raise ValueError("Diskas nerastas arba formatas netinkamas")
    
    def __dict__(self):
        return {
            "disks": [disk.__dict__() for disk in self.disks]
        }
    
    def from_dict(self, data):
        self.disks = [Diskas.from_dict(disk_data) for disk_data in data["disks"]]
        return self

class Diskas():
    def __init__(self, pavadinimas, talpa, price):
        self.disk_id = str(uuid4())
        self.disk_name = pavadinimas
        self.price = price
        self.size = talpa # In bytes
        self.used_size = 0
        self.files = []

    def add_file(self, file):
        if isinstance(file, Failas):
            if self.size - self.used_size < file.file_size:
                raise DiskFullError("Diskas pilnas ir negali išsaugoti daugiau informacijos")
            if self.file_exists(file.name):
                raise FileDublicateError("Toks failas su tokiu pavadinimu jau egzistuoja šioje vietoje")
            self.files.append(file)
            self.increase_size(file.file_size)
        else:
            raise ValueError("Failas turi būti 'Failas' klasės objektas")
        
    def file_exists(self, file_name):
        for file in self.files:
            if file.name == file_name:
                return True
        return False
    
    def overwrite_file(self, file):
        if isinstance(file, Failas):
            for f in self.files:
                if f.name == file.name:
                    self.decrease_size(f.file_size)
                    self.increase_size(file.file_size)
                    f.content = file.content
                    f.file_size = file.file_size
                    f.last_modified = file.last_modified
                    return
            raise ValueError("Toks failas neegzistuoja")
        else:
            raise ValueError("Failas turi būti 'Failas' klasės objektas")
        
    def delete_file(self, file):
        if isinstance(file, Failas):
            if file in self.files:
                self.decrease_size(file.file_size)
                self.files.remove(file)
                return
        elif isinstance(file, str):
            for f in self.files:
                if f.name == file:
                    self.decrease_size(f.file_size)
                    self.files.remove(f)
                    return
        raise ValueError("Toks failas neegzistuoja")
    
    def list_files(self):
        for file in self.files:
            print(file.name)
        
    def increase_size(self, size):
        if self.size - self.used_size < size:
            raise DiskFullError("Diskas pilnas ir negali išsaugoti daugiau informacijos")
        self.used_size += size

    def decrease_size(self, size):
        self.used_size -= size
        if self.used_size < 0:
            self.used_size = 0

    def __str__(self):
        size = bytes_to_human_readable(self.size)
        used_size = bytes_to_human_readable(self.used_size)
        left_size = bytes_to_human_readable(self.size - self.used_size)
        return f"{self.disk_id} - {self.disk_name} - {used_size} / {size} ({left_size} free)"
    
    def __dict__(self):
        return {
            "disk_id": self.disk_id,
            "disk_name": self.disk_name,
            "price": self.price,
            "size": self.size,
            "used_size": self.used_size,
            "files": [file.__dict__() for file in self.files]
        }
    
    @classmethod
    def from_dict(cls, data):
        disk = cls(data["disk_name"], data["size"], data["price"])
        disk.disk_id = data["disk_id"]
        disk.used_size = data["used_size"]
        disk.files = [Failas.from_dict(file_data) for file_data in data["files"]]
        return disk
    
class Serveris():
    def __init__(self, server_name, max_disk, price):
        self.server_id = str(uuid4())
        self.server_name = server_name
        self.mounted_disks = []
        self.max_disk_slots = max_disk
        self.price = price

    def mount_disk(self, disk):
        if len(self.mounted_disks) >= self.max_disk_slots:
            raise ServerNoEmptyDiskSlots("Serveris turi maksimalų diskų skaičių")
        if isinstance(disk, Diskas):
            if disk in self.mounted_disks:
                raise ServerDiskAlreadyMounted("Diskas jau prijungtas")
            self.mounted_disks.append(disk)
        else:
            raise ValueError("Diskas turi būti 'Diskas' klasės objektas")
        
    def unmount_disk(self, disk):
        if isinstance(disk, Diskas):
            self.mounted_disks.remove(disk)
            return
        elif isinstance(disk, str):
            for d in self.mounted_disks:
                if d.disk_id == disk:
                    self.mounted_disks.remove(d)
                    return
        raise ValueError("Diskas nerastas arba formatas netinkamas")
    
    def list_mounted_disks(self):
        for disk in self.mounted_disks:
            print(disk)

    def get_total_server_storage_size(self):
        return sum([disk.size for disk in self.mounted_disks])

    def purchase_server(self, user):
        serveriu_sarasas = user.serveriai

        if not isinstance(serveriu_sarasas, NAS):
            raise ValueError("Serveriu_sarasas turi būti NAS klasės objektas")

        if user.money >= self.price:
            user.money -= self.price
            serveriu_sarasas.add_server(self)
        else:
            raise NotEnoughMoneyError("Jūs neturite tiek šaibu gaidy")
    
    def __dict__(self):
        return {
            "server_id": self.server_id,
            "server_name": self.server_name,
            "mounted_disks": [disk.__dict__() for disk in self.mounted_disks],
            "max_disk_slots": self.max_disk_slots,
            "price": self.price
        }
    
    @classmethod
    def from_dict(cls, data):
        server = cls(data["server_name"], data["max_disk_slots"], data["price"])
        server.server_id = data["server_id"]
        server.mounted_disks = [Diskas.from_dict(disk_data) for disk_data in data["mounted_disks"]]
        return server
    
class NAS():
    def __init__(self):
        self.servers = []

    def add_server(self, server):
        if isinstance(server, Serveris):
            self.servers.append(server)
        else:
            raise ValueError("Serveris turi būti 'Serveris' klasės objektas")

    def get_server(self, server_id):
        for server in self.servers:
            if server.server_id == server_id:
                return server
        raise ValueError("Serveris nerastas")
    
    def mount_disk(self, disk):
        for server in self.servers:
            try:
                server.mount_disk(disk)
                return
            except ServerNoEmptyDiskSlots:
                pass
        raise NASNoFreeServers("Nepavyko prijungti disko")

    def list_servers(self):
        for server in self.servers:
            print(server)

    def remove_server(self, server_id):
        for server in self.servers:
            if server.server_id == server_id:
                self.servers.remove(server)
                return server
        raise ValueError("Serveris nerastas")
    
    def __dict__(self):
        return {
            "servers": [server.__dict__() for server in self.servers]
        }
    
    def from_dict(self, data):
        self.servers = [Serveris.from_dict(server_data) for server_data in data["servers"]]
        return self
