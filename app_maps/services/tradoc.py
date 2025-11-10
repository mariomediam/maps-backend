import os
from dotenv import load_dotenv
import requests

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class TradocService:

    def __init__(self):
        self.SIAC_IP = os.getenv('SIAC_IP')
        self.SIAC_PORT = os.getenv('SIAC_PORT')

    def get_tradoc_by_depend_numero(self, depend: int, numero: str):
        url = f'http://{self.SIAC_IP}:{self.SIAC_PORT}/api/tradoc/selecc-docum?opcion=NUMERO&c_depend={depend}&m_docum_numdoc={numero}'
        response = requests.get(url)
        return response.json()

    def get_tradoc_by_c_docum(self, c_docum: str):
        url = f'http://{self.SIAC_IP}:{self.SIAC_PORT}/api/tradoc/selecc-docum?opcion=C_DOCUM&c_docum={c_docum}'
        response = requests.get(url)
        return response.json()

    def get_path(self, c_docum: str):
        url = f'http://{self.SIAC_IP}:{self.SIAC_PORT}/api/tradoc/ver-ultima-rama-arbol?c_docum={c_docum}'
        response = requests.get(url)
        return response.json()



