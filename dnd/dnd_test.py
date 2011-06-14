import dnd

# Initialize character
Brashman = dnd.Character("Brashman", 2, 14, 12, 11, 10, 13, 16)

# Dragonborn racial bonuses
# +2 str, +2 cha
Brashman.abilities['str'] += 2
Brashman.abilities['cha'] += 2
# Speed 6
Brashman.speed_base = 6
# +2 History, +2 Intimidate
Brashman.skills['History'][3] = 2
Brashman.skills['Intimidate'][3] = 2
# Dragonborn Fury: +1 attack when bloodied
# Dragconic Heritage: Healing surge value = 1/4 hp + con mod
func_type = type(Brashman.hp_surge_value)
def draconic_hp_surge_value(self):
  return int(self.hp()/4) + self.abil_mod("con")
Brashman.hp_surge_value = func_type(draconic_hp_surge_value, Brashman, dnd.Character)
# Dragon Breath: ability

# Class bonuses
# Armor proficiencies: cloth, leather, hide, chainmail, scale, plate, light/heavy shield
# Weapon proficiencies: Simple/military melee, simple ranged
# +1 fort, ref & will
Brashman.fort_class = 1
Brashman.ref_class = 1
Brashman.will_class = 1
# 1st level hit points = 15 + con
Brashman.hp_init = 15 + Brashman.abilities["con"]
# Hit points per level = 6
Brashman.hp_per_lvl = 6
# Healing surges per day = 10 + con
Brashman.healing_surges = 10 + Brashman.abil_mod("con")
# Trained skills: Religion + 3 of: Diplomacy, Endurance, Heal, History, Insight, Intimidate
for skill in ["Religion", "Diplomacy", "Heal", "Insight"]:
  Brashman.skills[skill][1] = True

Brashman.display()

while True:
  pass

# Equipment
melee_weapon = "1d10"
melee_weapon_prof = 2

# Attack bonus
melee_attack = half_level + melee_weapon_prof

bolstering_strike = powers.Powers()
bolstering_strike.name = "Bolstering Strike"
bolstering_strike.type = "At-Will"
bolstering_strike.action_type = "Standard Action"
bolstering_strike.weapon = "Melee weapon"
bolstering_strike.target = "One creature"
bolstering_strike.attack = "+%d vs. AC" % (melee_attack + cha_mod)
bolstering_strike.hit = "%s + %d damage and you gain %d temporary hit points" % (melee_weapon, cha_mod, wis_mod)
print bolstering_strike

enfeebling_strike = powers.Powers()
enfeebling_strike.name = "Enfeebling Strike"
enfeebling_strike.type = "At-Will"
enfeebling_strike.action_type = "Standard Action"
enfeebling_strike.weapon = "Melee weapon"
enfeebling_strike.target = "One creature"
enfeebling_strike.attack = "+%d vs. AC" % (melee_attack + cha_mod)
enfeebling_strike.hit = "%s + %d damage. If you marked the target, it takes a -2 penalty to attack rolls until the end of your next turn" % (melee_weapon, cha_mod)
print enfeebling_strike

