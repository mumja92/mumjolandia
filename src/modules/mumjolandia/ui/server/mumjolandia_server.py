import logging
from threading import Thread

from src.modules.mumjolandia.config_loader import ConfigLoader
from src.modules.mumjolandia.ui.server.mumjolandia_server_connection_handler import MumjolandiaServerConnectionHandler


class MumjolandiaServer(Thread):
    def __init__(self, data_passer):
        Thread.__init__(self)
        self.data_passer = data_passer

    def __del__(self):
        logging.info('Server exited')

    def run(self):
        try:
            logging.info('Server started')
            MumjolandiaServerConnectionHandler(data_passer=self.data_passer,
                                               port=ConfigLoader.get_config().background_server_port,
                                               server_accepted_networks_mask="127.0.0.1",
                                               ).start_server(run_once=False)
        except OSError as e:
            logging.error("Server failed to start: " + str(e))
