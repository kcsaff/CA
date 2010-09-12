
from simple import typed_object as rule
import registry

def life(birth = [3], survival = [2,3]):
    return rule('life', birth=birth, survival=survival)

def brain(birth = [2], survival = [], decay = 1):
    return rule('brain', birth=birth, survival=survival, decay=decay)

print 'asdf'
