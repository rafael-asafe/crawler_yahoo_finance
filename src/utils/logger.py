"""Configuração centralizada do logger da aplicação.

Cria um logger nomeado pelo módulo com nível, formato e handlers definidos
pelas variáveis de ambiente via ``Settings``. Um ``execution_id`` UUID único
por processo é embutido em todas as mensagens, permitindo correlacionar logs
de uma mesma instância da aplicação mesmo em ambientes com múltiplos containers.

Handlers disponíveis (ativados via settings):
    - Console (``CONSOLE_LOG=true``): escreve em ``stdout``.
    - Arquivo (``LOG_FILE=<path>``): escreve em arquivo com encoding UTF-8.
"""

import logging
import sys

from utils.settings import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)

formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)

if settings.CONSOLE_LOG:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(settings.LOG_LEVEL)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

if settings.LOG_FILE:
    file_log_handler = logging.FileHandler(settings.LOG_FILE, encoding="utf-8")
    file_log_handler.setLevel(settings.LOG_LEVEL)
    file_log_handler.setFormatter(formatter)
    logger.addHandler(file_log_handler)
