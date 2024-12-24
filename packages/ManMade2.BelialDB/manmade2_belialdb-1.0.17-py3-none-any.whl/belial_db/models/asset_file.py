from typing import Any, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .relationships import Base, MapAssetFileAssociation

if TYPE_CHECKING:
    from .map import Map


class AssetFile(Base):
    """
    Represents an asset file in the database.

    Attributes:
        id (int): The primary key for the asset file.
        path (str): The file path of the asset.
        type (str): The type of the asset.
        doodad_set_index (int): The index of the doodad set.
        doodad_set_names (str): The names of the doodad sets.
        map_id (int): The foreign key referencing the associated map.
        map (Mapped[MapModel]): The relationship to the MapModel.
    """

    __tablename__ = "asset_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    doodad_set_index: Mapped[int] = mapped_column(Integer, nullable=False)
    doodad_set_names: Mapped[str] = mapped_column(String, nullable=True)

    maps: Mapped[list["Map"]] = relationship(
        "Map", secondary=MapAssetFileAssociation, back_populates="asset_files"
    )

    def __eq__(self, other: Any):
        if not isinstance(other, AssetFile):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"<AssetFile(id={self.id}, path='{self.path}', type='{self.type}', doodad_set_index={self.doodad_set_index})>"
