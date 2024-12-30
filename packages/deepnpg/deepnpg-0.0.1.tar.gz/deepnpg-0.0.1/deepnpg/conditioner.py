# define your preconditioner class for your customized model
import torch



class FPreconditioner: # factorization-based preconditioner, such as LU
    def __init__(self, model, spd=True, **kwargs):
        self.model = model
        self.spd = spd
        self.unit_lower = kwargs.get("unit_lower", False)
        self.unit_upper = kwargs.get("unit_upper", False)
        

    def compute_factors(self, A, **kwargs):
        with torch.inference_mode():
            M, N, _ = self.model(A, **kwargs)
            
            if self.spd:
                N = torch.transpose(M, 0, 1).to_dense()

        return M, N


    def build(self, A):
        self.M, self.N = self.compute_factors(A)


    def compute_inverse(self):
        if not (hasattr(self, "M") and hasattr(self, "N")):
            raise ValueError("Please build the preconditioner first via method `.build`. ")
        
        M_inv = torch.inverse(self.M.to_dense()) 
        N_inv = torch.inverse(self.N.to_dense())
        
        return M_inv, N_inv
    

    def compute_P(self):
        if not (hasattr(self, "M") and hasattr(self, "N")):
            raise ValueError("Please build the preconditioner first via method `.build`. ")
        
        return self.M@self.N


    def compute_inverse_P(self):
        M_inv, N_inv = self.compute_inverse()
        return N_inv@M_inv
    
    def __call__(self, x):
        y = torch.linalg.solve(self.M, x)
        x = torch.linalg.solve(self.N, y)
        return x


class NIFPreconditioner(FPreconditioner): 
    def __init__(self, model):
        super().__init__(model, spd=True)
    
    def __call__(self, x):
        if not (hasattr(self, "M") and hasattr(self, "N")):
            raise ValueError("Please build the preconditioner first via method `.build`. ")
        
        return LUSolve(self.M, self.N, x, unit_lower=False, unit_upper=False)


class LUPreconditioner(FPreconditioner): 
    def __init__(self, model):
        super().__init__(model, spd=False)
    
    def __call__(self, x):
        if not (hasattr(self, "M") and hasattr(self, "N")):
            raise ValueError("Please build the preconditioner first via method `.build`. ")
        
        return LUSolve(self.M, self.N, x, unit_lower=False, unit_upper=False)


def LUSolve(L, U, b, unit_lower=False, unit_upper=False):
    L = L.to('cpu').to_dense()
    U = U.to('cpu').to_dense()
    b = b.to('cpu')

    y = torch.linalg.solve_triangular(L, b, upper=False, left=True, unitriangular=unit_lower)  # L.solve_triangular(upper=False, unit=unit_lower, b=r)
    x = torch.linalg.solve_triangular(U, y, upper=True, left=True, unitriangular=unit_upper)  # U.solve_triangular(upper=True, unit=unit_upper, b=y)
    return x

