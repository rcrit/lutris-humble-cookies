# Purpose
Configure the required Humble Bundle cookies so Lutris can connect and manage your games.

# Introduction
At some point in early 2022 Humble Bundle authentication from Lutris
started to fail. It is my guess this change is related to dropping support for Linux and the addition of the Humble App to play games from the Humble Connection.

Either way it stopped working. This was reported at https://github.com/lutris/lutris/issues/4099 .

I traced this down to a cookies problem and a found manual but annoying workaround of copying the cookie data from within the Firefox debugger.

These cookies eventually expire so the connection will fail with the dreaded "Access to https://www.humblebundle.com/api/v1/user/order denied" error. Then you have to go through the whole process again.

I got tired of doing this every few months so I wrote a cookie extraction script to do it for me.

There is probably some equivalent in Chrome but I don't use Chrome.

# Usage

If you find yourself in Lutris and you can't view or reload your Humble Bundle Games...

1. Disconnect from Humble Bundle so click the right-most icon next to Humble Bundle which is Quit. It is a recycle symbol with a right arrow coming out of it.
2. Quit Lutris
3. Launch or go to Firefox and logout then log back into your Humble Bundle account.
4. `python extract_cookies.py > ~/.cache/lutris/.humblebundle.auth` (see below for more details)
5. Launch Lutris
6. Click the Reload icon next to Humble Bundle
7. It should sync up shortly

# Details

If no PATH is provided then the script will search in ~/.mozilla/firefox for the latest accessed profile directory. It will use the cookies.sqlite in there.

If a PATH is provided it must be fully qualified and include cookies.sqlite, e.g. `/home/user/.mozilla/firefox/someprofile/cookies.sqlite`

The two required cookies will be printed on stdout. This can be used to redirect to the location you need. For example on a Fedora desktop this is:

`python extract_cookies.py > ~/.cache/lutris/.humblebundle.auth`

I originally thought that three cookies were required but during development I found that only the `_simpleauth_sess` and `csrf_cookie` cookies are.

# Flatpack / Steam Deck

It is reported in the ticket that for Flatpack/Steam Deck users you should redirect the output to `~/.var/app/net.lutris.Lutris/cache/lutris/.humblebundle.auth` instead. This is unverified by me.

# License
Released under the GPL v3 license.