# Copyright (c) 2023 - 2024, HaiyangLi <quantocean.li at gmail dot com>
#
# SPDX-License-Identifier: Apache-2.0

from lionagi.protocols.adapters.adapter import AdapterRegistry
from lionagi.protocols.adapters.json_adapter import (
    JsonAdapter,
    JsonFileAdapter,
)
from lionagi.protocols.adapters.pandas_adapter import PandasSeriesAdapter

ADAPTERS = [
    JsonAdapter,
    JsonFileAdapter,
    PandasSeriesAdapter,
]


class ComponentAdapterRegistry(AdapterRegistry):
    _adapters = {k.obj_key: k() for k in ADAPTERS}


__all__ = ["ComponentAdapterRegistry"]
