from typing import Dict
from typing import List

from hip_online_store.ponyta.core import config
from hip_online_store.ponyta.online_store._ponyta_online_store_client import (
    _PonytaOnlineStore,
)
from hip_online_store.ponyta.registry._ponyta_registry_client import (
    _PonytaRegistry,
)
from loguru import logger


class PonytaClient:
    """
    The client is used to manage the databricks online feature store, which currently
    includes creation of online feature spec and table, and retrieval of features via
    postgres endpoint.

    The online tables are synced from the streaming sdc type 1 DLT
    The connection and setup is done via the databricks PAT + oauth token(linked to SPs)

    TODO: online store will need to do some test auth for databricks for init
    TODO: registry will need to do some test auth for databricks for init
    TODO: need to properly do the retrieval of similar users using vector store
    """

    def __init__(
        self,
        settings_config: config.Settings,
    ):
        """
        Initialise growlithe client

        Parameters
        ----------
        vs_endpoint_name: str = None
            name of vector search endpoint
        vs_index_name: str = None
            name of vector search index
        """

        self.settings_config = settings_config

        self.online_store_client = None
        if self.settings_config.DATABRICKS_CLUSTER_HOST not in ("", None, "test"):
            self.online_store_client = _PonytaOnlineStore(
                settings_config=self.settings_config,
            )
        self.registry = None
        if self.settings_config.DATABRICKS_CLUSTER_HOST not in ("", None, "test"):
            self.registry = _PonytaRegistry(settings_config=self.settings_config)

    def create_online_feature_table(
        self,
        primary_keys: List,
        source_table_name: str,
        online_table_name: str,
        timeout: int = 30,
        polling_step: int = 20,
        polling_max_tries: int = 90,
    ) -> int:
        """
        function to convert delta table to enable continuous or triggered sync

        Parameters
        ----------
        primary_keys: List
            list of primary keys for lookup
        source_table_name: str
            name of source table
        online_table_name: str
            name of online table to be created
        timeout: int = 30
            timeout duration of creating the online table, default 30 minutes
        polling_step: int = 20
            polling interval
        polling_max_tries: int = 90
            maximum number of tries for polling

        Returns
        ----------
        int
            return non exit value function
        """

        if self.online_store_client._create_online_table(
            primary_keys=primary_keys,
            source_table_name=source_table_name,
            online_table_name=online_table_name,
            timeout=timeout,
            polling_step=polling_step,
            polling_max_tries=polling_max_tries,
        ):
            logger.info(f"error in creating online table: {online_table_name}")

    def retrieve_features(
        self,
        which_perspective: str,
        filter_column: str,
        endpoint_url: str,
        columns_selection: Dict,
        primary_key_values_dict: Dict,
        accept_profile: str,
        oauth_token: str,
        limit_return: int = 1,
        similar_limit_return: int = 100,
        filter_selection: Dict = None,
        query_values_dict: Dict = None,
    ) -> Dict:
        """
        function to retrieve features from online table via postgres endpoint

        Parameters
        ----------
        which_perspective: str
            if features is tradie or job perspective
        filter_column: str
            check of column if its 0 activity
        online_table_name: str
            name of online table
        client_id: str
            oauth client id
        client_secret: str
            oauth client secret
        endpoint_url: str
            name of tradie online table url
        primary_key_values_dict: Dict
            dictionary that stores the primary keys
        accept_profile: str
            name of accept profile; schema of UC
        oauth_token: str
            oauth token
        limit_return: int = 1
            number of rows returned; default at 1
        filter_selection: Dict = None
            filter selection column dictionary
        query_values_dict: Dict = None
            query values dictionary
        similar_limit_return: int = 100


        Returns
        -------
        Dict
            return retrieved feature in dictionary
        """

        # retrieve features
        _features_dict = self.registry._retrieve_online_features_table_data_exact_match(
            endpoint_url=endpoint_url,
            columns_selection=columns_selection,
            primary_key_values_dict=primary_key_values_dict,
            accept_profile=accept_profile,
            oauth_token=oauth_token,
            limit_return=limit_return,
        )

        if (
            (which_perspective == "tradie")
            & (
                (_features_dict[filter_column] == 0)
                | (_features_dict[filter_column] > 2)
            )
        ) | (which_perspective != "tradie"):
            return _features_dict

        # check if the tradie has 0 activity
        if (which_perspective == "tradie") & (_features_dict[filter_column] == 0):
            # retrieve random active tradie
            _new_features_dict = self.registry._retrieve_online_features_table_data_active_tradies(  # noqa: E501
                endpoint_url=endpoint_url,
                filter_selection=filter_selection,
                query_values_dict=query_values_dict,
                accept_profile=accept_profile,
                oauth_token=oauth_token,
                limit_return=similar_limit_return,
            )

        return {
            "accountId": _features_dict["accountId"],
            "job_categoryId": _features_dict["job_categoryId"],
            "parent_category": _features_dict["parent_category"],
            "value_cap": _features_dict["value_cap"],
            "tenure_tradie": _features_dict["tenure_tradie"],
            "credit_available": _features_dict["credit_available"],
            **_new_features_dict,
        }
