import jax
from jax import numpy as jnp
from typing import Union, overload


@jax.tree_util.register_pytree_node_class
class Twist:
    def __init__(self, linear: jax.Array, angular: jax.Array, frame: str):
        if linear.shape != (3, 1):
            raise ValueError(
                f"Expected linear velocity to have shape (3, 1) got {linear.shape}"
            )
        if angular.shape != (3, 1):
            raise ValueError(
                f"Expected angular velocity to have shape (3, 1), got {angular.shape}"
            )

        self.linear = linear
        self.angular = angular
        self.frame = frame

    def tree_flatten(self):
        return (
            self.linear,
            self.angular,
        ), (self.frame,)

    @classmethod
    def tree_unflatten(cls, aux_data, children):
        (frame,) = aux_data
        (
            linear,
            angular,
        ) = children
        return cls(linear, angular, frame)

    def __repr__(self):
        # Transpose to row vectors for cleaner printing
        return f"Twist(angular={self.angular.T}, linear={self.linear.T}, frame={self.frame})"
