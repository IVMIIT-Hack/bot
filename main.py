import src.core
from src.tg_main import TelegramInterface
from src.database import DataBaseAbiturents, DataBaseAbiturentsExport

if __name__ == "__main__":
    dba = DataBaseAbiturents();
    dba.importfulldata();