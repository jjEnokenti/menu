import asyncio

from src.cache.service import get_cache
from src.celery.app import app
from src.celery.parser import Parser
from src.celery.utils import Synchronizer
from src.config import settings
from src.db.core import session as async_session


async def run_synchronize():
    """Run synchronization."""

    session = async_session
    cache = await get_cache()
    parse_data = Parser(mode=settings.FILE_READ_MODE).get_data

    synchronizer = Synchronizer(session=session, excel_data=parse_data, cache=cache)

    await synchronizer.setup()


@app.task
def synchronize_db():
    """Excel file synchronization task."""

    loop = asyncio.get_event_loop()
    task = loop.create_task(run_synchronize())
    loop.run_until_complete(task)


app.conf.beat_schedule = {
    'sync-every-15-seconds': {
        'task': 'src.celery.tasks.synchronize_db',
        'schedule': 15.0,
    },
}
