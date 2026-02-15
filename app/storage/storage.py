class Storage:
    def __init__(self):
        self.__ip:list = []
    def add_ip(self,ip):
        self.__ip.append(ip)
    def get_ip(self):
        return self.__ip

storage = Storage()