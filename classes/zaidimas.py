aukso_kaina = 0
import os
from classes.saugyklos import Diskas, Serveris
from classes.parduotuve import Shop

def init():
    if not os.path.exists("saves"):
        os.makedirs("saves")

    # Shop items
    shop = Shop()
    serveriai = []

    gb = 1024*1024*1024
    tb = 1024*1024*1024*1024

    shop.add_item(Diskas("HDD 256 GB", 256*gb, 10))
    shop.add_item(Diskas("HDD 512 GB", 512*gb, 25))
    shop.add_item(Diskas("HDD 1 TB", 1*tb, 50))
    shop.add_item(Diskas("HDD 2 TB", 2*tb, 75))
    shop.add_item(Diskas("HDD 4 TB", 4*tb, 100))
    shop.add_item(Diskas("HDD 8 TB", 8*tb, 150))
    shop.add_item(Diskas("HDD 16 TB", 16*tb, 200))

    shop.add_item(Diskas("SSD 128 GB", 128*gb, 15))
    shop.add_item(Diskas("SSD 256 GB", 256*gb, 30))
    shop.add_item(Diskas("SSD 512 GB", 512*gb, 50))
    shop.add_item(Diskas("SSD 1 TB", 1*tb, 100))
    shop.add_item(Diskas("SSD 2 TB", 2*tb, 200))
    shop.add_item(Diskas("SSD 4 TB", 4*tb, 400))

    shop.add_item(Diskas("MicroSD 1 GB", 1*gb, 2))
    shop.add_item(Diskas("MicroSD 2 GB", 2*gb, 3))
    shop.add_item(Diskas("MicroSD 4 GB", 4*gb, 6))
    shop.add_item(Diskas("MicroSD 8 GB", 8*gb, 10))
    shop.add_item(Diskas("MicroSD 16 GB", 16*gb, 20))
    shop.add_item(Diskas("MicroSD 32 GB", 32*gb, 40))
    shop.add_item(Diskas("MicroSD 64 GB", 64*gb, 80))
    shop.add_item(Diskas("MicroSD 128 GB", 128*gb, 150))

    # Servers
    serveriai.append(Serveris("Serveris XS", 1, 25))
    serveriai.append(Serveris("Serveris S", 2, 50))
    serveriai.append(Serveris("Serveris XM", 3, 75))
    serveriai.append(Serveris("Serveris M", 4, 100))
    serveriai.append(Serveris("Serveris L", 8, 200))
    serveriai.append(Serveris("Serveris XL", 10, 250))

    serveriai.append(Serveris("Serveris II XS", 12, 300))
    serveriai.append(Serveris("Serveris II S", 14, 350))
    serveriai.append(Serveris("Serveris II M", 16, 400))
    serveriai.append(Serveris("Serveris II L", 20, 600))


    return shop, serveriai