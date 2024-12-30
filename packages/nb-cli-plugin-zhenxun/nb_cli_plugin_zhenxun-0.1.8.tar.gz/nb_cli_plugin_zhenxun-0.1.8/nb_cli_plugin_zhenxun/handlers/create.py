import asyncio
from pathlib import Path
import sys

import click
from nb_cli.cli import CLI_DEFAULT_STYLE
from nb_cli.handlers import get_default_python
from noneprompt import InputPrompt

from ..utils.download_help import DownloadInstallHelp
from ..utils.git_help import GitInstallHelp


def check_python_version():
    """
    检查 python 版本
    """
    return sys.version_info < (3, 10)


async def run_git_install(ctx: click.Context) -> str:
    project_name = await GitInstallHelp.check_path(ctx)
    if not project_name:
        click.secho("项目克隆源码失败...", fg="yellow")
        ctx.exit()
    await GitInstallHelp.start_clone(ctx, project_name)
    return project_name


async def run_download_install(ctx: click.Context) -> str:
    return await DownloadInstallHelp.download_install(ctx)


async def setting_env(ctx: click.Context, project_name: str):
    """设置配置文件

    参数:
        ctx: ctx
        project_name: 项目名称
    """
    project_path = Path() / project_name
    env_path = project_path / ".env.dev"
    if not env_path.is_file():
        ctx.exit()

    env_file = env_path.read_text(
        encoding="utf-8",
    )
    superusers = await InputPrompt(
        "超级用户QQ(即你自己的QQ号，多个用空格隔开):",
        validator=lambda x: x.replace(" ", "").isdigit(),
    ).prompt_async(style=CLI_DEFAULT_STYLE)
    if superusers := superusers.replace(" ", '", "'):
        env_file = env_file.replace(
            'SUPERUSERS=[""]',
            f'SUPERUSERS=["{superusers}"]',
        )

    db_url = await InputPrompt(
        "请输入数据库连接地址（为空则使用sqlite）:",
    ).prompt_async(style=CLI_DEFAULT_STYLE)
    if not db_url:
        (project_path / "data" / "db").mkdir(parents=True, exist_ok=True)
        db_url = "sqlite:data/db/zhenxun.db"
        env_file = env_file.replace(
            'DB_URL = ""',
            f'DB_URL = "{db_url}"',
        )

    env_path.write_text(
        env_file,
        encoding="utf-8",
    )


async def install_poetry(
    project_path: Path, python_path: str | None, pip_args: list[str] | None = None
):
    """
    安装poetry
    """
    if pip_args is None:
        pip_args = []
    if python_path is None:
        python_path = await get_default_python()
    return await asyncio.create_subprocess_exec(
        python_path,
        "-m",
        "pip",
        "install",
        "poetry",
        *pip_args,
        cwd=project_path.absolute(),
    )


async def install_dependencies(
    project_name: str,
    python_path: str | None,
    pip_args: list[str] | None = None,
):
    if pip_args is None:
        pip_args = []
    project_path = Path() / project_name
    click.secho("开始安装Poetry包管理器...", fg="yellow")
    proc = await install_poetry(project_path, python_path, pip_args)
    await proc.wait()
    click.secho("安装Poetry包管理器完成！", fg="yellow")
    if python_path is None:
        python_path = await get_default_python()
    requirement_path = project_path / "requirements.txt"
    click.secho("开始尝试安装小真寻依赖...", fg="yellow")
    return await asyncio.create_subprocess_exec(
        python_path,
        "-m",
        "poetry",
        "run",
        "pip",
        "install",
        "-r",
        str(requirement_path),
        *pip_args,
        cwd=project_path.absolute(),
    )
