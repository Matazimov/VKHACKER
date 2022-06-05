from MyClasses.FirstMethod import FirstMethod
from loguru import logger
import asyncio

logger.add('logs.log')
first_method = FirstMethod()
asyncio.run(first_method.run())
