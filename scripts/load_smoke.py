import argparse
import asyncio
import time

import httpx


async def hit(client: httpx.AsyncClient, idx: int) -> tuple[bool, float]:
    started = time.perf_counter()
    route = ["/api/v1/health", "/api/v1/ready", "/api/v1/ops/top-skus"][idx % 3]
    ok = False
    try:
        if route.endswith("top-skus"):
            response = await client.get(route, params={"days": 30, "limit": 5})
        else:
            response = await client.get(route)
        ok = response.status_code < 500
    except Exception:
        ok = False
    return ok, time.perf_counter() - started


async def main() -> None:
    parser = argparse.ArgumentParser(description="Load smoke for AI Retail Copilot API")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--requests", type=int, default=30)
    parser.add_argument("--concurrency", type=int, default=10)
    args = parser.parse_args()

    sem = asyncio.Semaphore(args.concurrency)
    async with httpx.AsyncClient(base_url=args.base_url, timeout=10.0) as client:
        async def bounded(i: int):
            async with sem:
                return await hit(client, i)

        results = await asyncio.gather(*(bounded(i) for i in range(args.requests)))

    successes = sum(1 for ok, _ in results if ok)
    latencies = [elapsed for _, elapsed in results]
    avg = sum(latencies) / len(latencies) if latencies else 0.0
    p95 = sorted(latencies)[max(0, int(len(latencies) * 0.95) - 1)] if latencies else 0.0

    print(f"Requests: {args.requests}")
    print(f"Successes: {successes}")
    print(f"Failures: {args.requests - successes}")
    print(f"Avg latency: {avg:.3f}s")
    print(f"P95 latency: {p95:.3f}s")


if __name__ == "__main__":
    asyncio.run(main())

