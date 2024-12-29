import unittest as ut

from seismicrna.core.version import (__version__,
                                     MAJOR,
                                     MINOR,
                                     PATCH,
                                     PRTAG,
                                     format_version,
                                     parse_version)


class TestFormatVersion(ut.TestCase):

    def test_format_default(self):
        self.assertEqual(format_version(), __version__)

    def test_format_notag(self):
        self.assertEqual(format_version(3, 6, 5, ""), "3.6.5")

    def test_format_prtag(self):
        self.assertEqual(format_version(0, 24, 0, "b"), "0.24.0b")


class TestParseVersion(ut.TestCase):

    def test_parse_default(self):
        self.assertEqual(parse_version(), (MAJOR, MINOR, PATCH, PRTAG))

    def test_parse_notag(self):
        self.assertEqual(parse_version("12.18.25"), (12, 18, 25, ""))

    def test_parse_prtag_letter(self):
        self.assertEqual(parse_version("0.9.5a"), (0, 9, 5, "a"))

    def test_parse_prtag_letters(self):
        self.assertEqual(parse_version("1.16.2rc"), (1, 16, 2, "rc"))

    def test_parse_prtag_letters_numbers(self):
        self.assertEqual(parse_version("8.7.4xyz321"), (8, 7, 4, "xyz321"))

    def test_invalid_1(self):
        self.assertRaisesRegex(ValueError,
                               "Malformatted version",
                               parse_version,
                               "123456")

    def test_invalid_2(self):
        self.assertRaisesRegex(ValueError,
                               "Malformatted version",
                               parse_version,
                               "12.689")

    def test_invalid_3(self):
        self.assertRaisesRegex(ValueError,
                               "Malformatted version",
                               parse_version,
                               "7.0.a")

    def test_invalid_4(self):
        self.assertRaisesRegex(ValueError,
                               "Malformatted version",
                               parse_version,
                               "0.9.5.a")

    def test_invalid_5(self):
        self.assertRaisesRegex(ValueError,
                               "Malformatted version",
                               parse_version,
                               "8.7.4xyz321b")


if __name__ == "__main__":
    ut.main()

########################################################################
#                                                                      #
# © Copyright 2024, the Rouskin Lab.                                   #
#                                                                      #
# This file is part of SEISMIC-RNA.                                    #
#                                                                      #
# SEISMIC-RNA is free software; you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation; either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# SEISMIC-RNA is distributed in the hope that it will be useful, but   #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANT- #
# ABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General     #
# Public License for more details.                                     #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with SEISMIC-RNA; if not, see <https://www.gnu.org/licenses>.  #
#                                                                      #
########################################################################
