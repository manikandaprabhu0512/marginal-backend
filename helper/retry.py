import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def retry_async(
    func: Callable[[], Awaitable[T]],
    retries: int = 3,
    delay: float = 1,
) -> T:

    last_exception = None

    for attempt in range(1, retries + 1):
        try:
            return await func()

        except Exception as e:
            last_exception = e

            if attempt == retries:
                break

            await asyncio.sleep(delay)

    raise last_exception