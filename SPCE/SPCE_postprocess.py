from UQpy.distributions import Normal, Uniform, JointIndependent
from SPCE_optuna import *

import numpy as np
from numpy.polynomial.hermite_e import hermegauss
from numpy.polynomial.legendre import leggauss


def sample_from_cond_pdf(x, n_samples, c, sigma, D, A, dist_obj):
    """
    Used to obtain samples from conditional distibution from SPCE model.
    """
    
    if D=="Normal":
        Z = Normal(loc=0, scale=1)
    elif D=="Uniform":
        Z = Uniform(loc=-1, scale=2)
        
    z = Z.rvs(n_samples)
    
    marg_x  = dist_obj.marginals
    marg_xz = marg_x.copy()
    marg_xz.append(Z)  
    joint_xz = JointIndependent(marginals=marg_xz)
    
    A_basis = CustomBasis(joint_xz, A)
    
    Xz = np.concatenate((np.repeat(np.asarray([x]), len(z), axis=0), z), axis=1)
    
    Psi = A_basis.evaluate_basis(Xz)
    
    pce_approx_ = np.dot(Psi, c)
    
    eps = np.random.normal(0, sigma, n_samples)
    
    return pce_approx_ + eps



def explicit_pdf(y_pts, x, c, sigma, D, A, dist_obj, NQ=40):
    """
    Used to obtain explicit form of the conditional response distribution.
    """

    if D=="Normal":
        Z = Normal(loc=0, scale=1)
        zs, ws_ = hermegauss(NQ)
        ws = ws_ / (2 * np.pi * sigma)
    elif D=="Uniform":
        Z = Uniform(loc=-1, scale=2)
        zs, ws_ = leggauss(NQ) #points and weights
        ws = ws_ / (2 * np.pi * sigma)
        
    marg_x  = dist_obj.marginals
    marg_xz = marg_x.copy()
    marg_xz.append(Z)  
    joint_xz = JointIndependent(marginals=marg_xz)
    
    y_pdf = []
    for y in y_pts:
        Xz = np.concatenate((np.repeat(np.asarray([x]), len(zs), axis=0), 
                     zs.reshape(-1, 1)), axis=1)

        y_expanded = np.repeat(y, len(zs), axis=0)

        A_basis = CustomBasis(joint_xz, A)
        Psi = A_basis.evaluate_basis(Xz)

        pce_approx = np.dot(Psi, c)

        exponent = -((y_expanded - pce_approx) ** 2) / (2 * sigma**2)
        integrand = np.exp(exponent) * ws
        integrand_sums = np.sum(integrand)
        
        y_pdf.append(integrand_sums)

    return y_pdf


