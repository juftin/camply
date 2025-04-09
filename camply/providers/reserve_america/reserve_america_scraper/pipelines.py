from datetime import datetime

import pandas as pd


class DataFramePipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        # Create a DataFrame
        df = pd.DataFrame(self.items)

        # Ensure there is only one unique parkId
        if "parkId" in df.columns:
            unique_park_ids = df["parkId"].unique()
            if len(unique_park_ids) != 1:
                spider.logger.error("Multiple or no unique parkId values found.")
                return
            park_id = unique_park_ids[0]
        else:
            spider.logger.error("parkId column not found in data.")
            return

        # Export to Parquet with parkId in filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fpath = f"../data/availability_{park_id}_{timestamp}.parquet"
        df.to_parquet(fpath, index=False)
        spider.logger.info(f"Saved dataframe to {fpath}")
