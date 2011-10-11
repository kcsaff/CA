
from simple import rule
import numpy, math

def complex(moore=[0.0, 0.5, 0.0,
                   0.5, 0.0, 0.5,
                   0.0, 0.5, 0.0],
            history = -1.0,
            potential = 0.005,
            denom = False,
            ):
    return rule('complex',
                moore=moore,
                history=history,
                potential=potential,
                denom=denom)
    
def schroedinger(mass=1.0,
                 dt=0.01,
                 dx=1.0):
    mdx2 = mass * dx * dx
    A = 0.5j * dt / mdx2
    moore=[0.0,       A,       0.0,
           A,   -4 * A,       A,
           0.0,       A,       0.0]
    return complex(moore=moore,
                   history=1,
                   potential=0,#-1j * dt,
                   )
    
    
def schroedingerD(mass=1.0,
                  dt=1.0,
                  dx=1.0):
    mdx2 = mass * dx * dx
    A = 0.5j * dt / mdx2
    B = A * math.sqrt(2)
    moore=[B,       A,       B,
           A, 1 - 4*A - 4*B, A,
           B,       A,       B]
    return complex(moore=moore,
                   history=0,
                   potential=0,#-1j * dt,
                   )
    
def schroedingerA(mass=1.0,
                  dt=1.0,
                  dx=1.0):
    mdx2 = mass * dx * dx
    N = 2
    V = 0 # Can't do x-dependent V this way, may need to rewrite solver.
    D = -1j / dt + N / mdx2 + V
    history = -1j / dt / D
    A = 0.5 / mdx2 / D
    moore=[0.0,       A,       0.0,
            A,       0.0,       A,
           0.0,       A,       0.0]
    return complex(moore=moore,
                   history=history,
                   potential=0)
    
def schroedingerAD(mass=1.0,
                   dt=1.0,
                   dx=1.0):
    mdx2 = mass * dx * dx
    N = 2.5
    V = 0 # Can't do x-dependent V this way, may need to rewrite solver.
    D = -1j / dt + N / mdx2 + V
    H = -1j / dt / D
    history = 0 #H
    A = 0.5 / mdx2 / D
    B = A * 0.25
    moore=[B, A, B,
           A, H, A,
           B, A, B]
    return complex(moore=moore,
                   history=history,
                   potential=0,
                   denom=D)
    
def schroedingerB(mass=1.0,
                  dt=1.0,
                  dx=1.0,
                  mix=0.782): #.780, .782
    
    mdx2 = mass * dx * dx
    AN = 2
    AD = -1j / dt + AN / mdx2 + 0
    Ahistory = -1j / dt / AD
    AA = 0.5 / mdx2 / AD
    Amoore=[0.0,       AA,       0.0,
             AA,       0.0,       AA,
            0.0,       AA,       0.0]
    NA = 0.5j * dt / mdx2
    Nhistory = 0
    Nmoore=[0.0,       NA,       0.0,
             NA,   1 - 4*NA,       NA,
            0.0,       NA,       0.0]
    history = (1 - mix) * Nhistory + mix * Ahistory
    moore = [(1-mix) * N + mix * A
             for (N,A) in zip(Nmoore, Amoore)]
    return complex(moore=moore,
                   history=history)    
