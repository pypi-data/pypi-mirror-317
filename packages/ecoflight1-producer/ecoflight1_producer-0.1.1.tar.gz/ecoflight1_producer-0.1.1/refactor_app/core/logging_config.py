"""
Модуль для конфигурации логирования

"""

import logging
from refactor_app.core.config import settings


LOG_FORMAT = f"%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
LOG_LEVEL = settings.logger_settings.log_level  # Динамическая переменная для prod и dev среды

numerical_level = logging.getLevelName(LOG_LEVEL)

logging.basicConfig(level=numerical_level, format=LOG_FORMAT, handlers=[logging.StreamHandler()])

logger = logging.getLogger("app_logger")
