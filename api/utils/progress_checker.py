import sys
import time


class ProgressChecker:
    @staticmethod
    def get_progress(detail: str, current: int, total: int, start_time: float) -> None:
        progress = current / total
        bar_length = 50
        bar_str = (
            f"{detail}: ["
            + "=" * int(progress * bar_length)
            + " " * (bar_length - int(progress * bar_length))
            + "]"
        )
        sys.stdout.write(
            "\r"
            + bar_str
            + " "
            + str(int(progress * 100))
            + "%"
            + f" (Tempo decorrido: {time.time() - start_time:.2f}s) "
        )
        sys.stdout.flush()
