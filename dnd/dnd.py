class Character:
  """
  Class for a DnD character.
  """
  
  def __init__(self, name, lvl, str, con, dex, inl, wis, cha):
    """
    Constructor for character.
    Takes in a name, level, and abilities.
    """
    # Save passed parameters
    self.name = name
    self.lvl = lvl
    self.abilities = {"str" : str,
                      "con" : con,
                      "dex" : dex,
                      "int" : inl,
                      "wis" : wis,
                      "cha" : cha}
    
    # Initialize other parameters
    # Speed
    self.speed_base = 0
    self.speed_armor = 0
    self.speed_item = 0
    self.speed_misc = 0
    # Fort
    self.fort_class = 0
    self.fort_feat = 0
    self.fort_enh = 0
    self.fort_misc1 = 0
    self.fort_misc2 = 0
    # Reflex
    self.ref_class = 0
    self.ref_feat = 0
    self.ref_enh = 0
    self.ref_misc1 = 0
    self.ref_misc2 = 0
    # Will
    self.will_class = 0
    self.will_feat = 0
    self.will_enh = 0
    self.will_misc1 = 0
    self.will_misc2 = 0
    # Skills 
    # All possible skills
    all_skills = ["Acrobatics", "Arcana", "Athletics", "Bluff", "Diplomacy",
                  "Dungeoneering", "Endurance", "Heal", "History", "Insight", 
                  "Intimidate", "Nature", "Perception", "Religion", "Stealth",
                  "Streetwise", "Thievery"]
    # Initialize dictionary
    self.skills = {}
    # Entries listed as ability modifier, trained, armor penalty, misc
    for skill in all_skills:
      self.skills[skill] = ["", False, 0, 0]
    for skill in ["Athletics"]:
      self.skills[skill][0] = "str"
    for skill in ["Endurance"]:
      self.skills[skill][0] = "con"
    for skill in ["Acrobatics", "Stealth", "Thievery"]:
      self.skills[skill][0] = "dex"
    for skill in ["Arcana", "History", "Religion"]:
      self.skills[skill][0] = "int"
    for skill in ["Dungeoneering", "Heal", "Insight", "Nature", "Perception"]:
      self.skills[skill][0] = "wis"
    for skill in ["Bluff", "Diplomacy", "Intimidate", "Streetwise"]:
      self.skills[skill][0] = "cha"
    # Hit points at 1st level
    self.hp_init = 0
    # Hit points per level
    self.hp_per_lvl = 0
    # Healing surges per day
    self.healing_surges = 0

  def half_lvl(self):
    """ Returns half of level rounded down. """
    return int(self.lvl/2)
    
  def abil_mod(self, abil):
    """ Returns ability modifier for the specified ability. """
    modifier = int((self.abilities[abil]-10)/2)
    return modifier
      
  def fort(self):
    """ Returns fortitude. """
    abil = max(self.abil_mod('str'), self.abil_mod('con'))
    return 10 + self.half_lvl() + abil + self.fort_class + self.fort_feat + \
      self.fort_enh + self.fort_misc1 + self.fort_misc2
    
  def ref(self):
    """ Returns reflex. """
    abil = max(self.abil_mod('dex'), self.abil_mod('int'))
    return 10 + self.half_lvl() + abil + self.ref_class + self.ref_feat + \
      self.ref_enh + self.ref_misc1 + self.ref_misc2
    
  def will(self):
    """ Returns will. """
    abil = max(self.abil_mod('wis'), self.abil_mod('cha'))
    return 10 + self.half_lvl() + abil + self.will_class + self.will_feat + \
      self.will_enh + self.will_misc1 + self.will_misc2
    
  def initiative(self):
    """ Returns initiative modifier for character. """
    return self.half_lvl() + self.abil_mod('dex')
    
  def speed(self):
    """ Returns movement speed. """
    return self.speed_base + self.speed_armor + self.speed_item + self.speed_misc
    
  def skill_bonus(self, skill):
    """ Returns bonus for specified skill. """
    [abil, trained, armor, misc] = self.skills[skill]
    bonus = self.half_lvl() + self.abil_mod(abil) + armor + misc
    if trained:
      bonus += 5
    return bonus
    
  def hp(self):
    """ Max HP. """
    return self.hp_init + (self.lvl - 1) * self.hp_per_lvl
   
  def hp_bloodied(self):
    """ Bloodied HP is half max HP. """
    return int(self.hp()/2)
    
  def hp_surge_value(self):
    """ Healing surge is quarter max HP. """
    return int(self.hp()/4)
    
  def display(self):
    """
    Output character info.
    """
    print "**************"
    print self.name
    print "Speed: %d" % (self.speed())
    print "Initiative: %s" % (self.initiative())
    print "HP: %d, Bloodied: %d, Healing Surge: %d (%d per day)" % (self.hp(), self.hp_bloodied(), self.hp_surge_value(), self.healing_surges)
    print self.abilities
    for key in self.abilities.keys():
      print "%s: %d, " % (key, self.abil_mod(key)),
    print
    print "Fort: %d, Ref: %d, Will: %d" % (self.fort(), self.ref(), self.will())
    print
    max_skill_name = len("Dungeoneering")
    for skill in sorted(self.skills.keys()):
      print "%-*s: %s" % (max_skill_name, skill, self.skill_bonus(skill))
    print "**************"

class Power:
  """
  Class for DnD power.
  """
  
  def __init__(self):
    default = "undefined"
    self.name = default
    self.type = default
    self.action_type = default
    self.target = default
    self.attack = default
    self.weapon = default
    self.hit = default
    
  def __str__(self):
    # Name
    string = self.name + "\n"
    # Type
    string += "\t" + self.type + ", "  + self.action_type + ", " + self.weapon + "\n"
    # Target and Attack
    string += "\tTarget: " + self.target + ", Attack: " + self.attack + "\n"
    # Hit description
    string += "\tHit: " + self.hit + "\n"
    return string
    

