from typing import List, Optional
import numpy as np
from .optimizer import Optimizer


class Adamax(Optimizer):
    """
    Adamax optimizer for adaptive gradient updates.

    This optimizer adapts the learning rates individually for each parameter.

    Parameters:
    -----------
    beta1 : float, optional
        Exponential decay rate for the first moment estimates. Default is 0.9.
    beta2 : float, optional
        Exponential decay rate for the infinite norm estimates. Default is 0.999.
    epsilon : float, optional
        A small constant added to prevent division by zero. Default is 1e-8.
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
    beta1 : float
        Exponential decay rate for the first moment estimates.
    beta2 : float
        Exponential decay rate for the infinite norm estimates.
    epsilon : float
        A small constant added to prevent division by zero.
    first_moments : list of arrays or None
        First moment estimates, initialized to None.
    second_moments : list of arrays or None
        Second moment estimates, initialized to None.
    time_step : int
        Time step.

    Methods:
    --------
    update(parameters, gradients)
        Update the parameters using the Adamax algorithm.

    """
    def __init__(self, beta1: float = 0.9, beta2: float = 0.999, epsilon: float = 1e-8, *args, **kwargs):
        """
        Initialize the Adamax optimizer with hyperparameters.

        Parameters:
        -----------
        beta1 : float, optional
            Exponential decay rate for the first moment estimates. Default is 0.9.
        beta2 : float, optional
            Exponential decay rate for the infinite norm estimates. Default is 0.999.
        epsilon : float, optional
            A small constant added to prevent division by zero. Default is 1e-8.
        *args, **kwargs
            Additional arguments passed to the base class Optimizer.

        """
        self.beta1: float = beta1
        self.beta2: float = beta2
        self.epsilon: float = epsilon
        self.first_moments: Optional[List[np.ndarray]] = None
        self.second_moments: Optional[List[np.ndarray]] = None
        self.time_step: int = 0
        super().__init__(*args, **kwargs)

    def update(self, parameters: List[np.ndarray], gradients: List[np.ndarray]) -> List[np.ndarray]:
        """
        Update the parameters using the Adamax algorithm.

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
        self.time_step += 1

        # Compute the bias-corrected learning rate
        adjusted_learning_rate = self.learning_rate / (1 - self.beta1 ** self.time_step)

        if self.first_moments is None:
            self.first_moments = [np.zeros(shape=parameter.shape, dtype=float) for parameter in parameters]

        if self.second_moments is None:
            self.second_moments = [np.zeros(shape=parameter.shape, dtype=float) for parameter in parameters]

        updated_parameters = []
        for i, (first_moment, second_moment, parameter, gradient) in enumerate(zip(self.first_moments, self.second_moments, parameters, gradients)):
            # Update first moment estimate: first_moment = beta1 * first_moment + (1 - beta1) * gradient
            first_moment = self.beta1 * first_moment + (1 - self.beta1) * gradient

            # Update second moment estimate: second_moment = max(beta2 * second_moment, abs(gradient))
            second_moment = np.maximum(self.beta2 * second_moment, np.abs(gradient))

            # Update parameter: parameter -= adjusted_learning_rate * first_moment / (second_moment + epsilon)
            parameter -= adjusted_learning_rate * first_moment / (second_moment + self.epsilon)

            # Update attributes
            self.first_moments[i] = first_moment
            self.second_moments[i] = second_moment
            updated_parameters.append(parameter)

        return updated_parameters
