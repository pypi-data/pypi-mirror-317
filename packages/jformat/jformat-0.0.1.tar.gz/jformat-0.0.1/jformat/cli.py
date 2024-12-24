import click
import json

def format_json(content, sort_keys):
    """Format JSON content with specified sorting."""
    loaded_json = json.loads(content)
    return json.dumps(loaded_json, sort_keys=sort_keys, indent=4)

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--sort/--no-sort', default=True, help='Enable/disable sorting of JSON keys')
def main(file_path, sort):
    """JSON formatting tool that reads a file and outputs formatted JSON."""
    with open(file_path, 'r') as file:
        print(format_json(file.read(), sort))

if __name__ == '__main__':
    main()