#   ---------------------------------------------------------------------------------
#   Copyright (c) Declare CloudInfra Limited Liability Company. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

from declare_cloudinfra_standard_template_library.hello_world import hello_goodbye
from unittest.mock import patch


@patch("declare_cloudinfra_standard_template_library.hello_world.hello_world")
@patch("declare_cloudinfra_standard_template_library.hello_world.good_night")
def test_hello_goodbye(mock_good_night, mock_hello_world):
    hello_goodbye()
    mock_hello_world.assert_called_once_with(1)
    mock_good_night.assert_called_once()
