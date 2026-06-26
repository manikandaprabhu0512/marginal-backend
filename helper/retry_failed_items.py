import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


async def retry_failed_items(
    items: list[T],
    processor: Callable[[T], Awaitable[R | None]],
    retries: int = 3,
    delay: float = 1,
) -> list[R]:

    remaining_items = items
    successful_results: list[R] = []

    for attempt in range(1, retries + 1):

        results = await asyncio.gather(
            *(processor(item) for item in remaining_items),
            return_exceptions=True,
        )

        failed_items: list[T] = []

        for item, result in zip(remaining_items, results):

            if isinstance(result, Exception):
                failed_items.append(item)
                continue

            if result is None:
                failed_items.append(item)
                continue

            successful_results.append(result)

        if not failed_items:
            break

        remaining_items = failed_items

        if attempt < retries:
            await asyncio.sleep(delay * (2 ** (attempt - 1)))

    return successful_results