import torch
from torch import float as TFLOAT
from torch import long as TLONG 
from torch import sparse_coo_tensor
import numpy as np
from scipy.sparse import coo_matrix, _coo, isspmatrix
from torch_geometric.data import Data as Graph

def matrix_to_graph(A, node_feats=None, return_graph_feats=False):
     
    if isinstance(A, np.ndarray): # for numpy array
        A = coo_matrix(A)
        
    if not isspmatrix(A): # for scipy sparse format, e.g., csr_matrix, bsr_matrix, csc_matrix, coo_matrix, dia_matri
        A = coo_matrix(A)

    if isspmatrix(A) and (not isinstance(A, _coo.coo_matrix)): # for non coo format
        A = A.tocoo()

        ## add torch type check
        
    edge_index = torch.tensor(
            list(map(lambda x: [x[0], x[1]], zip(A.row, A.col))), 
        dtype=TLONG)
    
    edge_feats = torch.tensor(list(map(lambda x: [x], A.data)), dtype=TFLOAT) 

    if node_feats is not None:
        if len(node_feats.shape) == 1: # 2-D torch tensor
            node_feats = torch.tensor(list(map(lambda x: [x], node_feats)), dtype=TFLOAT)
        else:
            node_feats = torch.tensor(list(map(lambda x: x, node_feats)), dtype=TFLOAT)
            
    if return_graph_feats:
        return edge_index, edge_feats, node_feats
    else:
        return Graph(x=node_feats, edge_index=edge_index.t().contiguous(), edge_attr=edge_feats)


def graph_to_matrix(A, to_dense=False):
    if to_dense:
        return sparse_coo_tensor(A.edge_index, A.edge_attr[:, 0].squeeze(), requires_grad=False).to_dense()
    else:
        return sparse_coo_tensor(A.edge_index, A.edge_attr[:, 0].squeeze(), requires_grad=False)