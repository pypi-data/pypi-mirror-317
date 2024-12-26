import asyncio
import time
import shutil
import os
import traceback


async def run_find_files_asyncio(root: str) -> list[str]:
    """
    异步调用 find 命令并返回结果, 仅支持 Linux 系统, 返回文件，不包括目录

    Args:
        root (str): 要扫描的目录

    Returns:
        List[str]: 文件的路径列表
    """
    process = await asyncio.create_subprocess_exec(
        'find', root, '-type', 'f',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise RuntimeError(f"find error: {stderr.decode().strip()}")
    output_str = stdout.decode().strip()
    if not output_str:
        return []
    return output_str.split('\n')


async def run_fd_files_asyncio(root: str, allow_find: bool = False) -> list[str]:
    """
    异步调用 fd 或 fdfind 或 find 命令并返回结果，仅支持 Linux 系统，返回文件路径列表，不包括目录。

    Args:
        root (str): 要扫描的目录
        allow_find (bool): 是否允许回退到 find 命令

    Returns:
        List[str]: 文件的路径列表
    """
    # 自动检测可用的命令
    fd_command = shutil.which('fdfind') or shutil.which('fd')

    if fd_command:
        # 使用 fd 或 fdfind
        process = await asyncio.create_subprocess_exec(
            fd_command, '--type', 'f', '--hidden', '--absolute-path', '.',
            root,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"{fd_command} error: {stderr.decode().strip()}")
        output_str = stdout.decode().strip()
        if not output_str:
            return []
        return output_str.split('\n')
    elif allow_find:
        # 回退到 find
        return await run_find_files_asyncio(root)
    else:
        raise RuntimeError("fd or fdfind not found, 'apt install fd-find' can be used to install.")


def handle_background_task_completion(task: asyncio.Task):
    """处理重要的后台任务完成, 不允许出现异常"""
    try:
        task.result()  # 获取任务结果，触发异常
    except asyncio.CancelledError:
        # 不退出，因为手动取消是正常行为
        ...
    except BaseException as e:
        print(f"Critical task failed: {e}")
        traceback.print_exc()
        os._exit(1)  # 终止主进程，重要任务不应该出现异常


async def main():
    root_directory = os.path.dirname(os.getcwd())
    start = time.time()
    files = await run_fd_files_asyncio(root_directory)
    print(f"Found {len(files)} files.", time.time() - start)


if __name__ == "__main__":
    asyncio.run(main())
