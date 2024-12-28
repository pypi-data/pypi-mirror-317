import contextlib
import json
import logging
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import Retry, Timeout

from ..models.dataset import DatasetEntry
from ..models.folder import Folder
from ..models.prompt import (Prompt, VersionAndRulesWithPromptId,
                             VersionsAndRules)
from ..models.promptChain import VersionAndRulesWithPromptChainId


class ConnectionPool:
    def __init__(self):
        self.session = requests.Session()
        retries = Retry(connect=5, read=3, redirect=1, status=3, backoff_factor=0.4,
                        status_forcelist=frozenset({413, 429, 500, 502, 503, 504}))
        self.http = PoolManager(num_pools=2, maxsize=3, retries=retries, timeout=Timeout(connect=10, read=10))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        self.session.mount('http://', HTTPAdapter(max_retries=retries))

    @contextlib.contextmanager
    def get_session(self):
        try:
            yield self.session
        finally:
            self.session.close()

    @contextlib.contextmanager
    def get_connection(self):
        try:
            yield self.http
        finally:
            self.http.clear()


class MaximAPI:
    connection_pool: ConnectionPool

    def __init__(self,base_url: str, api_key: str):
        self.connection_pool = ConnectionPool()
        self.base_url = base_url
        self.api_key = api_key

    def __make_network_call(self, method: str, endpoint: str, body: Optional[str] = None) -> bytes:
        headers = {"x-maxim-api-key": self.api_key}
        url = f"{self.base_url}{endpoint}"
        with self.connection_pool.get_session() as session:
            response = session.request(
                method,
                url,
                data=body,
                headers=headers
            )
            response.raise_for_status()
            return response.content

    def get_prompt(self, id: str) -> VersionAndRulesWithPromptId:
        res = self.__make_network_call(
            "GET", f"/api/sdk/v4/prompts?promptId={id}")
        data = json.loads(res.decode())['data']
        return VersionAndRulesWithPromptId.from_dict(data)

    def get_prompts(self) -> List[VersionAndRulesWithPromptId]:
        res = self.__make_network_call("GET", "/api/sdk/v4/prompts")
        return [VersionAndRulesWithPromptId.from_dict(data) for data in json.loads(res)['data']]

    def getPromptChain(self, id: str) -> VersionAndRulesWithPromptChainId:
        res = self.__make_network_call(
            "GET", f"/api/sdk/v4/prompt-chains?promptChainId={id}")
        json_response = json.loads(res.decode())
        return VersionAndRulesWithPromptChainId(**json_response['data'])

    def get_prompt_chains(self) -> List[VersionAndRulesWithPromptChainId]:
        res = self.__make_network_call("GET", "/api/sdk/v4/prompt-chains")
        json_response = json.loads(res.decode())
        return [VersionAndRulesWithPromptChainId(**elem) for elem in json_response['data']]

    def get_folder(self, id: str) -> Folder:
        res = self.__make_network_call("GET", f"/api/sdk/v3/folders?folderId={id}")
        json_response = json.loads(res.decode())
        if 'tags' not in json_response:
            json_response['tags'] = {}
        return Folder(**json_response['data'])

    def get_folders(self) -> List[Folder]:
        res = self.__make_network_call("GET", "/api/sdk/v3/folders")
        json_response = json.loads(res.decode())
        for elem in json_response['data']:
            if 'tags' not in elem:
                elem['tags'] = {}
        return [Folder(**elem) for elem in json_response['data']]

    def addDatasetEntries(self,dataset_id: str, dataset_entries: List[DatasetEntry]) -> dict:
        res = self.__make_network_call("POST", "/api/sdk/v3/datasets/entries", json.dumps({"datasetId": dataset_id, "entries": [entry.to_json() for entry in dataset_entries]}))
        return json.loads(res.decode())

    def does_log_repository_exist(self, logger_id: str) -> bool:
        try:
            res = self.__make_network_call("GET", f"/api/sdk/v3/log-repositories?loggerId={logger_id}")
            json_response = json.loads(res.decode())
            if 'error' in json_response:
                return False
            return True
        except Exception as e:
            return False

    def pushLogs(self, repository_id: str, logs: str) -> None:
        try:
            res = self.__make_network_call("POST", f"/api/sdk/v3/log?id={repository_id}", logs)
            json_response = json.loads(res.decode())
            if 'error' in json_response:
                raise Exception(json_response['error'])
        except Exception as e:
            raise Exception(e)
