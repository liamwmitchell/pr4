"""
todo:
- cleanup combat
- impliment targeting, sneak advantage, skill and item use, multiple combatants
- create character/mob and item/weapon classes
- do math for character/weapon stats
- rework ENCUM
- add miss option to basic_attack
"""
import os
import random

def clear(): #Clears screen
    os.system('cls' if os.name == 'nt' else 'clear')

class Character: #Parent of Player and Mob
    def __init__(self):
        pass

class Player(Character):
    def __init__(self):
        self.location=None
        self.STR=self.base_stats['STR'] # Strength: How strong a player is; determines attack damage
        self.DEX=self.base_stats['DEX'] # Dexterity: How nimble a player is; determines turn order and 
        self.CON=self.base_stats['CON'] # Constitution: determines health
        self.LUC=self.base_stats['LUC'] # Luck: determines critical hit chance
        self.HP=None
        self.weapon_prof={'slash':.01, 'stab':.01, 'blunt':.01, 'ranged':.01} #The initial idea was that each of these has the chance to increase with each use of type of weapon. chance to increase decreases as value increases

    def refresh_derived(self): #Derived stats pull from base stats above; Will needs to rethink this... Pssibly just refresh on level up?
        self.max_HP=2*self.CON #hit-points
        self.HP=self.max_HP # current
        self.AC=self.equip['armor'].rating #armor class; can accomodate multiple items using a sum
        self.CRIT=self.LUC/100 #crit chance
        self.ENCUM=self.equip['armor'].wt #encumberance-- ie. heavier armor means slower movement-- did not impliment
        self.SPD=self.DEX
        if self.equip['RH']: #checks if char is using 2 handed weapon; if not checks if both hands occupied. adds wt. of each hand's item to ENCUM if so. if not, just RH
            self.ENCUM+=self.equip['RH'].wt
            if self.equip['LH'] and self.equip['RH']!=self.equip['LH']:
                self.ENCUM+=self.equip['LH'].wt
        #can rework ENCUM as long as LH is occupied when RH is holding a 2h Weapon
    
    def basic_attack(self):
        # need to incorporate to-hit check
        damage=0
        crit=False
        if random.random()<=self.CRIT: #crit roll
            crit=True
            damage=self.equip['RH'].dmg[1]# weapon damage is a range (tuple) of two values, so here crit is using the highest of those values
        elif self.equip['RH'].wt<=self.STR/2: #penalty if character is not stron enough to use weapon
            damage=random.randint(self.equip['RH'].dmg[0], self.equip['RH'].dmg[1]) #damge roll
        else: #applies penalty
            damage=self.equip['RH'].dmg[0] # indexes used here refer to min/max of weapon damage. need to spend some time reworking values
        return damage, crit #returns an integer and a boolean. boolean is used to change output string in battle function
    
    def go_direction(self, dir):
        dir = dir.lower()
        valid=False
        while not valid:
            if dir in self.location.available_exits():
                if dir == "east":
                    self.location = self.location.east[0]
                if dir == "west":
                    self.location = self.location.west[0]
                if dir == "north":
                    self.location = self.location.north[0]
                if dir == "south":
                    self.location = self.location.south[0]
                valid=True
            else:
                dir=input("You cannot go in that direction. Try again.\n")

class Farmer(Player): #pulls from Player. Idea was that we could make several of these "character sheets" and players could choose from them. base stats and equipment would vary with each
    def __init__(self):
        self.base_stats={'DEX':5, 'STR':5, 'CON':5, 'LUC':5}
        Player.__init__(self)
        self.equip={'RH':Weapon('pitchfork'), 'LH':None, 'armor':Armor('clothes'), 'trinket':None} #'LH' considered off-hand; equipment here works by looking up the key in the associated dictionary (look to Weapon and Armor classes
        self.bag=[]
        self.gold=0

    #def skill(self, mob): #was planning on making a skilled attack that was specific to each player class

class Item: # Parent of any item classes
    def __init__(self): 
        pass

class Weapon(Item): #acts as a builder function for weapon items
    def __init__(self, key):
        self.name=key #names the weapon by the given key
        self.wt=weapons[key]['weight'] #each of these looks up the key in the weapons dictionary and pulls the relevant stats
        self.dmg=weapons[key]['damage']
        self.two_h=weapons[key]['two-handed']
        self.type=weapons[key]['type']

class Armor(Item): # works similarly to Weapon
    def __init__(self, key):
        self.name=key
        self.wt=armors[key]['weight']
        self.rating=armors[key]['rating']

#item dictionaries; can easily make new items by following template below
weapons={'pitchfork':{'weight':3, 'damage':[1,4], 'two-handed':True, 'type':'stab'}} #planning on creating seperate.py for item library; can do same for mobs if necc
armors={'clothes':{'weight':0, 'rating':0}}
mobs={'Goblin':{'HP':6, 'DMG':[2,3], 'AC':None, 'SPD':2, 'CRIT':0.03, 'drop':None}}

class Mob(Character): #derived from Character, works similarly to Player, only with simpliefied stats. Pulls stats using smae method as Weapon and Armor
    def __init__ (self, key):
        self.name=key
        self.max_HP=mobs[key]['HP']
        self.HP=self.max_HP
        self.DMG=mobs[key]['DMG']
        self.SPD=mobs[key]['SPD']

    def basic_attack(self): #temp just for demo sake, need to add crit
        damage=random.randint(self.DMG[0], self.DMG[1]) #damage roll
        crit=False #temporary, have not impliemnted crit roll for mobs
        return damage, crit #returns int and boolean, just like Player().basic_attack()

def battle(party, mobs): #this is where the magic happens... takes as input two lists-- I was pn allowing us to have battles between more than just two participants but did not get around to it. Should be easy to modify this function to accomodate for that however
    turn_order=sorted(party+mobs, key=lambda char: char.SPD, reverse=True) #determines turn order using participants speed
    player_alive=True #will be checked each turn to see if player is dead
    mobs_alive=True #similarly...
    prev_round={} #information about the previous round in the turn; stored as a dict. this is needed to print to terminal
    turn_in_round=0
    #round_counter=0
    #print('You have encountered a {}'.format(mob.name)) #dont know why this is commented out
    while player_alive and mobs_alive:
        #round_counter+=1
        clear()
        i=1
        while len(prev_round)>0 and i<len(prev_round)+1: #prints each entry in pre_round line by line 
            for pair in prev_round[str(i)]:
                print(prev_round[str(i)][pair].format(pair[0], pair[1]))
            i+=1
        for x in range(5-len(prev_round)): #fills in unused lines; keeps screen regularly sized
            print()
        for char in turn_order:
            print("{}: {}/{} HP".format(char.name, char.HP, char.max_HP)) #prints characters HP to the console
        prev_round={} #resets prev_round
        turn_in_round=0
        for char in turn_order:
            if char in party: #if PC
                print("---")
                #print("What is {}'s move?\n1. attack\n2. use skill\n3. use item\n".format(char.name), end="") #the idea here was that you would be able to choose your action each turn. skill would make use of the skill_attack() function above; use item would be eg. a potion
                print("What is {}'s move?\n1. attack".format(char.name), end="")
                action=input("")
                if '1' in action or 'a' in action: #only have this choice for now
                    attack_roll=char.basic_attack()
                    target=mobs[0] #temporary until multiple combatants is implimented
                    if attack_roll[1]: #if critical hit...
                        turn_in_round+=1
                        prev_round[str(turn_in_round)]={(char.name, target.name.lower()):"Critical hit! {} struck {} for " + str(attack_roll[0]) + " damage."} #stores this turns text to pre_round dictionary in order for it to be printed to the console next turn
                        target.HP-=attack_roll[0] #reduce target's HP by damage dealt
                        if target.HP<=0: #checks if target is dead
                            target.HP=0 #insures not negative values
                            mobs.remove(target) #removes them from mob list
                            prev_round[str(turn_in_round)][(char.name, target.name)]+=" " + char.name + " has defeated " + target.name.lower() + "." #appends this turns entry in prev_round
                    else: #if not critical hit... works pretty much the same as above, only with different text stored in the dictionary
                        turn_in_round+=1
                        prev_round[str(turn_in_round)]={(char.name, target.name):"{} struck {} for " + str(attack_roll[0]) + " damage."}
                        print(  )
                        target.HP-=attack_roll[0]
                        if target.HP<=0:
                            target.HP=0
                            mobs.remove(target)
                            prev_round[str(turn_in_round)][(char.name, target.name)]+=" " + char.name + " has defeated " + target.name.lower() + "."
                #elif '2' in action or 'sk' in action:
                #elif '3' in action or 'it' in action:
                #else: #error recognition? THIS IS IMPORTANT
            elif char in mobs: #if NPC
                print(char) #simplified version of PC turn
                attack_roll=char.basic_attack()
                target=party[0] #temp
                turn_in_round+=1
                prev_round[str(turn_in_round)]={(char.name, target.name):"{} struck {} for " + str(attack_roll[0]) + " damage."}
                target.HP-=attack_roll[0]
                if target.HP<=0:
                    target.HP=0
                    player_alive=False #temporary
                    last_round=prev_round.copy()
                    prev_round[str(turn_in_round)][(char.name, target.name)]+=" " + char.name + " has defeated " + target.name.lower() + "."
        if len(mobs)==0:
            mobs_alive=False
            last_round=prev_round.copy() #saves entry to print to console at end of battle
    clear()
    i=1 #does pretty much the same thing as above; slightly modified as this marks the end of a battle
    while i<len(last_round)+1:
        for pair in last_round[str(i)]:
            print(last_round[str(i)][pair].format(pair[0], pair[1]))
        i+=1
    for x in range(5-len(last_round)):
        print()
    for char in turn_order:
        print("{}: {}/{} HP".format(char.name, char.HP, char.max_HP))
    print("---")
    cont=input("Press any key to continue.")
    # possibly create self.alive attribute for all characters so that battle() can check through participants and
    # show list of dead at the end

##hero=Farmer()
##hero.name='Alex'
##hero.player=True
##hero.refresh_derived()
##g=Mob('Goblin')
##battle([hero],[g])
