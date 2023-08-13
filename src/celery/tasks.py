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
    parser = Parser(settings.ADMIN_FILE_PATH)

    synchronizer = Synchronizer(session=session, excel_data=parser.parse_obj(), cache=cache)

    await synchronizer.setup()


@app.task
def generate_excel_table():
    """Excel file synchronization task."""

    print('SUCCESS')

    loop = asyncio.get_event_loop()
    task = loop.create_task(run_synchronize())
    loop.run_until_complete(task)


app.conf.beat_schedule = {
    'sync-every-15-seconds': {
        'task': 'src.celery.tasks.generate_excel_table',
        'schedule': 15.0,
    },
}
