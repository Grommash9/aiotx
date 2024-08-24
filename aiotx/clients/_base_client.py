import asyncio
import os
import signal
from contextlib import suppress
from typing import List, Optional


class AioTxClient:
    def __init__(self, node_url: str, headers: dict = {}):
        self.node_url = node_url
        self._headers = headers
        self.monitor: Optional[BlockMonitor] = None
        self._stop_signal: Optional[asyncio.Event] = None
        self._stopped_signal: Optional[asyncio.Event] = None
        self._running_lock = asyncio.Lock()

    def _setup_signal_handlers(self):
        if os.name == "nt":
            # TODO WINDOWS SUPPORT FOR SIGNALS
            return
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, self.stop_monitoring)

    async def start_monitoring(
        self,
        monitoring_start_block: Optional[int] = None,
        timeout_between_blocks: int = 1,
        **kwargs,
    ) -> None:
        if not self.monitor:
            raise ValueError(
                "BlockMonitor instance must be set before starting monitoring"
            )

        async with self._running_lock:
            if self._stop_signal is None:
                self._stop_signal = asyncio.Event()
            if self._stopped_signal is None:
                self._stopped_signal = asyncio.Event()

            self._stop_signal.clear()
            self._stopped_signal.clear()

            self._setup_signal_handlers()

            workflow_data = {
                "client": self,
                **kwargs,
            }

            try:
                stop_task = asyncio.create_task(self._stop_signal.wait())
                monitoring_task = asyncio.create_task(
                    self.monitor.start(
                        monitoring_start_block, timeout_between_blocks, **workflow_data
                    )
                )

                done, pending = await asyncio.wait(
                    [monitoring_task, stop_task], return_when=asyncio.FIRST_COMPLETED
                )

                for task in pending:
                    task.cancel()
                    with suppress(asyncio.CancelledError):
                        await task

                # Check for exceptions in completed tasks
                for task in done:
                    exc = task.exception()
                    if exc is not None:
                        raise exc

            finally:
                try:
                    await self.monitor.shutdown(**workflow_data)
                finally:
                    self._stopped_signal.set()

    def stop_monitoring(self):
        if self._stop_signal:
            self._stop_signal.set()

    async def wait_closed(self):
        if self._stopped_signal:
            await self._stopped_signal.wait()


class BlockMonitor:
    def __init__(self, client: AioTxClient):
        self.client = client
        self.block_handlers: List[callable] = []
        self.transaction_handlers: List[callable] = []
        self.new_utxo_transaction_handlers: List[callable] = []
        self.block_transactions_handlers: List[callable] = []
        self._stop_signal: Optional[asyncio.Event] = None
        self._latest_block: Optional[int] = None

    def on_block(self, func):
        self.block_handlers.append(func)
        return func

    def on_block_transactions(self, func):
        self.block_transactions_handlers.append(func)
        return func

    def on_transaction(self, func):
        self.transaction_handlers.append(func)
        return func

    def on_new_utxo_transaction(self, func):
        self.new_utxo_transaction_handlers.append(func)
        return func

    async def start(
        self,
        monitoring_start_block: Optional[int],
        timeout_between_blocks: int,
        **kwargs,
    ):
        self._stop_signal = asyncio.Event()
        self._latest_block = monitoring_start_block

        while not self._stop_signal.is_set():
            try:
                await self.poll_blocks(timeout_between_blocks)
                await asyncio.sleep(timeout_between_blocks)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error during block monitoring: {e}")
                self._stop_signal.set()
                raise

    async def poll_blocks(self, timeout: int, **kwargs):
        # This method should be implemented by subclasses
        raise NotImplementedError(
            "poll_blocks method must be implemented by subclasses"
        )

    async def process_block(self, block, **kwargs):
        # This method should be implemented by subclasses
        raise NotImplementedError(
            "process_block method must be implemented by subclasses"
        )

    async def shutdown(self, **kwargs):
        pass
