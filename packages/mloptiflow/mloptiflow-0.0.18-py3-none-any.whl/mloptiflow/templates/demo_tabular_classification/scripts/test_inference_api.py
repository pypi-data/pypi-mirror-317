"""
Load testing script for continuous API calls.
"""


import sys
import time
import asyncio
import numpy as np
import aiohttp
import signal
from typing import List, Dict, Any
import random
from mloptiflow.monitoring import highlighters


class InferenceAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.running = True
        self.sample_data = [
            1.799e01,
            1.038e01,
            1.228e02,
            1.001e03,
            1.184e-01,
            2.776e-01,
            3.001e-01,
            1.471e-01,
            2.419e-01,
            7.871e-02,
            1.095e00,
            9.053e-01,
            8.589e00,
            1.534e02,
            6.399e-03,
            4.904e-02,
            5.373e-02,
            1.587e-02,
            3.003e-02,
            6.193e-03,
            2.538e01,
            1.733e01,
            1.846e02,
            2.019e03,
            1.622e-01,
            6.656e-01,
            7.119e-01,
            2.654e-01,
            4.601e-01,
            1.189e-01,
        ]
        self.setup_signal_handlers()

    def setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    def handle_shutdown(self, signum, frame):
        print("\nShutting down gracefully...")
        self.running = False

    def generate_variation(self) -> List[float]:
        variation_factor = random.uniform(0.5, 2.0)
        noise = np.random.normal(0, 0.3, len(self.sample_data))
        if random.random() < 0.2:
            spike_idx = random.randint(0, len(self.sample_data) - 1)
            noise[spike_idx] *= 3.0
        varied_data = [
            x * variation_factor + n for x, n in zip(self.sample_data, noise)
        ]
        return varied_data

    async def make_prediction(self, session: aiohttp.ClientSession) -> Dict[str, Any]:
        varied_features = self.generate_variation()
        async with session.post(
            f"{self.base_url}/predict", json={"features": varied_features}
        ) as response:
            return await response.json()

    async def run(self, timeout=None):
        async with aiohttp.ClientSession() as session:
            request_count = 0
            start_time = time.time()
            while self.running:
                try:
                    if timeout and (time.time() - start_time) > timeout:
                        print("\nTest mode timeout reached")
                        self.running = False
                        break

                    result = await self.make_prediction(session)
                    request_count += 1
                    print(
                        f"Request {highlighters.yellow(request_count)}: Predicted class = {highlighters.green(result['predicted_class'])} with probabilities {highlighters.red(result['class_probabilities'])}"
                    )
                    await asyncio.sleep(0.1)
                except Exception as e:
                    print(highlighters.log_error(f"Error making prediction: {e}"))
                    await asyncio.sleep(1)


def main():
    tester = InferenceAPITester()
    if len(sys.argv) > 1 and sys.argv[1] == "--test-mode":
        print("Running in test mode with 5 second timeout")
        asyncio.run(tester.run(timeout=5))
        sys.exit(0)
    else:
        print("Starting continuous API calls. Press Ctrl/^ + C to stop.")
        asyncio.run(tester.run())


if __name__ == "__main__":
    main()
