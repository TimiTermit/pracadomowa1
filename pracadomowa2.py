import random

class Character:
    def __init__(self, name, hp, atak):
        self.name = name
        self.hp = hp
        self.atak = atak
        self.zyje = True

    def odejmij_hp(self, a):
        self.hp -= a
        if self.hp <= 0:
            self.zyje = False

    def czy_zyje(self):
        return self.zyje

    def basic_atak(self):
        return self.atak

    def power_strike(self):
        return self.atak * 2

    def quick_slash(self):
        return self.atak * 0.5

    def heavy_blow(self):
        return self.atak * 1.5

    def magic_blast(self):
        return self.atak * 3

class Sigma(Character):
    def __init__(self, name):
        super().__init__(name, 100, 10)

class Monster:
    def __init__(self, name, hp, atak):
        self.name = name
        self.hp = hp
        self.atak = atak
        self.zyje = True

    def odejmij_hp(self, a):
        self.hp -= a
        if self.hp <= 0:
            self.zyje = False

    def czy_zyje(self):
        return self.zyje

    def basic_atak(self):
        return self.atak

class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

class Equipment:
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense

# Przykładowe bronie
sword = Weapon("Sword", 10)
axe = Weapon("Axe", 12)
bow = Weapon("Bow", 8)
dagger = Weapon("Dagger", 6)
staff = Weapon("Staff", 9)

# Przykładowy ekwipunek
helmet = Equipment("Helmet", 5)
armor = Equipment("Armor", 15)
boots = Equipment("Boots", 3)
shield = Equipment("Shield", 10)
gloves = Equipment("Gloves", 2)

# Biomy i potwory
biomes = {
    "Forest": [
        Monster("Goblin", 20, 2),
        Monster("Orc", 30, 5),
        Monster("Troll", 50, 7),
        Monster("Wolf", 15, 3),
        Monster("Bear", 40, 6),
        Monster("Spider", 10, 2),
        Monster("Ent", 60, 8),
        Monster("Fairy", 5, 1),
        Monster("Elf", 25, 4),
        Monster("Dryad", 20, 3)
    ],
    "Desert": [
        Monster("Scorpion", 15, 3),
        Monster("Sand Worm", 50, 7),
        Monster("Mummy", 30, 5),
        Monster("Desert Bandit", 25, 4),
        Monster("Camel Spider", 10, 2),
        Monster("Sand Golem", 60, 8),
        Monster("Cactus Monster", 20, 3),
        Monster("Desert Snake", 15, 3),
        Monster("Fire Ant", 10, 2),
        Monster("Desert Ghost", 25, 4)
    ],
    "Mountain": [
        Monster("Mountain Troll", 50, 7),
        Monster("Eagle", 15, 3),
        Monster("Mountain Lion", 30, 5),
        Monster("Yeti", 60, 8),
        Monster("Rock Golem", 40, 6),
        Monster("Snow Wolf", 20, 3),
        Monster("Ice Elemental", 35, 5),
        Monster("Mountain Bandit", 25, 4),
        Monster("Griffin", 45, 7),
        Monster("Mountain Spirit", 30, 5)
    ],
    "Swamp": [
        Monster("Swamp Monster", 40, 6),
        Monster("Crocodile", 30, 5),
        Monster("Swamp Snake", 15, 3),
        Monster("Bog Witch", 25, 4),
        Monster("Swamp Troll", 50, 7),
        Monster("Leech", 10, 2),
        Monster("Swamp Ghost", 20, 3),
        Monster("Frogman", 20, 3),
        Monster("Swamp Spider", 15, 3),
        Monster("Swamp Spirit", 30, 5)
    ],
    "Cave": [
        Monster("Cave Bat", 10, 2),
        Monster("Cave Troll", 50, 7),
        Monster("Cave Spider", 15, 3),
        Monster("Cave Goblin", 20, 3),
        Monster("Cave Dragon", 60, 8),
        Monster("Cave Worm", 30, 5),
        Monster("Cave Ghost", 25, 4),
        Monster("Cave Bandit", 25, 4),
        Monster("Cave Bear", 40, 6),
        Monster("Cave Spirit", 30, 5)
    ]
}

# Wybór postaci
def wybierz_postac():
    print("Wybierz postać:")
    print("1. Sigma")
    wybor = input("Wybierz numer postaci: ")
    imie = input("Podaj imię bohatera: ")

    if wybor == "1":
        return Sigma(imie)
    else:
        print("Nieprawidłowy wybór, domyślnie wybrano Sigma.")
        return Sigma(imie)

# Wybór biomu
def wybierz_biom():
    print("Wybierz biom:")
    for i, biom in enumerate(biomes.keys(), 1):
        print(f"{i}. {biom}")
    wybor = int(input("Wybierz numer biomu: "))
    return list(biomes.keys())[wybor - 1]

# Przykładowa walka
bohater = wybierz_postac()
biom = wybierz_biom()
licznik_zabitych_potworow = 0

while bohater.czy_zyje():
    print('Walka rozpoczęta')
    potwor = random.choice(biomes[biom])
    print(f'Nowy {potwor.name} wkroczył do gry')
    while potwor.czy_zyje():
        potwor.odejmij_hp(bohater.basic_atak())
        if potwor.czy_zyje():
            bohater.odejmij_hp(potwor.basic_atak())
    licznik_zabitych_potworow += 1
    print(f'{potwor.name} zabity! Liczba zabitych potworów: {licznik_zabitych_potworow}')
    if not bohater.czy_zyje():
        print(f'{bohater.name} zginął w walce.')
        break