import asyncio
from QorpoApp.dataBase.models import create_tables

asyncio.run(create_tables())
