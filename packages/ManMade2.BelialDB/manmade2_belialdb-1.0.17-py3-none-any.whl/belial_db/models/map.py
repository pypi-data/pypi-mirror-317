from typing import Any, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .relationships import Base, MapAssetAssociation, MapAssetFileAssociation

if TYPE_CHECKING:
    from .asset import Asset
    from .asset_file import AssetFile


class Map(Base):
    """Represents a map in the database.

    Attributes:
        Id (int): The primary key for the map.
        Name (str): The name of the map.
        Assets (list[AssetModel]): A list of assets associated with the map.
        AssetFiles (list[AssetFileModel]): A list of asset files associated with the map.
    """

    __tablename__ = "maps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    assets: Mapped[list["Asset"]] = relationship(
        "Asset", secondary=MapAssetAssociation, back_populates="maps"
    )
    asset_files: Mapped[list["AssetFile"]] = relationship(
        "AssetFile", secondary=MapAssetFileAssociation, back_populates="maps"
    )

    def __eq__(self, other: Any):
        if not isinstance(other, Map):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"<Map(id={self.id}, name='{self.name}')>"
