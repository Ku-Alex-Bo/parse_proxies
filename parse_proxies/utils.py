import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import cycle
from typing import Dict, List

from .api_client import ProxyAPIClient

"""
Утилиты для работы пайплайнов
"""


def get_save_id_proxies_dict(
    token: str,
    proxies: List[str],
    upstreams: List[str],
    chunk_size: int = 25,
    max_workers: int = 5,
    pause: float = 0.3,
) -> Dict[str, List[str]]:
    """
    Разбивает proxies на чанки по chunk_size и отправляет
    параллельно через пул upstreams, избегая блокировки Too Many Requests.
    """
    results: Dict[str, List[str]] = {}
    proxy_cycle = cycle(upstreams)

    def _send_chunk(chunk: List[str], upstream: str) -> None:
        client = ProxyAPIClient(token, upstream)
        client.get_token()
        resp = client.post_proxies(chunk)
        save_id = resp.get("save_id", f"chunk_{len(results)}")
        results[save_id] = chunk

    chunks = [proxies[i : i + chunk_size] for i in range(0, len(proxies), chunk_size)]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for chunk in chunks:
            upstream = next(proxy_cycle)
            futures.append(executor.submit(_send_chunk, chunk, upstream))
            time.sleep(pause)

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"[ERROR] отправка чанка не удалась: {e}")

    return results


def save_results(results: Dict[str, List[str]], filename: str = "results.json") -> None:
    """Сохраняет результат в result.json"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def save_execution_time(start_time: float, filename: str = "time.txt") -> None:
    """Сохраняет время выполнения в требуемом формате в time.txt"""
    elapsed = int(time.time() - start_time)
    h, rem = divmod(elapsed, 3600)
    m, s = divmod(rem, 60)
    with open(filename, "w") as f:
        f.write(f"{h:02d}:{m:02d}:{s:02d}")
