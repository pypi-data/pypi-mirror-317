"""Tests for gmail module"""

import pytest

from sxolar.util import gmail

class TestGmail:
    """Test the gmail module"""

    @pytest.mark.skip("Something about smtp is broken in pytest")
    def test_send_email(self):
        """Test the send_email function"""
        body = (
            "<h2>TestHtml</h2>\n"
            '<p><h3><a href="http://arxiv.org/abs/1005.5383v1">Interacting bosons in one '
            "dimension and Luttinger liquid theory [1005.5383v1]</a></h3><br>Adrian Del "
            "Maestro, Ian Affleck<br><br></p>\n"
            '<p><h3><a href="http://arxiv.org/abs/1312.6177v1">Quantum Monte Carlo '
            "measurement of the chemical potential of helium-4 "
            "[1312.6177v1]</a></h3><br>C. M. Herdman, A. Rommal, A. Del "
            "Maestro<br><br></p>"
        )
        gmail.send_email(
            subject="Test Email Sxolar",
            to="jameswkennington@gmail.com",
            body=body,
            is_plain=False,
        )
