import click
import requests
from dataclasses import dataclass, field
from typing import Optional
import pydantic
import httpx
import asyncio
import json
from google.cloud import storage
import os

SECRET_MANAGER = "https://visiocue--secretmanager-api-app.modal.run/"
# do curl SECRET_MANAGER

async def get_secrets(key: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(SECRET_MANAGER, params={"key": str})
        return response.json()

@dataclass
class Part:
    binary_content: Optional[bytes]
    text_content: Optional[str]
    
    def draw_box(self, box):
        # assume binary_content is image
        pass


@click.group()
def cli():
    pass

@cli.command()
@click.option(
    "--option", type=click.Choice(["luggage", "cat"]), help="Pick an option"
)
@click.option("--width", type=int, help="Specify the width")
@click.option("--height", type=int, help="Specify the height")
def mock(option, width, height):
    name = "mock_"
    import random

    name += str(random.randint(1, 10000))
    if not option or option == "luggage":
        from .luggage import conveyor_belt

        conveyor_data_uri = conveyor_belt
        import base64
    
        from term_image.image import from_file, from_url


        if "data:image/jpeg;base64," in conveyor_data_uri:
            conveyor_data_uri = conveyor_data_uri.replace("data:image/jpeg;base64,", "")
        conveyor_data_uri = base64.b64decode(conveyor_data_uri)
        with open(name + ".jpg", "wb") as f:
            f.write(conveyor_data_uri)
        image = from_url("https://cataas.com/cat")

        terminal_image = from_file(name + ".jpg")
        terminal_image.draw()
        pass
    width = width or 200
    height = height or 200

    if option == "cat" or not option:
        response = requests.get(
            "https://cataas.com/cat?width=" + str(width) + "&height=" + str(height)
        )
        import random

        opts = ["full", "blaze", "act", "inst", "woo"]
        opts2 = ["box", "way", "play", "tune"]
        name = random.choice(opts) + random.choice(opts2)
        with open(f"{name}.jpg", "wb") as f:
            f.write(response.content)
        click.echo(f"Downloaded image to {name}.jpg")

    if width and height:
        click.echo(f"Width: {width}, Height: {height}")


@cli.command()
@click.option("--norm", type=click.Path(exists=True), help="Path to the image file")
@click.argument("image_path", type=str)
def bbox(norm):
    click.echo(f"Processing image: {norm}")
    part = asyncio.parse_part(norm)


@cli.command()
@click.option("--bbox", type=bool)
@click.option("--key", type=str)
@click.argument("parts", type=str, nargs=-1)
def ask(bbox, key, parts):
    click.echo(f"Running command: {command} on image: {image_path}")
    # Add your image processing logic here
    # For example, you can use the supervision library to process the image
    # image = sv.Image.open(image_path)
    # Process the image based on the command
    if command == "example_command":
        # Example processing
        processed_image = image.process_example()
        processed_image.save("processed_" + image_path)
        click.echo(f"Processed image saved as: processed_{image_path}")
    else:
        click.echo(f"Unknown command: {command}")


@cli.command()
def dump():
    """Dump"""
    password = "F0e|q?qSb%U@"
    password += "NF="
    sec = get_secrets(password)
    secrets = asyncio.run(sec)
    click.echo(json.dumps(secrets, indent=4))


@cli.command()
@click.argument("image_path", type=click.Path(exists=True))
def annotate(image_path):
    """Annotate an image by sending it to the annotation service and drawing the results."""
    import random
    from PIL import Image, ImageDraw
    if "jpg" not in image_path:
        click.echo("Only JPG images are supported.")
        return
    # Read the image
    with open(image_path, "rb") as f:
        image_data = f.read()

    # Send the image to the annotation service as a binary octet stream
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post("https://annotate.cloud.visiocue.com/", data=image_data, headers=headers)
    bboxes = response.json()

    # Open the image with PIL
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Draw the bounding boxes
    for bbox in bboxes:
        y1, x1, y2, x2, label = bbox
        width, height = image.size
        draw.rectangle([x1 * width, y1 * height, x2 * width, y2 * height], outline="red", width=2)
        draw.text((x1 * width, y1 * height), label, fill="red")

    # Save the annotated image to a random path
    random_name = f"annotated_{random.randint(1, 10000)}.jpg"
    image.save(random_name)
    click.echo(f"Annotated image saved as: {random_name}")


@cli.command()
@click.argument("service_account_json", type=str)
@click.argument("bucket_name", type=str)
@click.argument("source_blob_name", type=str)
@click.argument("destination_file_name", type=str)
def download_file(service_account_json, bucket_name, source_blob_name, destination_file_name):
    """Download a file from a Google Cloud Storage bucket to a local path."""
    # Set the environment variable for the service account
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_json

    # Initialize a client
    storage_client = storage.Client.from_()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Get the blob
    blob = bucket.blob(source_blob_name)

    # Download the blob to a local file
    blob.download_to_filename(destination_file_name)

    click.echo(f"Downloaded {source_blob_name} from bucket {bucket_name} to {destination_file_name}")


if __name__ == "__main__":
    print("AA")
    cli()
