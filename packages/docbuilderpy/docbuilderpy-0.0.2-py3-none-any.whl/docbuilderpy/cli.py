import click
import os
import importlib.util
from docbuilderpy.generate import generate
from docbuilderpy.generators.generator import Generator


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--output", "-o", default="docs", help="Output path for the documentation."
)
@click.option(
    "--custom_generator",
    "-cg",
    default=None,
    help="A generator class extending from generator.py.",
)
@click.option(
    "--format",
    "-f",
    default="markdown",
    type=click.Choice(["markdown"], case_sensitive=False),
    help="Format of the documentation.",
)
def main(path, output, custom_generator, format):

    if custom_generator:
        if not os.path.isfile(custom_generator):
            print(
                f"Error: The custom generator file '{custom_generator}' does not exist."
            )
            return

        try:
            module_name = os.path.splitext(os.path.basename(custom_generator))[0]
            spec = importlib.util.spec_from_file_location(module_name, custom_generator)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, Generator)
                    and attr is not Generator
                ):
                    generator = attr()
                    break

            if not generator:
                print(f"Error: No valid Generator class found in '{custom_generator}'.")
                return

        except Exception as e:
            print(f"Error loading custom generator from '{custom_generator}': {e}")
            return

    elif format == "markdown":
        from docbuilderpy.file_generators.markdown import Markdown

        generator = Markdown()

    generate(path, output, generator)

    print(f"Docs generated {output} ({format}-Format).")


if __name__ == "__main__":
    main()
