import torch
from torch import Tensor
from pathlib import Path
from queue import Queue, Empty as QueueEmpty
from threading import Event
from typing import Tuple, List, Dict, Literal, Generator, Callable

from epilepsy_bids_loader import Segment


def read_json(json_file: str | Path) -> Dict:
    import json
    with open(json_file, "r") as f:
        meta = json.load(f)
    return meta


def read_yaml(path: Path) -> Dict:
    import yaml
    with open(path) as f:
        out: dict = yaml.safe_load(f)
        return out


def batch_segments(
    segments: List[Segment],
    batch_size: int,
    select: Literal["all", "random", "first"]
) -> Generator[Tuple[Tensor, Tensor, Tensor], None, None]:
    """
    Creates batches of data from a list of segments.

    Args:
        segments (List[Segment]): List of segments.
        batch_size (int): Size of the batch dimension "N".
        select (all, random, first): The type of data to select from each
            segment based on Segment.data method.

    Returns:
        Generator[Tuple[Tensor, Tensor, Tensor]]: Tuple of:
        - x: (N, C, L)
        - y: (N,)
        - t: (N,)
    """
    # batches: List[Tuple[ndarray, ndarray, ndarray]] = []
    for i in range(0, len(segments), batch_size):
        j = i + batch_size
        batch: List[Segment] = segments[i : j]
        batch_x = []
        batch_y = []
        batch_t = []

        for seg in batch:
            x, y, t = seg.data(select=select)
            device = x.device

            batch_x.append(x) # (1, C, L)
            batch_y.append(
                torch.tensor(1. if y.any() else 0., device=device)
            ) # (L,) -> 1
            batch_t.append(t[0]) # (L,) -> 1, use the start of the seg
            continue

        batch = (
            torch.concatenate(batch_x, axis=0), # (N, C, L)
            torch.stack(batch_y, axis=0), # (N,)
            torch.stack(batch_t, axis=0) # (N,)
        )
        yield batch
    return


def empty_queue(queue: Queue):
    while True:
        try:
            queue.get_nowait()
        except QueueEmpty:
            break
    return


def threaded_batching(
    maxsize: int,
    worker: Callable,
    **kwargs
) -> Generator[Tuple[Tensor, Tensor, Tensor], None, None]:
    """
    Uses multi-threading to execute batching procedure.

    Args:
        maxsize (int): Maximum number of threads to use.
        worker (Callable): The worker function.
        kwargs: Other keyword arguments to pass to worker. The worker will
            in addition receive queue (queue.Queue) and stop_event
            (threading.Event).

    Yields:
        Generator[Tuple[Tensor, Tensor, Tensor], None, None]: (x, y, t)
    """
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event

    queue = Queue(maxsize=maxsize)
    executor = ThreadPoolExecutor()
    stop_event = Event()
    future = executor.submit(
        worker,
        queue=queue,
        stop_event=stop_event,
        **kwargs
    )
    try:
        while True:
            batch = queue.get()
            if batch is None:
                break
            yield batch

    except GeneratorExit:
        stop_event.set()

    finally:
        empty_queue(queue)
        future.cancel()
        future.result()
        executor.shutdown()

    return


def batch_segments_with_prefetch(
    segments: List[Segment],
    batch_size: int,
    select: Literal["all", "random", "first"],
    prefetch: int = 5
) -> Generator[Tuple[Tensor, Tensor, Tensor], None, None]:

    def worker(
        queue: Queue,
        stop_event: Event,
        segments: List[Segment],
        batch_size: int,
        select: Literal["all", "random", "first"]
    ) -> Generator[Tuple[Tensor, Tensor, Tensor], None, None]:
        for i in range(0, len(segments), batch_size):
            j = i + batch_size
            batch: List[Segment] = segments[i : j]
            batch_x = []
            batch_y = []
            batch_t = []

            for seg in batch:
                x, y, t = seg.data(select=select)
                device = x.device

                batch_x.append(x) # (1, C, L)
                batch_y.append(
                    torch.tensor(1. if y.any() else 0., device=device)
                ) # (L,) -> 1
                batch_t.append(t[0]) # (L,) -> 1, use the start of the seg
                continue

            batch = (
                torch.concatenate(batch_x, axis=0), # (N, C, L)
                torch.stack(batch_y, axis=0), # (N,)
                torch.stack(batch_t, axis=0) # (N,)
            )

            if stop_event.is_set():
                break

            else:
                queue.put(batch)

        queue.put(None)
        return

    batch = threaded_batching(
        maxsize=prefetch,
        worker=worker,
        segments=segments,
        batch_size=batch_size,
        select=select
    )
    return batch
