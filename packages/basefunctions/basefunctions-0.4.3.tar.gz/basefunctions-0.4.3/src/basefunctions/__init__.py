# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : basefunctions
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  simple library to have some commonly used functions for everyday purpose
#
# =============================================================================

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------

from basefunctions.singleton import SingletonMeta
from basefunctions.config_handler import ConfigHandler
from basefunctions.filefunctions import (
    check_if_dir_exists,
    check_if_exists,
    check_if_file_exists,
    create_directory,
    create_file_list,
    get_base_name,
    get_base_name_prefix,
    get_current_directory,
    get_extension,
    get_file_extension,
    get_file_name,
    get_parent_path_name,
    get_path_and_base_name_prefix,
    get_path_name,
    get_home_path,
    is_directory,
    is_file,
    norm_path,
    remove_directory,
    remove_file,
    rename_file,
    set_current_directory,
)
from basefunctions.observer import Observer, Subject
from basefunctions.secret_handler import SecretHandler
from basefunctions.threadpool import (
    ThreadPoolMessage,
    ThreadPoolHookObjectInterface,
    ThreadPoolUserObjectInterface,
    create_threadpool_message,
    ThreadPool,
)

from basefunctions.database_handler import (
    DataBaseHandler,
    SQLiteDataBaseHandler,
    MySQLDataBaseHandler,
    PostgreSQLDataBaseHandler,
)

from basefunctions.utils import get_current_function_name

__all__ = [
    "ThreadPool",
    "ThreadPoolMessage",
    "ThreadPoolHookObjectInterface",
    "ThreadPoolUserObjectInterface",
    "check_if_dir_exists",
    "check_if_exists",
    "check_if_file_exists",
    "check_if_table_exists",
    "connect_to_database",
    "create_database",
    "create_directory",
    "create_file_list",
    "create_threadpool_message",
    "execute_sql_command",
    "get_base_name",
    "get_base_name_prefix",
    "get_current_directory",
    "get_current_function_name",
    "get_default_threadpool",
    "get_extension",
    "get_file_extension",
    "get_file_name",
    "get_number_of_elements_in_table",
    "get_parent_path_name",
    "get_path_name",
    "get_path_and_base_name_prefix",
    "get_home_path",
    "is_directory",
    "is_file",
    "norm_path",
    "remove_directory",
    "remove_file",
    "rename_file",
    "set_current_directory",
    "SingletonMeta",
    "Observer",
    "Subject",
    "ConfigHandler",
    "DataBaseHandler",
    "SQLiteDataBaseHandler",
    "MySQLDataBaseHandler",
    "PostgreSQLDataBaseHandler",
    "SecretHandler",
]

# load default config
ConfigHandler().load_default_config("basefunctions")
