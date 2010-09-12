
from _rule import rule
import registry

def life(birth = [3], survival = [2,3]):
    return rule('life', birth=birth, survival=survival)

def brain(birth = [2], survival = [], decay = 1):
    return rule('brain', birth=birth, survival=survival, decay=decay)

#in order NESW, like mcell
def banks(birth = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
          survival = [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
          decay = 0): 
    return rule('banks', birth=birth, survival=survival, decay=decay)
