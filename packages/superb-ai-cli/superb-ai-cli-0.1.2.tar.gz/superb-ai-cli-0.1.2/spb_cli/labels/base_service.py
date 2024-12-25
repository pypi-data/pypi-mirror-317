from spb_label.sdk import Client


class BaseService():
    def __init__(self):
        self.client = Client()
