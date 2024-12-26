"""
██╗░░░░░██╗████████╗███████╗░░░░░██╗░██████╗░█████╗░███╗░░██╗██████╗░██████╗░░░░██████╗░██╗░░░██╗
██║░░░░░██║╚══██╔══╝██╔════╝░░░░░██║██╔════╝██╔══██╗████╗░██║██╔══██╗██╔══██╗░░░██╔══██╗╚██╗░██╔╝
██║░░░░░██║░░░██║░░░█████╗░░░░░░░██║╚█████╗░██║░░██║██╔██╗██║██║░░██║██████╦╝░░░██████╔╝░╚████╔╝░
██║░░░░░██║░░░██║░░░██╔══╝░░██╗░░██║░╚═══██╗██║░░██║██║╚████║██║░░██║██╔══██╗░░░██╔═══╝░░░╚██╔╝░░
███████╗██║░░░██║░░░███████╗╚█████╔╝██████╔╝╚█████╔╝██║░╚███║██████╔╝██████╦╝██╗██║░░░░░░░░██║░░░
╚══════╝╚═╝░░░╚═╝░░░╚══════╝░╚════╝░╚═════╝░░╚════╝░╚═╝░░╚══╝╚═════╝░╚═════╝░╚═╝╚═╝░░░░░░░░╚═╝░░░
"""

import json
import os
import base64
import logging
import shutil
from typing import Any, Dict, Optional, Union, Callable
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from .utils import (
    convert_to_datetime, get_or_default, key_exists_or_add, normalize_keys,
    flatten_json, filter_data, sort_data, hash_password, check_password,
    sanitize_output, pretty_print
)
from .modules.search import search_data
from .modules.tgbot import BackupToTelegram
from .modules.csv import CSVExporter

DATABASE_DIR = 'database'
if not os.path.exists(DATABASE_DIR):
    try:
        os.makedirs(DATABASE_DIR)
    except OSError as e:
        print(f"🐛 \033[91mWhoops! Looks like we couldn't create the database directory. Check your permissions, buddy!\033[0m")
        logging.error(f"Failed to create database directory: {e}")
        raise

DEFAULT_LOG_FILE = os.path.join(DATABASE_DIR, 'LiteJsonDb.log')

# Setup a very verbose logger
logging.basicConfig(filename=DEFAULT_LOG_FILE, 
                    level=logging.DEBUG,  # Set to DEBUG for maximum verbosity
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s')

class JsonDB:
   def __init__(self, filename="db.json", backup_filename="db_backup.json",
                 crypted=False, encryption_type="base64", log=False, auto_backup=False,
                 schema=None, log_file=DEFAULT_LOG_FILE, encryption_key: Optional[str]=None):
        self.filename = os.path.join(DATABASE_DIR, filename)
        self.backup_filename = os.path.join(DATABASE_DIR, backup_filename)
        self.crypted = crypted
        self.encryption_type = encryption_type
        self.db = {}
        self.observers = {}
        self.csv_exporter = CSVExporter(DATABASE_DIR)
        self.lock = RLock()
        self.log_enabled = log
        self.auto_backup_enabled = auto_backup
        self.schema = schema
        self.log_file = log_file
        self.encryption_key = encryption_key
        self.executor = ThreadPoolExecutor(max_workers=5) # Initialize the thread pool

        if self.encryption_key and self.encryption_type == "fernet":
             self._generate_fernet_key()
        
        if self.log_enabled:
            self._setup_logger()
        self._load_db()
        logging.info("JsonDB instance initialized.")
    
   def _setup_logger(self):
        """Set up the logger."""
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s')
        logging.debug("Logger setup completed.")
    
   def _generate_fernet_key(self):
        """Generate Fernet key from user-provided key or generate a new one"""
        if self.encryption_key:
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=480000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.encryption_key.encode('utf-8')))
            self.fernet_key = key
            logging.debug("Fernet key generated using user-provided key.")
        else:
            self.fernet_key = Fernet.generate_key()
            logging.debug("New Fernet key generated.")

    # ==================================================
    #               ENCRYPTION/DECRYPTION
    # ==================================================

   def _pad_data(self, data: bytes) -> bytes:
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data
    
   def _unpad_data(self, padded_data: bytes) -> bytes:
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data

   def _encrypt_base64(self, data: Dict[str, Any]) -> str:
        """Encode data to base64."""
        try:
            json_data = json.dumps(data).encode('utf-8')
            encoded_data = base64.b64encode(json_data).decode('utf-8')
            logging.debug("Data encrypted using base64.")
            return encoded_data
        except Exception as e:
            logging.error(f"Error during base64 encryption: {e}")
            raise

   def _decrypt_base64(self, encoded_data: str) -> Dict[str, Any]:
        """Decode data from base64."""
        try:
            decoded_data = base64.b64decode(encoded_data.encode('utf-8')).decode('utf-8')
            logging.debug("Data decrypted using base64.")
            return json.loads(decoded_data)
        except Exception as e:
             logging.warning(f"Failed to decrypt base64 data. Returning empty dict. Error: {e}")
             return {}

   def _encrypt_fernet(self, data: Dict[str, Any]) -> str:
        """Encrypt data using Fernet."""
        try:
            f = Fernet(self.fernet_key)
            json_data = json.dumps(data).encode('utf-8')
            padded_data = self._pad_data(json_data)
            encrypted_data = f.encrypt(padded_data).decode('utf-8')
            logging.debug("Data encrypted using Fernet.")
            return encrypted_data
        except Exception as e:
            logging.error(f"Error during Fernet encryption: {e}")
            raise
    
   def _decrypt_fernet(self, encrypted_data_str: str) -> Dict[str, Any]:
        """Decrypt data using Fernet."""
        try:
             f = Fernet(self.fernet_key)
             encrypted_data = encrypted_data_str.encode('utf-8')
             decrypted_data = f.decrypt(encrypted_data)
             unpadded_data = self._unpad_data(decrypted_data)
             logging.debug("Data decrypted using Fernet.")
             return json.loads(unpadded_data.decode('utf-8'))
        except Exception as e:
            logging.warning(f"Failed to decrypt Fernet data. Returning empty dict. Error: {e}")
            return {}

   def _encrypt(self, data: Dict[str, Any]) -> str:
        if self.encryption_type == "fernet" and self.crypted:
            return self._encrypt_fernet(data)
        return self._encrypt_base64(data)

   def _decrypt(self, encoded_data: str) -> Dict[str, Any]:
        if self.encryption_type == "fernet" and self.crypted:
            return self._decrypt_fernet(encoded_data)
        return self._decrypt_base64(encoded_data)

    # ==================================================
    #               DATABASE OPERATIONS
    #           SAVE, RESTORE, AND RETRIEVE
    # ==================================================
   def _load_db(self) -> None:
        """Load the database from the JSON file, or create a new one if it doesn't exist."""
        if not os.path.exists(self.filename):
            try:
                with open(self.filename, 'w') as file:
                    json.dump({}, file)
                    logging.info(f"Database file created: {self.filename}")
            except OSError as e:
                print(f"🐛 \033[91mWhoops! Unable to create the database file. Check your file permissions, explorer!\033[0m")
                logging.error(f"Failed to create database file: {e}")
                raise
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                if self.crypted and data:
                    self.db = self._decrypt(data)
                else:
                    self.db = data
            logging.info(f"Database loaded from: {self.filename}")
        except (OSError, json.JSONDecodeError) as e:
            print(f"🐛 \033[91mWhoops! Can't load the database file. Is it corrupted, or is the path blocked?\033[0m")
            logging.error(f"Failed to load database file: {e}")
            raise

   def _save_db(self) -> None:
        """Save the database to the JSON file."""
        try:
            data = self.db if not self.crypted else self._encrypt(self.db)
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)
            logging.info(f"Database saved to {self.filename}")
        except OSError as e:
             print(f"🐛 \033[91mWhoops! Saving the database went wrong. Is the disk full, or did we anger the file system?\033[0m")
             logging.error(f"Failed to save database file: {e}")
             raise

   def _backup_db(self) -> None:
        """Create a backup of the database."""
        try:
            shutil.copy(self.filename, self.backup_filename)
            logging.info(f"Backup created: {self.backup_filename}")
        except OSError as e:
            print(f"🐛 \033[91mWhoops! Backup failed. Looks like the file system is playing hard to get.\033[0m")
            logging.error(f"Failed to create backup: {e}")
            raise

   def backup_to_telegram(self, token: str, chat_id: str):
        """Create db backup using Telegram API"""
        self._save_db()
        telegram_bot = BackupToTelegram(token=token, chat_id=chat_id)
        telegram_bot.backup_to_telegram(self.filename)
        logging.info("Database backed up to Telegram.")

   def _restore_db(self) -> None:
        """Restore the database from backup."""
        if os.path.exists(self.backup_filename):
            try:
                shutil.copy(self.backup_filename, self.filename)
                self._load_db()
                logging.info(f"Database restored from backup: {self.backup_filename}")
            except OSError as e:
                print(f"🐛 \033[91mWhoops! Can't restore from backup. Did the backup file vanish or become corrupted?\033[0m")
                logging.error(f"Failed to restore from backup: {e}")
                raise
        else:
            print(f"🐛 \033[91mWhoops! No backup found to restore. Looks like we didn't plan this one too well.\033[0m")
            logging.error("No backup file found to restore.")

    # ==================================================
    #                EXPORT TO CSV
    # --------------------------------------------------
    # Exports either a specified collection or the entire
    # database to a CSV file.
    # ==================================================
   def export_to_csv(self, data_key: Optional[str] = None):
        def _export_csv_task():
            if data_key:
                if data_key in self.db:
                    data = self.db[data_key]
                    csv_path = self.csv_exporter.export(data, f"{data_key}_export.csv")
                    if csv_path:
                        print(f"🎉 \033[92mFile created: {csv_path}\033[0m")
                    else:
                        print(f"🐛 \033[91mWhoops! Could not export '{data_key}' to CSV. Check the data and permissions.\033[0m")
                        logging.error(f"Failed to export '{data_key}' to CSV.")
                else:
                    print(f"🐛 \033[91mWhoops! The key '{data_key}' doesn't exist. Are you sure you typed it correctly?\033[0m")
                    logging.warning(f"Key '{data_key}' not found for CSV export.")
            else:
                if self.db:
                    csv_path = self.csv_exporter.export(self.db, "full_database_export.csv")
                    if csv_path:
                        print(f"🎉 \033[92mFile created: {csv_path}\033[0m")
                    else:
                        print(f"🐛 \033[91mWhoops! Could not export the database to CSV. Please verify data and permissions.\033[0m")
                        logging.error("Failed to export full database to CSV.")
                else:
                    print(f"🐛 \033[91mWhoops! The database is empty. Nothing to export. Maybe we should add some data first!\033[0m")
                    logging.warning("Attempted to export an empty database to CSV.")
        self.executor.submit(_export_csv_task)

    # ==================================================
    #                DATA VALIDATION
    # --------------------------------------------------
    # ==================================================
   def validate_data(self, data: Any) -> bool:
       """Validate data before insertion."""
       if not isinstance(data, dict):
          print(f"🐛 \033[91mWhoops! Data should be a dictionary. Let's try that again!\033[0m")
          logging.warning("Data validation failed: Data is not a dictionary.")
          return False
    
       def _validate_inner(obj: Any) -> bool:
           if isinstance(obj, dict):
              for key, value in obj.items():
                  if not isinstance(key, str):
                     print(f"🐛 \033[91mWhoops! Data keys should be strings. Found a non-string key: '{key}'\033[0m")
                     logging.warning(f"Data validation failed: Non-string key found: '{key}'")
                     return False
                  if not isinstance(value, (str, int, float, list, dict, bool, type(None))):
                     print(f"🐛 \033[91mWhoops! Data validation failed. Only 'str', 'int', 'float', 'list', 'dict', 'bool', and 'None' values are supported.\033[0m")
                     logging.warning(f"Data validation failed: Invalid data type found for key: '{key}'.")
                     return False
                  if isinstance(value, dict):
                        if not _validate_inner(value):
                            return False
           elif isinstance(obj, list):
                 for item in obj:
                   if isinstance(item,dict):
                        if not _validate_inner(item):
                         return False
                   elif not isinstance(item, (str, int, float,  bool, type(None))):
                      print(f"🐛 \033[91mWhoops! Data validation failed. Only 'str', 'int', 'float', 'bool' and 'None' values are supported in lists.\033[0m")
                      logging.warning(f"Data validation failed: Invalid data type found in list: {item}")
                      return False
           return True
       
       return _validate_inner(data)


   def _set_child(self, parent: Dict[str, Any], child_key: str, value: Any) -> None:
        """Helper to set data in a nested dictionary."""
        keys = child_key.split('/')
        for key in keys[:-1]:
            parent = parent.setdefault(key, {})
        parent[keys[-1]] = value
    
   def _merge_dicts(self, dict1, dict2):
        """Merge dict2 into dict1."""
        for key, value in dict2.items():
            if isinstance(value, dict) and key in dict1 and isinstance(dict1[key], dict):
                self._merge_dicts(dict1[key], value)
            else:
                dict1[key] = value
        return dict1

   def key_exists(self, key: str) -> bool:
        """Check if a key exists in the database."""
        keys = key.split('/')
        data = self.db
        for k in keys:
            if k in data:
                data = data[k]
            else:
                return False
        return True

   def get_data(self, key: str) -> Optional[Any]:
        """Get data from the database by key."""
        keys = key.split('/')
        data = self.db
        for k in keys:
            if k in data:
                data = data[k]
            else:
                print(f"🐛 \033[91mWhoops! The key '{key}' doesn't exist. Are you sure you got the right map?\033[0m")
                logging.warning(f"Key '{key}' not found in database.")
                return None
        return data

   def set_data(self, key: str, value: Optional[Any] = None) -> None:
        """Set data in the database and notify observers.
    
        If `value` is not provided, initialize the key with an empty dictionary.
        """
        if value is None:
            value = {}
        
        if not self.validate_data(value):
            print(f"🐛 \033[91mWhoops! Invalid data format. Let's use a valid dictionary next time!\033[0m")
            logging.warning(f"Data validation failed for key '{key}'.")
            return
        if self.key_exists(key):
            print(f"🐛 \033[91mWhoops! The key '{key}' already exists. Use 'edit_data' to change an existing key. It's like trying to build a house on the same spot!\033[0m")
            logging.warning(f"Key '{key}' already exists. Use 'edit_data' to modify.")
            return
        
        with self.lock:
            self._set_child(self.db, key, value)
        self.notify_observers("set_data", key, value)
        self.executor.submit(self._backup_db)
        self.executor.submit(self._save_db)
        logging.info(f"Data set with key '{key}'.")

   def edit_data(self, key: str, value: Any) -> None:
        """Edit data in the database and notify observers."""
        if not self.key_exists(key):
            print(f"🐛 \033[91mWhoops! The key '{key}' doesn't exist. You can't change something that isn't there!\033[0m")
            logging.warning(f"Attempted to edit non-existent key: '{key}'.")
            return
        if not self.validate_data(value):
            print(f"🐛 \033[91mWhoops! Invalid data format. Stick to the dictionary format, buddy!\033[0m")
            logging.warning(f"Data validation failed for edit on key: '{key}'.")
            return
        
        keys = key.split('/')
        data = self.db
        for k in keys[:-1]:
            data = data.setdefault(k, {})
        
        current_data = data.get(keys[-1], {})
        
        if isinstance(value, dict) and "increment" in value:
             for field, increment_value in value["increment"].items():
                 if field in current_data:
                     if isinstance(current_data[field], (int, float)):
                         if isinstance(increment_value, (int, float)):
                             current_data[field] += increment_value
                         else:
                             print(f"🐛 \033[91mWhoops! The increment value for '{field}' is not a number. Check that you are passing a number, pal!\033[0m")
                             logging.warning(f"Invalid increment value type for field '{field}' in key '{key}'.")
                             return
                     else:
                         print(f"🐛 \033[91mWhoops! The field '{field}' is not a number. We can only increment numbers.\033[0m")
                         logging.warning(f"Attempted to increment non-numeric field '{field}' in key '{key}'.")
                         return
                 else:
                     print(f"🐛 \033[91mWhoops! The field '{field}' doesn't exist. You cannot increment what doesn't exist.\033[0m")
                     logging.warning(f"Attempted to increment non-existent field '{field}' in key '{key}'.")
                     return
        else:
             if isinstance(current_data, dict):
                value = self._merge_dicts(current_data, value)
             data[keys[-1]] = value
        
        self.executor.submit(self._backup_db)
        self.executor.submit(self._save_db)
        logging.info(f"Data edited for key '{key}'.")
    
    # ==================================================
    #                DATA OBSERVERS
    # --------------------------------------------------
    # ==================================================
   def add_observer(self, key: str, observer_func: Callable[[str, str, Any], None]) -> None:
        """Add an observer for a specific key."""
        if key not in self.observers:
            self.observers[key] = []
        self.observers[key].append(observer_func)
        logging.debug(f"Observer added for key '{key}'.")

   def remove_observer(self, key: str, observer_func: Callable[[str, str, Any], None]) -> None:
        """Remove an observer for a specific key."""
        if key in self.observers:
            self.observers[key].remove(observer_func)
            if not self.observers[key]:
                del self.observers[key]
        logging.debug(f"Observer removed for key '{key}'.")

   def notify_observers(self, action: str, key: str, value: Any) -> None:
        """Notify all observers about a change."""
        for observer_key, observers in self.observers.items():
            if key.startswith(observer_key):
                for observer in observers:
                    observer(action, key, value)
                    print(f"✨ \033[93mValue changed in '{key}': {value}\033[0m")
        logging.debug(f"Observers notified for key '{key}' with action '{action}'.")
   
   def remove_data(self, key: str) -> None:
       """Remove data from the database by key."""
       keys = key.split('/')
       data = self.db
       for k in keys[:-1]:
           if k in data:
               data = data[k]
           else:
               print(f"🐛 \033[91mWhoops! The key '{key}' doesn't exist. You can't delete what isn't there!\033[0m")
               logging.warning(f"Attempted to remove non-existent key: '{key}'.")
               return
       if keys[-1] in data:
          with self.lock:
             del data[keys[-1]]
             self.executor.submit(self._backup_db)
             self.executor.submit(self._save_db)
          logging.info(f"Data removed for key '{key}'.")
       else:
          print(f"🐛 \033[91mWhoops! The key '{key}' doesn't exist. Cannot delete, bro!\033[0m")
          logging.warning(f"Attempted to remove non-existent key: '{key}'.")

    # ==================================================
    #                WHOLE DATABASE
    # --------------------------------------------------
    # ==================================================

   def get_db(self, raw: bool = False) -> Union[Dict[str, Any], str]:
        """Get the entire database, optionally in raw format."""
        if raw:
            logging.debug("Retrieved raw database data.")
            return self.db
        if self.crypted:
            logging.debug("Retrieved decrypted database data.")
            return self._decrypt(self._encrypt(self.db))
        logging.debug("Retrieved unencrypted database data.")
        return self.db

    # ==================================================
    #            SUBCOLLECTION VALIDATION
    # --------------------------------------------------
    # ==================================================

   def get_subcollection(self, collection_name: str, item_id: Optional[str] = None) -> Optional[Any]:
        """Get a specific subcollection or an item within a subcollection."""
        collection = self.db.get(collection_name, {})
        if item_id is not None:
            if item_id in collection:
                logging.debug(f"Retrieved item '{item_id}' from subcollection '{collection_name}'.")
                return collection[item_id]
            else:
                print(f"🐛 \033[91mWhoops! The ID '{item_id}' does not exist in the collection '{collection_name}'. Double-check!\033[0m")
                logging.warning(f"Item '{item_id}' not found in subcollection '{collection_name}'.")
                return None
        logging.debug(f"Retrieved subcollection '{collection_name}'.")
        return collection

   def set_subcollection(self, collection_name: str, item_id: str, value: Any) -> None:
        """Set an item in a specific subcollection."""
        if not self.validate_data(value):
            print(f"🐛 \033[91mWhoops! Invalid data format. Use a dictionary like a pro!\033[0m")
            logging.warning(f"Data validation failed for subcollection '{collection_name}' and item '{item_id}'.")
            return
        if collection_name not in self.db:
            self.db[collection_name] = {}
        if item_id in self.db[collection_name]:
            print(f"🐛 \033[91mWhoops! The ID '{item_id}' already exists in the collection '{collection_name}'. Use 'edit_subcollection' to modify the existing item.\033[0m")
            logging.warning(f"Item '{item_id}' already exists in subcollection '{collection_name}'. Use 'edit_subcollection'.")
            return
        with self.lock:
           self.db[collection_name][item_id] = value
           self.executor.submit(self._backup_db)
           self.executor.submit(self._save_db)
        logging.info(f"Item '{item_id}' set in subcollection '{collection_name}'.")


   def edit_subcollection(self, collection_name: str, item_id: str, value: Any) -> None:
        """Edit an item in a specific subcollection."""
        if not self.validate_data(value):
            print(f"🐛 \033[91mWhoops! Invalid data format. Let's keep the dictionary theme going!\033[0m")
            logging.warning(f"Data validation failed for edit in subcollection '{collection_name}', item '{item_id}'.")
            return
        if collection_name in self.db and item_id in self.db[collection_name]:
            current_data = self.db[collection_name][item_id]
            if isinstance(current_data, dict):
                value = self._merge_dicts(current_data, value)
            with self.lock:
                self.db[collection_name][item_id] = value
                self.executor.submit(self._backup_db)
                self.executor.submit(self._save_db)
            logging.info(f"Item '{item_id}' edited in subcollection '{collection_name}'.")
        else:
            print(f"🐛 \033[91mWhoops! The ID '{item_id}' does not exist in the collection '{collection_name}'. You can't edit what isn't there, bro!\033[0m")
            logging.warning(f"Attempted to edit non-existent item '{item_id}' in subcollection '{collection_name}'.")

   def remove_subcollection(self, collection_name: str, item_id: Optional[str] = None) -> None:
        """Remove an entire subcollection or a specific item within it."""
        if item_id is None:
            if collection_name in self.db:
               with self.lock:
                 del self.db[collection_name]
                 self.executor.submit(self._backup_db)
                 self.executor.submit(self._save_db)
               logging.info(f"Subcollection '{collection_name}' removed.")
            else:
                print(f"🐛 \033[91mWhoops! The collection '{collection_name}' doesn't exist. Nothing to delete here.\033[0m")
                logging.warning(f"Attempted to remove non-existent subcollection: '{collection_name}'.")
                return
        else:
            if collection_name in self.db and item_id in self.db[collection_name]:
                with self.lock:
                   del self.db[collection_name][item_id]
                   self.executor.submit(self._backup_db)
                   self.executor.submit(self._save_db)
                logging.info(f"Item '{item_id}' removed from subcollection '{collection_name}'.")
            else:
                print(f"🐛 \033[91mWhoops! The ID '{item_id}' does not exist in the collection '{collection_name}'. Can't delete what isn't there!\033[0m")
                logging.warning(f"Attempted to remove non-existent item '{item_id}' from subcollection '{collection_name}'.")
                return

    # ==================================================
    #                DATA SEARCH
    # ==================================================

   def search_data(self, value: Any, key: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Search for a value in the database.

        :param value: The elusive treasure you're hunting for.
        :param key: A specific key to search within the documents. If None, we'll search everywhere like a treasure map with no boundaries.
        :return: A dictionary of found items or None if the treasure remains hidden.
        """
        try:
            result = search_data(self.db, value, key)
            if result:
                logging.info(f"Search for value '{value}' (key: '{key}') successful.")
                return result
            else:
                logging.info(f"Search for value '{value}' (key: '{key}') yielded no results.")
                return None
        except Exception as e:
            print(f"🐛 \033[91mWhoops! An error occurred during the search. Are you sure the data is there?\033[0m")
            logging.error(f"Error during search: {e}")
            return None

    # ==================================================
    #               UTILITY FUNCTIONS
    #         (Methods for commonly used utilities)
    # --------------------------------------------------
    # This section provides static methods that act as
    # wrappers for various utility functions. They are
    # designed to be used across different parts of the
    # application for convenience and consistency.
    # ==================================================

   @staticmethod
   def call_utility_function(func_name: str, *args, **kwargs):
        functions: Dict[str, Callable] = {
            'convert_to_datetime': convert_to_datetime,
            'get_or_default': get_or_default,
            'key_exists_or_add': key_exists_or_add,
            'normalize_keys': normalize_keys,
            'flatten_json': flatten_json,
            'filter_data': filter_data,
            'sort_data': sort_data,
            'hash_password': hash_password,
            'check_password': check_password,
            'sanitize_output': sanitize_output,
            'pretty_print': pretty_print
        }
        if func_name in functions:
            return functions[func_name](*args, **kwargs)
        raise ValueError(f"Function {func_name} not found.")
    
   @staticmethod
   def convert_to_datetime(date_str):
        return JsonDB.call_utility_function('convert_to_datetime', date_str)

   @staticmethod
   def get_or_default(data, key, default=None):
        return JsonDB.call_utility_function('get_or_default', data, key, default)

   @staticmethod
   def key_exists_or_add(data, key, default):
        return JsonDB.call_utility_function('key_exists_or_add', data, key, default)

   @staticmethod
   def normalize_keys(data):
        return JsonDB.call_utility_function('normalize_keys', data)

   @staticmethod
   def flatten_json(data):
        return JsonDB.call_utility_function('flatten_json', data)

   @staticmethod
   def filter_data(data, condition):
        return JsonDB.call_utility_function('filter_data', data, condition)

   @staticmethod
   def sort_data(data, key, reverse=False):
        return JsonDB.call_utility_function('sort_data', data, key, reverse)

   @staticmethod
   def hash_password(password):
        return JsonDB.call_utility_function('hash_password', password)

   @staticmethod
   def check_password(stored_hash, password):
        return JsonDB.call_utility_function('check_password', stored_hash, password)

   @staticmethod
   def sanitize_output(data):
        return JsonDB.call_utility_function('sanitize_output', data)

   @staticmethod
   def pretty_print(data):
        return JsonDB.call_utility_function('pretty_print', data)
