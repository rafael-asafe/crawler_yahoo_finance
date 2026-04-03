from logging import WARNING

from selenium.common.exceptions import TimeoutException
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from utils.logger import logger

retry_selenium = retry(
    retry=retry_if_exception_type(TimeoutException),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    before_sleep=before_sleep_log(logger, WARNING),
    reraise=True,
)
