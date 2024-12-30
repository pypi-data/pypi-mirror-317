from pathlib import Path

import click
from nb_cli.cli import CLI_DEFAULT_STYLE, ClickAliasedCommand, run_async
from noneprompt import (
    CancelledError,
    ConfirmPrompt,
)

from ..handlers.create import (
    GitInstallHelp,
    check_python_version,
    install_dependencies,
    run_download_install,
    run_git_install,
    setting_env,
)


@click.command(
    cls=ClickAliasedCommand,
    aliases=["new", "init"],
    context_settings={"ignore_unknown_options": True},
    help="在当前目录下安装小真寻.",
)
@click.option(
    "-p",
    "--python-interpreter",
    default=None,
    help="指定Python解释器的路径",
)
@click.option(
    "-i",
    "--index-url",
    "index_url",
    default="https://mirrors.aliyun.com/pypi/simple/",
    help="pip下载所使用的镜像源",
)
@click.pass_context
@run_async
async def create(
    ctx: click.Context,
    python_interpreter: str | None,
    index_url: str,
):
    """在当前目录下安装小派蒙以及go-cqhttp."""
    try:
        click.clear()
        click.secho("正在检测python版本...", fg="yellow")
        if not check_python_version():
            click.secho(
                "当前python版本过低，python版本至少需要3.10及以上！", fg="yellow"
            )
            ctx.exit()
        click.secho("开始安装小真寻...", fg="yellow")
        if not await GitInstallHelp.check_git():
            project_name = await run_download_install(ctx)
        else:
            project_name = await run_git_install(ctx)
        await setting_env(ctx, project_name)
        is_install_dependencies = await ConfirmPrompt(
            "立刻安装依赖?",
            default_choice=True,
        ).prompt_async(style=CLI_DEFAULT_STYLE)
        if is_install_dependencies:
            proc = await install_dependencies(
                project_name, python_interpreter, ["-i", index_url]
            )
            await proc.wait()
            click.secho("安装小真寻依赖完成！", fg="yellow")
        if not (Path() / project_name).is_dir():
            ctx.exit()

        click.secho(
            "一切准备就绪，请使用命令 poetry run python bot.py 启动小真寻吧！",
            fg="yellow",
        )

    except CancelledError:
        ctx.exit()
