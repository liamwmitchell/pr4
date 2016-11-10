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

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Character:
    def __init__(self):
        pass

class Player(Character):
    def __init__(self):
        self.STR=self.base_stats['STR']
        self.DEX=self.base_stats['DEX']
        self.CON=self.base_stats['CON']
        self.LUC=self.base_stats['LUC']
        self.HP=None
        self.weapon_prof={'slash':.01, 'stab':.01, 'blunt':.01, 'ranged':.01} #has chance to increase with each use of type of weapon. chance to increase decreases as value increases

    def refresh_derived(self): #rethink this...
        self.max_HP=2*self.CON #hit-points
        self.HP=self.max_HP
        self.AC=self.equip['armor'].rating #armor class; can accomodate multiple items using a sum
        self.CRIT=self.LUC/100 #crit chance
        self.ENCUM=self.equip['armor'].wt #encumberance
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
        if random.random()<=self.CRIT:
            crit=True
            damage=self.equip['RH'].dmg[1]
        elif self.equip['RH'].wt<=self.STR/2:
            damage=random.randint(self.equip['RH'].dmg[0], self.equip['RH'].dmg[1])
        else:
            damage=self.equip['RH'].dmg[0] # indexes used here refer to min/max of weapon damage. need to spend some time reworking values
        return damage, crit

class Farmer(Player):
    def __init__(self):
        self.base_stats={'DEX':5, 'STR':5, 'CON':5, 'LUC':5}
        Player.__init__(self)
        self.equip={'RH':Weapon('pitchfork'), 'LH':None, 'armor':Armor('clothes'), 'trinket':None} #'LH' considered off-hand
        self.bag=[]
        self.gold=0

    #def skill(self, mob):

class Item:
    def __init__(self):
        pass

class Weapon(Item):
    def __init__(self, key):
        self.name=key
        self.wt=weapons[key]['weight']
        self.dmg=weapons[key]['damage']
        self.two_h=weapons[key]['two-handed']
        self.type=weapons[key]['type']

class Armor(Item):
    def __init__(self, key):
        self.name=key
        self.wt=armors[key]['weight']
        self.rating=armors[key]['rating']

weapons={'pitchfork':{'weight':3, 'damage':[1,4], 'two-handed':True, 'type':'stab'}} #planning on creating seperate.py for item library; can do same for mobs if necc
armors={'clothes':{'weight':0, 'rating':0}}
mobs={'Goblin':{'HP':6, 'DMG':[2,3], 'AC':None, 'SPD':2, 'CRIT':0.03, 'drop':None}}

class Mob(Character):
    def __init__ (self, key):
        self.name=key
        self.max_HP=mobs[key]['HP']
        self.HP=self.max_HP
        self.DMG=mobs[key]['DMG']
        self.SPD=mobs[key]['SPD']

    def basic_attack(self): #temp just for demo sake, need to add crit
        damage=random.randint(self.DMG[0], self.DMG[1])
        crit=False
        return damage, crit

def battle(party, mobs):
    turn_order=sorted(party+mobs, key=lambda char: char.SPD, reverse=True)
    player_alive=True #
    mobs_alive=True
    prev_round={}
    turn_in_round=0
    #round_counter=0
    #print('You have encountered a {}'.format(mob.name))
    while player_alive and mobs_alive:
        #round_counter+=1
        clear()
        i=1
        while len(prev_round)>0 and i<len(prev_round)+1:
            for pair in prev_round[str(i)]:
                print(prev_round[str(i)][pair].format(pair[0], pair[1]))
            i+=1
        for x in range(5-len(prev_round)):
            print()
        for char in turn_order:
            print("{}: {}/{} HP".format(char.name, char.HP, char.max_HP))
        prev_round={}
        turn_in_round=0
        for char in turn_order:
            if char in party:
                print("---")
                print("What is {}'s move?\n1. attack\n2. use skill\n3. use item\n".format(char.name), end="")
                action=input("")
                if '1' in action or 'a' in action:
                    attack_roll=char.basic_attack()
                    target=g #temp
                    if attack_roll[1]: #crit check
                        turn_in_round+=1
                        prev_round[str(turn_in_round)]={(char.name, target.name.lower()):"Critical hit! {} struck {} for " + str(attack_roll[0]) + " damage."}
                        target.HP-=attack_roll[0]
                        if target.HP<=0:
                            target.HP=0
                            mobs.remove(target)
                            prev_round[str(turn_in_round)][(char.name, target.name)]+=" " + char.name + " has defeated " + target.name.lower() + "."
                    else: #standard
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
                #else: #error recognition?
            elif char in mobs:
                print(char)
                attack_roll=char.basic_attack()
                target=hero #temp
                turn_in_round+=1
                prev_round[str(turn_in_round)]={(char.name, target.name):"{} struck {} for " + str(attack_roll[0]) + " damage."}
                target.HP-=attack_roll[0]
                if target.HP<=0:
                    target.HP=0
                    player_alive=False #temp
                    last_round=prev_round.copy()
                    prev_round[str(turn_in_round)][(char.name, target.name)]+=" " + char.name + " has defeated " + target.name.lower() + "."
        if len(mobs)==0:
            mobs_alive=False
            last_round=prev_round.copy()
    clear()
    i=1
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

hero=Farmer()
hero.name='Alex'
hero.player=True
hero.refresh_derived()
g=Mob('Goblin')
battle([hero],[g])