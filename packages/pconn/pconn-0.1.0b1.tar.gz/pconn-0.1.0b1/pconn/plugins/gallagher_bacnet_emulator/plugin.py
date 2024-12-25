"""BACnet Emulator plugin."""

import logging
from typing import Any

import BAC0
from gallagher_restapi import Client
from gallagher_restapi.models import (
    FTInput,
    FTItem,
    FTItemReference,
    FTItemStatus,
    FTOutput,
)

from pconn.const import SIGNAL_DATA_UPDATED
from pconn.core import PConn
from pconn.plugin_entries import PluginEntry
from pconn.plugins import Plugin
from pconn.plugins.bacnet_emulator.plugin import BACnetEmulator
from pconn.plugins.gallagher_rest import GallagherREST
from pconn.plugins.gallagher_rest.const import CONTROLLER_TYPES

from .bacnet_objects import (
    GallagherControllerObject,
    GallagherInputObject,
    GallagherObject,
    GallagherOutputObject,
)
from .const import CONTROLLERS, DOMAIN, INPUTS, OUTPUTS

_LOGGER = logging.getLogger(__name__)


class GallagherBACnetEmulator(
    Plugin[list[dict[str, Any]]], GallagherREST, BACnetEmulator
):
    """BACnet emulator for Gallagher items."""

    items: dict[str, GallagherObject]

    def __init__(
        self,
        pconn: PConn,
        entry: PluginEntry,
        gll_client: Client,
        device: BAC0.lite,
    ) -> None:
        """Initialize the emulator."""
        Plugin.__init__(self, pconn, entry, _LOGGER, name=DOMAIN, stream_data=True)
        GallagherREST.__init__(self, pconn, entry, gll_client)
        BACnetEmulator.__init__(self, pconn, entry, device)
        self.update_link: FTItemReference | None = None

    @property
    def monitor_controllers(self) -> bool:
        """Return True if controllers should be monitored."""
        return self.plugin_entry.options.get(CONTROLLERS, False)

    @property
    def monitor_inputs(self) -> bool:
        """Return True if inputs should be monitored."""
        return self.plugin_entry.options.get(INPUTS, False)

    @property
    def monitor_outputs(self) -> bool:
        """Return True if outputs should be monitored."""
        return self.plugin_entry.options.get(OUTPUTS, False)

    # @property
    # def monitor_door(self) -> bool:
    #     """Return True if doors should be monitored."""
    #     return self.plugin_entry.options.get(DOORS, False)

    async def initialize_items(self) -> None:
        """Initialize the items."""
        if self.monitor_controllers and (
            controllers := await self.gll_client.get_item(
                item_types=CONTROLLER_TYPES,
                extra_fields=["status", "statusFlags"],
            )
        ):
            await self.pconn.async_add_executor_job(
                self._initialize_controllers, controllers
            )
        if self.monitor_inputs and (
            inputs := await self.gll_client.get_input(extra_fields=["statusFlags"])
        ):
            await self.pconn.async_add_executor_job(self._initialize_inputs, inputs)
        if self.monitor_outputs and (
            outputs := await self.gll_client.get_output(
                extra_fields=["statusFlags", "commands"]
            )
        ):
            await self.pconn.async_add_executor_job(self._initialize_outputs, outputs)
        await self.pconn.async_add_executor_job(self._save_to_file)
        _LOGGER.debug("Starting BACnet emulator in a separate thread")
        await self.pconn.async_add_executor_job(self.device.start)

        if self.registered_items_ids:
            self.plugin_entry.async_on_unload(
                self.listen_for_updates(
                    self.registered_items_ids, self.async_update_objects
                )
            )

    async def async_update_objects(self, items_status: list[FTItemStatus]) -> None:
        """Update objects."""
        previous_data = self._get_objects()
        for item_status in items_status:
            if bacnet_object := self.items.get(item_status.id):
                if not item_status.statusFlags and "tamper" in item_status.status:
                    item_status.statusFlags.append("tamper")
                bacnet_object.update_object_value(item_status.statusFlags)
        if (new_data := self._get_objects()) != previous_data:
            await self.event_queue.put((SIGNAL_DATA_UPDATED, new_data))

    def _initialize_controllers(self, controllers: list[FTItem]) -> None:
        """Create bacnet objects for detected controllers."""
        _registered_controller_ids = self._registered_items.setdefault(CONTROLLERS, {})
        controller_ids = {controller.id for controller in controllers}
        registered_ids = set(_registered_controller_ids.keys())
        existing_controller_ids = registered_ids & controller_ids
        new_controller_ids = controller_ids - registered_ids

        if deleted_controllers := registered_ids - controller_ids:
            for deleted_controller in deleted_controllers:
                del _registered_controller_ids[deleted_controller]

        for controller in [
            controller
            for controller in controllers
            if controller.id in existing_controller_ids
        ]:
            self.items[controller.id] = controller_object = GallagherControllerObject(
                controller, self.device, disabled=controller.id in self._disabled_items
            )
            for identifier in _registered_controller_ids[controller.id]:
                controller_object.add_object_to_device(identifier[0], identifier[1])

        for controller in [
            controller
            for controller in controllers
            if controller.id in new_controller_ids
        ]:
            if "unconfigured" in controller.extra_fields["statusFlags"]:
                continue
            for label in ("Health", "Tamper"):
                self.items[controller.id] = controller_object = (
                    GallagherControllerObject(controller, self.device)
                )
                controller_object.add_object_to_device(self._new_id, label)
                _registered_controller_ids.setdefault(controller.id, []).append(
                    (self._new_id, label)
                )
                self._new_id += 1

    def _initialize_inputs(self, inputs: list[FTInput]) -> None:
        """Create bacnet objects for detected inputs."""
        _registered_inputs = self._registered_items.setdefault(INPUTS, {})
        input_ids = {input.id for input in inputs}
        registered_ids = set(_registered_inputs.keys())
        existing_inputs = registered_ids & input_ids
        new_inputs = input_ids - registered_ids

        if deleted_inputs := registered_ids - input_ids:
            for deleted_input in deleted_inputs:
                del _registered_inputs[deleted_input]

        for input_item in [input for input in inputs if input.id in existing_inputs]:
            self.items[input_item.id] = input_object = GallagherInputObject(
                input_item, self.device, disabled=input_item.id in self._disabled_items
            )
            for identifier in _registered_inputs[input_item.id]:
                input_object.add_object_to_device(identifier[0], identifier[1])

        for input_item in [input for input in inputs if input.id in new_inputs]:
            if "unconfigured" in input_item.statusFlags:
                continue
            self.items[input_item.id] = input_object = GallagherInputObject(
                input_item, self.device
            )
            input_object.add_object_to_device(self._new_id)
            _registered_inputs.setdefault(input_item.id, []).append(
                (self._new_id, None)
            )
            self._new_id += 1

    def _initialize_outputs(self, outputs: list[FTOutput]) -> None:
        """Create bacnet objects for detected outputs."""
        _registered_output_ids = self._registered_items.setdefault(OUTPUTS, {})
        output_ids = {output.id for output in outputs}
        registered_ids = set(_registered_output_ids.keys())
        existing_outputs = registered_ids & output_ids
        new_outputs = output_ids - registered_ids

        if deleted_outputs := registered_ids - output_ids:
            for deleted_output in deleted_outputs:
                del _registered_output_ids[deleted_output]

        for output_item in [
            output for output in outputs if output.id in existing_outputs
        ]:
            self.items[output_item.id] = output_object = GallagherOutputObject(
                output_item,
                self.device,
                disabled=output_item.id in self._disabled_items,
                gll_client=self.gll_client,
            )
            for identifier in _registered_output_ids[output_item.id]:
                output_object.add_object_to_device(identifier[0], identifier[1])
                self.commendable_items[identifier[0]] = output_object

        for output_item in [output for output in outputs if output.id in new_outputs]:
            self.items[output_item.id] = output_object = GallagherOutputObject(
                output_item, self.device, gll_client=self.gll_client
            )
            output_object.add_object_to_device(self._new_id)
            _registered_output_ids.setdefault(output_item.id, []).append(
                (self._new_id, None)
            )
            self.commendable_items[self._new_id] = output_object
            self._new_id += 1

    # TODO: need to add a method for reader and door  and fence(AI) items.
