import torch
import logging
from glob import glob
from .errors import *
from .models.models import *
from .transform import graph_to_matrix, matrix_to_graph
from .losses import Loss

from .conditioner import *
import torch_geometric
from torch_geometric.loader import DataLoader
from .models.optimizers import get_optimizer
from .models.callbacks import EarlyStopping
from tqdm import tqdm

class DeepNPG:
    def __init__(self, optimizer:str=None, loss:Loss=None, **kwargs):
        logging.basicConfig()
        self.log = logging.getLogger(__file__)
        self.optimizer = optimizer

        self.kwargs = kwargs
        self.method = self.kwargs.get("method",  None)
        
        if loss is None:
            if self.method is None:
                self.loss = loss if loss is not None else Loss(method="frobenius")
            
            elif self.method in {"nif", "npcg", "pcnt"}:
                self.loss = Loss(method="sketched")

            elif self.method == "llu":
                self.loss = Loss(method="supervised")
            
            else:
                self.loss = Loss(method="frobenius")
        else:
            self.loss = loss

        self.model = self.kwargs.get("model", None)
        self.best_val_model_params = None
        self.verbose = self.kwargs.get("verbose", 1)
        self.random_state = self.kwargs.get("random_state", 42)
        self.seeding(self.random_state)
        self.check_deepnpc_params()


    def train(self, data, val_data=None, train_val_split=[0.8, 0.2], num_epochs=10, learning_rate=0.01, 
              callback=None, early_stopping=False, optim_params:dict={}, model_params:dict={}, device:str="cpu", 
              val_num:int=100, **kwargs):

        device_id = kwargs.get("device_id", 0)

        batch_size = kwargs.get("batch_size", 2)
        disable_solution = kwargs.get("disable_solution", True)
        validate_with_solver = kwargs.get("validate_with_solver", False)

        solver = kwargs.get("solver", None)
        if validate_with_solver:
            if solver is None:
                raise ParameterMissingError("Please specify a parameter for solver if `validate_with_solver` is set to True.")

        if early_stopping == True:
            if callback is None:
                patience = kwargs.get("patience", 10)
                min_delta = kwargs.get("min_delta", 2)
                callback = EarlyStopping(patience=patience, min_delta=min_delta)
            
 
        optim_params["lr"] = learning_rate
        optim_params["scheduler"] = kwargs.get("scheduler", None)
        optim_params["scheduler_params"] = kwargs.get("scheduler_params", {})

        self.model_params = model_params

        if device != "cpu":
            device = torch.device(f"cuda:{device_id}" if torch.cuda.is_available() else "cpu")

            if device == "cpu":
                self.log.warning("No available GPU for training, the training will use CPU instead.")

        if self.model is None:
            if self.method == "nif":
                self.model = NeuralIF(**self.model_params)

            elif self.method == "npcg":
                self.model = NeuralPCG(**self.model_params)

            elif self.method == "pcnt":
                self.model = PreCondNet(**self.model_params)

            elif self.method == "llu":
                self.model = LearnedLU(**self.model_params)

            else:
                raise ModelMissingError("Model missing, please enter an valid method.")

        else:
            self.model = self.model(**self.model_params)

        optim, scheduler = get_optimizer(self.model.parameters(), self.optimizer, **optim_params)
        self.model.to(device)
        best_val_score = float("inf")

        if val_data is None:
            train_data, val_data = torch.utils.data.random_split(data, train_val_split)
            train_data = DataLoader(train_data, batch_size=batch_size, shuffle=True)
        else:    
            train_data = DataLoader(data, batch_size=batch_size, shuffle=True)

        val_data = DataLoader(val_data, batch_size=1, shuffle=False)
    
        for epoch in range(num_epochs):
            running_loss = 0.0

            for batch_idx, batch_data in tqdm(enumerate(train_data)):
                self.model.train()
                
                batch_data = batch_data.to(device)
                
                output, reg, _ = self.model(batch_data)

                if hasattr(batch_data, 'solution') and not disable_solution:
                    loss = self.loss(output, batch_data, x=batch_data.solution, c=reg)

                else:
                    loss = self.loss(output, batch_data, c=reg)
                
                loss.backward()
                running_loss += loss.item()
                
                optim.step()
                optim.zero_grad()
            
                if (batch_idx + 1) % val_num == 0:
                    val_score = self.validate(obj=self, model=self.model, data=val_data, 
                                                        validate_with_solver=validate_with_solver, device=device,
                                                        solver=solver)
                    
                    if val_score < best_val_score:
                        self.best_val_model_weights = self.model.state_dict()
                
                    best_val_score = val_score

                    if early_stopping:
                        if callback(val_score):
                            break

            if scheduler is not None:
                scheduler.step()

            if self.verbose:
                print(f"Epoch {epoch+1}: loss - {loss.item()}, best model score - {best_val_score}")
        
        self.fitted_model = True


    @staticmethod
    def validate(obj:"DeepNPC", model, data, validate_with_solver=False, solver=None, **kwargs):
        device = kwargs.get("device", "cpu")
        model.eval()
        model.to(device)
        
        total_loss = 0.0
       
        with torch.no_grad():
            for batch_idx, batch_data in enumerate(data):
                batch_data = batch_data.to(device)
                
                A = graph_to_matrix(batch_data)
                b = batch_data.x[:, 0].view(-1,1)

                if validate_with_solver:
                    with torch.inference_mode():
                        if obj.method is not None:
                            if obj.method in {"nif", "npcg", "pcnt"}:
                                preconditioner = NIFPreconditioner(model)
                            elif obj.method == "llu":
                                preconditioner = LUPreconditioner(model)
                    
                    
                    A = A.to("cpu").to(torch.float64)
                    b = b.to("cpu").to(torch.float64)
                    
                    preconditioner.build(batch_data)
                    loss = solver(A=A, b=b, preconditioner=preconditioner)
                    total_loss = total_loss + loss
                
                else:
                    output, _, _ = model(batch_data)
                    loss = obj.loss(output, batch_data)
                    total_loss = total_loss + loss.item()
        
        return total_loss
    

    def __call__(self, x=None):
        return self.inference(x=x)


    def build(self, A, node_feats=None):
        if not hasattr(self, "model"):
            self.log.warning("Please train model first or load an existing trained model.")
            return

        if self.method is not None:
            if self.method in {"nif", "npcg", "pcnt"}:
                self.preconditioner = NIFPreconditioner(self.model)

            elif self.method == "llu":
                self.preconditioner = LUPreconditioner(self.model)

        if not isinstance(A, torch_geometric.data.data.Data):
            A = matrix_to_graph(A, node_feats=node_feats, return_graph_feats=False)

        self.preconditioner.build(A)


    def inference(self, mode=None, x=None):
        if not hasattr(self, "preconditioner"):
            self.log.warning("Please build the proconditioner first via the method `.build`.")
            return

        if mode == 1:
            if x is None:
                raise ValueError("Invalid value of x.")

            return self.preconditioner(x)

        elif mode == 2:
            return self.preconditioner.compute_inverse_P()
        
        elif mode == 3:
            return self.preconditioner.compute_P()
        
        else: #if mode == 'factors':
            return self.preconditioner.compute_factors()


    def load_model(self, load_best:bool=True, path:str=None, device:str="cpu"):
        from pickle import load
        params_files = glob(f"{path}/{self.method}_model_params.pt")
        weights_files = glob(f"{path}/{self.method}_model_weights.pt")

        if load_best:
            if len(params_files) == 0:
                raise FileMissingError('Cannot find target model parameters file.')
            
            if len(weights_files) == 0:
                raise FileMissingError('Cannot find target model weights file.')
            
            with open(f"{path}/{self.method}_model_params.pt", "rb") as f:
                self.model_params = load(f)

            if self.method == "nif":
                self.model = NeuralIF(**self.model_params)
     
            self.model.load_state_dict(torch.load(weights_files[0], weights_only=False, map_location=torch.device(device)))

        else:
            if len(params_files) == 0:
                raise FileMissingError('Cannot find target model parameters file.')
            
            if len(weights_files) == 0:
                raise FileMissingError('Cannot find target model weights file.')
            
            with open(f"{path}/{self.method}_model_params.pt", "rb") as f:
                self.model_params = load(f)

            if self.method == "nif":
                self.model = NeuralIF(**self.model_params)
     
            self.model.load_state_dict(torch.load(weights_files[0], weights_only=False, map_location=torch.device(device)))
        

        
    def save_model(self, save_best:bool=True, path:str=None):
        from pickle import dump

        if not hasattr(self, "model"):
            self.log.warning("Please train model first or load an existing trained model.")

        try:
            with open(f"{path}/{self.method}_model_params.pt", "wb") as f:
                dump(self.model_params, f)

            if save_best and hasattr(self, "best_val_model_weights"):
                torch.save(self.best_val_model_weights, f"{path}/{self.method}_best_model_weights.pt")
                
            else:
                self.log.warning("The best model is missing, please ensure the trainning setting is proper. Save final model instead.")
                torch.save(self.model.state_dict(), f"{path}/{self.method}_model_weights.pt")

            self.log.info('model saving succeeds.')

        except:
            self.log.warning("model saving fails.")

    

    def check_deepnpc_params(self):
        args = self.__dict__
        if args['optimizer'] is None:
            raise ValueError('optimizer parameter must be a string or class, None value is not permitted.')
        


    def seeding(self, seed:int=0) -> None:
        """Sets the seed for generating random numbers in :pytorch:`PyTorch`,
        :obj:`numpy` and :python:`Python`.

        Args:
            seed (int): The desired seed.
        """
        import random, numpy
        random.seed(seed)
        numpy.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)