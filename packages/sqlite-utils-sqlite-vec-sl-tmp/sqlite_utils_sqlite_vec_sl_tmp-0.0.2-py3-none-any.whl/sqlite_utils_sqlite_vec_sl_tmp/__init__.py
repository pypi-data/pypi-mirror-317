
from sqlite_utils import hookimpl
import sqlite_vec_sl_tmp

__version__ = "0.0.2"
__version_info__ = tuple(__version__.split("."))

@hookimpl
def prepare_connection(conn):
  conn.enable_load_extension(True)
  sqlite_vec_sl_tmp.load(conn)
  conn.enable_load_extension(False)
