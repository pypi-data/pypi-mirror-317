import logging
from urllib.error import HTTPError, URLError

from django.db import DatabaseError
from ebird.api import get_taxonomy

from ..models import Species

logger = logging.getLogger(__name__)


class SpeciesLoader:
    def __init__(self, api_key: str, locale="en"):
        self.api_key: str = api_key
        self.locale: str = locale

    def load(self):
        order: str = ""
        entries: list

        logger.info("Loading eBird taxonomy")
        logger.info("Loading locale: %s", self.locale)

        try:
            logger.info("Downloading eBird taxonomy")
            entries = get_taxonomy(self.api_key, locale=self.locale)
            logger.info("Downloaded eBird taxonomy")
        except (HTTPError, URLError):
            entries = []
            logger.exception("Taxonomy not downloaded")

        for entry in entries:
            try:
                if "order" in entry and entry["order"] != order:
                    logger.info("Loading %s " % entry["order"])
                    order = entry["order"]

                Species.objects.update_or_create(
                    species_code=entry["speciesCode"],
                    defaults={
                        "taxon_order": int(entry["taxonOrder"]),
                        "order": entry.get("order", ""),
                        "category": entry["category"],
                        "species_code": entry["speciesCode"],
                        "family_code": entry.get("familyCode", ""),
                        "common_name": entry["comName"],
                        "scientific_name": entry["sciName"],
                        "local_name": "",
                        "family_common_name": entry.get("familyComName", ""),
                        "family_scientific_name": entry.get("familySciName", ""),
                        "family_local_name": "",
                        "subspecies_common_name": "",
                        "subspecies_scientific_name": "",
                        "subspecies_local_name": "",
                        "exotic_code": "",
                    }
                )

            except DatabaseError:
                logger.exception("Could not load %s" % entry["comName"])
                break

        logger.info("Loaded eBird taxonomy")
