# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
"""Handles speculative plugins for third-party modules.

Please check out the source code of this module for examples of how plugins work and how you can
write your own one. Currently, we support plugins for

- :meth:`transformers<modelopt.torch.speculative.plugins.transformers>`
"""

from modelopt.torch.utils import import_plugin

with import_plugin("megatron"):
    from .megatron import *

with import_plugin("transformers"):
    from .transformers import *
