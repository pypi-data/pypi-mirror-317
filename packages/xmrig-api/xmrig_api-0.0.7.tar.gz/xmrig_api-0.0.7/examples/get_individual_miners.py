import logging
from xmrig import XMRigManager

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,  # Set the log level for the entire application, change to DEBUG to print all responses.
    format='[%(asctime)s - %(name)s] - %(levelname)s - %(message)s',  # Consistent format
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)
log = logging.getLogger("ExampleLog")

log.info("###############################################################################################################################")
log.info("## Please ensure you have a running XMRig instance to connect to and have updated the connection details within the example. ##")
log.info("###############################################################################################################################")

# Get individual miners
manager = XMRigManager()

log.info("Adding miners to the manager")
manager.add_miner("Miner1", "127.0.0.1", "37841", "SECRET", tls_enabled=False)
manager.add_miner("Miner2", "127.0.0.1", "37842", "SECRET", tls_enabled=False)

log.info("Retrieving individual miners")
miner_a = manager.get_miner("Miner1")
miner_b = manager.get_miner("Miner2")