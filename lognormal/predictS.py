from __future__ import division
import numpy as np
import random
import scipy as sc
from scipy import stats
import os
import sys
import statsmodels.stats.api as sms
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from statsmodels.stats.outliers_influence import summary_table
from numpy import log, log2, exp, sqrt, log10, pi
from scipy.optimize import fsolve
import scipy.optimize as opt
import pandas as pd #import patsy
import mpmath as mpm
from scipy.optimize import fsolve
from math import erf, pi
import math

mydir = os.path.expanduser("~/GitHub/MicroMETE/")
mydir2 = os.path.expanduser("~/")
pi = math.pi


def alpha(a, N, Nmax, Nmin=1):

    """Numerically solve for Preston's a. Needed to estimate S using the lognormal"""

    y = sqrt(pi*Nmin*Nmax)/(2.0*a) * exp((a * log2(sqrt(Nmax/Nmin)))**2.0)
    y = y * exp((log(2.0)/(2.0*a))**2.0)
    y = y * erf(a * log2(sqrt(Nmax/Nmin)) - log(2.0)/(2.0*a))
    y += erf(a * log2(sqrt(Nmax/Nmin)) + log(2.0)/(2.0*a))
    y -= N

    return y # find alpha

def s(a, Nmax, Nmin=1):

    """Predict S from the lognormal using Nmax as the only empirical input"""

    return sqrt(pi)/a * exp( (a * log2(sqrt(Nmax/Nmin)))**2) # Using equation 10


def getNmax(N, b=0.4, slope=0.9126):

    """Predict Nmax using N and the scaling law of Nmax with N predicted by the lognormal"""

    return 10 ** (b + slope*(log10(N)))


def getS(N, Nmax, predictNmax=True):

    guess = 0.2 # initial guess for Preston's alpha
    Nmin = 1

    if predictNmax == True:
        Nmax = getNmax(N)

    a = opt.fsolve(alpha, guess, (N, Nmax, Nmin))[0]
    S2 = s(a, Nmax, 1)

    return S2


#S = getS(1000, 900, predictNmax=True)
#print S