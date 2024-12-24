from asyncio import events
import functools
import contextvars


async def to_thread(executor, func, /, *args, **kwargs):
    loop = events.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(executor, func_call)
