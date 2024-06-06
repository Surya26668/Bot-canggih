from .start import *
from .convert import *
from .pecahtxt import *
from .pecahvcf import *
from .convertvcf import *
from .convertxlsx import *

def handle_command(user_id, command):
    if not is_whitelisted(user_id):
        print("Pengguna tidak termasuk whitelist.")
        return
        
    if command == "start":
        start()
    elif command == "convert":
        convert()
    else:
        print("Perintah tidak dikenal")

user_id = "6243471475"
