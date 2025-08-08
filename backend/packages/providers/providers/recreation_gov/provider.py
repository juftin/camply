"""
Recreation.gov API client for accessing recreation data.
"""

import time
import zipfile
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import ClassVar

import platformdirs
import rich.progress
import structlog

from db.creds import DatabaseCredentials
from providers.base import BaseProvider, DatabasePopulator
from providers.recreation_gov import PROVIDER
from providers.recreation_gov.models.campgrounds import RecDotGovCampgroundData
from providers.recreation_gov.models.recreation_area import RecDotGovRecreationAreaData

logger = structlog.getLogger()


@dataclass
class ZippedDataContents:
    """
    TypedDict for Zipped Data Contents
    """

    json_file: str
    data_model: type[DatabasePopulator]


class RecreationGovProvider(BaseProvider):
    """
    Recreation.gov Provider Class
    """

    data_source: ClassVar[str] = (
        "https://ridb.recreation.gov/downloads/RIDBFullExport_V1_JSON.zip"
    )
    expiration_time: ClassVar[timedelta] = timedelta(hours=12)
    data_files: ClassVar[list[ZippedDataContents]] = [
        ZippedDataContents(
            json_file="RecAreas_API_v1.json",
            data_model=RecDotGovRecreationAreaData,
        ),
        ZippedDataContents(
            json_file="Facilities_API_v1.json",
            data_model=RecDotGovCampgroundData,
        ),
    ]

    async def download_offline_data(self) -> Path:
        """
        Download offline data for the provider.
        """
        download_dir = Path(
            platformdirs.user_data_dir(appname="camply", ensure_exists=True)
        )
        destination_file = download_dir / "RIDBFullExport_V1_JSON.zip"
        if destination_file.exists():
            age = time.time() - destination_file.stat().st_mtime
            age_delta = timedelta(seconds=age)
            if age_delta < self.expiration_time:
                logger.info(
                    "Using cached offline data",
                    provider=PROVIDER,
                )
                return destination_file
        with destination_file.open("wb") as download_file:
            logger.info(
                "Downloading offline data from %s",
                self.data_source,
                provider=PROVIDER,
            )
            async with self.async_client.stream("GET", self.data_source) as response:
                total = int(response.headers["Content-Length"])
                with rich.progress.Progress(
                    "[progress.percentage]{task.percentage:>3.0f}%",
                    rich.progress.BarColumn(bar_width=None),
                    rich.progress.DownloadColumn(),
                    rich.progress.TransferSpeedColumn(),
                ) as progress:
                    download_task = progress.add_task("Download", total=total)
                    async for chunk in response.aiter_bytes():
                        download_file.write(chunk)
                        progress.update(
                            download_task, completed=response.num_bytes_downloaded
                        )
        return destination_file

    async def populate_database(self) -> None:
        """
        Process the downloaded offline data.
        """
        creds = DatabaseCredentials()
        logger.info(
            "Populating database",
            provider=PROVIDER,
        )
        async with creds.get_session() as session:
            data_file = await self.download_offline_data()
            with zipfile.ZipFile(data_file, "r") as zipped:
                for data in self.data_files:
                    with zipped.open(data.json_file, mode="r") as json_file:
                        parsed = data.data_model.model_validate_json(json_file.read())
                        await parsed.to_database(session)
