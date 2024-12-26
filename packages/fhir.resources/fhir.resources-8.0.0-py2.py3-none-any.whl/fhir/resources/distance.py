from __future__ import annotations as _annotations

"""
Profile: http://hl7.org/fhir/StructureDefinition/Distance
Release: R5
Version: 5.0.0
Build ID: 2aecd53
Last updated: 2023-03-26T15:21:02.749+11:00
"""
from . import quantity


class Distance(quantity.Quantity):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    A length - a value with a unit that is a physical distance.
    """

    __resource_type__ = "Distance"

    @classmethod
    def elements_sequence(cls):
        """returning all elements names from
        ``Distance`` according specification,
        with preserving original sequence order.
        """
        return ["id", "extension", "value", "comparator", "unit", "system", "code"]
