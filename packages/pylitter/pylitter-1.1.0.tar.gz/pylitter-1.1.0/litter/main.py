from litter.uploader import *
import click

uploader_classes = {
    "catbox": CatboxUploader,
    "litterbox": LitterboxUploader,
}


def upload(host, file, **time):
    try:
        uploader_class = uploader_classes[host]
        uploader_instance = uploader_class(file, **time)

        result = uploader_instance.execute()
        print(f"\nYour link : {result}")
    except Exception as e:
        print(e)


@click.group(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
    epilog="Check out our repo at https://github.com/moiSentineL/litter for more details",
)
@click.argument("file")
@click.pass_context
def cli(ctx, file):
    """
    Upload to Litterbox/Catbox

    Usage: throw file (for|forever) [1h|12h|24h|72h]

    \b
    Example: throw file.jpg for 12h -> temporary
    Example: throw file.mp4 forever -> permanent
    """
    ctx.ensure_object(dict)
    ctx.obj["file"] = file  # Store arg1 for use in commands


@cli.command(name="for")
@click.argument("time")
@click.pass_context
def for_command(ctx, time):
    """
    Upload to Litterbox (temporarily);

    TIME can be 1h/12h/24h/72h
    """
    upload("litterbox", ctx.obj["file"], time=time)


@cli.command()
@click.pass_context
def forever(ctx):
    """
    Upload to Catbox (forever)
    """
    upload("catbox", ctx.obj["file"])


if __name__ == "__main__":
    cli()
