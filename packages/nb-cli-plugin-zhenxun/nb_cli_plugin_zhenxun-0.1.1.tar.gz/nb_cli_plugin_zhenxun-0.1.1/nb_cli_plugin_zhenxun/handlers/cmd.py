import asyncio
from pathlib import Path

from nb_cli.handlers import get_default_python


async def clone_zhenxun(git_url: str, dir_name: str = "zhenxun_bot"):
    """克隆派蒙项目

    参数:
        git_url: git仓库地址
        dir_name: 要存放的文件夹名
    """
    return await asyncio.create_subprocess_exec(
        "git",
        "clone",
        "--depth=1",
        "--single-branch",
        git_url,
        dir_name,
    )


async def run_python_command(
    command: List[str],
    python_path: Optional[str] = None,
    cwd: Optional[Path] = None,
):
    if python_path is None:
        python_path = await get_default_python()
    return await asyncio.create_subprocess_exec(
        python_path,
        "-m",
        *command,
        cwd=cwd,
    )


async def check_git() -> bool:
    """
    检查环境变量中是否存在 git

    :return: 布尔值
    """
    process = await asyncio.create_subprocess_shell(
        "git --version",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await process.communicate()
    return bool(stdout)


async def git_pull(cwd: Path | None = None):
    """
    通过git更新派蒙项目

    """
    process = await asyncio.create_subprocess_shell("git pull", cwd=cwd)
    stdout, _ = await process.communicate()
    return process
