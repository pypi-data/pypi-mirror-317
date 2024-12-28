__version__ = '0.0.12'
__usage__ = """
    USAGE:
        As a module from any location
            python3 -m myhttps [-option value]

    OPTIONS:
        --v             Version Info(**)
        --help          Help and usage Info(**)
        -p              Port Number [default: 11443]
        -h              Host address
        -c              ssl cert file location
        -k              ssl key file location
        -mode           HTTPS or HTTP

"""
from outdated import check_outdated
is_outdated, latest = check_outdated("myhttps", __version__)
if is_outdated:
    print("The package myhttps is out of date. Your version is %s, the latest is %s." % (__version__, latest))