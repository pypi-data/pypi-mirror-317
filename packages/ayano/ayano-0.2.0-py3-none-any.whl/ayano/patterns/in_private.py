from ayano.middlewares import ChatTypeValidationMiddleware, AiogramChatTypes


def private_chat_middleware():
    return ChatTypeValidationMiddleware(AiogramChatTypes.private)


def channel_chat_middleware():
    return ChatTypeValidationMiddleware(AiogramChatTypes.channel)


def group_chat_middleware():
    return ChatTypeValidationMiddleware(AiogramChatTypes.group)


def supergroup_chat_middleware():
    return ChatTypeValidationMiddleware(AiogramChatTypes.supergroup)


def private_and_group_chat_middleware():
    return ChatTypeValidationMiddleware(AiogramChatTypes.private, AiogramChatTypes.group)
