from ayano.middlewares.valistaions import CompareAttrsMiddleware


def block_middleware() -> CompareAttrsMiddleware:
    return CompareAttrsMiddleware("user", "is_block", True)
