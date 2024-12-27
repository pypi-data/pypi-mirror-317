import click
import pathlib
import os
import shutil
import build.__main__ as bm


@click.command()
@click.argument("package_path", type=str, default=".")
def cli(package_path):
    package_path = pathlib.Path(package_path).absolute()
    parent = package_path.parent
    basename = os.path.basename(package_path)

    folder_list = ["dist", f"{basename}.egg-info"]
    file_list = ["pyproject.toml", "README.md", "README.rst"]

    # 清理文件
    for pre in [parent, package_path]:
        for folder in folder_list:
            path = pre.joinpath(folder)
            if os.path.exists(path):
                shutil.rmtree(path)

    # 移出文件
    for file in file_list:
        path = package_path.joinpath(file)
        if os.path.exists(path):
            shutil.move(path, parent.joinpath(file))

    # build
    os.chdir(parent)
    bm.main([], "python -m build")
    # os.system(r"python -m build")

    # 移入文件和文件夹
    for file in file_list:
        path = parent.joinpath(file)
        if os.path.exists(path):
            shutil.move(path, package_path.joinpath(file))
    for folder in folder_list:
        shutil.move(parent.joinpath(folder), package_path)


if __name__ == "__main__":
    cli()
