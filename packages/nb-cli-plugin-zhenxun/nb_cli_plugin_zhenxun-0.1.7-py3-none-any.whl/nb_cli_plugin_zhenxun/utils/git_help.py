import asyncio
import os
from pathlib import Path
import shutil
import stat

import click
from nb_cli.cli import CLI_DEFAULT_STYLE
from nb_cli.cli.commands.project import project_name_validator
from noneprompt import (
    Choice,
    InputPrompt,
    ListPrompt,
)


class GitInstallHelp:
    @classmethod
    async def check_git(cls):
        """
        检查环境变量中是否存在 git
        """
        process = await asyncio.create_subprocess_shell(
            "git --version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await process.communicate()
        return bool(stdout)

    @classmethod
    async def __clone_zhenxun(cls, git_url: str, dir_name: str = "zhenxun_bot"):
        """克隆项目

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

    @classmethod
    async def check_path(cls, ctx: click.Context) -> str:
        """路径检测

        参数:
            ctx: ctx
            project_name: 项目名称

        返回:
            str: 项目名称
        """
        project_name = await InputPrompt(
            "项目名称:",
            default_text="zhenxun_bot",
            validator=project_name_validator,
        ).prompt_async(style=CLI_DEFAULT_STYLE)
        while True:
            project_path = Path() / project_name
            if project_path.is_dir():
                dir_choice = await ListPrompt(
                    "当前目录下已存在同名项目文件夹，如何操作?",
                    [
                        Choice("删除该文件夹并重新克隆", "delete"),
                        Choice("使用该文件夹中的内容并继续", "use"),
                        Choice("重新命名", "rename"),
                        Choice("取消安装", "exit"),
                    ],
                    default_select=0,
                ).prompt_async(style=CLI_DEFAULT_STYLE)
                if dir_choice.data == "rename":
                    pass
                elif dir_choice.data == "delete":

                    def delete(func, path_, execinfo):
                        os.chmod(path_, stat.S_IWUSR)
                        func(path_)

                    shutil.rmtree((project_path).absolute(), onerror=delete)
                    await asyncio.sleep(0.2)
                    return ""
                elif dir_choice.data == "use":
                    return project_name
                else:
                    ctx.exit()
            else:
                return ""

    @classmethod
    async def start_clone(cls, ctx: click.Context, project_name: str):
        """克隆项目

        参数:
            ctx: ctx
            project_name: 项目文件夹名称
        """
        git_url = await ListPrompt(
            "要使用的克隆源?",
            [
                Choice(
                    "github官方源(国外推荐)",
                    "https://github.com/HibiKier/zhenxun_bot",
                ),
                Choice(
                    "cherishmoon镜像源(国内推荐)",
                    "https://github.cherishmoon.fun/https://github.com/HibiKier/zhenxun_bot",
                ),
                Choice(
                    "ghproxy镜像源(国内备选1)",
                    "https://ghproxy.com/https://github.com/HibiKier/zhenxun_bot",
                ),
            ],
            default_select=1,
        ).prompt_async(style=CLI_DEFAULT_STYLE)
        click.secho(f"在 {project_name} 文件夹克隆源码...", fg="yellow")
        clone_result = await cls.__clone_zhenxun(git_url.data, project_name)
        await clone_result.wait()
        click.secho(f"{project_name} 克隆完成！", fg="yellow")
