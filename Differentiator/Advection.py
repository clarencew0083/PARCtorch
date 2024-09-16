# Differentiator/Advection.py

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from .FiniteDifference import FiniteDifference

class Advection(nn.Module):
    """
    Computes the advection term based on the state variable and velocity field.
    
    Args:
        finite_difference_method (nn.Module): Numerical method to calculate spatial deriviatives
    """
    def __init__(self, finite_difference_method):
        super(Advection, self).__init__()
        self.cdiff = finite_difference_method

    def forward(self, state_variable, velocity_field):
        """
        Forward pass to compute advection.
        
        Args:
            state_variable (torch.Tensor): Tensor of shape [N, C, H, W]
            velocity_field (torch.Tensor): Tensor of shape [N, 2C, H-1, W-1]
        
        Returns:
            advect (torch.Tensor): Advection term of shape [N, 1, H-1, W-1]
        """
        dy, dx = self.cdiff(state_variable)  # Each of shape [N, C, H-1, W-1]
        spatial_deriv = torch.cat([dx, dy], dim=1)  # Concatenate along channel dimension: [N, 2C, H-1, W-1]
        advect = torch.sum(spatial_deriv * velocity_field, dim=1, keepdim=True)  # [N, 1, H-1, W-1]
        return advect
