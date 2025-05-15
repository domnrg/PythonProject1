import functools


def log(filename=None):
    """Декоратор, который будет автоматически регистрировать детали выполнения функций"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log_message = ""
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
                return result
            except Exception as e:
                log_message = f"{func.__name__} error: {type(e).__name__}. " f"Inputs: {args}, {kwargs}"
                raise
            finally:
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

        return wrapper

    return decorator
