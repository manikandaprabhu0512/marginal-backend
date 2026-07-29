import asyncio
import logging
from collections.abc import Coroutine
from typing import Any

logger = logging.getLogger(__name__)


class BackgroundManager:

    print("Background Task Started...")
    def submit(self, coroutine: Coroutine[Any, Any, Any]) -> None:
        """
        Schedule a coroutine to run in the background.

        The caller does not wait for completion.
        """

        task = asyncio.create_task(coroutine)
        print("Task created...")
        task.add_done_callback(self._handle_completion)
        print("Task Completed....")

    @staticmethod
    def _handle_completion(task: asyncio.Task) -> None:

        try:
            task.result()

        except Exception:
            logger.exception("Background task failed")


background_manager = BackgroundManager()