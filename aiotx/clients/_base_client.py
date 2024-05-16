import asyncio


class AioTxClient:
    def __init__(self, node_url):
        self.node_url = node_url
        self.monitor = BlockMonitor(self)
        self._monitoring_task = None

    async def start_monitoring(self, monitoring_start_block: int = None):
        if self._monitoring_task is None:
            self._monitoring_task = asyncio.create_task(self._run_monitoring(monitoring_start_block))
        return self._monitoring_task

    def stop_monitoring(self):
        if self._monitoring_task is not None:
            self._monitoring_task.cancel()
            try:
                asyncio.get_event_loop().run_until_complete(self._monitoring_task)
            except asyncio.CancelledError:
                pass
            self._monitoring_task = None

    async def _run_monitoring(self, monitoring_start_block):
        try:
            async with self.monitor:
                await self.monitor.start(monitoring_start_block)
        except asyncio.CancelledError:
            pass

    async def get_block_by_number(self, block_number: int):
        pass

    async def get_last_block_number(self) -> int:
        pass


class BlockMonitor:
    def __init__(self, client: AioTxClient):
        self.client = client
        self.block_handlers = []
        self.transaction_handlers = []
        self.running = False
        self._latest_block = None

    def on_block(self, func):
        self.block_handlers.append(func)
        return func

    def on_transaction(self, func):
        self.transaction_handlers.append(func)
        return func

    async def __aenter__(self):
        self.running = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    async def start(self, monitoring_start_block):
        self.running = True
        self._latest_block = monitoring_start_block
        while self.running:
            try:
                await self.poll_blocks()
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Error during polling: {e}")
                await asyncio.sleep(2)

    def stop(self):
        self.running = False

    async def poll_blocks(self):
        pass

    async def process_block(self, block):
        pass
