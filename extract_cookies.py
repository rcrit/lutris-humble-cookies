#!/usr/bin/python3 -I
#
# extract lutris cookies
# Copyright (C) 2022 Rob Crittenden
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import click
import os
import shutil
import sqlite3
import sys
import tempfile

from pathlib import Path

query = """
SELECT
    host,
    CASE substr(host,1,1)='.'
        WHEN 0 THEN 'FALSE' ELSE 'TRUE'
    END,
    path,
    CASE isSecure
        WHEN 0 THEN 'FALSE' ELSE 'TRUE'
    END,
    expiry,
    name,
    value
FROM moz_cookies WHERE host = '.humblebundle.com' AND name IN \
('csrf_cookie', '_simpleauth_sess')
"""


def get_cookies(dbpath, debug=False):
    """Run the query to return only the Humble cookies and print them"""
    if dbpath is None:
        print("No cookies file found", file=sys.stderr)
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    results = cur.execute(query)
    for res in results:
        print('\t'.join(map(lambda i: str(i), res)))
    con.close()


def find_cookie_dir(cookies, debug=False):
    """Return either the user-provided cookie db or find one"""
    if cookies:
        if debug:
            print("Returning provided cookies file {}".format(
                cookies), file=sys.stderr)
        return cookies

    ffdir = Path.home().joinpath(".mozilla/firefox/")
    paths = sorted(Path(ffdir).iterdir(), key=os.path.getatime)

    # Add some smarter filtering to make sure the directory we're requesting
    # is a profile and not some junk directory.
    valid_paths = [
        candidate
        for candidate in paths
        if candidate.joinpath(Path("cookies.sqlite")).exists()
    ]

    if valid_paths and debug:
        print("Candidates\n{}".format(
            "\n".join([str(x) for x in valid_paths])), file=sys.stderr
        )

        print("Choosing {}".format(str(valid_paths[-1])), file=sys.stderr)

    return valid_paths[-1].joinpath("cookies.sqlite")


@click.command("cli", context_settings={"show_default": True})
@click.argument("cookies", nargs=-1)
@click.option("--debug", default=False, help="Debug logging", is_flag=True)
def main(cookies, debug):
    with tempfile.NamedTemporaryFile() as temp:
        dbpath = find_cookie_dir(cookies, debug=debug)
        shutil.copy(dbpath, temp.name)
        get_cookies(temp.name, debug=debug)


if __name__ == '__main__':
    main()
