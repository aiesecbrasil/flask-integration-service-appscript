import logging
from ..globals import List,Literal
from ..dto import HttpStatus

logger = logging.getLogger(__name__)

class Storage:
    def __init__(self):
        self.__ip:list = []
    def add_ip(self,ip) -> tuple[str, Literal[HttpStatus.CONFLICT]] | None:
        logger.info(f"Permitindo IP: {ip}")
        if ip in self.__ip:
            logger.info("Ip já está liberado")
            return "IP já existe",HttpStatus.CONFLICT
        logger.info("Ip liberado com sucesso!")
        self.__ip.append(ip)
        return None

    def get_ip(self) -> List[str]:
        return self.__ip

storage = Storage()