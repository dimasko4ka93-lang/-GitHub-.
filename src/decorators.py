import functools
import logging
from datetime import datetime
from typing import Any, Callable, Optional, TypeVar, cast

# Настраиваем базовый логгер, чтобы избежать дублирования записей,
# если где-то еще в проекте используется logging.basicConfig()
logging.getLogger().handlers.clear()
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Создаем консольный обработчик по умолчанию
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(message)s'))
root_logger.addHandler(console_handler)

F = TypeVar('F', bound=Callable[..., Any])


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """
    Фабрика декоратора для логирования вызовов функций.

    :param filename: Имя файла для записи логов. Если None, вывод идет в консоль.
    """

    def decorator_log(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # На каждый вызов функции настраиваем логгер заново,
            # чтобы корректно обрабатывать смену вывода (консоль/файл).
            root_logger.handlers.clear()

            if filename:
                file_handler = logging.FileHandler(filename, mode='a', encoding='utf-8')
                file_handler.setFormatter(logging.Formatter('%(message)s'))
                root_logger.addHandler(file_handler)
            else:
                root_logger.addHandler(console_handler)

            try:
                start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                root_logger.info(f"[{start_time}] Calling function '{func.__name__}' with args={args}, kwargs={kwargs}")

                result = func(*args, **kwargs)

                end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                root_logger.info(f"[{end_time}] Function '{func.__name__}' executed successfully. Result: {result}")

                # Упрощенный вывод согласно ТЗ
                print(f"{func.__name__} ok", file=open(filename, 'a') if filename else None)  # noqa: E501

                return result
            except Exception as e:
                error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                root_logger.error(f"[{error_time}] Error in function '{func.__name__}': {e}. Inputs: {args}, {kwargs}")

                # Упрощенный вывод согласно ТЗ
                print(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}",
                      file=open(filename, 'a') if filename else None)  # noqa: E501

                raise  # Важно пробросить исключение дальше после логирования

        return cast(F, wrapper)

    return decorator_log