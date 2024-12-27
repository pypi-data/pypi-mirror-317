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
    return obj


class MyDataLoader:
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
    def _get_location(data: dict[str, Any]) -> Location:
        identifier: str = data["Location ID"]

        values: dict[str, Any] = {
            "identifier": identifier,
            "type": "",
            "name": data["Location"],
            "county": data["County"],
            "county_code": "",
            "state": data["State/Province"],
            "state_code": "",
            "country": "",
            "country_code": data["County"].split("-")[0],
            "iba_code": "",
            "bcr_code": "",
            "usfws_code": "",
            "atlas_block": "",
            "latitude": _decimal_value(data["Latitude"]),
            "longitude": _decimal_value(data["Longitude"]),
            "url": "",
        }

        if obj := Location.objects.filter(identifier=identifier).first():
            location = _update(obj, values)
        else:
            location = Location.objects.create(**values)

        return location

    @staticmethod
    def _get_observer(name: str) -> Observer:
        timestamp: dt.datetime = dt.datetime.now()
        observer: Observer

        values = {"modified": timestamp, "identifier": "", "name": name}

        if obj := Observer.objects.filter(name=name).first():
            observer = _update(obj, values)
        else:
            observer = Location.objects.create(**values)

        return observer

    @staticmethod
    def _get_species(data: dict[str, Any]) -> Species:
        order = data["Taxonomic Order"]
        species: Species

        values: dict[str, Any] = {
            "taxon_order": order,
            "order": "",
            "category": "",
            "species_code": "",
            "family_code": "",
            "common_name": data["Common Name"],
            "scientific_name": data["Scientific Name"],
            "local_name": "",
            "family_common_name": "",
            "family_scientific_name": "",
            "family_local_name": "",
            "subspecies_common_name": "",
            "subspecies_scientific_name": "",
            "subspecies_local_name": "",
            "exotic_code": "",
        }

        if obj := Species.objects.filter(order=order).first():
            species = _update(obj, values)
        else:
            species = Species.objects.create(**values)

        return species

    def _get_observation(
        self, data: dict[str, Any], checklist: Checklist
    ) -> Observation:
        count: Optional[int]

        if re.match(r"\d+", data["Count"]):
            count = _integer_value(data["Count"])
            if count == 0:
                count = None
        else:
            count = None

        values: dict[str, Any] = {
            "edited": checklist.edited,
            "identifier": "",
            "species": self._get_species(data),
            "checklist": checklist,
            "location": checklist.location,
            "observer": checklist.observer,
            "count": count,
            "breeding_code": data["Breeding Code"] or "",
            "breeding_category": "",
            "behavior_code": "",
            "age_sex": "",
            "media": len(data["ML Catalog Num`bers"] or "") > 0,
            "approved": None,
            "reviewed": None,
            "reason": "",
            "comments": data["Observation Details"] or "",
        }

        # There is no unique identifier for an observation, only the
        # count, species, date, time, checklist identifier and location
        # serve to identify it. If any of these change then the original
        # observation cannot be retrieved, so updating records is not
        # practical / possible. It only makes sense to add the record each
        # time the data is loaded. Unless the data is cleared that will
        # result in duplicate records being created.
        return Observation.objects.create(**values)

    @staticmethod
    def _get_checklist(
        data: dict[str, Any], location: Location, observer: Observer
    ) -> Checklist:
        identifier: str = data["Submission ID"]
        edited: dt.datetime = dt.datetime.fromisoformat(data["lastEditedDt"]).replace(
            tzinfo=get_default_timezone()
        )
        time: Optional[dt.time]

        if value := data["Time"]:
            time = dt.datetime.strptime(value, "%H:%M %p").time()
        else:
            time = None

        values: dict[str, Any] = {
            "edited": edited,
            "identifier": identifier,
            "location": location,
            "observer": observer,
            "observer_count": _integer_value(data["Number of Observers"]),
            "group": "",
            "species_count": None,
            "date": dt.datetime.strptime(data["Date"], "%Y-%m-%d").date(),
            "time": time,
            "protocol": data["Protocol"],
            "protocol_code": "",
            "project_code": "",
            "duration": _integer_value(data["Duration (Min)"]),
            "distance": _decimal_value(data["Distance Traveled (km)"]),
            "area": _decimal_value(data["Area Covered (ha)"]),
            "complete": data["All Obs Reported"] == "1",
            "comments": data["Checklist Comments"] or "",
            "url": "",
        }

        if obj := Checklist.objects.filter(identifier=identifier).first():
            checklist = _update(obj, values)
        else:
            checklist = Checklist.objects.create(**values)

        return checklist

    def load(self, path: Path, observer_name: str) -> None:
        if not path.exists():
            raise IOError('File "%s" does not exist' % path)

        logger.info("Loading My eBird Data: %s", path)

        with open(path) as csvfile:
            loaded: int = 0
            reader = csv.DictReader(csvfile, delimiter=",")
            observer: Observer = self._get_observer(observer_name)
            for data in reader:
                location: Location = self._get_location(data)
                checklist: Checklist = self._get_checklist(data, location, observer)
                self._get_observation(data, checklist)

                loaded += 1

                if loaded % 10 == 0:
                    sys.stderr.write("Records added: %d\r" % loaded)
                    sys.stderr.flush()

        logger.info("Records added: %d", loaded)
        logger.info("Loading completed successfully")
