from sqlalchemy import Engine
from sqlalchemy.orm import Session

from belial_db.models import AssetModel, MapModel


class AssetRepo:
    """
    Repository for managing assets in the database.
    """

    def __init__(self, engine: Engine):
        """
        Initializes the AssetRepo with a database engine.

        :param engine: SQLAlchemy Engine instance for database connection.
        """
        self._engine = engine

    def get_asset(self, id: int) -> AssetModel | None:
        """
        Retrieves an asset by its ID.

        :param id: The ID of the asset to retrieve.
        :return: The AssetModel instance if found, otherwise None.
        """
        with Session(self._engine) as session:
            return session.query(AssetModel).filter(AssetModel.id == id).first()

    def get_assets(self, map_id: int) -> list[AssetModel]:
        """
        Retrieves all assets linked with a specific map.

        :param map_id: The ID of the map to retrieve assets for.
        :return: A list of AssetModel instances linked with the specified map.
        """
        with Session(self._engine) as session:
            return session.query(AssetModel).join(AssetModel.maps).filter(MapModel.id == map_id).all()

    def create_asset(self, asset: AssetModel) -> AssetModel:
        """
        Creates a new asset in the database.

        :param asset: The AssetModel instance to create.
        :return: The created AssetModel instance.
        """
        with Session(self._engine) as session:
            session.add(asset)
            session.commit()
            return asset

    def update_asset(self, asset: AssetModel) -> AssetModel:
        """
        Updates an existing asset in the database.

        :param asset: The AssetModel instance to update.
        :return: The updated AssetModel instance.
        """
        with Session(self._engine) as session:
            session.merge(asset)
            session.commit()
            return asset

    def delete_asset(self, id: int) -> None:
        """
        Deletes an asset by its ID.

        :param id: The ID of the asset to delete.
        """
        with Session(self._engine) as session:
            asset = session.query(AssetModel).filter(AssetModel.id == id).first()
            if asset:
                session.delete(asset)
                session.commit()
