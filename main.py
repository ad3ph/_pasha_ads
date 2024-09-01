from src.logger import logger
from src.handlers import ExcelDownloadHandler, OneHandler, ThreeHandler, FourHandler, AvitoHandler
from tests.tests import dummy_1, dummy_2, dummy_3
import time
from config import run_every
import os

def main():
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    
    im1_handler = OneHandler("TORGI_1_INVESTMOSCOW", filename="test_output/inv_mos_dev.xlsx")
    im2_handler = OneHandler("TORGI_2_INVESTMOSCOW", filename="test_output/inv_mos_dev.xlsx")
    t_gov = ExcelDownloadHandler("TORGI_GOV_RU", filename="test_output/inv_mos_dev.xlsx")
    tr = ThreeHandler("TORGI_ROSSII", filename="test_output/inv_mos_dev.xlsx")
    tb = FourHandler("TBANKROT", filename="test_output/inv_mos_dev.xlsx")
    ah = AvitoHandler("AVITO", filename="test_output/avito.xlsx")

    handlers = (im1_handler, im2_handler, t_gov, tr, tb, ah)
    # handlers = [t_gov]

    while True:
        starttime = time.monotonic()
        logger.info(f"Started updating. Next start in {run_every} seconds")
        for handler in handlers:
            try:
                handler.complete_workflow()
                # dummy_1()
                # dummy_2()
                # dummy_3()

            except Exception as e:
                logger.error(f"Updating {handler.site_id} failed: {e}")

        if run_every == -1:
            # Killing
            logger.success(f"Exiting after single update because run_every parameter (see config) is set to {run_every}")
            return

        if run_every - ((time.monotonic() - starttime)) < 0:
            logger.warning(f"The update took longer than {run_every}. Must be an error!")  
        time.sleep(max(run_every - ((time.monotonic() - starttime)), 0))

def dev_tr():
    h = FourHandler("TBANKROT", filename="test_output/tb.xlsx")
    h.complete_workflow()

def dev():
    ah = AvitoHandler("AVITO", filename="test_output/avito.xlsx")
    # ah.complete_workflow()
    with open("avito_outp.html", "r") as f:
        ah.source = f.read()
    res, cnt = ah.parse()
    ah.excel_handler.append_df(res)
    ah.excel_handler.save()

if __name__ == "__main__":
    main()
    # dev()
    # dev_tr()
