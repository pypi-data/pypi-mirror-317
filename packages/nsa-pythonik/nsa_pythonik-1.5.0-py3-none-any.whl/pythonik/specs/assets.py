from typing import Union, Dict, Any

from pythonik.models.assets.assets import Asset, AssetCreate, BulkDelete
from pythonik.models.assets.segments import SegmentBody, SegmentResponse
from pythonik.models.assets.versions import (
    AssetVersionCreate,
    AssetVersionResponse,
    AssetVersionFromAssetCreate,
)
from pythonik.models.base import Response
from pythonik.specs.base import Spec
from pythonik.specs.collection import CollectionSpec

BASE = "assets"
DELETE_QUEUE = "delete_queue"
GET_URL = BASE + "/{}/"
SEGMENT_URL = BASE + "/{}/segments/"
SEGMENT_URL_UPDATE = SEGMENT_URL + "{}/"
VERSIONS_URL = BASE + "/{}/versions/"
VERSIONS_FROM_ASSET_URL = BASE + "/{}/versions/from/assets/{}/"
BULK_DELETE_URL = DELETE_QUEUE + "/bulk/"
PURGE_ALL_URL = DELETE_QUEUE + "/purge/all/"


class AssetSpec(Spec):
    server = "API/assets/"

    def __init__(self, session, timeout=3, base_url: str ="https://app.iconik.io"):
        self._collection_spec = CollectionSpec(session=session, timeout=timeout)
        return super().__init__(session, timeout, base_url)

    @property
    def collections(self) -> CollectionSpec:
        """
        Access the collections API

        Returns:
            CollectionSpec: An instance of CollectionSpec for working with collections
        """
        return self._collection_spec

    def permanently_delete(self, **kwargs) -> Response:
        """
        Purge all assets and collections from the delete queue (Permanently delete)

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response with no data model (202 status code)

        Required roles:
            - can_purge_assets
            - can_purge_collections

        Raises:
            401 Invalid token
            403 User does not have permission
        """
        response = self._post(PURGE_ALL_URL, **kwargs)
        return self.parse_response(response, model=None)

    def bulk_delete(
        self,
        body: Union[BulkDelete, Dict[str, Any]],
        permanently_delete=False,
        exclude_defaults: bool = True,
        **kwargs
    ) -> Response:
        """
        Bulk delete objects. If `permanently_delete` is True, the objects are
        first added to the delete queue then the queue is purged,
        permanently deleting.

        Args:
            body: Bulk delete parameters, either as BulkDelete model or dict
            permanently_delete: If True, Purge all assets and collections from
                delete queue (Permanently delete)
            exclude_defaults: Whether to exclude default values when dumping Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response with no data model (202 status code)

        Required roles:
            - To bulk delete objects:
                - can_delete_assets
            - To permanently delete objects:
                - can_purge_assets
                - can_purge_collections

        Raises:
            400 Bad request
            401 Invalid token
            403 User does not have permission
        """
        json_data = self._prepare_model_data(body, exclude_defaults=exclude_defaults)
        response = self._post(
            BULK_DELETE_URL,
            json=json_data,
            **kwargs
        )
        if permanently_delete:
            response = self.permanently_delete().response
        return self.parse_response(response, model=None)

    def partial_update_asset(
        self,
        asset_id: str,
        body: Union[Asset, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs
    ) -> Response:
        """Partially update an asset using PATCH
        
        Args:
            asset_id: The asset ID to update
            body: Asset data to update, either as Asset model or dict
            exclude_defaults: Whether to exclude default values when dumping Pydantic models
            **kwargs: Additional kwargs to pass to the request
        """
        json_data = self._prepare_model_data(body, exclude_defaults=exclude_defaults)
        response = self._patch(
            GET_URL.format(asset_id),
            json=json_data,
            **kwargs
        )
        return self.parse_response(response, Asset)

    def get(self, asset_id: str, **kwargs) -> Response:
        """
        Get an iconik asset by id
        
        Args:
            asset_id: The asset ID to get
            **kwargs: Additional kwargs to pass to the request
            
        Returns: Response(model=Asset)
        """
        resp = self._get(GET_URL.format(asset_id), **kwargs)
        return self.parse_response(resp, Asset)

    def create(
        self,
        body: Union[AssetCreate, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs
    ) -> Response:
        """
        Create a new asset
        
        Args:
            body: Asset creation parameters, either as AssetCreate model or dict
            exclude_defaults: Whether to exclude default values when dumping Pydantic models
            **kwargs: Additional kwargs to pass to the request
            
        Returns: Response(model=Asset)
        """
        json_data = self._prepare_model_data(body, exclude_defaults=exclude_defaults)
        response = self._post(
            BASE,
            json=json_data,
            **kwargs
        )
        return self.parse_response(response, Asset)

    def create_segment(
        self,
        asset_id: str,
        body: Union[SegmentBody, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs
    ) -> Response:
        """
        Create a segment on an asset, such as a comment
        
        Args:
            asset_id: The asset ID to create segment for
            body: Segment data, either as SegmentBody model or dict
            exclude_defaults: Whether to exclude default values when dumping Pydantic models
            **kwargs: Additional kwargs to pass to the request
        """
        json_data = self._prepare_model_data(body, exclude_defaults=exclude_defaults)
        resp = self._post(
            SEGMENT_URL.format(asset_id),
            json=json_data,
            **kwargs
        )

        return self.parse_response(resp, SegmentResponse)

    def update_segment(
        self,
        asset_id: str,
        segment_id: str,
        body: Union[SegmentBody, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs
    ) -> Response:
        """
        Update a segment on an asset
        
        Args:
            asset_id: The asset ID to update segment for
            segment_id: The segment ID to update
            body: Segment data, either as SegmentBody model or dict
            exclude_defaults: Whether to exclude default values when dumping Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Note:
            Full Representation: A PUT request requires a complete representation of the segment.
            If you want to update only specific fields, use partial_update_segment instead.
        """
        json_data = self._prepare_model_data(body, exclude_defaults=exclude_defaults)
        resp = self._put(
            SEGMENT_URL_UPDATE.format(asset_id, segment_id),
            json=json_data,
            **kwargs
        )

        return self.parse_response(resp, SegmentResponse)

    def partial_update_segment(
        self,
        asset_id: str,
        segment_id: str,
        body: Union[SegmentBody, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs
    ) -> Response:
        """
        Partially update a segment on an asset
        
        Args:
            asset_id: The asset ID to update segment for
            segment_id: The segment ID to update
            body: Segment data, either as SegmentBody model or dict
            exclude_defaults: Whether to exclude default values when dumping Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Note:
            Sparse Representation: A PATCH request typically contains only the fields that need to be modified.
        """
        json_data = self._prepare_model_data(body, exclude_defaults=exclude_defaults)
        resp = self._patch(
            SEGMENT_URL_UPDATE.format(asset_id, segment_id),
            json=json_data,
            **kwargs
        )

        return self.parse_response(resp, SegmentResponse)

    def create_version(
        self,
        asset_id: str,
        body: Union[AssetVersionCreate, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs
    ) -> Response:
        """
        Create a new version of an asset
        
        Args:
            asset_id: The ID of the asset to create a version for
            body: Version creation parameters, either as AssetVersionCreate model or dict
            exclude_defaults: Whether to exclude default values when dumping Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response[AssetVersionResponse]

        Required roles:
            - can_write_versions
        """
        json_data = self._prepare_model_data(body, exclude_defaults=exclude_defaults)
        response = self._post(
            VERSIONS_URL.format(asset_id),
            json=json_data,
            **kwargs
        )
        return self.parse_response(response, AssetVersionResponse)

    def create_version_from_asset(
        self,
        asset_id: str,
        source_asset_id: str,
        body: Union[AssetVersionFromAssetCreate, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs
    ) -> Response:
        """
        Create a new version of an asset from another asset
        
        Args:
            asset_id: The ID of the asset to create a version for
            source_asset_id: The ID of the source asset to create version from
            body: Version creation parameters, either as AssetVersionFromAssetCreate model or dict
            exclude_defaults: Whether to exclude default values when dumping Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response with no data model (202 status code)

        Required roles:
            - can_write_versions

        Raises:
            - 400: Bad request
            - 401: Invalid token
            - 403: User does not have permission
            - 404: Source or destination asset does not exist
            - 409: The asset is being transcoded and cannot be set as a new version
        """
        json_data = self._prepare_model_data(body, exclude_defaults=exclude_defaults)
        response = self._post(
            VERSIONS_FROM_ASSET_URL.format(asset_id, source_asset_id),
            json=json_data,
            **kwargs
        )
        # Since this returns 202 with no content, we don't need a response model
        return self.parse_response(response, None)
