from src.logger import logger
from src.handlers import ExcelDownloadHandler, OneHandler
from tests.tests import dummy_1, dummy_2, dummy_3
import time
from config import run_every

def main():
    im1_handler = OneHandler("TORGI_1_INVESTMOSCOW", filename="test_output/inv_mos_dev.xlsx")
    im2_handler = OneHandler("TORGI_2_INVESTMOSCOW", filename="test_output/inv_mos_dev.xlsx")
    h = ExcelDownloadHandler("TORGI_GOV_RU", filename="test_output/inv_mos_dev.xlsx")

    while True:
        starttime = time.monotonic()
        logger.info(f"Started updating. Next start in {run_every} seconds")
        try:
            im1_handler.complete_workflow()
            im2_handler.complete_workflow()
            h.complete_workflow()
            # dummy_1()
            # dummy_2()
            # dummy_3()

        except Exception as e:
            logger.error(f"Updating failed: {e}")

        if run_every - ((time.monotonic() - starttime)) < 0:
            logger.warning(f"The update took longer than {run_every}. Must be an error!")  
        time.sleep(max(run_every - ((time.monotonic() - starttime)), 0))
    
if __name__ == "__main__":
    main()

