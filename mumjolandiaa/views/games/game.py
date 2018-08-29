import xml.etree.ElementTree as ET


class Game:
    def __init__(self, text):
        self.name = text
        self.tags = ['raz', 'dwa', 'trzy']

    def to_xml(self):
        root_element = ET.Element("game")
        tags_element = ET.Element("tags")
        ET.SubElement(root_element, "name").text = self.name
        root_element.append(tags_element)
        for t in self.tags:
            ET.SubElement(tags_element, "tag").text = t
        xmlstr = ET.tostring(root_element).decode()
        print(xmlstr)
        return xmlstr
