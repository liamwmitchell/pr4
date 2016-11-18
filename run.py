from room import Room
from combat import battle, Character, Player, Item, Mob, Farmer, Weapon, Armor, Key
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

player = Farmer()
player.name = input("What is your name?")
def print_situation():
    clear()
    print(player.location.desc)
    if player.location.chest[0]:
        print("This room has a chest")
        print()
    if player.location.has_items():
        print("This room has the following items:")
        print(player.location.show_items())
        print()
    exits = ""
    if player.location.north[0]:
        exits = "north"
        if player.location.north[1]:
            exits = exits + " (locked)"
        exits = exits + "\n"
    if player.location.east[0]:
        exits = exits + "east"
        if player.location.east[1]:
            exits = exits + " (locked)"
        exits = exits + "\n"
    if player.location.south[0]:
        exits = exits + "south"
        if player.location.south[1]:
            exits = exits + " (locked)"
        exits = exits + "\n"
    if player.location.west[0]:
        exits = exits + "west"
        if player.location.west[1]:
            exits = exits + " (locked)"
        exits = exits + "\n"
    print("This room has exits to the")
    print(exits)
    print()

def create_world():
    a = Room("You are in room 1")
    b = Room("You are in room 2")
    c = Room("You are in room 3")
    d = Room("You are in room 4")
    e = Room("You are in room 5")
    f = Room("You are in room 6")
    g = Room("You are in room 7")
    h = Room("You are in room 8")
    a.add_exit(b, "east")
    b.add_exit(c, "east")
    c.add_exit(d, "east")
    d.add_exit(e, "south")
    e.add_exit(f, "west")
    f.add_exit(g, "west")
    g.add_exit(b, "north")
    g.add_exit(h, "south")
    player.location = a
    mob = Mob("Goblin")
    b.add_monster(mob)
    sword = Weapon('sword')
    d.add_item(sword)
    mob2 = Mob("Goblin")
    e.add_monster(mob2)
    g.lock_door()
    key = Key()
    g.add_item(key)

def showHelp():
    clear()
    print("go <direction> -- moves you in the given direction")
    print("inventory -- opens your inventory")
    print("pickup <item> -- picks up the item")
    print()
    input("Press enter to continue...")

create_world()
playing = True
while playing:
    if player.location.desc == "You are in room 8":
        clear()
        print("You Win!")
        input("Press enter to exit...")
        playing = False
    else:
        if player.location.monsters != []:
            player.refresh_derived()
            battle([player], player.location.monsters)
        print_situation()
        commandSuccess = False
        while not commandSuccess:
            commandSuccess = True
            command = input("What now? ")
            commandWords = command.split()
            if commandWords[0].lower() == "go":   #cannot handle multi-word directions
                player.go_direction(commandWords[1]) 
            elif commandWords[0].lower() == "pickup":  #can handle multi-word objects
                targetName = command[7:]
                target = player.location.getItemByName(targetName)
                if target != False:
                    player.pickup(target)
                    player.location.remove_item(target)
                else:
                    print("No such item.")
                    commandSuccess = False
            elif commandWords[0].lower() == "unlock":
                commandSuccess = False
                player.unlock_door()
                print_situation()
            elif commandWords[0].lower() == "inventory":
                player.show_inventory()       
            elif commandWords[0].lower() == "help":
                showHelp()
            elif commandWords[0].lower() == "exit":
                playing = False
            else:
                print("Not a valid command")
                commandSuccess = False

