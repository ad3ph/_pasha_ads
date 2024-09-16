from src.logger import logger
from src.handlers import ExcelDownloadHandler, OneHandler, ThreeHandler, FourHandler, AvitoHandler
from tests.tests import dummy_1, dummy_2, dummy_3
import time
from config import run_every, excel_paths
import os

def main():
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    
    im1_handler = OneHandler(site_id:="TORGI_1_INVESTMOSCOW", filename=excel_paths[site_id])
    im2_handler = OneHandler(site_id:="TORGI_2_INVESTMOSCOW", filename=excel_paths[site_id])
    t_gov = ExcelDownloadHandler(site_id:="TORGI_GOV_RU", filename=excel_paths[site_id])
    tr = ThreeHandler(site_id:="TORGI_ROSSII", filename=excel_paths[site_id])
    tb = FourHandler(site_id:="TBANKROT", filename=excel_paths[site_id])
    ah = AvitoHandler(site_id:="AVITO", filename=excel_paths[site_id])

    handlers = (im1_handler, im2_handler, t_gov, tr, tb, ah)
    # handlers = [t_gov]

    while True:
        starttime = time.monotonic()
        logger.info(f"Started updating. Next start in {run_every} seconds")
        for handler in handlers:
            try:
                handler.excel_handler.load()
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
