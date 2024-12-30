import json
import os
from typing import TypedDict, Literal, Union

CONFIG_FILENAME = 'datafact.json'
DEFAULT_TARGET = 'default'


class DatasetLocalTarget(TypedDict):
    type: Literal['local']
    name: str


class DatasetRemoteTarget(TypedDict):
    type: Literal['remote']
    name: str
    host: str
    profile: str


type DatasetTarget = Union[DatasetLocalTarget, DatasetRemoteTarget]


def target_to_str(label: str, target: DatasetTarget):
    if target['type'] == 'local':
        return f"{target['label']}: local  : {target['name']}"
    else:
        return f"{target['label']}: remote : {target['name']}: {target['profile']}@{target['host']}"


class ProjectConfig:
    name: str
    targets: dict[str, DatasetTarget]

    def __init__(self, name, targets):
        self.name = name
        self.targets = targets

    @staticmethod
    def load_config():
        with open(CONFIG_FILENAME, 'r') as f:
            data = json.load(f)
            return ProjectConfig(**data)

    @staticmethod
    def init_config(name: str, base_folder='./'):
        init_config = {
            'name': name,
            'targets': {
                'default': {
                    'type': 'local',
                    'name': name,
                }
            }
        }

        fp = os.path.join(base_folder, CONFIG_FILENAME)

        with open(fp, 'w') as f:
            json.dump(init_config, f, indent=4, sort_keys=True)
            return ProjectConfig(**init_config)

    def get_target(self, label='default'):
        target = self.targets.get(label)
        return target

    def add_target(self, target_type, name, host, profile, label='default'):
        if target_type == 'local':
            self.targets[label] = dict(
                type=target_type,
                name=name,
            )
        elif target_type == 'remote':
            self.targets[label] = dict(
                type=target_type,
                name=name,
                host=host,
                profile=profile
            )

    def remove_target(self, label):
        del self.targets[label]

    def list_targets(self, filter_type=None):
        for label, target in self.targets.items():
            if filter_type is None or target['type'] == filter_type:
                yield label, target

    def publish(self, source_file, target_def):
        pass

    def save(self):
        with open(CONFIG_FILENAME, 'w') as f:
            json.dump({
                'name': self.name,
                'targets': self.targets,
            }, f)


load_config = ProjectConfig.load_config


def init_project(name: str):
    """
    createCONFIG_FILENAME file
    create type.py
    create
    :return:
    """
    if '/' not in name:
        name = 'local/' + name

    ProjectConfig.init_config(name)


def locate_draft_file(file_name):
    return os.path.join('./dist', file_name, 'dataset-draft.dsh')
