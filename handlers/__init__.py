from .start import *
from .convert import *
from .pecahtxt import *
from .pecahvcf import *
from .convertvcf import *
from .convertxlsx import *

# Contoh fungsi penanganan perintah
def handle_command(user_id, command):
    if not is_whitelisted(user_id):
        print("Pengguna tidak termasuk whitelist.")
        return

    # Logika penanganan perintah yang ada
    if command == "start":
        start()
    elif command == "convert":
        convert()
    # Tambahkan perintah lain sesuai kebutuhan
    else:
        print("Perintah tidak dikenal")

# Contoh pemanggilan
user_id = "6243471475"
command = "start"
handle_command(user_id, command)
