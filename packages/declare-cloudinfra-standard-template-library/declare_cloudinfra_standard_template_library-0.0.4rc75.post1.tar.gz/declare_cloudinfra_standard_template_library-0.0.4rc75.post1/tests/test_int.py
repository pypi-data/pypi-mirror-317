#   ---------------------------------------------------------------------------------
#   Copyright (c) Declare CloudInfra Limited Liability Company. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

from declare_cloudinfra_standard_template_library.hello_world import hello_goodbye_int


def test_int_hello_goodbye():
    """Test the hello_goodbye_int function."""
    hello_goodbye_int()
