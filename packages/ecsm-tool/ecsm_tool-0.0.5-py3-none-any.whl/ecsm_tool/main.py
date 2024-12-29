
from ecsm_tool.ecsm_cli import cli, cli_images, cli_node

def main():

    client = cli.CLI()
    client.register_command_group(cli_images.CLI_IMAGES())
    client.register_command_group(cli_node.CLI_NODE())
    client.run()

if __name__ == "__main__":
    main()
