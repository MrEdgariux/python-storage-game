import unittest
from classes.vartotojo import Vartotojas
from classes.encryptions import WindowsHelloEncryptor
from classes.saugyklos import Inventory, Diskas, NAS
from classes.failai import Failas
from classes.zaidimas import bytes_to_human_readable
import os

class TestVartotojas(unittest.TestCase):
    def setUp(self):
        self.vartotojas = Vartotojas()

    def test_initialization(self):
        self.assertIsInstance(self.vartotojas.inventory, Inventory)
        self.assertIsInstance(self.vartotojas.serveriai, NAS)
        self.assertEqual(self.vartotojas.money, 0)
        self.assertEqual(self.vartotojas.gold, 0)

    def test_add_money(self):
        self.vartotojas.add_money(100)
        self.assertEqual(self.vartotojas.money, 100)

    def test_add_gold(self):
        self.vartotojas.add_gold(50)
        self.assertEqual(self.vartotojas.gold, 50)

    def test_save_and_load(self):
        self.vartotojas.add_money(100)
        self.vartotojas.add_gold(50)
        self.vartotojas.save()
        save_path = f"saves/{self.vartotojas.save_id}.dat"
        self.assertTrue(os.path.exists(save_path))

        new_vartotojas = Vartotojas()
        new_vartotojas.load(save_path)
        self.assertEqual(new_vartotojas.money, 100)
        self.assertEqual(new_vartotojas.gold, 50)
        os.remove(save_path)

class TestWindowsHelloEncryptor(unittest.TestCase):
    def test_encrypt_decrypt(self):
        data = {"test": "data"}
        save_path = "test.dat"
        WindowsHelloEncryptor.encrypt_save(data, save_path)
        self.assertTrue(os.path.exists(save_path))

        decrypted_data = WindowsHelloEncryptor.decrypt_save(save_path)
        self.assertEqual(data, decrypted_data)
        os.remove(save_path)

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.disk = Diskas("TestDisk", 1024, 10)

    def test_add_disk(self):
        self.inventory.add_disk(self.disk)
        self.assertIn(self.disk, self.inventory.disks)

    def test_list_disks(self):
        self.inventory.add_disk(self.disk)
        self.inventory.list_disks()

    def test_remove_disk(self):
        self.inventory.add_disk(self.disk)
        removed_disk = self.inventory.remove_disk("TestDisk")
        self.assertEqual(removed_disk, self.disk)
        self.assertNotIn(self.disk, self.inventory.disks)

class TestDiskas(unittest.TestCase):
    def setUp(self):
        self.disk = Diskas("TestDisk", 1024, 10)
        self.file = Failas("TestFile", b"content")

    def test_add_file(self):
        self.disk.add_file(self.file)
        self.assertIn(self.file, self.disk.files)

    def test_overwrite_file(self):
        self.disk.add_file(self.file)
        new_file = Failas("TestFile", b"new content")
        self.disk.overwrite_file(new_file)
        self.assertEqual(self.disk.files[0].content, b"new content")

    def test_delete_file(self):
        self.disk.add_file(self.file)
        self.disk.delete_file("TestFile")
        self.assertNotIn(self.file, self.disk.files)

    def test_list_files(self):
        self.disk.add_file(self.file)
        self.disk.list_files()

    def test_size_management(self):
        self.disk.add_file(self.file)
        self.assertEqual(self.disk.used_size, len(self.file.content))
        self.disk.delete_file("TestFile")
        self.assertEqual(self.disk.used_size, 0)

class TestNAS(unittest.TestCase):
    def setUp(self):
        self.nas = NAS()
        self.disk = Diskas("TestDisk", 1024, 10)

    def test_mount_disk(self):
        self.nas.mount_disk(self.disk)
        self.assertIn(self.disk, self.nas.mounted_disks)

    def test_unmount_disk(self):
        self.nas.mount_disk(self.disk)
        unmounted_disk = self.nas.unmount_disk("TestDisk")
        self.assertEqual(unmounted_disk, self.disk)
        self.assertNotIn(self.disk, self.nas.mounted_disks)

    def test_list_mounted_disks(self):
        self.nas.mount_disk(self.disk)
        self.nas.list_mounted_disks()

class TestFailas(unittest.TestCase):
    def setUp(self):
        self.file = Failas("TestFile", b"content")

    def test_read(self):
        self.assertEqual(self.file.read(), b"content")

    def test_write(self):
        self.file.write(b"new content")
        self.assertEqual(self.file.read(), b"new content")

    def test_to_from_dict(self):
        file_dict = self.file.__dict__()
        new_file = Failas.from_dict(file_dict)
        self.assertEqual(new_file.name, self.file.name)
        self.assertEqual(new_file.content, self.file.content)

class TestBytesToHumanReadable(unittest.TestCase):
    def test_conversion(self):
        self.assertEqual(bytes_to_human_readable(1024), "1.00 KB")
        self.assertEqual(bytes_to_human_readable(1048576), "1.00 MB")

if __name__ == "__main__":
    unittest.main()