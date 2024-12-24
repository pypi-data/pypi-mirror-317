import random
from typing import Dict

import requests
from databricks.sdk import WorkspaceClient
from hip_online_store.ponyta.common.request_utils import _define_request_headers
from hip_online_store.ponyta.core import config
from loguru import logger


class _PonytaRegistry:
    """
    The registry client is a wrapper for the databricks python libraries.
    Here, we mainly deal with the creation of the online table, read
    of online tables, and retrieving similar tradies

    TODO: add similarity lookup of tradies
    """

    def __init__(self, settings_config: config.Settings):
        """
        Initialise ponyta registry client

        Parameters
        ----------
        settings_config: config.Settings
            settings config
        """

        self.settings_config = settings_config
        self.workspace_client = WorkspaceClient(
            host=self.settings_config.DATABRICKS_CLUSTER_HOST,
            token=self.settings_config.DATABRICKS_PAT_TOKEN,
        )

        # test databricks connection
        if not self._test_connection_databricks():
            raise ValueError("Databricks creds provided are incorrect")

    def _test_connection_databricks(self) -> bool:
        """
        function to test connection to databricks

        Returns
        ----------
        bool
            if the test connection is successful or not
        """
        try:
            self.workspace_client.serving_endpoints.list()
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def _retrieve_online_features_table_data_exact_match(
        self,
        endpoint_url: str,
        columns_selection: Dict,
        primary_key_values_dict: Dict,
        accept_profile: str,
        oauth_token: str,
        limit_return: int = 1,
        timeout_request: int = 60,
    ) -> Dict:
        """
        function to retrieve similar contexts from vector index

        Parameters
        ----------
        type_of_retrieval: str
            type of retrieval; active_tradie or exact_retrival
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
        timeout_request: int = 60
            request timeout is set to seconds

        Returns
        ----------
        Dict
            dictionary of retrieved features
        """
        _response = requests.get(
            url=endpoint_url,
            headers=_define_request_headers(
                oauth_token=oauth_token, accept_profile=accept_profile
            ),
            params={
                **columns_selection,
                **primary_key_values_dict,
                "limit": limit_return,
            },
            timeout=timeout_request,
        )
        return _response.json()[0]

    def _retrieve_online_features_table_data_active_tradies(
        self,
        endpoint_url: str,
        filter_selection: Dict,
        query_values_dict: Dict,
        accept_profile: str,
        oauth_token: str,
        limit_return: int = 100,
        timeout_request: int = 60,
    ) -> Dict:
        """
        function to retrieve similar contexts from vector index

        Parameters
        ----------
        endpoint_url: str
            name of tradie online table url
        filter_selection: str
            filter selection column
        query_values_dict: Dict
            dictionary that stores the primary keys
        accept_profile: str
            name of accept profile; schema of UC
        oauth_token: str
            oauth token
        limit_return: int = 100
            number of rows returned; default at 100
        timeout_request: int = 60
            request timeout is set to seconds

        Returns
        ----------
        Dict
            dictionary of a single active tradies
        """

        _response = requests.get(
            url=endpoint_url,
            headers=_define_request_headers(
                oauth_token=oauth_token, accept_profile=accept_profile
            ),
            params={**filter_selection, **query_values_dict, "limit": limit_return},
            timeout=timeout_request,
        )

        return random.sample(_response.json(), 1)[0]
