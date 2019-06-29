import datetime
import logging

from src.interface.event.event import Event


class EventFactory:
    @staticmethod
    def get_event(name=None, date=None):
        try:
            if isinstance(date, str):
                date = datetime.datetime.strptime(date, '%d-%m')
        except ValueError:
            logging.warning('Incorrect date format: ' + date)
            date = None
        if name is None:
            logging.warning('Name is "None"')
        else:
            try:
                name = str(name)
            except ValueError:
                logging.warning('Name is not a string, but: "' + type(name) + '"')
                name = None
        if name is None or date is None:
            logging.warning('Event creation failed')
            return None
        else:
            return Event(name, date)
