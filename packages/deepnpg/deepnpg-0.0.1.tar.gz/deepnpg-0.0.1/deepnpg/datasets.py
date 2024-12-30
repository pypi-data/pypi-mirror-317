
import os
import torch
from scipy.sparse import coo_matrix, identity
import scipy
import numpy as np
from glob import glob
from scipy.sparse import coo_matrix, _coo
from .transform import *

class BuildCoatesGraph(torch.utils.data.Dataset):
    def __init__(self, path=None, A=None, b=None, x=None, size:int=1, n:int=1):
        super().__init__()
        self.data_loaded = False

        if path is not None:
            self.A = readA(path=path, size=size, n=n)
            self.b = readb(path=path, size=size, n=n)
            self.x = readx(path=path, size=size, n=n)

            if len(self.A) == 0 or len(self.b) == 0: 
                raise FileNotFoundError(f"No files found in {path} with n={n}")
        
        else:
            self.A = A
            self.b = []
            self.x = []
            if b is not None: self.b = b
            if x is not None: self.x = x
            self.data_loaded = True

    def __len__(self):
        return len(self.A)
    
    def __getitem__(self, idx):
        if self.data_loaded:
            A = torch.Tensor(self.A[idx])
        else:
            A = torch.load(self.A[idx], weights_only=False)

        if len(self.b) > 0:
            if self.data_loaded:
                b = torch.Tensor(self.b[idx]).flatten()
            else:
                b = torch.load(self.b[idx], weights_only=False).flatten()

            g = matrix_to_graph(A, b) # add b to graph as node features
            
        else:
            g = matrix_to_graph(A)

        if len(self.x) > 0:
            if self.data_loaded:
                g.solution = torch.Tensor(self.x[idx]).flatten()
            else:
                g.solution = torch.load(self.x[idx], weights_only=False).flatten()
            
        return g


def CreateExampleDatasets(train_test_split=[1000, 10, 200], size=100, 
                            train_path='./data/train', val_path='./data/val', 
                            test_path='./data/test'):
    
    os.makedirs(train_path, exist_ok=True)
    os.makedirs(val_path, exist_ok=True)
    os.makedirs(test_path, exist_ok=True)

    for i in range(max(train_test_split)):
        if i < train_test_split[0]:
            A, x, b = sparseRLS(size=size, solution_return=True, d='normal')
            torch.save(A, train_path+f'/{size}_{i}_A.pt')
            torch.save(torch.tensor(x, dtype=torch.float), train_path+f'/{size}_{i}_x.pt')
            torch.save(torch.tensor(b, dtype=torch.float), train_path+f'/{size}_{i}_b.pt')

        if i < train_test_split[1]:
            A, b = sparseRLS(size=size, d='normal')
            torch.save(A, val_path+f'/{size}_{i}_A.pt')
            torch.save(torch.tensor(b, dtype=torch.float), val_path+f'/{size}_{i}_b.pt')

        if i < train_test_split[2]:
            A, b = sparseRLS(size=size, d='normal')
            torch.save(A, test_path+f'/{size}_{i}_A.pt')
            torch.save(torch.tensor(b, dtype=torch.float), test_path+f'/{size}_{i}_b.pt')


def readA(path=None, size:int=1, n:int=1, suffix="pt"):
    files = list(
        filter(lambda x: x.split("/")[-1].split('_')[0] == str(size), glob(path+f"*_A.{suffix}"))
        )
    assert len(files) >= n, f"The number of files for A is smaller than the requested number:" \
                                        f"{len(files)} files found in {path} with matrix size={size}"
    
    return files[:n]


def readb(path=None, size:int=1, n:int=1, suffix="pt"):
    files = list(
        filter(lambda x: x.split("/")[-1].split('_')[0] == str(size), glob(path+f"*_b.{suffix}"))
        )
    assert len(files) >= n, f"The number of files for b is smaller than the requested number:" \
                                        f"{len(files)} files found in {path} with matrix size={size}"
    
    return files[:n]


def readx(path=None, size:int=1, n:int=1, suffix="pt"):
    files = list(
        filter(lambda x: x.split("/")[-1].split('_')[0] == str(size), glob(path+f"*_x.{suffix}"))
        )
    return files[:n]


def sparseRLS(size=100, d='normal', beta=1e-5, solution_return=False, 
                         ood=False, sparsity=1e-2, random_state=0, verbose=True,
                         lower=0.8, upper=1.2, lower_beta=1e-4, upper_beta=1e-2):
    
    rng = np.random.RandomState(random_state)
    
    if beta is None: beta = rng.uniform(lower_beta, upper_beta)
    
    # out of distribution samples
    if ood:  sparsity = rng.uniform(lower, upper) * sparsity 
    
    nnz = int(sparsity * (size ** 2)) # this is 1% sparsity for n = 10 000
    
    size_one_dim = int(np.round(np.sqrt(nnz)))
    
    rows = np.random.choice(size, size_one_dim, replace=True)
    cols = np.random.choice(size, size_one_dim, replace=True)
    carrs = np.array(np.meshgrid(rows[:nnz], cols[:nnz])).T.reshape(-1, 2) 

    if d == 'normal':
        vals = rng.standard_normal(nnz) 
    
    A = coo_matrix((vals, (carrs[:nnz, 0], carrs[:nnz, 1])), shape=(size, size))
    I = identity(size)
    
    A = (A @ A.T) + beta * I # create spd matrix in coo format

    if verbose:
        print("Create random matrix with approximately "
              "{:.3f}% non-zero elements".format(100 * A.nnz / size**2))
        
    b = rng.uniform(0, 1, size=(size, 1))
    
    if solution_return:
        x = scipy.sparse.linalg.spsolve(A, b)
        return A, x, b
    else:
        return A, b
    

def sparse_scipy_to_torch(A):
    if isinstance(A, _coo.coo_matrix):
        A = coo_matrix(A)

    row = torch.from_numpy(A.row.astype(np.int64)).to(torch.long)
    col = torch.from_numpy(A.col.astype(np.int64)).to(torch.long)
    edge_index = torch.stack([row, col], dim=0)

    #Presuming values are floats, can use np.int64 for dtype=int8
    val = torch.from_numpy(A.data.astype(np.float64)).to(torch.float)

    A = torch.sparse_coo_tensor(edge_index, val, torch.Size(A.shape)).to_dense() 
    return A



def sparse_torch_to_scipy(A, to_dense=True):
    if to_dense:
        return coo_matrix(A.to_dense()).toarray()

    else:
        return coo_matrix(A.to_dense())
