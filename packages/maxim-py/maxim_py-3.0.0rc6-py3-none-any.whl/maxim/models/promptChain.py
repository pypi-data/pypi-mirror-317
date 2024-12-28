from dataclasses import asdict, dataclass
import json
from typing import List, Optional, Union, Dict
from datetime import datetime
from .prompt import Prompt

@dataclass
class PromptNode:
    prompt: Prompt

@dataclass
class CodeBlockNode:
    code: str

@dataclass
class ApiParams:
    id: str
    key: str
    value: str

@dataclass
class ApiNode:
    api: dict

@dataclass
class Node:
    order: int
    content: Union[PromptNode, CodeBlockNode, ApiNode]

    @staticmethod
    def from_dict(data: Dict) -> 'Node':
        content_type = next(iter(set(data.keys()) - {'order'}))
        content_class = {
            'prompt': PromptNode,
            'code': CodeBlockNode,
            'api': ApiNode
        }[content_type]
        content_data = data[content_type]
        if content_type == 'prompt':
            content = PromptNode(prompt=Prompt.from_dict(content_data))
        elif content_type == 'code':
            content = CodeBlockNode(code=content_data)
        else:  # api
            content = ApiNode(api=content_data)
        return Node(order=data['order'], content=content)

@dataclass
class PromptChain:
    promptChainId: str
    version: int
    versionId: str
    nodes: List[Node]

@dataclass
class PromptChainVersionConfig:
    nodes: List[Node]

    @staticmethod
    def from_dict(data: Dict) -> 'PromptChainVersionConfig':
        return PromptChainVersionConfig(
            nodes=[Node.from_dict(node) for node in data['nodes']]
        )

@dataclass
class PromptChainVersion:
    id: str
    version: int
    promptChainId: str
    description: Optional[str]
    config: Optional[PromptChainVersionConfig]
    createdAt: str
    updatedAt: str

    @staticmethod
    def from_dict(data: Dict) -> 'PromptChainVersion':
        return PromptChainVersion(
            id=data['id'],
            version=data['version'],
            promptChainId=data['promptChainId'],
            description=data.get('description'),
            config=PromptChainVersionConfig.from_dict(data['config']) if data.get('config') else None,
            createdAt=data['createdAt'],
            updatedAt=data['updatedAt']
        )
@dataclass
class PromptChainRuleType():
    field: str
    value: Union[str, int, List[str], bool, None]  # adding None here
    operator: str
    valueSource: Optional[str] = None
    exactMatch: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Dict):
        return PromptChainRuleType(field=obj['field'], value=obj['value'], operator=obj['operator'], valueSource=obj.get('valueSource', None), exactMatch=obj.get('exactMatch', None))


@dataclass
class PromptChainRuleGroupType():
    rules: List[Union['PromptChainRuleType', 'PromptChainRuleGroupType']]
    combinator: str

    @staticmethod
    def from_dict(obj: Dict):
        rules = []
        for rule in obj['rules']:
            if 'rules' in rule:
                rules.append(PromptChainRuleGroupType.from_dict(rule))
            else:
                rules.append(PromptChainRuleType(**rule))
        return PromptChainRuleGroupType(rules=rules, combinator=obj['combinator'])


@dataclass
class PromptChainDeploymentRules():
    version: int
    query: Optional[PromptChainRuleGroupType] = None

    @staticmethod
    def from_dict(obj: Dict):
        query = obj.get('query', None)
        if query:
            query = PromptChainRuleGroupType.from_dict(query)
        return PromptChainDeploymentRules(version=obj['version'], query=query)
    
@dataclass
class VersionSpecificDeploymentConfig():
    id: str
    timestamp: datetime
    rules: PromptChainDeploymentRules
    isFallback: bool = False

    @staticmethod
    def from_dict(obj: Dict):
        rules = PromptChainDeploymentRules.from_dict(obj['rules'])
        return VersionSpecificDeploymentConfig(id=obj['id'], timestamp=obj['timestamp'], rules=rules, isFallback=obj.get('isFallback', False))
        
@dataclass
class PromptChainVersionsAndRules:
    folderId: str
    rules: Dict[str, List[VersionSpecificDeploymentConfig]]
    # rules: Dict[str, Union[str, int, bool, None]];
    versions: List[PromptChainVersion]
    fallbackVersion: Optional[PromptChainVersion]

    @staticmethod
    def from_dict(obj: Dict):
        rules = obj['rules']
        # Decoding each rule
        for key in rules:
            rules[key] = [VersionSpecificDeploymentConfig.from_dict(
                rule) for rule in rules[key]]
        versions = [PromptChainVersion.from_dict(version)
                    for version in obj['versions']]
        fallbackVersion = obj.get('fallbackVersion', None)
        if fallbackVersion:
            fallbackVersion = PromptChainVersion.from_dict(fallbackVersion)
        return PromptChainVersionsAndRules(rules=rules, versions=versions,  folderId=obj.get('folderId', None), fallbackVersion=fallbackVersion)

@ dataclass
class VersionAndRulesWithPromptChainId(PromptChainVersionsAndRules):
    promptChainId: str = ""

    @ staticmethod
    def from_dict(obj: Dict):
        rules = obj['rules']
        # Decoding each rule
        for key in rules:
            rules[key] = [VersionAndRulesWithPromptChainId(
                **rule) for rule in rules[key]]
        return VersionAndRulesWithPromptChainId(rules=rules, versions=obj['versions'], promptChainId=obj['promptChainId'], folderId=obj.get('folderId', None), fallbackVersion=obj.get('fallbackVersion', None))

@dataclass
class MaximApiPromptChainResponse:
    data: PromptChainVersionsAndRules
    error: Optional[dict]

    @staticmethod
    def from_dict(data: Dict) -> 'MaximApiPromptChainResponse':
        return MaximApiPromptChainResponse(
            data=PromptChainVersionsAndRules.from_dict(data['data']),
            error=data.get('error')
        )

@dataclass
class PromptChainWithId(PromptChainVersionsAndRules):
    promptChainId: str

class VersionAndRulesWithPromptChainIdEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, VersionAndRulesWithPromptChainId):
            return asdict(obj)
        return super().default(obj)
    
@dataclass
class MaximApiPromptChainsResponse:
    data: List[PromptChainWithId]
    error: Optional[dict]

    @staticmethod
    def from_dict(data: Dict) -> 'MaximApiPromptChainsResponse':
        return MaximApiPromptChainsResponse(
            data=[PromptChainWithId(**item) for item in data['data']],
            error=data.get('error')
        )