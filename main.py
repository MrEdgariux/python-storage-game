from classes.vartotojo import Vartotojas, WindowsHelloEncryptor
from classes.failai import Failas
from classes.klaidos import *
from classes.zaidimas import init
from classes.funkcijos import bytes_to_human_readable
from random import randint, random
from datetime import datetime
import os, json

def hr():
    term_size = os.get_terminal_size()
    os.system('cls')
    print('━' * term_size.columns)

def main():
    vartotojas = Vartotojas()
    parduotuve, serveriai = init()
    aukso_kaina = 25
    print("Sveikas atvykęs į žaidimą!")
    print("Šis žaidimas dar nėra baigtas kurti bei yra tik kūrybos stadijoje, todėl tikėkites sutikti žaidimo klaidų")
    print()
    print(f"Žaidimo versija: {vartotojas.game_version}")

    while True:
        print('━' * os.get_terminal_size().columns)
        print()
        print("Vartotojas:")
        print(f"Pinigai: {vartotojas.money} €")
        print(f"Aukso kiekis: {vartotojas.gold}")
        print()
        print('━' * os.get_terminal_size().columns)
        print()
        print("Pasirinkimai:")
        print("1. Parduotuvė")
        print("2. Inventorius")
        print("3. Gauti pinigų")
        print("4. Keitykla")
        print("5. Serveriai")
        print("97. Išsaugoti progresą")
        print("98. Įkrauti išsaugota failą")
        print("99. Iššifruoti išsaugotą failą (Dalinimosi / Debug tikslais)")
        print("100. Išeiti")

        pasirinkimas = input("Pasirinkite veiksmą: ")

        if pasirinkimas == "1":
            hr()
            print("Pasirinkite ką norite pirkti:")
            print("1. Saugyklos medijas")
            print("2. Serverius")

            pasirinkimas = input("Pasirinkite: ")
            if pasirinkimas == "1":
                hr()
                print("Pasirinkite diskų tipą:")
                disk_types = parduotuve.get_disk_types()
                for i, disk_type in enumerate(disk_types):
                    print(f"{i + 1}. {disk_type}")
                pasirinkimas = int(input("Pasirinkite: ")) - 1
                
                pasirinktas_disko_tipas = disk_types[pasirinkimas]
                shopas = parduotuve.get_disks_by_that_type(pasirinktas_disko_tipas)
                hr()
                for i, disk in enumerate(shopas):
                    print(f"{i + 1}. {disk.disk_name} - {disk.price} €")

                pasirinkimas = input("Pasirinkite diską: ")
                hr()
                try:
                    pasirinktas_diskas = shopas[int(pasirinkimas) - 1]
                    parduotuve.purchase_disk(vartotojas, pasirinktas_diskas.disk_name)
                    print("Nupirktas!")
                except NotEnoughMoneyError as e:
                    print(f"Nepavyko nupirkti dėl pinigų trūkumo")
                except ValueError as e:
                    print(f"{e}")
            elif pasirinkimas == "2":
                hr()
                print("Pasirinkite serverį")
                for i, serveris in enumerate(serveriai):
                    print(f"{i + 1}. {serveris.server_name} - {serveris.price} €")

                pasirinkimas = input("Pasirinkite serverį: ")
                hr()
                try:
                    pasirinktas_serveris = serveriai[int(pasirinkimas) - 1]
                    pasirinktas_serveris.purchase_server(vartotojas)
                    print("Nupirktas!")
                except NotEnoughMoneyError as e:
                    print(f"Nepavyko nupirkti dėl pinigų trūkumo")
                except ValueError as e:
                    print(f"{e}")

        elif pasirinkimas == "2":
            hr()
            inventorius = vartotojas.inventory
            print("Inventorius:")
            inventorius.list_disks()
        elif pasirinkimas == "3":
            hr()
            pinigai = randint(1,5)
            aukso_sansas = randint(1, 100)
            if aukso_sansas > 75:
                auksas = random()
                print(f"Jūs radote {pinigai} € ir {auksas} aukso!")
                vartotojas.money += pinigai
                vartotojas.gold += auksas
            else:
                print(f"Jūs radote {pinigai} €!")
                vartotojas.money += pinigai
        elif pasirinkimas == "4":
            hr()
            if vartotojas.gold > 0:
                print(f"Jūs turite {vartotojas.gold} aukso bei aukso kaina dabar yra {aukso_kaina}! Norite jį parduoti?")
                pasirinkimas = input("Taip/Ne: ")
                if pasirinkimas.lower() == "taip":
                    try:
                        kiekis = float(input("Kiek aukso norite parduoti? "))
                    except ValueError:
                        print("Neteisingas skaičius gaidy")
                        continue
                    if kiekis > vartotojas.gold:
                        print("Neturite tiek aukso, eik į darbą")
                    else:
                        vartotojas.money += kiekis * aukso_kaina
                        vartotojas.gold -= kiekis
                    print("Parduota!")
                else:
                    print("Gerai, nenori tai pizdink iš čia ožy")
            else:
                print("Pirmiausiai nueik į darbą ir iškask aukso su rankom prieš einant į keitykla!")
        elif pasirinkimas == "5":
            hr()
            if len(vartotojas.serveriai.servers) > 0:
                print("Jūs turite šiuos serverius:")
                for i, serveris in enumerate(vartotojas.serveriai.servers):
                    print(f"{i + 1}. {serveris.server_name} - {bytes_to_human_readable(serveris.get_total_server_storage_size())} ({len(serveris.mounted_disks)} / {serveris.max_disk_slots} disko vietų išnaudota)")

                pasirinkimas = input("Pasirinkite serverį: ")
                try:
                    pasirinktas_serveris = vartotojas.serveriai.servers[int(pasirinkimas) - 1]
                    while True:
                        hr()
                        print(f"Serverio {pasirinktas_serveris.server_name} duomenys:")
                        print(f"Serverio ID: {pasirinktas_serveris.server_id}")
                        print(f"Serverio pavadinimas: {pasirinktas_serveris.server_name}")
                        print(f"Serverio disko vietų skaičius: {pasirinktas_serveris.max_disk_slots}")
                        print(f"Serverio kaina: {pasirinktas_serveris.price}")
                        print(f"Serverio disku informacija:")
                        for i, diskas in enumerate(pasirinktas_serveris.mounted_disks):
                            print(f"{i + 1}. {diskas.disk_name} - ( {bytes_to_human_readable(diskas.used_size)} / {bytes_to_human_readable(diskas.size)} )")
                        print()
                        print("Pasirinkite veiksmą:")
                        print("1. Diskų tvarkymas")
                        print("2. Failų tvarkymas")
                        print("3. Serverio tvarkymas")
                        print("100. Išeiti iš serverio")

                        pasirinkimas = input("Pasirinkite: ")
                        
                        if pasirinkimas == "1":
                            hr()
                            print("Pasirinkite veiksmą:")
                            print("1. Prijungti diską")
                            print("2. Atjungti diską")

                            pasirinkimas = input("Pasirinkite: ")
                            if pasirinkimas == "1":
                                hr()
                                if len(vartotojas.inventory.disks) == 0:
                                    print("Jūs neturite diskų inventoriuje kurios galėtumėte prijungti")
                                    continue
                                print("Jūsų turimi diskai inventoriuje:")
                                for i, diskas in enumerate(vartotojas.inventory.disks):
                                    print(f"{i + 1}. {diskas.disk_name} - {bytes_to_human_readable(diskas.size)}")

                                pasirinkimas = input("Pasirinkite diską: ")
                                try:
                                    if (int(pasirinkimas) - 1) < 0 or (int(pasirinkimas) - 1) > len(vartotojas.inventory.disks):
                                        print("Toks diskas neegzistuoja")
                                        continue
                                    pasirinktas_diskas = vartotojas.inventory.disks[int(pasirinkimas) - 1]
                                    pasirinktas_serveris.mount_disk(pasirinktas_diskas)
                                    print("Diskas prijungtas sekmingai!")
                                except ValueError as e:
                                    print(f"{e}")
                            elif pasirinkimas == "2":
                                hr()
                                print("Pasirinkite diską:")
                                for i, diskas in enumerate(pasirinktas_serveris.mounted_disks):
                                    print(f"{i + 1}. {diskas.disk_name} - {bytes_to_human_readable(diskas.size)}")

                                pasirinkimas = input("Pasirinkite diską: ")
                                try:
                                    if (int(pasirinkimas) - 1) < 0 or (int(pasirinkimas) - 1) > len(pasirinktas_serveris.mounted_disks):
                                        print("Toks diskas neegzistuoja")
                                        continue
                                    pasirinktas_diskas = pasirinktas_serveris.mounted_disks[int(pasirinkimas) - 1]
                                    pasirinktas_serveris.unmount_disk(pasirinktas_diskas.disk_name)
                                    print("Diskas atjungtas!")
                                except ValueError as e:
                                    print(f"{e}")
                        elif pasirinkimas == "2":
                            hr()
                            print("Pasirinkite diską kuriam norite tvarkyti failus:")
                            for i, diskas in enumerate(pasirinktas_serveris.mounted_disks):
                                print(f"{i + 1}. {diskas.disk_name} - {bytes_to_human_readable(diskas.size)}")

                            pasirinkimas = input("Pasirinkite diską: ")
                            try:
                                if (int(pasirinkimas) - 1) < 0 or (int(pasirinkimas) - 1) > len(pasirinktas_serveris.mounted_disks):
                                    print("Toks diskas neegzistuoja")
                                    continue
                                pasirinktas_diskas = pasirinktas_serveris.mounted_disks[int(pasirinkimas) - 1]
                                while True:
                                    hr()
                                    print("Pasirinkite veiksmą:")
                                    print("1. Sukurti failą")
                                    print("2. Redaguoti failą")
                                    print("3. Perskaityti failą")
                                    print("4. Ištrinti failą")
                                    print("5. Perkelti failą į kitą serverį")
                                    print("6. Perkelti failą į kitą diską")
                                    print("7. Peržiūrėti failų sąrašą")
                                    print("8. Aplankalų tvarkymas")
                                    print("100. Išeiti iš failų tvarkymo")

                                    pasirinkimas = input("Pasirinkite: ")
                                    if pasirinkimas == "1":
                                        hr()
                                        print("Įveskite failo pavadinimą:")
                                        failo_pavadinimas = input("Pavadinimas: ")
                                        print("Įveskite failo turinį:")
                                        failo_turinys = input("Turinys:\n")
                                        failas = Failas(failo_pavadinimas, failo_turinys)
                                        try:
                                            pasirinktas_diskas.add_file(failas)
                                            print("Failas sukurtas!")
                                        except DiskFullError:
                                            print("Šis diskas yra pilnas, dėja...")
                                        except FileDublicateError:
                                            print("Toks failas jau egzistuoja!")
                                        except ValueError as e:
                                            print(f"{e}")
                                    elif pasirinkimas == "2":
                                        hr()
                                        print("Pasirinkite failą:")
                                        for i, failas in enumerate(pasirinktas_diskas.files):
                                            print(f"{i + 1}. {failas.name}")

                                        pasirinkimas = input("Pasirinkite failą: ")
                                        try:
                                            if (int(pasirinkimas) - 1) < 0 or (int(pasirinkimas) - 1) > len(pasirinktas_diskas.files):
                                                print("Toks failas neegzistuoja")
                                                continue
                                            pasirinktas_failas = pasirinktas_diskas.files[int(pasirinkimas) - 1]
                                            print("Įveskite naują turinį:")
                                            naujas_turinys = input("Turinys: ")
                                            pasirinktas_failas.write(naujas_turinys)
                                            pasirinktas_diskas.overwrite_file(pasirinktas_failas)
                                            print("Failas paredaguotas sekmingai!")
                                        except ValueError as e:
                                            print(f"{e}")
                                    elif pasirinkimas == "3":
                                        hr()
                                        print("Pasirinkite failą:")
                                        for i, failas in enumerate(pasirinktas_diskas.files):
                                            print(f"{i + 1}. {failas.file_name}")

                                        pasirinkimas = input("Pasirinkite failą: ")
                                        try:
                                            if (int(pasirinkimas) - 1) < 0 or (int(pasirinkimas) - 1) > len(pasirinktas_diskas.files):
                                                print("Toks failas neegzistuoja")
                                                continue
                                            hr()
                                            pasirinktas_failas = pasirinktas_diskas.files[int(pasirinkimas) - 1]
                                            print(pasirinktas_failas.read())
                                        except ValueError as e:
                                            print(f"{e}")
                                    elif pasirinkimas == "4":
                                        hr()
                                        print("Pasirinkite failą:")
                                        for i, failas in enumerate(pasirinktas_diskas.files):
                                            print(f"{i + 1}. {failas.file_name}")

                                        pasirinkimas = input("Pasirinkite failą: ")
                                        try:
                                            if (int(pasirinkimas) - 1) < 0 or (int(pasirinkimas) - 1) > len(pasirinktas_diskas.files):
                                                print("Toks failas neegzistuoja")
                                                continue
                                            pasirinktas_failas = pasirinktas_diskas.files[int(pasirinkimas) - 1]
                                            if pasirinktas_diskas.file_exists(pasirinktas_failas.file_name):
                                                pasirinktas_diskas.delete_file(pasirinktas_failas.file_name)
                                                print("Failas ištrintas!")
                                            else:
                                                print("Toks failas neegzistuoja")
                                        except ValueError as e:
                                            print(f"{e}")
                                    elif pasirinkimas == "5":
                                        hr()
                                        print("Pasirinkite serverį:")
                                        for i, serveris in enumerate(vartotojas.serveriai.servers):
                                            print(f"{i + 1}. {serveris.server_name}")

                                        pasirinkimas = input("Pasirinkite serverį: ")
                                        try:
                                            if (int(pasirinkimas) - 1) < 0 or (int(pasirinkimas) - 1) > len(vartotojas.serveriai.servers):
                                                print("Toks serveris neegzistuoja")
                                                continue
                                            pasirinktas_serveris_2 = vartotojas.serveriai.servers[int(pasirinkimas) - 1]
                                            print("Pasirinkite diską:")
                                            for i, diskas in enumerate(pasirinktas_serveris_2.mounted_disks):
                                                print(f"{i + 1}. {diskas.disk_name}")

                                            pasirinkimas = input("Pasirinkite diską: ")
                                            try:
                                                if (int(pasirinkimas) - 1) < 0 or (int(pasirinkimas) - 1) > len(pasirinktas_serveris_2.mounted_disks):
                                                    print("Toks diskas neegzistuoja")
                                                    continue
                                                pasirinktas_diskas_2 = pasirinktas_serveris_2.mounted_disks[int(pasirinkimas) - 1]
                                                print("Pasirinkite failą kurį perkelsite:")
                                                for i, failas in enumerate(pasirinktas_diskas.files):
                                                    print(f"{i + 1}. {failas.file_name}")

                                                pasirinkimas = input("Pasirinkite failą: ")
                                                try:
                                                    pasirinktas_failas = pasirinktas_diskas.files[int(pasirinkimas) - 1]
                                                    pasirinktas_diskas_2.add_file(pasirinktas_failas)
                                                    pasirinktas_diskas.delete_file(pasirinktas_failas.file_name)
                                                    print("Failas perkeltas sekmingai!")
                                                except DiskFullError:
                                                    print("Diskas yra pilnas į kurį failą jūs perkelinėjate, dėja...")
                                                except FileDublicateError:
                                                    print("Toks failas jau egzistuoja diske į kurį perkeliate failą!")
                                                except ValueError as e:
                                                    print(f"{e}")
                                            except ValueError as e:
                                                print(f"{e}")
                                        except ValueError as e:
                                            print(f"{e}")
                                    elif pasirinkimas == "6":
                                        hr()
                                        print("Pasirinkite diską:")
                                        for i, diskas in enumerate(pasirinktas_serveris.mounted_disks):
                                            print(f"{i + 1}. {diskas.disk_name}")

                                        pasirinkimas = input("Pasirinkite diską: ")
                                        try:
                                            if (int(pasirinkimas) - 1) < 0 or (int(pasirinkimas) - 1) > len(pasirinktas_serveris.mounted_disks):
                                                print("Toks diskas neegzistuoja")
                                                continue
                                            pasirinktas_diskas_2 = pasirinktas_serveris.mounted_disks[int(pasirinkimas) - 1]
                                            print("Pasirinkite failą kurį perkelsite:")
                                            for i, failas in enumerate(pasirinktas_diskas.files):
                                                print(f"{i + 1}. {failas.file_name}")

                                            pasirinkimas = input("Pasirinkite failą: ")
                                            try:
                                                if (int(pasirinkimas) - 1) < 0 or (int(pasirinkimas) - 1) > len(pasirinktas_diskas.files):
                                                    print("Toks failas neegzistuoja")
                                                    continue
                                                pasirinktas_failas = pasirinktas_diskas.files[int(pasirinkimas) - 1]
                                                pasirinktas_diskas_2.add_file(pasirinktas_failas)
                                                pasirinktas_diskas.delete_file(pasirinktas_failas.file_name)
                                                print("Failas perkeltas sekmingai!")
                                            except DiskFullError:
                                                print("Diskas yra pilnas į kurį failą jūs perkelinėjate, dėja...")
                                            except FileDublicateError:
                                                print("Toks failas jau egzistuoja diske į kurį perkeliate failą!")
                                            except ValueError as e:
                                                print(f"{e}")
                                        except ValueError as e:
                                            print(f"{e}")
                                    elif pasirinkimas == "7":
                                        hr()
                                        print(f"Serverio {pasirinktas_serveris.server_name} bei disko {pasirinktas_diskas.disk_name} failai:")
                                        pasirinktas_diskas.list_files()
                                    elif pasirinkimas == "8":
                                        print("Will be implemented in the future")
                                    elif pasirinkimas == "100":
                                        break
                                    else:
                                        print("Neteisingas pasirinkimas")
                            except ValueError as e:
                                print(f"{e}")
                        elif pasirinkimas == "3":
                            hr()
                            print("Pasirinkite veiksmą:")
                            print("1. Pakeisti serverio pavadinimą")
                            print("2. Ištrinti serverį")

                            pasirinkimas = input("Pasirinkite: ")
                            if pasirinkimas == "1":
                                hr()
                                naujas_pavadinimas = input("Įveskite naują pavadinimą: ")
                                pasirinktas_serveris.server_name = naujas_pavadinimas
                                print("Pavadinimas pakeistas sekmingai!")
                            elif pasirinkimas == "2":
                                hr()
                                vartotojas.serveriai.remove_server(pasirinktas_serveris.server_id)
                                print("Serveris ištrintas sekmingai!")
                            else:
                                print("Neteisingas pasirinkimas")
                        elif pasirinkimas == "100":
                            break
                        else:
                            print("Neteisingas pasirinkimas")
                except ValueError as e:
                    print(f"{e}")
            else:
                print("Jūs neturite serverių")

        elif pasirinkimas == "97":
            hr()
            try:
                vartotojas.save()
                print("Išsaugota!")
            except Exception as e:
                print(f"Klaida išsaugant: {e}")
        elif pasirinkimas == "98":
            hr()
            save_files = [f for f in os.listdir("saves") if f.endswith('.dat')]
            save_files.sort(key=lambda x: os.path.getctime(os.path.join("saves", x)))
            print("Pasirinkite išsaugotą failą:")
            for i, file in enumerate(save_files):
                print(f"{i + 1}. {file} - {datetime.fromtimestamp(os.path.getctime(os.path.join('saves', file)))}")
            pasirinkimas = int(input("Pasirinkite: ")) - 1
            try:
                vartotojas.load(f"saves/{save_files[pasirinkimas]}")
                print("Įkrauta!")
            except SaveVersionDismatch:
                print("Dėja, tačiau šis išsaugotas failas yra senesnės versijos ir nebegali būti įkrautas :(")
            except SaveFileDecryptionError:
                print("Dėja, tačiau jūs negalite pasiekti šio failo, jis buvo užšifruotas kito vartotojo :(")
            except Exception as e:
                print("Nepavyko įkrauti :(")
                print(f"Klaida: {e}")
        elif pasirinkimas == "99":
            hr()
            save_files = [f for f in os.listdir("saves") if f.endswith('.dat')]
            save_files.sort(key=lambda x: os.path.getctime(os.path.join("saves", x)))
            print("Pasirinkite išsaugotą failą:")
            for i, file in enumerate(save_files):
                print(f"{i + 1}. {file} - {datetime.fromtimestamp(os.path.getctime(os.path.join('saves', file)))}")
            pasirinkimas = int(input("Pasirinkite: ")) - 1
            try:
                data = WindowsHelloEncryptor.decrypt_save(f"saves/{save_files[pasirinkimas]}")
                with open(f"saves/decrypted_{save_files[pasirinkimas]}.json", "w") as f:
                    json.dump(data, f, indent=4)
                print("Failas iššifruotas sekmingai!")
            except Exception as e:
                print(f"Klaida: {e}")
        elif pasirinkimas == "100":
            os.system("cls")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma sustabdoma")
        exit()
    except Exception as e:
        print(f"Programos klaida: {e}")
        exit()