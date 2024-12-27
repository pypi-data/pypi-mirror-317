import csv
import datetime as dt
import decimal
import logging
import re
import sys
from pathlib import Path
from typing import Any, Optional, TypeVar

from django.db.models import Model
from django.utils.timezone import get_default_timezone

from ..models import Checklist, Location, Observation, Observer, Species

logger = logging.getLogger(__name__)


def _boolean_value(value: Optional[str]) -> Optional[bool]:
    return bool(value) if value else None


def _integer_value(value: Optional[str]) -> Optional[int]:
    return int(value) if value else None


def _decimal_value(value: Optional[str]) -> Optional[decimal.Decimal]:
    return decimal.Decimal(value) if value else None


def _update(obj: Model, values: dict[str, Any]) -> Model:
    for key, value in values.items():
        setattr(obj, key, value)
    obj.save()
    return obj


class BasicDatasetLoader:
    @staticmethod
    def _get_checklist_status(identifier: str, last_edited: str) -> tuple[bool, bool]:
        last_edited_date: dt.datetime = dt.datetime.fromisoformat(last_edited).replace(
            tzinfo=get_default_timezone()
        )
        new: bool
        modified: bool

        if obj := Checklist.objects.filter(identifier=identifier).first():
            if obj.edited < last_edited_date:
                new = False
                modified = True
            else:
                new = False
                modified = False
        else:
            new = True
            modified = False
        return new, modified

    @staticmethod
    def _get_location(data: dict[str, str]) -> Location:
        identifier: str = data["LOCALITY ID"]

        values: dict[str, Any] = {
            "identifier": identifier,
            "type": data["LOCALITY TYPE"],
            "name": data["LOCALITY"],
            "county": data["COUNTY"],
            "county_code": data["COUNTY CODE"],
            "state": data["STATE"],
            "state_code": data["STATE CODE"],
            "country": data["COUNTRY"],
            "country_code": data["COUNTRY CODE"],
            "latitude": _decimal_value(data["LATITUDE"]),
            "longitude": _decimal_value(data["LONGITUDE"]),
            "iba_code": data["IBA CODE"],
            "bcr_code": data["BCR CODE"],
            "usfws_code": data["USFWS CODE"],
            "atlas_block": data["ATLAS BLOCK"],
            "url": "",
        }

        if obj := Location.objects.filter(identifier=identifier).first():
            location = _update(obj, values)
        else:
            location = Location.objects.create(**values)
        return location

    @staticmethod
    def _get_observer(data: dict[str, str]) -> Observer:
        identifier: str = data["OBSERVER ID"]

        values: dict[str, Any] = {
            "identifier": identifier,
            "name": "",
        }

        if obj := Observer.objects.filter(identifier=identifier).first():
            observer = _update(obj, values)
        else:
            observer = Observer.objects.create(**values)
        return observer

    @staticmethod
    def _get_species(data: dict[str, str]) -> Species:
        taxon_order = data["TAXONOMIC ORDER"]
        species: Species

        values: dict[str, Any] = {
            "taxon_order": taxon_order,
            "order": "",
            "category": data["CATEGORY"],
            "species_code": "",
            "family_code": "",
            "common_name": data["COMMON NAME"],
            "scientific_name": data["SCIENTIFIC NAME"],
            "local_name": "",
            "family_common_name": "",
            "family_scientific_name": "",
            "family_local_name": "",
            "subspecies_common_name": data["SUBSPECIES COMMON NAME"],
            "subspecies_scientific_name": data["SUBSPECIES SCIENTIFIC NAME"],
            "subspecies_local_name": "",
            "exotic_code": data["EXOTIC CODE"],
        }

        if obj := Species.objects.filter(taxon_order=taxon_order).first():
            species = _update(obj, values)
        else:
            species = Species.objects.create(**values)
        return species

    def _get_observation(
        self, data: dict[str, str], checklist: Checklist, species: Species
    ) -> Observation:
        identifier = data["GLOBAL UNIQUE IDENTIFIER"]
        count: Optional[int]
        observation: Observation

        if re.match(r"\d+", data["OBSERVATION COUNT"]):
            count = _integer_value(data["OBSERVATION COUNT"])
            if count == 0:
                count = None
        else:
            count = None

        values: dict[str, Any] = {
            "edited": checklist.edited,
            "identifier": identifier,
            "checklist": checklist,
            "location": checklist.location,
            "observer": checklist.observer,
            "species": species,
            "count": count,
            "breeding_code": data["BREEDING CODE"],
            "breeding_category": data["BREEDING CATEGORY"],
            "behavior_code": data["BEHAVIOR CODE"],
            "age_sex": data["AGE/SEX"],
            "media": _boolean_value(data["HAS MEDIA"]),
            "approved": _boolean_value(data["APPROVED"]),
            "reviewed": _boolean_value(data["REVIEWED"]),
            "reason": data["REASON"] or "",
            "comments": data["SPECIES COMMENTS"] or "",
        }

        if obj := Observation.objects.filter(identifier=identifier).first():
            observation = _update(obj, values)
        else:
            observation = Observation.objects.create(**values)

        return observation

    def _get_checklist(
        self,
        row: dict[str, str],
        location: Location,
        observer: Observer,
    ) -> Checklist:
        identifier: str = row["SAMPLING EVENT IDENTIFIER"]
        edited: dt.datetime = dt.datetime.fromisoformat(
            row["LAST EDITED DATE"]
        ).replace(tzinfo=get_default_timezone())
        time: Optional[dt.time]

        if value := row["TIME OBSERVATIONS STARTED"]:
            time = dt.datetime.strptime(value, "%H:%M:%S").time()
        else:
            time = None

        values: dict[str, Any] = {
            "identifier": identifier,
            "edited": edited,
            "location": location,
            "observer": observer,
            "group": row["GROUP IDENTIFIER"],
            "observer_count": row["NUMBER OBSERVERS"],
            "date": dt.datetime.strptime(row["OBSERVATION DATE"], "%Y-%m-%d").date(),
            "time": time,
            "protocol": row["PROTOCOL TYPE"],
            "protocol_code": row["PROTOCOL CODE"],
            "project_code": row["PROJECT CODE"],
            "duration": _integer_value(row["DURATION MINUTES"]),
            "distance": _decimal_value(row["EFFORT DISTANCE KM"]),
            "area": _decimal_value(row["EFFORT AREA HA"]),
            "complete": _boolean_value(row["ALL SPECIES REPORTED"]),
            "comments": row["TRIP COMMENTS"] or "",
            "url": "",
        }

        if obj := Checklist.objects.filter(identifier=identifier).first():
            checklist = _update(obj, values)
        else:
            checklist = Checklist.objects.create(**values)

        return checklist

    def load(self, path: Path) -> None:
        if not path.exists():
            raise IOError('File "%s" does not exist' % path)

        logger.info("Loading eBird Basic Dataset: %s", path)

        with open(path) as csvfile:
            added: int = 0
            updated: int = 0
            unchanged: int = 0
            loaded: int = 0
            new: bool
            modified: bool

            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                identifier: str = row["GLOBAL UNIQUE IDENTIFIER"]
                last_edited: str = row["LAST EDITED DATE"]

                new, modified = self._get_checklist_status(identifier, last_edited)

                if new or modified:
                    location: Location = self._get_location(row)
                    observer: Observer = self._get_observer(row)
                    checklist: Checklist = self._get_checklist(row, location, observer)
                    species: Species = self._get_species(row)
                    self._get_observation(row, checklist, species)

                if new:
                    added += 1
                elif modified:
                    updated += 1
                else:
                    unchanged += 1

                loaded += 1

                if loaded % 10 == 0:
                    # Write the running total to stderr so it does not
                    # get into the logs
                    sys.stderr.write("Records loaded: %d\r" % loaded)
                    sys.stderr.flush()

        logger.info("Records loaded: %d", loaded)
        logger.info("Records added: %d", added)
        logger.info("Records updated: %d", updated)
        logger.info("Records unchanged: %d", unchanged)
        logger.info("Loading completed successfully")
