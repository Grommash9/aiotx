import asyncio
import threading


class AioTxClient:
    def __init__(self, node_url):
        self.node_url = node_url
        self.monitor = BlockMonitor(self)
        self._monitor_thread = None

    def start_monitoring(self, monitoring_start_block: int = None):
        self._monitor_thread = threading.Thread(target=self._start_monitoring_thread, args=(monitoring_start_block,))
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def _start_monitoring_thread(self, monitoring_start_block):
        
        asyncio.run(self.monitor.start(monitoring_start_block))

    def stop_monitoring(self):
        self.monitor.stop()
        if self._monitor_thread:
            self._monitor_thread.join()

    async def get_block_by_number(self, block_number: int):
        pass

    async def get_last_block(self) -> int:
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