import argparse
import statistics
import time
import requests

DEFAULT_URL = (
    "https://volleykarelia.ru/media/referees/1000022545.jpg"
)


def measure_speed(url: str, count: int = 10) -> None:
    print(f"Запуск замеров ({count} запросов) по адресу:\n{url}\n")

    durations = []
    sizes = []

    session = requests.Session()
    session.headers.update({"User-Agent": "SpeedTester/1.0"})

    for i in range(1, count + 1):
        try:
            start_time = time.perf_counter()

            # stream=True позволяет точно замерить время скачивания всего тела ответа
            response = session.get(url, stream=True, timeout=30)
            response.raise_for_status()

            downloaded_bytes = 0
            for chunk in response.iter_content(chunk_size=8192):
                downloaded_bytes += len(chunk)

            end_time = time.perf_counter()

            duration = end_time - start_time
            durations.append(duration)
            sizes.append(downloaded_bytes)

            size_mb = downloaded_bytes / (1024 * 1024)
            speed_mbps = size_mb / duration if duration > 0 else 0

            print(
                f"Запрос {i:2d}/{count}: "
                f"Время = {duration:.3f} с | "
                f"Размер = {size_mb:.2f} МБ | "
                f"Скорость = {speed_mbps:.2f} МБ/с"
            )

        except requests.RequestException as e:
            print(f"Ошибка при выполнении запроса {i}: {e}")
            return

    total_bytes = sum(sizes)
    total_time = sum(durations)
    avg_time = statistics.mean(durations)
    total_mb = total_bytes / (1024 * 1024)

    # Средняя скорость = общее количество МБ / общее время в секундах
    overall_speed_mbps = total_mb / total_time if total_time > 0 else 0

    print("\n" + "=" * 50)
    print("Результаты замеров:")
    print(f"Всего скачано данных: {total_mb:.2f} МБ ({total_bytes} байт)")
    print(f"Общее время загрузки: {total_time:.3f} с")
    print(f"Среднее время запроса:{avg_time:.3f} с")
    print(f"Средняя скорость:     {overall_speed_mbps:.2f} МБ/с")
    print("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Скрипт для измерения скорости интернет-соединения."
    )
    parser.add_argument(
        "--url",
        type=str,
        default=DEFAULT_URL,
        help="URL-адрес тяжелого файла или картинки",
    )
    parser.add_argument(
        "--count", type=int, default=10, help="Количество запросов (по умолчанию: 10)"
    )

    args = parser.parse_args()
    measure_speed(args.url, args.count)
