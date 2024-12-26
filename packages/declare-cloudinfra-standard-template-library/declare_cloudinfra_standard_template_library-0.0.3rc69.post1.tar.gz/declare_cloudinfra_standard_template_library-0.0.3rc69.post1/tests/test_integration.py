#   ---------------------------------------------------------------------------------
#   Copyright (c) Declare CloudInfra Limited Liability Company. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

from declare_cloudinfra_standard_template_library.hello_world import hello_goodbye_int


def test_hello_goodbye_int(mocker):
    mock_hello_world = mocker.patch("declare_cloudinfra_standard_template_library.hello_world.hello_world")
    mock_good_night = mocker.patch("declare_cloudinfra_standard_template_library.hello_world.good_night")

    hello_goodbye_int()

    mock_hello_world.assert_called_once_with(2)
    mock_good_night.assert_called_once()
