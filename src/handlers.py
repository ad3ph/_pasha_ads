# basehandler will see each site as:
# url и способ достать хтмл (для большинства одинаково, но авито например по другому, еще сайт5 тоже другой)  
# правила парсинга и столбцы (площадь, стоимость, адрес, назначение, ссылка)
# имя файла

# Методы:
# воркфлоу, включает:
# - получить хтмл не падая, , если не получилось, то залогировать и завершить
# - пропарсить хтмл
# - сохранить

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import unicodedata
import time
import pandas as pd
import re

from src.logger import logger
from src.timer import timered, Timeout
from src.fileops import ExcelTableHandler
from config import urls, WebSettings
from src.utils import first, get_tmp_name, random_wait, remove_spaces, get_dates_span


class BaseSiteHandler:
    def __init__(self, site_id, filename=None):
        self.filename = filename or f'{site_id}.xlsx'
        self.site_id = site_id
        self.excel_handler = ExcelTableHandler(filename, site_id=site_id)
        self.is_paginated = False
        self.is_date_parametrized = False
        self.url, self.max_pages = self.get_url()
        self.source = ""

        self.launchable = self.url != "Failed"

    def get_url(self, param=urls):
        if isinstance(param, str):
            # TODO: validate url
            return param

        ret = urls.get(self.site_id)
        if not ret:
            logger.error(f'No url found for {self.site_id} using following parameter: {param}. Parser will not work')
            return "Failed", None

        if isinstance(ret, str):
            return ret, None

        if ret.get("paginator") != None:
            self.is_paginated = True
            max_pages = ret.get("max_pages")
            return ret.get("paginator"), max_pages

        if ret.get("date_parametrized") != None:
            date_offset = ret.get("date_offset")
            start_date, end_date = get_dates_span(date_offset)
            self.start_date, self.end_date = start_date, end_date
            return ret.get("date_parametrized").format(start_date, end_date), None    

        return ret.get("url"), None

    def get_source(self, page_num=1, wait=False) -> str:
        logger.trace(f"Launching Selenium")

        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        try:
            self.driver = webdriver.Chrome(options=options)
        except Exception as e:
            logger.error(f"Failed to start Selenium Chrome (web browser) for site {self.site_id}. Exception: {e}")
            return "Failed"
        
        if wait:
            random_wait()

        url_to_get = self.url
        if self.is_paginated:
            url_to_get = self.url.format(page_num)
        
        logger.debug(f"Getting URL request {url_to_get}")
        self.driver.get(url_to_get)
        
        WebDriverWait(self.driver, WebSettings.timeout).until(lambda x: self.driver.execute_script("return document.readyState;") == "complete")

        time.sleep(WebSettings.additional_wait)        

        source = self.driver.page_source
        self.driver.quit()
        self.source = source
        return source

    def parse(self) -> dict:
        return {}, 0

    def complete_workflow(self):
        if not self.launchable:
            logger.warning(f"Tried to run workflow for site {self.site_id}, but it's not launchable. Check earlier logs for errors")
            return

        logger.info(f"Started updating from site {self.site_id}")
        obtained_count = 1
        page_num = 1
        while obtained_count:
            try:
                #source = timered(self.get_source, WebSettings.timeout)
                self.get_source(page_num)
                ret, obtained_count = self.parse()
                logger.info(f"Obtained {obtained_count} elements from page {page_num} / {('...', self.max_pages)[bool(self.max_pages)]}")

                self.excel_handler.append_df(ret)
                self.save()
            except Timeout:
                logger.error(f"Could not get source code from {self.site_id}: site takes to long to connect. Please check access")
            finally:
                self.driver.quit()
            
            if not self.is_paginated:
                obtained_count = 0

            page_num += 1
            if self.max_pages and page_num > self.max_pages:
                break

    def save(self):
        self.excel_handler.table.to_excel(self.filename, index=False)


class AvitoHandler(BaseSiteHandler):
    def complete_workflow(self):
        if not self.launchable:
            logger.warning(f"Tried to run workflow for site {self.site_id}, but it's not launchable. Check earlier logs for errors")
            return

        random_wait()

        obtained_count = 1
        page_num = 1
        while obtained_count:
            try:
                #source = timered(self.get_source, WebSettings.timeout)
                self.get_source(page_num, wait=True)
                ret, obtained_count = self.parse()
                logger.info(f"Obtained {obtained_count} elements from page {page_num} / {('...', self.max_pages)[bool(self.max_pages)]}")

                self.excel_handler.append_df(ret)
                self.save()
            except Timeout:
                logger.error(f"Could not get source code from {self.site_id}: site takes to long to connect. Please check access")
            finally:
                self.driver.quit()
            
            if not self.is_paginated:
                obtained_count = 0

            page_num += 1
            random_wait()

            if self.max_pages and page_num > self.max_pages:
                break

    def parse(self, cols=['Площадь', 'Стоимость', 'Адрес', 'Назначение', 'Ссылка', 'Дата окончания торгов', 'Цена за м2']):
        def parse_item(item):
            outp = []
            # Ссылка
            link = f'{self.url.split("/")[0]}//{self.url.split("/")[2]}{item.findAll("a", {"itemprop": "url"})[0].attrs["href"]}'
            
            # Площадь  и цена
            price_root = item.findAll("span", class_="price-root-RA1pj")[0]
            cost = price_root.findAll("meta", {"itemprop": "price"})[0].attrs["content"]
            cost_per_sqm = price_root.findAll("p", class_="styles-module-root-YczkZ styles-module-size_s-xb_uK styles-module-size_s-_z7mI stylesMarningNormal-module-root-S7NIr stylesMarningNormal-module-paragraph-s-Yhr2e styles-module-noAccent-LowZ8")[0].get_text(strip=True)
            cost_per_sqm = float("".join(unicodedata.normalize("NFKD", str(cost_per_sqm)).split(" ₽")[0].split(" ")))
            area = float(cost) / cost_per_sqm
            area = f"{area:.2f} м²"

            # Адрес
            addr = item.findAll("div", {"data-marker": "item-address"})[0].findAll("span")[0].get_text(strip=True)

            # Назначение
            name_text = item.findAll("h3", {"itemprop": "name"})[0].get_text(strip=True).lower()
            purp = understand_purpose(name_text)

            endt = ""

            return [unicodedata.normalize("NFKD", x) for x in [area, cost, addr, purp, link, endt, str(cost_per_sqm)]]

        self.soup = BeautifulSoup(self.source)
        items = self.soup.findAll('div', {"data-marker": "item"})
        results = []
        for item in items:
            try:
                results.append(parse_item(item))
                # print("__________--\nitem|||||||||||||||||\n", item)
            except:
                logger.error(f"Problem parsing item from site {self.site_id}. Skipping item...")
        results_dict = dict(zip(cols, [list(x) for x in zip(*results)]))
        
        return results_dict, len(results)

class OneHandler(BaseSiteHandler):
    def parse(self, cols=['Площадь', 'Стоимость', 'Адрес', 'Назначение', 'Ссылка', 'Дата окончания торгов', 'Цена за м2']):
        logger.trace(f"Parsing source code")
        def parse_item(item):
            outp = []
            # Ссылка
            link = f'{self.url.split("/")[0]}//{self.url.split("/")[2]}{item.attrs["href"]}'
            
            # Площадь
            name_area = item.findAll("div", class_="uid-title-3 uid-tenders-card__main-title uid-mt-0")[0]
            name_area_splitted = name_area.get_text(strip=True).split(", ")
            area = ""
            for x in name_area_splitted:
                if "м²" in x:
                    area = x
                    break
            
            # Стоимость
            cost = item.findAll("div", class_="uid-title-3 uid-mt-0 uid-mt-tab-20")[0].get_text(strip=True)

            # Адрес
            addr = item.findAll("div", class_="uid-mb-12")[0].get_text(strip=True)
            # Назначение
            purp = item.findAll("div", class_="uid-text-light uid-tenders-card__purpose")[0].get_text(strip=True).split(": ")[-1]

            endt = item.findAll("div", class_="uid-text-small uid-text-gray")[0]
            if not endt.get_text(strip=True).split(": ")[-1] == "Торги завершены":
                endt = endt.findAll("span")[0].get_text(strip=True).split(": ")[-1]
            else:
                endt = endt.get_text(strip=True).split(": ")[-1]

            if area and cost:
                try:
                    cost_per_sqm = int(remove_spaces(unicodedata.normalize("NFKD", cost)).split("руб.")[0].split(",")[0]) / float(remove_spaces(area.split(" м²")[0].replace(",", ".")))
                    cost_per_sqm = f"{cost_per_sqm:.1f} руб за м2"
                except ValueError:
                    logger.warning(f"Couldn't calculate cost per square meter for an item")
                    cost_per_sqm = ""
                    
            return [unicodedata.normalize("NFKD", x) for x in [area, cost, addr, purp, link, endt, cost_per_sqm]]

        self.soup = BeautifulSoup(self.source)
        items = self.soup.findAll('a', class_='uid-tenders-card uid-tenders-card_with-image') # May be moved to a text config file: {"site_id": {"item_tag": "a", "item_class": "...", ...}}
        results = []
        for item in items:
            try:
                results.append(parse_item(item))
            except:
                logger.error(f"Problem parsing item from site {self.site_id}. Skipping item...")
        results_dict = dict(zip(cols, [list(x) for x in zip(*results)]))
        return results_dict, len(results)

class ExcelDownloadHandler:
    def __init__(self, site_id, filename=None):
        self.filename = filename or f'{site_id}.xlsx'
        self.site_id = site_id
        self.url = urls[site_id]

        self.downloaded_file_name = f"tmp/{get_tmp_name()}.xlsx"
        self.downloaded_table = None
        self.output_excel_handler = ExcelTableHandler(filename, site_id=site_id)

    def complete_workflow(self):
        self.download()
        self.process()
        self.save()

    def download(self):
        req = requests.get(self.url, allow_redirects=True)
        if not req.ok:
            logger.error(f"Couldn't get XLSX from site {site_id}. Request status: {req.status_code}")

        self.downloaded_file_name = f"tmp/{get_tmp_name()}.xlsx"
        with open(self.downloaded_file_name, "wb") as f:
            f.write(req.content)

        self.downloaded_table = pd.read_excel(self.downloaded_file_name, index_col=False, header=1)
    
    def extract_area(self, description):
        start_index = description.find('площадью')
        if start_index == -1:
            start_index = description.find('площадь')
            if start_index == -1:
                return None
        start_index += len('площадь') + 1  # +1 чтобы пропустить пробел после слова
        end_index = description.find('кв.', start_index)
        if end_index == -1:
            return None
        return description[start_index:end_index].strip()

    def process(self):
        # Выбор нужных столбцов
        self.downloaded_table = self.downloaded_table[['Дата и время окончания подачи заявок', 'Ссылка на лот в ОЧ Реестра лотов', 
                'Субъект РФ', 'Местонахождение имущества', 'Начальная цена', 
                'Итоговая цена', 'Описание лота']]

        # Преобразование значений в числовой формат
        self.downloaded_table['Начальная цена'] = pd.to_numeric(self.downloaded_table['Начальная цена'], errors='coerce')
        self.downloaded_table['Итоговая цена'] = pd.to_numeric(self.downloaded_table['Итоговая цена'], errors='coerce')

        # Оставляем только строки, где Начальная цена >= 35000000 и Итоговая цена либо не указана, либо >= 45000000
        self.downloaded_table = self.downloaded_table[(self.downloaded_table['Начальная цена'] >= 35000000) & ((self.downloaded_table['Итоговая цена'].isnull()) | (self.downloaded_table['Итоговая цена'] >= 45000000))]

        # Применяем функцию к столбцу 'Описание' и создаем новый столбец 'Площадь'
        self.downloaded_table['Площадь'] = self.downloaded_table['Описание лота'].apply(self.extract_area)
        self.downloaded_table['Площадь'] = self.downloaded_table['Площадь'].str.replace(' ', '')
        self.downloaded_table['Площадь'] = self.downloaded_table['Площадь'].str.replace('-', '')
        self.downloaded_table['Площадь'] = self.downloaded_table['Площадь'].str.replace(',', '.').astype(float)


        # Убираем всё что идет до слов "по адресу"
        self.downloaded_table['Описание лота'] = self.downloaded_table['Описание лота'].str.split('по адресу').str[-1].str.strip()
        self.downloaded_table['Описание лота'] = self.downloaded_table['Описание лота'].str.lstrip(':')
        self.downloaded_table['Описание лота'] = self.downloaded_table['Описание лота'].str.lstrip(' ')

        # Переименовываем столбцы
        self.downloaded_table = self.downloaded_table.rename(columns={'Дата и время окончания подачи заявок': 'Дата окончания торгов',
                                'Ссылка на лот в ОЧ Реестра лотов': 'Ссылка',
                                'Субъект РФ': 'Субъект РФ',
                                'Местонахождение имущества': 'Адрес',
                                'Начальная цена': 'Стоимость',
                                'Итоговая цена': 'Итоговая цена',
                                'Описание лота': 'Описание',
                                'Площадь': 'Площадь'})

        self.downloaded_table['Адрес'] = self.downloaded_table['Субъект РФ'] + ", " + self.downloaded_table['Адрес']
        # self.downloaded_table['Дата окончания торгов'] = self.downloaded_table['Дата окончания торгов'].str.split(" ")[0]

        self.downloaded_table = self.downloaded_table[['Ссылка', 'Адрес',
                'Стоимость', 'Площадь', 'Описание', 'Дата окончания торгов']]

    def save(self):
        self.output_excel_handler.append_df(self.downloaded_table)
        self.output_excel_handler.save()



class ThreeHandler(BaseSiteHandler):
    def parse(self, cols=['Площадь', 'Стоимость', 'Адрес', 'Назначение', 'Ссылка', 'Дата окончания торгов', 'Цена за м2']):
        logger.trace(f"Parsing source code")
        def parse_item(item):
            outp = []
            desc = item.findAll("p", class_="card__excerpt")[0].findAll("a")[0]
            # Ссылка
            link = desc.attrs["href"]
            desc_text = desc.get_text()
            
            try:
                area = desc_text.split("Общая площадь: ")[1].split(" общ. пл")[0]
            except IndexError:
                try:
                    area = desc_text.lower().split("площадью ")[1].split(" м")[0]
                except IndexError:
                    try:
                        area = desc_text.lower().split("пл. ")[1].split(" м")[0]
                    except:
                        logger.warning(f"Failed to extract area for item {link}")
                        area = '-'                        

            area_num = area.split(" м²")[0]
            try:
                area_num = float(area_num)
            except ValueError:
                area_num = 1.

            # Стоимость
            cost = item.findAll("p", class_="bid__value")[0].get_text(strip=True)
            cost_num = remove_spaces(cost.split(" ₽")[0].replace(",", "."))
            try:
                cost_num = float(cost_num)
            except ValueError:
                cost_num = 1.            

            cost_per_sqm = f"{(cost_num / area_num):.2f}"

            # Адрес
            header3 = item.findAll("h3", class_="card__title")[0].get_text()

            try:
                part_with_addr = re.split('адрес[\у\ \-\:]?([- ])', header3)[1]
                addr = re.split("\n | ; | к.н. | кадастровый | цена | : | ", part_with_addr, re.IGNORECASE)
            except:
                logger.warning(f"Failed to extract address for item {link} from following text: {header3}")

            # Назначение
            purp = understand_purpose(desc_text)

            try:
                endt = f"между {self.start_date} и {self.end_date}"
            except AttributeError:
                endt = ""

            return [unicodedata.normalize("NFKD", x) for x in [area, cost, addr, purp, link, endt, cost_per_sqm]]

        self.soup = BeautifulSoup(self.source)
        items = self.soup.findAll('div', class_='card__wrapper')
        results = []
        for item in items:
            try:
                results.append(parse_item(item))
            except:
                logger.error(f"Problem parsing item from site {self.site_id}. Skipping item...")
        results_dict = dict(zip(cols, [list(x) for x in zip(*results)]))
        return results_dict, len(results)


# def dev_manual():
#     dev_handler = OneHandler("TORGI_1_INVESTMOSCOW", filename="test_output/inv_mos_dev.xlsx")
#     # DEBUG
#     with open("sample.htm", "r") as f:
#         dev_handler.source = f.read()
#     res, cnt = dev_handler.parse()
#     dev_handler.excel_handler.append_df(res)
#     print(dev_handler.excel_handler.table)

    
if __name__ == "__main__":
    # dev_manual()
    pass