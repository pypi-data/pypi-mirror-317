import threading
import time

import click

from dataset_sh.server.daemon import daemon_is_running, launch_daemon_app


@click.command(name='gui')
@click.argument('dataset')
@click.option('--host', '-h', 'host', help='if daemon is not running, make the daemon listen to this host.',
              default='localhost')
@click.option('--port', '-p', 'port', help='if daemon is not running, run the daemon on this port.', default=48989)
def gui_cli(dataset, host, port):
    """inspect dataset in web-based gui"""
    host_port = daemon_is_running()
    if host_port:
        host, port = host_port
        click.launch(f'http://{host}:{port}/dataset/{dataset}')
    else:

        def open_browser():
            # Wait a few seconds before opening the browser
            time.sleep(1)
            click.launch(f'http://{host}:{port}/dataset/{dataset}')

        threading.Thread(target=open_browser).start()
        launch_daemon_app(host, port)
