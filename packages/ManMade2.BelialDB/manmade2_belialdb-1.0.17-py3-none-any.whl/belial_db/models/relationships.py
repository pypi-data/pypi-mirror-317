"""
This module defines the relationships between different database models
using SQLAlchemy. It includes associations for maps, assets, and asset files.
"""

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base

Base = declarative_base()

MapAssetAssociation = Table(
    "map_asset_association",
    Base.metadata,
    Column("map_id", Integer, ForeignKey("maps.id"), primary_key=True),
    Column("asset_id", Integer, ForeignKey("assets.id"), primary_key=True),
)

MapAssetFileAssociation = Table(
    "map_assetfile_association",
    Base.metadata,
    Column("map_id", Integer, ForeignKey("maps.id"), primary_key=True),
    Column("asset_file_id", Integer, ForeignKey("asset_files.id"), primary_key=True),
)
