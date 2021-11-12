class ConfigParser:
    def __init__(self, config_path):
        self.path = config_path

    def get(self, name):
        with open(self.path, "r") as file:
            lines = file.readlines()
        wanted_start_tag = "<" + name + ">"
        wanted_end_tag = "</" + name + ">"
        for line in lines:
            start_index = line.find(wanted_start_tag)
            if start_index > -1:
                end_index = line.find(wanted_end_tag)
                if end_index > -1:
                    return line[start_index + len(wanted_start_tag):end_index]
        return None

    def set(self, name, value):
        with open(self.path, "r") as file:
            lines = file.readlines()
        value_updated = False
        wanted_start_tag = "<" + name + ">"
        wanted_end_tag = "</" + name + ">"
        for index, line in enumerate(lines):
            start_index = line.find(wanted_start_tag)
            if start_index > -1:
                end_index = line.find(wanted_end_tag)
                if end_index > -1:
                    old = line[start_index + len(wanted_start_tag):end_index]
                    lines[index] = line.replace(old, value)
                    value_updated = True
                    break
        if value_updated:
            with open(self.path, "w") as file:
                file.writelines(lines)
            return True
        return False
