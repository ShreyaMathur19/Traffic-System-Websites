import asyncio
from session import start_session_async

if __name__ == "__main__":
    print("=" * 60)
    print("[MODE] Google → Parallel destination tabs → 60s engagement")
    asyncio.run(start_session_async(parallel=3))