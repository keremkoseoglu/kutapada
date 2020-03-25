"""All JSON related data read / write stuff is here"""
from copy import deepcopy
from enum import Enum
import json
from typing import List
from config.config import ConfigFactory
from data.encryption import Encryption
from data.system import Account, System


class DatabaseError(Exception):
    """Database exceptions"""
    class ErrorCode(Enum):
        """Error codes"""
        system_not_found: 1

    def __init__(self,
                 error_code: ErrorCode,
                 system_name: str = ""):

        self.error_code = error_code

        if system_name is None:
            self.system_name = ""
        else:
            self.system_name = system_name

    @property
    def message(self) -> str:
        """Message in text format"""
        if self.error_code == DatabaseError.ErrorCode.system_not_found:
            return "System not found: " + self.system_name
        return "Database error"


class Database:
    """Central database class for JSON management"""
    _NEW_ACCOUNT_NAME_PREFIX = "New account"
    _NEW_SYSTEM_NAME_PREFIX = "New system"

    """ Main database class """
    def __init__(self):
        self._config = ConfigFactory.get_instance()
        with open(self._config.data_file_path, "r") as data_file:
            self._password_json = json.load(data_file)
        if self.encrypted:
            Database._decrypt_password_json(self._password_json)
        self._sort()

    @property
    def encrypted(self) -> bool:
        """ Are the passwords in the file encrpyted """
        return self._password_json["header"]["encrypted"]

    @property
    def systems(self) -> List[System]:
        """ List of systems """
        output = []
        for system_json in self._password_json["systems"]:
            output.append(self._json_to_system(system_json))
        return output

    def create_account(self, system_name: str):
        """Creates a new account"""
        account_name = self._get_new_account_name(system_name)
        new_account_dict = {
            "name": account_name,
            "credential": ""
        }

        for system_json in self._password_json["systems"]:
            if system_json["name"] == system_name:
                system_json["accounts"].append(new_account_dict)

        self._write_password_json_to_disk()

    def create_system(self):
        """ Creates a new system """
        name = self._get_new_system_name()
        new_system_dict = {
            "name": name,
            "connection": "",
            "accounts": []
        }
        self._password_json["systems"].append(new_system_dict)
        self._write_password_json_to_disk()

    def delete_account(self, system_name: str, account_name: str):
        """Deletes account from the JSON file"""
        for system_json in self._password_json["systems"]:
            if system_json["name"] == system_name:
                deletable_index = -1
                cursor = -1
                for account_json in system_json["accounts"]:
                    cursor += 1
                    if account_json["name"] == account_name:
                        deletable_index = cursor
                        break
                if deletable_index < 0:
                    return
                system_json["accounts"].pop(deletable_index)
        self._write_password_json_to_disk()

    def delete_system(self, name: str):
        """Deletes system from the JSON file"""
        deletable_index = self._get_system_index(name)
        if deletable_index < 0:
            return
        self._password_json["systems"].pop(deletable_index)
        self._write_password_json_to_disk()

    def does_account_exist(self, system_name: str, account_name: str) -> bool:
        """Checks if the account exists"""
        try:
            selected_system = self.get_system_by_name(system_name)
            for acc in selected_system.accounts:
                if acc.name == account_name:
                    return True
        except Exception:
            pass
        return False

    def does_system_exist(self, name: str) -> bool:
        """Checks if the system exists"""
        try:
            self.get_system_by_name(name)
            return True
        except Exception:
            return False

    def get_system_by_name(self, name: str) -> System:
        """ Get a single system """
        for system in self.systems:
            if system.name == name:
                return system
        raise DatabaseError(DatabaseError.ErrorCode.system_not_found, system_name=name)

    def get_system_by_index(self, index: int) -> System:
        """ Get a single system """
        return self.systems[index]

    def rename_account(self, system_name: str, old_name: str, new_name: str):
        """Renames an account"""
        for system_json in self._password_json["systems"]:
            if system_json["name"] == system_name:
                for account_json in system_json["accounts"]:
                    if account_json["name"] == old_name:
                        account_json["name"] = new_name
                        break
        self._write_password_json_to_disk()

    def rename_system(self, old_name: str, new_name: str):
        """Renames a system"""
        for system_json in self._password_json["systems"]:
            if system_json["name"] == old_name:
                system_json["name"] = new_name
                break
        self._write_password_json_to_disk()

    def update_system(self, updated_system: System):
        """ Updates a system in the JSON file """
        for system_json in self._password_json["systems"]:
            if system_json["name"] == updated_system.name:
                system_json["connection"] = updated_system.connection
                system_json["accounts"] = []
                for updated_account in updated_system.accounts:
                    system_json["accounts"].append(
                        {"name": updated_account.name,
                         "credential": updated_account.credential})
        self._write_password_json_to_disk()

    @staticmethod
    def _json_to_system(system_json: dict) -> System:
        system = System(name=system_json["name"], connection=system_json["connection"])

        for account_json in system_json["accounts"]:
            account = Account(name=account_json["name"], credential=account_json["credential"])
            system.accounts.append(account)
        return system

    @staticmethod
    def _decrypt_password_json(password_json: dict):
        for system_json in password_json["systems"]:
            for account_json in system_json["accounts"]:
                account_json["credential"] = Encryption.decrypt_text(account_json["credential"])

    @staticmethod
    def _encrypt_password_json(password_json: dict):
        for system_json in password_json["systems"]:
            for account_json in system_json["accounts"]:
                account_json["credential"] = Encryption.encrypt_text(account_json["credential"])

    def _get_new_account_name(self, system_name: str) -> str:
        base_candidate = Database._NEW_ACCOUNT_NAME_PREFIX
        number = 0
        for system_json in self._password_json["systems"]:
            if system_json["name"] == system_name:
                while True:
                    number += 1
                    candidate = base_candidate + " (" + str(number) + ")"
                    already_exists = False
                    for account_json in system_json["accounts"]:
                        if account_json["name"] == candidate:
                            already_exists = True
                    if not already_exists:
                        return candidate
        return base_candidate

    def _get_new_system_name(self) -> str:
        base_candidate = Database._NEW_SYSTEM_NAME_PREFIX
        number = 0
        while True:
            number += 1
            candidate = base_candidate + " (" + str(number) + ")"
            already_exists = False
            for system_json in self._password_json["systems"]:
                if system_json["name"] == candidate:
                    already_exists = True
            if not already_exists:
                return candidate

    def _get_system_index(self, name: str) -> int:
        cursor = -1
        for system_json in self._password_json["systems"]:
            cursor += 1
            if system_json["name"] == name:
                return cursor
        return -1

    def _sort(self):
        self._password_json["systems"].sort(key=lambda x: x["name"].upper())

    def _write_password_json_to_disk(self):
        self._sort()
        writeable_password_json = deepcopy(self._password_json)
        if self.encrypted:
            Database._encrypt_password_json(writeable_password_json)
        with open(self._config.data_file_path, "w") as data_file:
            json.dump(writeable_password_json, data_file)


class DatabaseFactory:
    """ Factory for singleton database object """
    _singleton: Database = None

    @staticmethod
    def get_instance() -> Database:
        """ Returns a singleton instance """
        if DatabaseFactory._singleton is None:
            DatabaseFactory._singleton = Database()
        return DatabaseFactory._singleton
