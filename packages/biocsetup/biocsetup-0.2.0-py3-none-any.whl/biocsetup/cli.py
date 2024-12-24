import click

from biocsetup.create_repository import create_repository

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


@click.command()
@click.argument("project_path")
@click.option("--description", "-d", help="Project description", default="Add a short description here!")
@click.option("--license", "-l", default="MIT", help="License (default: MIT)")
def main(project_path: str, description: str, license: str):
    """Create a new BiocPy Python package."""
    create_repository(
        project_path=project_path,
        description=description,
        license=license,
    )


if __name__ == "__main__":
    main()
