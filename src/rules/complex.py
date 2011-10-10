
from simple import rule
import numpy

def complex(moore=[0.0, 0.5, 0.0,
                   0.5, 0.0, 0.5,
                   0.0, 0.5, 0.0],
            history = -1.0,
            potential = 0.005,
            planes = 2,
            ):
    return rule('complex',
                moore=moore,
                history=history,
                potential=potential)
    
def schroedinger(mass=1.0,
                 dt=1.0):
    A = 0.5j * dt / mass
    moore=[0.0,       A,       0.0,
           A,   1 - 4*A,       A,
           0.0,       A,       0.0]
    return complex(moore=moore,
                   history=0,
                   potential=0,#-1j * dt,
                   )