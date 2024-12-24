
from contextlib import contextmanager
from pathlib import Path, PosixPath
from loguru import logger


@contextmanager
def lock(link_paths: list[str|PosixPath], timeout: int=10):
    """上下文管理器，确保在删除软链接时不被读取。"""

    lock_links = [Path(link_path).with_suffix('.lock') for link_path in link_paths]
    should_cleanup = [False] * len(lock_links)
    try:
        # 创建锁文件，表示正在使用链接
        for i,lock_file in enumerate(lock_links):
            lock_file.touch(exist_ok=False)
            should_cleanup[i] = True
        yield  # 在这个上下文中执行
    except FileExistsError:
        logger.warning('文件已被锁定，请稍后再试')
        raise
    finally:
        # 删除锁文件
        for j, lock_file in enumerate(lock_links):
            if lock_file.exists() and should_cleanup[j]:
                lock_file.unlink()


try:
    with lock(['a.txt', 'b.txt']):
        Path('a.txt').touch(exist_ok=True)
        Path('b.txt').touch(exist_ok=True)
except FileExistsError:
    logger.warning('文件已被锁定，请稍后再试')

