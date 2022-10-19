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


def get_cookies(dbpath):
    """Run the query to return only the Humble cookies and print them"""
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    results = cur.execute(query)
    for res in results:
        print('\t'.join(map(lambda i: str(i), res)))
    con.close()


def find_cookie_dir():
    """Return either the user-provided cookie db or find one"""
    if len(sys.argv) == 2:
        return sys.argv[1]

    ffdir = Path.home().joinpath(".mozilla/firefox/")
    paths = sorted(Path(ffdir).iterdir(), key=os.path.getatime)

    return paths[-1].joinpath("cookies.sqlite")


def main():
    with tempfile.NamedTemporaryFile() as temp:
        dbpath = find_cookie_dir()
        shutil.copy(dbpath, temp.name)
        get_cookies(temp.name)


if __name__ == '__main__':
    main()
