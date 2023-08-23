from typing import List, Optional
import numpy as np
from .optimizer import Optimizer


class Momentum(Optimizer):
    """
    Momentum optimizer for accelerating gradient descent.

    This optimizer uses momentum to accelerate the convergence of gradient descent.

    Parameters:
    -----------
    momentum : float, optional
        The momentum coefficient. Default is 0.9.
    learning_rate : float, optional
        The learning rate controlling the step size of parameter updates. Default is 1e-3.
    decay : float, optional
        The learning rate decay factor applied at the end of each epoch. Default is 0.
    lr_min : float, optional
        The minimum allowed learning rate after decay. Default is 0.
    lr_max : float, optional
        The maximum allowed learning rate after decay. Default is np.inf.
    *args, **kwargs
        Additional arguments passed to the base class Optimizer.

    Attributes:
    -----------
    momentum : float
        The momentum coefficient.
    velocity : list of arrays or None
        The velocity of each parameter's update, initialized to None.

    Methods:
    --------
    update(parameters, gradients)
        Update the parameters using the momentum-based gradient descent algorithm.

    """
    def __init__(self, momentum: float = 0.9, *args, **kwargs):
        """
        Initialize the Momentum optimizer with hyperparameters.

        Parameters:
        -----------
        momentum : float, optional
            The momentum coefficient. Default is 0.9.
        *args, **kwargs
            Additional arguments passed to the base class Optimizer.

        """
        self.momentum: float = momentum
        self.velocity: Optional[List[np.ndarray]] = None
        super().__init__(*args, **kwargs)

    def update(self, parameters: List[np.ndarray], gradients: List[np.ndarray]) -> List[np.ndarray]:
        """
        Update the parameters using the momentum-based gradient descent algorithm.

        Parameters:
        -----------
        parameters : list of arrays
            List of parameter arrays to be updated.
        gradients : list of arrays
            List of gradient arrays corresponding to the parameters.

        Returns:
        --------
        updated_parameters : list of arrays
            List of updated parameter arrays.

        """
        if self.velocity is None:
            self.velocity = [np.zeros(shape=parameter.shape, dtype=float) for parameter in parameters]

        updated_parameters = []
        for i, (velocity, parameter, gradient) in enumerate(zip(self.velocity, parameters, gradients)):
            velocity = self.momentum * velocity - self.learning_rate * gradient
            parameter += velocity
            self.velocity[i] = velocity
            updated_parameters.append(parameter)

        return updated_parameters