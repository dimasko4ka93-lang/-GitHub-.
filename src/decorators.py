import functools
import logging
from datetime import datetime
from typing import Any, Callable, Optional, TypeVar, cast

# Настраиваем базовый логгер
logging.getLogger().handlers.clear()
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

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
            root_logger.handlers.clear()

            if filename:
                file_handler = logging.FileHandler(
                    filename, mode='a', encoding='utf-8'
                )
                file_handler.setFormatter(logging.Formatter('%(message)s'))
                root_logger.addHandler(file_handler)
            else:
                root_logger.addHandler(console_handler)

            try:
                start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Используем переменную для длинного сообщения
                call_msg = (
                    f"[{start_time}] Calling '{func.__name__}' "
                    f"with args={args}, kwargs={kwargs}"
                )
                root_logger.info(call_msg)

                result = func(*args, **kwargs)

                end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                root_logger.info(f"[{end_time}] Function '{func.__name__}' OK")

                # Сокращаем строку print максимально
                msg_ok = f"{func.__name__} ok"
                print(msg_ok, file=open(filename, 'a') if filename else None)

                return result
            except Exception as e:
                error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Короткое сообщение для логгера ошибок
                err_msg = (
                    f"[{error_time}] Error in '{func.__name__}': {e}. "
                    f"Inputs:{args},{kwargs}"
                )
                root_logger.error(err_msg)

                # Ещё более короткая строка для print
                err_data = f"{type(e).__name__}. Inputs:{args},{kwargs}"
                print(
                    f"{func.__name__} error: {err_data}",
                    file=open(filename, 'a') if filename else None,
                )

                raise

        return cast(F, wrapper)

    return decorator_log
