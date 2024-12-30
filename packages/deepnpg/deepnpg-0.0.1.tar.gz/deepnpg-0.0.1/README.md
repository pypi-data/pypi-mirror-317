# DeepNPG: Deep Neural Preconditioner with Graph Neural Networks

``DeepNPG`` is a Python library for building preconditiioner with Graph Neural Networks. It provides straightforward interfaces to convert matrix into graph and perform efficient neural network training.

All data (e.g., ``numpy.ndarray``, ``spicpy.sparse.csc/csr/bsr``) will be automatically converted into sparse COOrdinate format (COO format), and then to gemetric data format.
