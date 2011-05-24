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
    self.abilities = {'str' : str,
                      'con' : con,
                      'dex' : dex,
                      'int' : inl,
                      'wis' : wis,
                      'cha' : cha}
    
    self.fort_class = 0
    self.ref_class = 0
    self.will_class = 0

  def half_lvl(self):
    """ Returns half of level rounded down. """
    return int(self.lvl/2)
    
  def abil_mod(self, abil):
    """ Returns ability modifier for the specified ability. """
    modifier = int((self.abilities[abil]-10)/2)
    modifier += self.half_lvl()
    return modifier
      
  def fort(self):
    """ Returns fortitude. """
    abil = max(self.abil_mod('str'), self.abil_mod('con'))
    return 10 + self.half_lvl() + abil + self.fort_class 
    
  def ref(self):
    """ Returns reflex. """
    abil = max(self.abil_mod('dex'), self.abil_mod('int'))
    return 10 + self.half_lvl() + abil + self.ref_class 
    
  def will(self):
    """ Returns will. """
    abil = max(self.abil_mod('wis'), self.abil_mod('cha'))
    return 10 + self.half_lvl() + abil + self.will_class 
    
  def initiative(self):
    """ Returns initiative modifier for character. """
    return self.half_lvl() + self.abil_mod('dex')
    
  def display(self):
    """
    Output character info.
    """
    print "**************"
    print self.name
    print "Initiative: %s" % (self.initiative())
    print self.abilities
    for key in self.abilities.keys():
      print "%s: %d, " % (key, self.abil_mod(key)),
    print
    print "Fort: %d, Ref: %d, Will: %d" % (self.fort(), self.ref(), self.will())
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
    

