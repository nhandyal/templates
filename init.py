#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
import os
import json
from typing import List, Optional, Tuple, Union

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

@dataclass
class InitConfig:
    merge_json: List[str]
    merge_list: List[str]
    append_file: List[str]
    copy_file: List[str]
    copy_dir: List[str]
    init_script: Optional[str] = None

class Utils:
    @staticmethod
    def load_source_and_target_paths(src: str, trg: str) -> Tuple[str, Optional[str]]:
        source = open(src, "r").read()
        target = open(trg, "r").read() if os.path.exists(trg) else None
        return source, target

    @staticmethod
    def write_to_file(path: str, content: str) -> None:
        os.system(f"mkdir -p {os.path.dirname(path)}")
        with open(path, "w") as f:
            f.write(content)
    
    @staticmethod
    def append_to_file(path: str, content: str) -> None:
        if os.path.exists(path):
            with open(path, "a") as f:
                f.write(content)
        else:
            Utils.write_to_file(path, content)
    
    @staticmethod
    def copy_dir(source: str, target: str) -> None:
        os.system(f"cp -r {source} {target}")
    
    @staticmethod
    def copy_file(source: str, target: str) -> None:
        os.system(f"cp {source} {target}")
            
    @staticmethod
    def deep_merge_dicts(dict1, dict2):
        """
        Recursively merges dict2 into dict1
        """
        for key in dict2:
            if key in dict1:
                if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                    Utils.deep_merge_dicts(dict1[key], dict2[key])
                elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
                    dict1[key].extend(dict2[key])
                else:
                    dict1[key] = dict2[key]
            else:
                dict1[key] = dict2[key]
        
        return dict1

    @staticmethod
    def unique_merge_lists(list1, list2):
        for i in list2:
            if i not in list1:
                list1.append(i)
        
        return list1

class Processor:
    def __init__(self, config: InitConfig, template_name: str, project_name: str) -> None:
        self.config = config
        self.template_project_root = f"{SCRIPT_DIR}/{template_name}"
        self.target_project_root = f"/workspaces/{project_name}"

    def _get_source_and_target_paths(self, source_path: str, target_project_root: str) -> Tuple[str, str]:
        return os.path.join(self.template_project_root, source_path), os.path.join(target_project_root, source_path)
    
    def process_all(self) -> None:
        if not os.path.exists(self.target_project_root):
            print(f"Error: {self.target_project_root} does not exist.")
            exit(1)
        
        if input(f"Initialize a python project in {self.target_project_root}? (y/n): ") != "y":
            exit(0)

        self.process_merge_json()
        self.process_merge_list()
        self.process_append_file()
        self.process_copy_file()
        self.process_copy_dir()
        self.process_init_script()

    def process_merge_json(self) -> None:
        for e in self.config.merge_json:
            source_path, target_path = self._get_source_and_target_paths(e, self.target_project_root)
            source, target = Utils.load_source_and_target_paths(source_path, target_path)
            
            if target:
                target = Utils.deep_merge_dicts(json.loads(target), json.loads(source))
                Utils.write_to_file(target_path, json.dumps(target, indent=4))
            else:
                Utils.write_to_file(target_path, source)
    
    def process_merge_list(self) -> None:
        for e in self.config.merge_list:
            source_path, target_path = self._get_source_and_target_paths(e, self.target_project_root)
            source, target = Utils.load_source_and_target_paths(source_path, target_path)
            
            if target:
                target = Utils.unique_merge_lists(target.split("\n"), source.split("\n"))
                Utils.write_to_file(target_path, "\n".join(target))
            else:
                Utils.write_to_file(target_path, source)

    def process_append_file(self) -> None:
        for e in self.config.append_file:
            source_path, target_path = self._get_source_and_target_paths(e, self.target_project_root)
            source, _ = Utils.load_source_and_target_paths(source_path, target_path)
            Utils.append_to_file(target_path, source)
    
    def process_copy_file(self) -> None:
        for e in self.config.copy_file:
            source_path, target_path = self._get_source_and_target_paths(e, self.target_project_root)
            Utils.copy_file(source_path, target_path)

    def process_copy_dir(self) -> None:
        for e in self.config.copy_dir:
            source_path, target_path = self._get_source_and_target_paths(e, self.target_project_root)
            Utils.copy_dir(source_path, os.path.dirname(target_path))
    
    def process_init_script(self) -> None:
        if self.config.init_script:
            os.system(f"{self.template_project_root}/{self.config.init_script} {self.target_project_root}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "template_name", 
        type=str,
        choices=["python"],
        help="The name of the template to initialize",
    )
    parser.add_argument("project_name", type=str, help="The target project to initialize into")
    args = parser.parse_args()

    init_config_path = f"{SCRIPT_DIR}/{args.template_name}/init_config.json"    
    config = InitConfig(**json.load(open(init_config_path)))
    Processor(config, args.template_name, args.project_name).process_all()

    print("")
    print("FINISHED INITIALIZING PROJECT")
    print("init script may have overriden files with customizations, verify changes")
    


if __name__ == "__main__":
    main()
