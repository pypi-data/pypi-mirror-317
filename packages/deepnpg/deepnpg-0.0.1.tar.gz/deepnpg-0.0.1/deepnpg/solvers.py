

import torch
from torch.linalg import solve_triangular
from torch import float as TFLOAT


class Solver(object):
    def __init__(self, **kwargs):
        self.tol = kwargs.get("tol", 1e-6)
        self.max_iters = kwargs.get("max_iters", 999)
        

    def __call__(self, A:TFLOAT, b:TFLOAT, preconditioner=None):
        if preconditioner == None:
            preconditioner = self.use_no_preconditioner

        A = A.float()
        b = b.float()
        size = A.size()
        n = size[0]

        x0 = torch.zeros(n, 1, dtype=TFLOAT)
        x = x0.clone()
        Z = torch.zeros(n, self.max_iters)
        C = torch.zeros(n, self.max_iters)
        gamma = torch.zeros(self.max_iters, self.max_iters)
        alpha= torch.zeros(self.max_iters, 1)

        iterations = self.max_iters 
        r = b - A@x

        for j in range(self.max_iters):
            Z[:, j] = preconditioner(r).flatten()
            c = A@Z[:,j]
            
            for i in range(j):
                gamma[i,j] = torch.inner(c, C[:,i])
                c -= gamma[i,j] * C[:,i]

            gamma[j,j] = torch.norm(c.flatten(), 2)
            
            C[:,j] = (c / gamma[j,j]).flatten()
            alpha[j] = torch.inner(r.T, C[:,j])[0]

            r -= torch.unsqueeze(alpha[j] * C[:,j], 1)
            residual = r.T @ r 

            if residual < self.tol:
                iterations = j + 1 
                break
        
        if iterations > 0: 
            tmp = solve_triangular(gamma[:iterations,:iterations], alpha[:iterations], upper=True)
            x += Z[:,:iterations]@tmp

        return iterations


    def use_no_preconditioner(self, x):
        return x


		



    
