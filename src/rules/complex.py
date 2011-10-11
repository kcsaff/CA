
from simple import rule
import numpy, math

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
                   history=0.0,
                   potential=0,#-1j * dt,
                   )
    
    
def schroedingerD(mass=1.0,
                  dt=1.0):
    A = 0.5j * dt / mass
    B = A * 0.25
    moore=[B,       A,       B,
           A, 1 - 4*A - 4*B, A,
           B,       A,       B]
    return complex(moore=moore,
                   history=0,
                   potential=0,#-1j * dt,
                   )
    
def schroedingerA(mass=1.0,
                  dt=1.0):
    N = 2
    V = 0 # Can't do x-dependent V this way, may need to rewrite solver.
    D = -1j / dt + N / mass + V
    history = -1j / dt / D
    A = 0.5 / mass / D
    moore=[0.0,       A,       0.0,
            A,       0.0,       A,
           0.0,       A,       0.0]
    return complex(moore=moore,
                   history=history,
                   potential=0)
    
def schroedingerAD(mass=1.0,
                  dt=10):
    N = 2.5
    V = 0 # Can't do x-dependent V this way, may need to rewrite solver.
    D = -1j / dt + N / mass + V
    history = -1j / dt / D
    A = 0.5 / mass / D
    B = A * 0.25
    moore=[B, A, B,
           A, 0, A,
           B, A, B]
    return complex(moore=moore,
                   history=history,
                   potential=0)
