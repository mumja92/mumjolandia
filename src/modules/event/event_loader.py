import logging
from pathlib import Path

from src.modules.event.event_factory import EventFactory
from src.external.xmltodict import xmltodict


class EventLoader:
    def __init__(self, filename):
        self.file = filename

    def get(self):
        events = []
        file = Path(self.file)
        if not file.is_file():
            logging.warning('Could not open events file based on name: "' + self.file + '"')
            return events
        with open(self.file, 'r') as my_file:
            data = my_file.read()
        d = xmltodict.parse(data)
        try:
            for e in d['events']['event']:
                try:
                    event = EventFactory.get_event(e['name'], e['date'])
                except KeyError:
                    logging.warning('Incorrect xml entry')
                    continue
                if event is not None:
                    events.append(event)
                else:
                    logging.warning('EventFactory returned None for name = "' +
                                    str(e['name'] or '') + '" and date="' + str(e['date'] or '') + '"')
        except KeyError:
            logging.warning('File does not have <events><event/></events> structure')
        return events

    def save(self, events):
        pass
