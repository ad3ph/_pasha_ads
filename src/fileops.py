from pathlib import Path
import pandas as pd
from numpy import nan

from src.logger import logger
from config import ExcelSettings

class ExcelTableHandler:
    def __init__(self, filename: Path | str, site_id: str, cols: list | tuple=ExcelSettings.default_cols):
        self.filename = Path(filename)
        self.dir = Path.parent
        self.site_id = site_id
        self.cols = cols
        logger.info(f"ExcelTableHandler created with id {self.site_id}. File: {self.filename}")

        # Check if file exists
        self.existed_upon_creation = self.filename.exists()

        if self.existed_upon_creation and not self.filename.is_file():
            logger.error(f"Filename {self.filename} represents a directory, not a file. Assigning temporary filename '{self.site_id}_tmp.xlsx'. Please check the filename for {self.site_id} site")
            self.dir = self.filename
            self.filename = self.dir / f"{self.site_id}_tmp.xlsx"
            self.existed_upon_creation = False

        # Check again if file exists before overwriting
        self.existed_upon_creation = self.filename.exists()

        if not self.existed_upon_creation:
            # File will be created when necessary
            logger.warning(f"Working with this site for the first time, file {self.filename} doesn't exist yet.")

        self.load()
        
    def load(self):
        if not self.existed_upon_creation:
            self.table = pd.DataFrame(columns=self.cols)
            self.table.to_excel(self.filename, index=False)
        self.table = pd.read_excel(self.filename)
        logger.info(f"Loaded table for site {self.site_id}")
        
        cols_in_file = self.table.columns.tolist()
        if self.existed_upon_creation and not cols_in_file == self.cols:
            newly_asked_cols = [x for x in self.cols if not x in cols_in_file]
            logger.error(f"Table for site {self.site_id} has columns {cols_in_file}, which doesn't match necessary columns list {self.cols}. Adding new columns {newly_asked_cols}")
            self.table[newly_asked_cols] = nan
            self.cols = self.table.columns.tolist()

    def append_df(self, new_df: pd.DataFrame | dict, remove_duplicates=ExcelSettings.remove_duplicates, safety_save=ExcelSettings.safety_save):
        '''Best practice is to build new_df from self.cols'''
            
        if not isinstance(new_df, pd.DataFrame):
            if new_df == {}:
                return
            new_df = pd.DataFrame(new_df)

        result = pd.concat([self.table, new_df], ignore_index=True)
        
        if remove_duplicates:
            result.drop_duplicates(inplace=True)
        
        # assert result.shape[0] >= self.table.shape[0]

        self.table = result

        if safety_save:
            self.save()

    def check_duplicates(self, list_of_paths):
        # Initialize the 'Duplicate' column to 'No'
        self.table['Дубликат'] = ''

        for path in list_of_paths:
            try:
                db = pd.read_excel(path, sheet_name='Worksheet')[['Площадь, м2', 'Стоимость', 'Ссылка']]
            except:
                logger.warning(f"Site: {self.site_id}. Couldn't check for duplicates with file {path}: error reading file")

            for index, row in self.table.iterrows():
                is_duplicate = db[(db['Ссылка'] == row['Ссылка'])].shape[0] > 0
                ## TODO: обрабатывать еще и примерную похожесть стоимости и площади 
                if is_duplicate:
                    self.table.at[index, 'Duplicate'] = '1'
                    break

    def save(self):
        self.table.to_excel(self.filename, index=False)

def dev():
    inv_moscow = ExcelTableHandler(Path("/home/ad3ph/_pasha_ads/test_output/invmos.xlsx"), cols=["Lol", "Kek", "Cheburek", "gay"], site_id="invmos")
    print(inv_moscow.table)
    print(inv_moscow.cols)
    tb = dict(zip(inv_moscow.cols, [[5, 6], [4, 2], [3, 2], [2, 1]]))
    print(tb)
    new_df = pd.DataFrame(tb)
    print(new_df)
    inv_moscow.append_df(new_df, safety_save=True, remove_duplicates=True)
    inv_moscow.append_df(new_df, safety_save=True)
    print(inv_moscow.table)
    inv_moscow.save()

if __name__ == "__main__":
    dev()