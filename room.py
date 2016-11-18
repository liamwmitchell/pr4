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
    def lock_door(self):
        ## Sets the 'locked' Boolean to True, which indicates that the door is locked
        self.south[1] = True
    def is_locked(self, dir):
        return dir[1]
    def add_item(self, item):
        self.items.append(item)
    def remove_item(self, item):
        self.items.remove(item)
    def show_items(self):
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
            self.south[0] = room
            room.north[0] = self
        if dir == "east":
            self.east[0] = room
            room.west[0] = self
        if dir == "north":
            self.north[0] = room
            room.south[0] = self
        if dir == "west":
            self.west[0] = room
            room.east[0] = self
    def available_exits(self):
        exits = []
        if self.north[0]:
            exits.append("north")
        if self.west[0]:
            exits.append("west")
        if self.south[0]:
            exits.append("south")
        if self.east[0]:
            exits.append("east")
        return(exits)
    def has_chest(self):
        return(self.chest[0])
    def chest_contents(self):
        for i in self.chest[1]:
            print(i.name)
