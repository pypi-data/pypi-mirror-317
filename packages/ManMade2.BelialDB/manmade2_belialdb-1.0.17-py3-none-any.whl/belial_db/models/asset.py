from typing import Any, TYPE_CHECKING
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .relationships import Base, MapAssetAssociation
from .vector_3_type import Vector3Type
from .vector_4_type import Vector4Type

if TYPE_CHECKING:
    from .map import Map


class Asset(Base):
    """Represents an asset in the game.

    Attributes:
        id (int): The primary key for the asset.
        asset_file_id (int): The ID of the associated asset file.
        path (str): The file path of the asset.
        type (str): The type of the asset (e.g., model, texture).
        scale_factor (float): The scale factor for the asset.
        position (Vector3Type): The 3D position of the asset in the game world.
        rotation (Vector4Type): The rotation of the asset represented as a quaternion.
        map_id (int): The ID of the map where the asset is located.
        map (MapModel): The map model associated with this asset.
    """

    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_file_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    scale_factor: Mapped[float] = mapped_column(Float(), nullable=False)
    position: Mapped[Vector3Type] = mapped_column(Vector3Type, nullable=False)
    rotation: Mapped[Vector4Type] = mapped_column(Vector4Type, nullable=False)

    maps: Mapped[list["Map"]] = relationship("Map", secondary=MapAssetAssociation, back_populates="assets")

    def __eq__(self, other: Any):
        if not isinstance(other, Asset):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return (
            f"<Asset(id={self.id}, path='{self.path}', type='{self.type}', scale_factor={self.scale_factor})>"
        )
