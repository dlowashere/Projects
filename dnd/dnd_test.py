import dnd

# Initialize character
Brashman = dnd.Character("Brashman", 2, 14, 12, 11, 10, 13, 16)
Brashman.display()

# Dragonborn racial bonuses
Brashman.abilities['str'] += 2
Brashman.abilities['cha'] += 2

# Class bonuses
Brashman.fort_class = 1
Brashman.ref_class = 1
Brashman.will_class = 1

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

