class PrintToList(object):
    def __init__(self, passed_list):
        self.list = passed_list

    def __enter__(self):
        return self   # return instance of A which is assign to `f`.

    def write(self, text):
        self.list.append(str(text))

    def __exit__(self, *args):
        return True
