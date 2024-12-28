# -*- coding: utf-8 -*-

# (c) Meta Platforms, Inc. and affiliates.
#
# SPDX-3.0-License-Identifier: GPL-2.0-or-later
#
# This program is free software.
# For more information on the license, see COPYING.md.
# For more information on free software, see
# <https://www.gnu.org/philosophy/free-sw.en.html>.

from yaml import Dumper


class YamlDumper(Dumper):
    """
    A replacement for yaml.Dumper with proper indentation
    see https://github.com/yaml/pyyaml/issues/234#issuecomment-765894586
    """

    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)
