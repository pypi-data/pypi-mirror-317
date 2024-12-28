import json
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Union

from .apis.maxim import MaximAPI
from .cache.cache import MaximCache
from .cache.inMemory import MaximInMemoryCache
from .filterObjects import (IncomingQuery, QueryObject, findAllMatches,
                            findBestMatch, parseIncomingQuery)
from .logger.logger import Logger, LoggerConfig
from .models.dataset import DatasetEntry
from .models.folder import Folder, FolderEncoder
from .models.prompt import (Prompt, PromptData, PromptVersion, RuleGroupType,
                            RuleType, VersionAndRulesWithPromptId,
                            VersionAndRulesWithPromptIdEncoder,
                            VersionsAndRules, VersionSpecificDeploymentConfig)
from .models.promptChain import (PromptChain, PromptChainRuleGroupType,
                                 PromptChainVersion,
                                 PromptChainVersionsAndRules,
                                 VersionAndRulesWithPromptChainIdEncoder)
from .models.queryBuilder import QueryRule

maximLogger = logging.getLogger("MaximSDK")


@dataclass
class Config():
    api_key: str
    base_url: Optional[str] = None
    cache: Optional[MaximCache] = None
    debug: Optional[bool] = False
    raise_exceptions: Optional[bool] = False
    prompt_management: Optional[bool] = False


EntityType = {
    "PROMPT": "PROMPT",
    "FOLDER": "FOLDER",
    "PROMPT_CHAIN": "PROMPT_CHAIN"
}


class Maxim:
    def __init__(self, config: Config):
        maximLogger.setLevel(logging.DEBUG if config.debug else logging.INFO)
        self.base_url = config.base_url or "https://app.getmaxim.ai"
        self.api_key = config.api_key
        self.is_running = True
        self.raise_exceptions = config.raise_exceptions or False
        self.maxim_api = MaximAPI(self.base_url, self.api_key)
        self.__is_debug = config.debug or False
        self.__loggers: Dict[str, Logger] = {}
        self.prompt_management = config.prompt_management
        if self.prompt_management:
            self.__cache = config.cache or MaximInMemoryCache()
            self.__sync_thread = threading.Thread(target=self.__sync_timer)
            self.__sync_thread.daemon = True
            self.__sync_thread.start()

    def __sync_timer(self):
        if not self.prompt_management:
            return
        while self.is_running:
            self.__sync_entities()
            time.sleep(60)

    def __sync_entities(self):
        maximLogger.debug(" Syncing prompts and folders")
        if not self.prompt_management:
            return
        if not self.is_running:
            return
        self.__sync_prompts()
        self.__sync_prompt_chains()
        self.__syncFolders()
        maximLogger.debug("Syncing completed")

    def __sync_prompts(self):
        maximLogger.debug("Syncing prompts")
        try:
            prompts = self.maxim_api.get_prompts()
            maximLogger.debug(f"Found {len(prompts)} prompts")
            for prompt in prompts:
                try:
                    self.__cache.set(
                        self.__get_cache_key(EntityType["PROMPT"], prompt.promptId),
                        json.dumps(prompt, cls=VersionAndRulesWithPromptIdEncoder),
                    )
                except Exception as err:
                    maximLogger.error(err)
                    if self.raise_exceptions:
                        raise err
        except Exception as err:
            maximLogger.error(f"Error while syncing prompts: {err}")
            if self.raise_exceptions:
                raise err

    def __sync_prompt_chains(self):
        maximLogger.debug("Syncing prompt Chains")
        try:
            promptChains = self.maxim_api.get_prompt_chains()
            maximLogger.debug(f"Found {len(promptChains)} prompt chains")
            for promptChain in promptChains:
                try:
                    self.__cache.set(
                        self.__get_cache_key(
                            EntityType["PROMPT_CHAIN"], promptChain.promptChainId
                        ),
                        json.dumps(
                            promptChain, cls=VersionAndRulesWithPromptChainIdEncoder
                        ),
                    )
                except Exception as err:
                    maximLogger.error(err)
                    if self.raise_exceptions:
                        raise err
        except Exception as err:
            maximLogger.error(f"Error while syncing prompts: {err}")
            if self.raise_exceptions:
                raise err

    def __syncFolders(self):
        maximLogger.debug("Syncing folders")
        try:
            folders = self.maxim_api.get_folders()
            maximLogger.debug(f"Found {len(folders)} folders")
            for folder in folders:
                try:
                    self.__cache.set(
                        self.__get_cache_key(EntityType["FOLDER"], folder.id),
                        json.dumps(folder, cls=FolderEncoder),
                    )
                except Exception as err:
                    maximLogger.error(err)
                    if self.raise_exceptions:
                        raise err
        except Exception as err:
            maximLogger.error(f"Error while syncing folders: {err}")
            if self.raise_exceptions:
                raise err

    def __get_cache_key(self, entity: str, id: str) -> str:
        if entity == 'PROMPT':
            return f"prompt:{id}"
        else:
            return f"folder:{id}"

    def __get_prompt_from_cache(self, key: str) -> Optional[VersionsAndRules]:
        data = self.__cache.get(key)
        if not data:
            return None
        json_data = json.loads(data)
        return VersionAndRulesWithPromptId.from_dict(json_data)

    def __get_all_prompts_from_cache(self) -> Optional[List[VersionsAndRules]]:
        keys = self.__cache.get_all_keys()
        if not keys:
            return None
        data = [self.__cache.get(key)
                for key in keys if key.startswith("prompt:")]
        promptList = []
        for d in data:
            if d is not None:
                json_data = json.loads(d)
                if 'promptId' in json_data:
                    json_data.pop('promptId')
                promptList.append(VersionsAndRules.from_dict(json_data))
        return promptList

    def __get_prompt_chain_from_cache(
        self, key: str
    ) -> Optional[PromptChainVersionsAndRules]:
        data = self.__cache.get(key)
        if not data:
            return None
        parsed_data = json.loads(data)
        return PromptChainVersionsAndRules.from_dict(parsed_data)

    def __get_all_prompt_chains_from_cache(
        self,
    ) -> Optional[List[PromptChainVersionsAndRules]]:
        keys = self.__cache.get_all_keys()
        if not keys:
            return None
        data = [self.__cache.get(key)
                for key in keys if key.startswith("prompt_chain:")]
        promptChainList = []
        for d in data:
            if d is not None:
                json_data = json.loads(d)
                if 'promptChainId' in json_data:
                    json_data.pop('promptChainId')
                promptChainList.append(
                    PromptChainVersionsAndRules.from_dict(json_data))
        return promptChainList

    def __get_folder_from_cache(self, key: str) -> Optional[Folder]:
        data = self.__cache.get(key)
        if not data:
            return None
        json_data = json.loads(data)
        return Folder(**json_data)

    def __get_all_folders_from_cache(self) -> Optional[List[Folder]]:
        keys = self.__cache.get_all_keys()
        if not keys:
            return None
        data = [self.__cache.get(key)
                for key in keys if key.startswith("folder:")]
        return [Folder(**json.loads(d)) for d in data if d is not None]

    def __format_prompt(self, prompt: PromptVersion) -> Prompt:
        json_data = {
            'promptId': prompt.promptId,
            'version': prompt.version,
            'versionId': prompt.id,
            'tags': prompt.config.tags if prompt.config else [],
            'model': prompt.config.model if prompt.config else None,
            'messages': prompt.config.messages if prompt.config else None,
            'modelParameters': prompt.config.modelParameters if prompt.config else None
        }
        return Prompt(**json_data)

    def __format_prompt_chain(
        self, promptChainVersion: PromptChainVersion
    ) -> PromptChain:
        json_data = {
            'promptChainId': promptChainVersion.promptChainId,
            'versionId': promptChainVersion.id,
            'versionId': promptChainVersion.version,
            'nodes': [n for n in promptChainVersion.config.nodes if hasattr(n, 'prompt') or (isinstance(n, dict) and 'prompt' in n)] if promptChainVersion.config else []
        }
        return PromptChain(**json_data)

    def __get_prompt_version_for_rule(
        self,
        promptVersionAndRules: VersionAndRulesWithPromptId,
        rule: Optional[QueryRule] = None,
    ) -> Optional[Prompt]:
        if rule:
            incomingQuery = IncomingQuery(
                query=rule.query, operator=rule.operator, exactMatch=rule.exactMatch)
            objects = []
            for versionId, versionRules in promptVersionAndRules.rules.items():
                for versionRule in versionRules:
                    if not versionRule.rules.query:
                        continue
                    if rule.scopes:
                        for key in rule.scopes.keys():
                            if key != "folder":
                                raise ValueError("Invalid scope added")
                    version = next(
                        (v for v in promptVersionAndRules.versions if v.id == versionId), None)
                    if not version:
                        continue
                    query = versionRule.rules.query
                    if version.config and version.config.tags:
                        parsedIncomingQuery = parseIncomingQuery(
                            incomingQuery.query)
                        tags = version.config.tags
                        for key, value in tags.items():
                            if value == None:
                                continue
                            if parsedIncomingQuery is None:
                                continue
                            incomingQueryFields = [
                                q.field for q in parsedIncomingQuery]
                            if key in incomingQueryFields:
                                query.rules.append(
                                    RuleType(field=key, operator='=', value=value))
                    objects.append(QueryObject(query=query, id=versionId))

            deployedVersionObject = findBestMatch(objects, incomingQuery)
            if deployedVersionObject:
                deployedVersion = next(
                    (v for v in promptVersionAndRules.versions if v.id == deployedVersionObject.id), None)
                if deployedVersion:
                    return self.__format_prompt(deployedVersion)

        else:
            if promptVersionAndRules.rules:
                for versionId, versionRules in promptVersionAndRules.rules.items():
                    logging.debug(f"type: {type(versionRules[0].rules)}")
                    doesQueryExist = any(
                        ruleElm.rules.query != None for ruleElm in versionRules)
                    if doesQueryExist:
                        deployedVersion = next(
                            (v for v in promptVersionAndRules.versions if v.id == versionId), None)
                        if deployedVersion:
                            return self.__format_prompt(deployedVersion)
            else:
                return self.__format_prompt(promptVersionAndRules.versions[0])

        if promptVersionAndRules.fallbackVersion:
            maximLogger.info(
                f"************* FALLBACK TRIGGERED : VERSION : {promptVersionAndRules.fallbackVersion} *************")
            return self.__format_prompt(promptVersionAndRules.fallbackVersion)
        return None

    def __get_prompt_chain_version_for_rule(
        self,
        promptChainVersionsAndRules: PromptChainVersionsAndRules,
        rule: Optional[QueryRule] = None,
    ) -> Optional[PromptChain]:
        if rule:
            incomingQuery = IncomingQuery(
                query=rule.query, operator=rule.operator, exactMatch=rule.exactMatch)
            objects = []
            for versionId, versionRules in promptChainVersionsAndRules.rules.items():
                for versionRule in versionRules:
                    if not versionRule.rules.query:
                        continue
                    if rule.scopes:
                        for key in rule.scopes.keys():
                            if key != "folder":
                                raise ValueError("Invalid scope added")
                    version = next(
                        (v for v in promptChainVersionsAndRules.versions if v.id == versionId), None)
                    if not version:
                        continue
                    query = RuleGroupType(**versionRule.rules.query.__dict__)
                    objects.append(QueryObject(query=query, id=versionId))

            deployedVersionObject = findBestMatch(objects, incomingQuery)
            if deployedVersionObject:
                deployedVersion = next(
                    (v for v in promptChainVersionsAndRules.versions if v.id == deployedVersionObject.id), None)
                if deployedVersion:
                    return self.__format_prompt_chain(deployedVersion)

        else:
            if promptChainVersionsAndRules.rules:
                for versionId, versionRules in promptChainVersionsAndRules.rules.items():
                    logging.debug(f"type: {type(versionRules[0].rules)}")
                    doesQueryExist = any(
                        ruleElm.rules.query != None for ruleElm in versionRules)
                    if doesQueryExist:
                        deployedVersion = next(
                            (v for v in promptChainVersionsAndRules.versions if v.id == versionId), None)
                        if deployedVersion:
                            return self.__format_prompt_chain(deployedVersion)
            else:
                return self.__format_prompt_chain(
                    promptChainVersionsAndRules.versions[0]
                )

        if promptChainVersionsAndRules.fallbackVersion:
            maximLogger.info(
                f"************* FALLBACK TRIGGERED : VERSION : {promptChainVersionsAndRules.fallbackVersion} *************")
            return self.__format_prompt_chain(
                promptChainVersionsAndRules.fallbackVersion
            )
        return None

    def __get_folders_for_rule(
        self, folders: List[Folder], rule: QueryRule
    ) -> List[Folder]:
        incomingQuery = IncomingQuery(
            query=rule.query, operator=rule.operator, exactMatch=rule.exactMatch)
        objects = []
        for folder in folders:
            query = RuleGroupType(rules=[], combinator='AND')
            if not folder.tags:
                continue
            parsedIncomingQuery = parseIncomingQuery(incomingQuery.query)
            tags = folder.tags
            for key, value in tags.items():
                if key in [q.field for q in parsedIncomingQuery]:
                    # if not isinstance(value,None):
                    query.rules.append(
                        RuleType(field=key, operator='=', value=value))
            if not query.rules:
                continue
            objects.append(QueryObject(query=query, id=folder.id))

        folderObjects = findAllMatches(objects, incomingQuery)
        ids = [fo.id for fo in folderObjects]
        return [f for f in folders if f.id in ids]

    def get_prompt(self, id: str, rule: QueryRule) -> Optional[Prompt]:
        if self.prompt_management is False:
            raise Exception(
                "prompt_management is disabled. Please enable it in config."
            )
        maximLogger.debug(f"getPrompt: id: {id} for rule: {rule}")
        key = self.__get_cache_key("PROMPT", id)
        versionAndRulesWithPromptId = self.__get_prompt_from_cache(key)
        if versionAndRulesWithPromptId is None:
            versionAndRulesWithPromptId = self.maxim_api.get_prompt(id)
            if len(versionAndRulesWithPromptId.versions) == 0:
                return None
            self.__cache.set(id, json.dumps(
                versionAndRulesWithPromptId, cls=VersionAndRulesWithPromptIdEncoder))
        if not versionAndRulesWithPromptId:
            return None
        prompt = self.__get_prompt_version_for_rule(versionAndRulesWithPromptId, rule)
        if not prompt:
            return None
        return prompt

    def get_prompts(self, rule: QueryRule) -> List[Prompt]:
        if self.prompt_management is False:
            raise Exception(
                "prompt_management is disabled. Please enable it in config."
            )
        versionAndRules = self.__get_all_prompts_from_cache()
        prompts = []
        if versionAndRules is None or len(versionAndRules) == 0:
            self.__sync_entities()
            versionAndRules = self.__get_all_prompts_from_cache()
        if not versionAndRules:
            return []
        for v in versionAndRules:
            if rule.scopes:
                if 'folder' not in rule.scopes.keys():
                    return []
                else:
                    if rule.scopes['folder'] != v.folderId:
                        continue
            prompt = self.__get_prompt_version_for_rule(v, rule)
            if prompt != None:
                prompts.append(prompt)
        if len(prompts) == 0:
            return []
        return prompts

    def get_prompt_chain(self, id: str, rule: QueryRule) -> Optional[PromptChain]:
        if self.prompt_management is False:
            raise Exception(
                "prompt_management is disabled. Please enable it in config."
            )
        key = self.__get_cache_key("PROMPT_CHAIN", id)
        versionAndRules = self.__get_prompt_chain_from_cache(key)
        if versionAndRules is None:
            versionAndRules = self.maxim_api.getPromptChain(id)
            if len(versionAndRules.versions) == 0:
                return None
            self.__cache.set(id, json.dumps(
                versionAndRules, cls=VersionAndRulesWithPromptChainIdEncoder))
        if not versionAndRules:
            return None
        promptChains = self.__get_prompt_chain_version_for_rule(versionAndRules, rule)
        if not promptChains:
            return None
        return promptChains

    def get_folder_by_id(self, id: str) -> Optional[Folder]:
        if self.prompt_management is False:
            raise Exception(
                "prompt_management is disabled. Please enable it in config."
            )
        key = self.__get_cache_key("FOLDER", id)
        folder = self.__get_folder_from_cache(key)
        if folder is None:
            try:
                folder = self.maxim_api.get_folder(id)
                if not folder:
                    return None
                self.__cache.set(key, json.dumps(folder, cls=FolderEncoder))
            except Exception as e:
                return None
        return folder

    def get_folders(self, rule: QueryRule) -> List[Folder]:
        if self.prompt_management is False:
            raise Exception(
                "prompt_management is disabled. Please enable it in config."
            )
        folders = self.__get_all_folders_from_cache()
        if folders is None or len(folders) == 0:
            self.__sync_entities()
            folders = self.__get_all_folders_from_cache()
        if not folders:
            return []
        return self.__get_folders_for_rule(folders, rule)

    def logger(self, config: LoggerConfig) -> Logger:
        # Checking if this log repository exist on server
        exists = self.maxim_api.does_log_repository_exist(config.id)
        if not exists:
            if config.id:
                maximLogger.error(f"Log repository not found")
                if self.raise_exceptions:
                    raise Exception(f"Log repository not found")
        if config.id in self.__loggers:
            return self.__loggers[config.id]
        logger = Logger(
            config=config,
            api_key=self.api_key,
            base_url=self.base_url,
            is_debug=self.__is_debug,
            raise_exceptions=self.raise_exceptions,
        )
        self.__loggers[config.id] = logger
        return logger

    def cleanup(self):
        maximLogger.debug("Cleaning up Maxim sync thread")
        self.is_running = False
        for logger in self.__loggers.values():
            logger.cleanup()
        maximLogger.debug("Cleanup done")
        logger.cleanup()
        maximLogger.debug("Cleanup done")
