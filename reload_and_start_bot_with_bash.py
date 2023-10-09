import asyncio
import os
from pathlib import Path
import subprocess
from subprocess import CREATE_NEW_CONSOLE
from psutil import Process, NoSuchProcess

from application.loader import logger
from shlex import quote as shlex_quote

DELAY: int = 5


async def start_bot() -> subprocess.Popen:
    """Запуск процесса бота из .bat"""

    proc_path: str = str(Path(__file__).resolve().parent)
    proc_path_file = str(Path(proc_path, 'application', 'activate'))
    path_to_venv = str(Path(proc_path, 'venv', 'Scripts', 'python.exe'))

    process: subprocess.Popen = subprocess.Popen(
        [proc_path_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        creationflags=CREATE_NEW_CONSOLE
    )
    stdout, stderr = process.communicate()
    print(f'{stdout = }')
    print(f'{stderr = }')
    return process

    # proc_path: str = str(Path(__file__).resolve().parent)
    # proc_path_file = f'{proc_path}\\MyBot_Run.bat'
    #
    # process: subprocess.Popen = subprocess.Popen(
    #     args=[proc_path_file],
    #     # stdout=subprocess.PIPE,
    #     # stderr=subprocess.PIPE,
    #     shell=True
    #     # creationflags=CREATE_NEW_CONSOLE)
    # )
    # # stdout, stderr = process.communicate()
    # # print(f'{stdout = }')
    # # print(f'{stderr = }')
    # return process

    # files = ["activate_this.py", "app.py", ]  # файлы, которые нужно запустить "start",
    #
    # # запускаем процессы
    # procs = [subprocess.Popen(args=["start", "/WAIT", "python3", f'{proc_path}\\application\\{file}'],
    #                           shell=True,
    #                           stdout=subprocess.PIPE)
    #          for file in files]
    # print(f"Запущено {len(procs)} процессов")
    #
    # # # ждём их завершения
    # while procs:
    #     procs.pop().wait()
    #     print(f"Осталось {len(procs)} процессов")
    #
    # print("Конец")
    #
    # return procs[0] if procs else []


async def kill_bot(proc):
    """Остановка процесса бота и всех дочерних процессов"""
    pobj = Process(proc.pid)

    try:
        for children in pobj.children(recursive=True):  # list children & kill them
            try:
                children.kill()
                logger.info(f'{children = }')
            except NoSuchProcess:
                logger.info('NoSuchProcess')

        pobj.kill()
        logger.info('all children processes kill')

    except Exception as err:
        logger.error(f'{repr(err)}')
        logger.info("taskkill /f /im MyBot_Run.bat")


async def get_trigger() -> bool:
    """

    :return: bool
    """

    for file in Path('.').iterdir():
        if 'trigger' in file.name:
            return True

    return False


async def del_trigger():
    """

    :return: bool
    """
    for file in Path('.').iterdir():
        if 'trigger' in file.name:
            try:
                os.remove(file)
                return True
            except FileNotFoundError as err:
                logger.error(f'{file.name = } {repr(err)}')

    return False


async def reload_bot():
    """

    :return:
    """

    # path = os.path.abspath(os.curdir)
    # repo = Repo(path)

    prog = await start_bot()
    try:
        while True:

            await asyncio.sleep(DELAY)

            # if await get_update_from_git(repo):
            if await get_trigger():
                await kill_bot(prog)
                await asyncio.sleep(DELAY)
                prog = await start_bot()
                await del_trigger()

    except Exception as err:
        logger.error(f'{repr(err)}')
        await kill_bot(prog)
        await reload_bot()
    finally:

        await kill_bot(prog)


if __name__ == '__main__':
    asyncio.run(reload_bot())
