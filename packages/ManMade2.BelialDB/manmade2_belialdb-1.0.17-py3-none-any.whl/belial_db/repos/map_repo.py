from sqlalchemy import Engine
from sqlalchemy.orm import Session, subqueryload

from belial_db.models import MapModel, AssetModel, AssetFileModel


class MapRepo:
    def __init__(self, engine: Engine):
        """Initialize the MapRepo with a SQLAlchemy engine.

        Args:
            engine (Engine): The SQLAlchemy engine to connect to the database.
        """
        self._engine = engine

    def get_map(self, id: int, include_assets: bool = False) -> MapModel | None:
        """Retrieve a map by its ID, optionally including assets and asset files.

        Args:
            id (int): The ID of the map to retrieve.
            include_assets (bool): Whether to include assets and asset files.

        Returns:
            MapModel | None: The map model if found, otherwise None.
        """
        with Session(self._engine) as session:
            query = session.query(MapModel).filter(MapModel.id == id)
            if include_assets:
                query = query.options(subqueryload(MapModel.assets), subqueryload(MapModel.asset_files))
            return query.first()

    def create_map(self, map: MapModel) -> MapModel:
        """Create a new map in the database.

        Args:
            map (MapModel): The map model to create.

        Returns:
            MapModel: The created map model.
        """
        with Session(self._engine) as session:
            new_assets: list[AssetModel] = []

            for asset in map.assets:
                existing_asset = session.query(AssetModel).filter(AssetModel.id == asset.id).first()
                if existing_asset is None:
                    new_assets.append(asset)

            new_files: list[AssetFileModel] = []

            for file in map.asset_files:
                existing_files = session.query(AssetFileModel).filter(AssetFileModel.id == file.id).first()
                if existing_files is None:
                    new_files.append(file)

            print(f"Adding {len(new_assets)} new assets.")
            print(f"Adding {len(new_files)} new files.")

            map.assets = new_assets
            map.asset_files = new_files
            session.add(map)
            session.commit()
            return map

    def update_map(self, map: MapModel) -> MapModel:
        """Update an existing map in the database.

        Args:
            map (MapModel): The map model to update.

        Returns:
            MapModel: The updated map model.
        """
        with Session(self._engine) as session:
            session.merge(map)
            session.commit()
            return map

    def delete_map(self, id: int) -> None:
        """Delete a map from the database by its ID.

        Args:
            id (int): The ID of the map to delete.
        """
        with Session(self._engine) as session:
            session.query(MapModel).filter(MapModel.id == id).delete()
            session.commit()
