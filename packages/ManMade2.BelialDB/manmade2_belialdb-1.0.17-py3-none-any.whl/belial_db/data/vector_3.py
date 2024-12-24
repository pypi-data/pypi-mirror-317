from pydantic import BaseModel


class Vector3(BaseModel):
    """
    A class to represent a 3D vector.

    Attributes:
        x (float): The x-coordinate of the vector.
        y (float): The y-coordinate of the vector.
        z (float): The z-coordinate of the vector.
    """

    x: float
    y: float
    z: float
