class Room:
    def __init__(self, desc, north = None, west = None, south = None, east = None):
        self.desc = desc
        self.north = [north, False]
        self.west = [west, False]
        self.south = [south, False]
        self.east = [east, False]
        self.items = []
        self.monsters = []
        self.chest = [False, []]
    def add_monster(self, monster):
        self.monsters.append(monster)
    def remove_monster(self, monster):
        self.monsters.remove(monster)
    def show_monsters(self):
        for m in monsters:
            print(m.name)
    def has_monsters(self):
        if self.monsters == []:
            return False
        else:
            return True
    def lock_door(dir):
        ## Sets the 'locked' Boolean to True, which indicates that the door is locked
        dir[1] = True
    def add_item(self, item):
        self.items.append(item)
    def remove_item(self, item):
        self.items.remove(item)
    def show_items(self, item):
        for i in self.items:
            print(i.name)
    def has_items(self):
        if self.items == []:
            return False
        else:
            return True
    def getItemByName(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False
    def add_exit(self, room, dir):
        if dir == "south":
            self.south = room
            room.north = self
        if dir == "east":
            self.east = room
            room.west = self
        if dir == "north":
            self.north = room
            room.south = self
        if dir == "west":
            self.west = room
            room.east = self
    def show_exits(self):
        if self.north:
            print("north")
        if self.west:
            print("west")
        if self.south:
            print("south")
        if self.east:
            print("east")
    def has_chest(self):
        return(self.chest[0])
    def chest_contents(self):
        for i in self.chest[1]:
            print(i.name)
