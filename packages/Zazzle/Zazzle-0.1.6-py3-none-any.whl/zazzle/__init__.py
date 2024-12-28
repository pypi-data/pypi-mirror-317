from zazzle.zz_logging import ZZ_Init, ZZ_Logging, ZZ_Files, ZZ_Colors

__version__ = "0.1.5"

# Declare what each of our functions will be referenced as when using zazzle.'function' syntax
configure_logger = ZZ_Init.configure_logger
log = ZZ_Logging.log
log_wide = ZZ_Logging.log_wide

delete_old_log_files = ZZ_Files.delete_old_log_files

colors = ZZ_Colors