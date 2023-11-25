#!/usr/bin/env python

import os
import subprocess
import csv
from typing import List

# Configuration
home_directory = os.path.expanduser('~')
envs_dir = os.path.join(home_directory, '.easyconda', "")  # Replace with your backup directory
print(f"Backup Directory: {envs_dir}")
#envs_dir = "./demo_envs/"

backup_file_name = 'backups.csv'

backup_file = os.path.join(envs_dir, backup_file_name)


line_format = "{:<30} | {:<10} | {:<10} | {:<12} | {}"


# Ensure backup directory exists
os.makedirs(envs_dir, exist_ok=True)

class Environment:

    def __init__(self, env_name: str, size: int, is_backed_up: bool, backup_path:str, env_directory: str = None):
        self.env_name = env_name
        self.size = size
        self.is_backed_up = is_backed_up
        self.backup_path = backup_path
        self.env_directory = env_directory

    @classmethod
    def from_conda(cls, env_name: str, directory: str):

        backup_path = os.path.join(envs_dir, f'{env_name}.yml')
        if os.path.exists(backup_path):
            is_backed_up = True
        else:
            is_backed_up = False
        
        size = subprocess.check_output(['du', '-sh', directory]).split()[0].decode('utf-8')

        return cls(env_name, size, is_backed_up, backup_path, directory)

    @classmethod
    def from_backup(cls, env_name:str, size: int):
        return cls(env_name, size, True, os.path.join(envs_dir, f'{env_name}.yml'))
    
    @property
    def is_installed(self):
        return self.env_directory is not None
    
    @property
    def is_up_to_date(self):
        if not self.is_backed_up:
            return False
        if os.path.exists(self.backup_path):
            current_env = subprocess.check_output(['conda', 'env', 'export', "--no-builds", '-n', self.env_name]).decode()
            with open(self.backup_path, 'r') as file:
                backed_up_env = file.read()
                return current_env == backed_up_env
        return False
    
    def backup(self):
        if not self.is_installed:
            return
        subprocess.run(['conda', 'env', 'export', '-n', self.env_name, '-f', self.backup_path])
        if not self.is_backed_up:
            with open(backup_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.env_name, self.size])
            self.is_backed_up = True

        print(f'Environment {self.env_name} backed up.')

    def install(self):
        if self.is_installed:
            return
        subprocess.run(['conda', 'env', 'create',  '-f', self.backup_path])

        output = subprocess.check_output(['conda', 'env', 'list']).decode()
        for line in output.splitlines():
            if self.env_name in line:
                split_line = line.split()
                if split_line[0] == self.env_name:
                    self.env_directory = split_line[1]
                    break

        # Filter using Python

        print(f'Environment {self.env_name} installed at {self.env_directory}.')

    def uninstall(self):
        if self.is_installed:
            subprocess.run(['conda', 'env', 'remove', '-n', self.env_name])
            self.env_directory = None
            print(f'Environment {self.env_name} removed from system.')
    
    def __repr__(self) -> str:
        return line_format.format(self.env_name, str(self.is_installed), str(self.is_backed_up), self.size, str(self.is_up_to_date))
            

def get_installed_envs():
    result = subprocess.check_output(['conda', 'env', 'list']).decode()
    envs = [line.split() for line in result.splitlines() if line and not line.startswith('#') and not line.split()[0] == 'base']
    return [Environment.from_conda(env[0], env[1]) for env in envs]

def add_backed_up_envs(installed_envs: List[Environment]):
    instances = []
    installed_env_names = [env.env_name for env in installed_envs]
    if not os.path.exists(backup_file):
        return installed_envs
    with open(backup_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            env_name, size = row
            if env_name not in installed_env_names:
                instance = Environment.from_backup(env_name, size)
                instances.append(instance)
    return installed_envs + instances

def load_all_envs():
    installed_envs = get_installed_envs()
    all_envs = add_backed_up_envs(installed_envs)
    return all_envs

def display_envs(envs: List[Environment]):
    
    print()
    print(line_format.format("Environment", "Installed", "Backed Up", "Size on Disk", "Up-to-date"))
    print("-" * 80)
    for env in envs:
        print(env)
    print()

def backup_all_envs(envs: List[Environment]):
    for env in envs:
        env.backup()



def main():
    print("Welcome to Easyconda!")
    print("Loading Environments...")
    envs = load_all_envs()
    while True:
        
        display_envs(envs)
        choice = input("Usage (q)uit or [(i)nstall|(r)emove|(b)ackup|(br)backupremove] [env_name1] [env_name2] ... [env_nameN]:\n")
        if choice.startswith('q'):
            break
        choice_list = choice.split()
        action = choice_list[0].lower()
        choosen_env_names = list(set(choice_list[1:]))
        current_envs = []
        if len(choosen_env_names) == 1 and choosen_env_names[0] == '*':
            current_envs = envs
        else:
            for env in envs:
                if env.env_name in choosen_env_names:
                    current_envs.append(env)
            if len(current_envs) == 0:
                print("No valid choice. Try again!\n")
                continue

        for env in current_envs:
        
            if action == 'b' or action == 'backup':
                env.backup()
            elif action == 'i' or action == 'install':
                env.install()
            elif action == 'r' or action == 'remove':
                env.uninstall()
            elif action == 'br' or action == 'backupremove':
                env.backup()
                env.uninstall()
            else:
                print("No valid action. Try again!\n")
                continue

if __name__ == '__main__':
    main()
