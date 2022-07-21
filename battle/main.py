from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Create Black Magic
fire = Spell("Fire", 15, 300, "black")
thunder = Spell("Thunder", 20, 400, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 32, 850, "black")

# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 40, 1200, "white")


# Create some Items
potion = Item("Potion", "potion", "Heals 500 HP", 500)
hipotion = Item("Hi-Potion", "potion", "Heals 1000 HP", 1000)
superpotion = Item("Super Potion", "potion", "Heals 5000 HP", 5000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
megaelixer = Item("Mega-Elixer", "elixer", "Fully restores HP/MP of all party members", 9999)

grenade = Item("Grenade", "attack", "Deals 1000 damage", 1000)
spear = Item("Spear", "attack", "Deals 2500 damage", 2500)


player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, cure]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": megaelixer, "quantity": 1},
                {"item": grenade, "quantity": 3},
                {"item": spear, "quantity": 5}]

# Instantiate People
player1 = Person("Brody", 3260, 265, 320, 34, player_spells, player_items)
player2 = Person("Daddy", 4160, 185, 380, 34, player_spells, player_items)
player3 = Person("Momma", 3080, 330, 260, 34, player_spells, player_items)

enemy1 = Person("Vecna", 12380, 720, 525, 25, enemy_spells, [])
enemy2 = Person("Imp", 1400, 130, 625, 325, enemy_spells, [])
enemy3 = Person("Imp", 1400, 130, 625, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=========================")

    print("\n\n")
    print("NAME                   HP                                    MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print(player.name, "attacked", enemies[enemy].name, "for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + player.name + "'s spell " + spell.name + " deals", str(magic_dmg), "points of damage to", enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + player.name + "'s item " + item.name + " heals for", str(item.prop), "HPs" + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "Mega-Elixer":
                    for p in players:
                        p.hp = p.maxhp
                        p.mp = p.maxmp
                    print(bcolors.OKGREEN + "\n" + player.name + "'s item " + item.name + " fully restores the party's HP/MP" + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + player.name + "'s item " + item.name + " fully restores their HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + player.name + "'s item " + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if Players won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    # Check if Enemies won
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False

    print("\n")

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # Chose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + enemy.name + " attacks " + players[target].name + " for", str(enemy_dmg) +
                  bcolors.ENDC)

        elif enemy_choice == 1:
            # Chose magic
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.WARNING + spell.name + " heals " + enemy.name + " for", str(magic_dmg),
                      "HP." + bcolors.ENDC)
            elif spell.type == "black":

                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)

                print(bcolors.FAIL + enemy.name + "'s spell " + spell.name + " deals", str(magic_dmg),
                      "points of damage to", players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name, "has died.")
                    del players[target]


                    #print("Enemy chose", spell, "damage is", magic_dmg)
