from src.modules.command.command_factory import CommandFactory
from src.modules.connection.mumjolandia_connection_handler import MumjolandiaConnectionHandler
from src.modules.mumjolandia.ui.mumjolandia_result_parser import MumjolandiaResultParser


class MumjolandiaServerConnectionHandler(MumjolandiaConnectionHandler):
    def __init__(self, data_passer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_passer = data_passer

    # override base private method
    def _MumjolandiaConnectionHandler__parse_received_message(self, message):
        if message == 'exit':
            self.server_loop_exit_flag = True
            return_value = 'Server shutting down'
        else:
            return_value = MumjolandiaResultParser().parse(self.data_passer.pass_command(CommandFactory.get_command(message)))
        return return_value
