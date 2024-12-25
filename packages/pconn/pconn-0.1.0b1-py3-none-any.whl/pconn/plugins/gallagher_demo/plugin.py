"""Demo plugin."""

import logging
from typing import Any

from gallagher_restapi import Client, FTCardholder, GllApiError
from gallagher_restapi.models import (
    FTItemReference,
    FTNewCardholder,
    FTPersonalDataFieldDefinition,
    SortMethod,
)

from pconn.const import CONF_ID, CONF_NAME
from pconn.core import PConn
from pconn.exceptions import PluginActionError
from pconn.plugin_entries import PluginEntry, view
from pconn.plugins import Plugin
from pconn.plugins.gallagher_rest.const import CONF_DIVISION

from .const import CONF_READ_ONLY, CONF_VALUE, DOMAIN, FIRST_NAME, LAST_NAME, PHOTO_PDF

_LOGGER = logging.getLogger(__name__)


class Demo(Plugin):
    """Demo plugin class."""

    def __init__(self, pconn: PConn, entry: PluginEntry, gll_client: Client) -> None:
        """Initialize plugin."""
        super().__init__(pconn, entry, _LOGGER, name=DOMAIN)
        self.gll_client = gll_client
        self.cardholders: dict[str, FTCardholder] = {}
        self.cardholder_pdfs: dict[str, Any] = {}
        self.pdfs: dict[str, FTPersonalDataFieldDefinition] = {}
        self.stopped = False

    @property
    def photo_pdf_id(self) -> str | None:
        """Return photo field id."""
        return self.plugin_entry.options.get(PHOTO_PDF)

    @view
    async def get_cardholders(self, name: str | None = None) -> list[dict[str, Any]]:
        """Return list of cardholders."""
        try:
            cardholders = await self.gll_client.get_cardholder(
                name=name,
                top=10,
                sort=SortMethod.NAME_ASC,
                extra_fields=[CONF_DIVISION, "personalDataFields"],
            )
        except GllApiError as err:
            _LOGGER.error(err)
            raise PluginActionError(err) from err
        self.cardholders.update(
            {cardholder.id: cardholder for cardholder in cardholders}
        )
        cardholders_list: list[dict[str, Any]] = []
        pdfs = {pdf.name: pdf.id for pdf in self.pdfs.values()}
        for cardholder in self.cardholders.values():
            cardholder_info: dict[str, Any] = {
                CONF_ID: cardholder.id,
                FIRST_NAME: cardholder.firstName,
                LAST_NAME: cardholder.lastName,
            }
            for pdf, value in cardholder.pdfs.items():
                if not (pdf_id := pdfs.get(pdf)):
                    continue
                if isinstance(value, FTItemReference) and (
                    b64_image := await self.gll_client.get_image_from_pdf(value)
                ):
                    value = b64_image
                    if self.photo_pdf_id == pdf_id:
                        cardholder_info["photo"] = value
                        continue
                cardholder_info.setdefault("pdfs", []).append(
                    {
                        CONF_ID: pdf_id,
                        CONF_NAME: pdf,
                        CONF_VALUE: value,
                        CONF_READ_ONLY: self.pdfs[pdf_id].operatorAccess
                        != "fullAccess",
                    }
                )
            cardholders_list.append(cardholder_info)
        return cardholders_list

    async def async_get_image_pdfs(
        self, pdfs: dict[str, str | FTItemReference]
    ) -> dict[str, Any]:
        """Return pdf fields with photo if available."""
        if self.photo_pdf_id:
            for pdf, value in pdfs.items():
                if isinstance(value, FTItemReference) and (
                    photo_b64_string := await self.gll_client.get_image_from_pdf(value)
                ):
                    pdfs[pdf] = photo_b64_string
                break
        return pdfs

    def get_photo_pdfs(self) -> list[FTPersonalDataFieldDefinition]:
        """Return list of unique personal fields."""
        return [pdf for pdf in self.pdfs.values() if pdf.type == "image"]

    @view
    async def update_cardholder(self, id: str, **kwargs: Any) -> bool:
        """Update cardholder personal fields."""
        if not (cardholder := self.cardholders.get(id)):
            raise PluginActionError(f"Cardholder with id {id} not found.")
        assert cardholder.division
        updated_cardholder = FTNewCardholder()
        updated_cardholder.patch(**kwargs)
        _LOGGER.debug(
            "Updating cardholder personal fields. %s", updated_cardholder.pdfs
        )
        try:
            await self.gll_client.update_cardholder(cardholder.href, updated_cardholder)
        except GllApiError as err:
            _LOGGER.error(err)
            raise PluginActionError(err) from err
        return True

    async def async_initialize(self) -> None:
        """Initialize demo plugin."""
        if pdfs := await self.gll_client.get_personal_data_field(
            extra_fields=["type", "operatorAccess"]
        ):
            self.pdfs = {pdf.id: pdf for pdf in pdfs}
