#
# Copyright (c) 2021 Dilili Labs, Inc.  All rights reserved. Contains Dilili Labs Proprietary Information. RESTRICTED COMPUTER SOFTWARE.  LIMITED RIGHTS DATA.
#
import os
import socket
from argparse import ArgumentParser
from pathlib import Path

from brainframe_apps.logger_factory import log


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(("192.255.255.255", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


class UrlList:
    def __new__(cls, url_list: Path):
        __url_list = __UrlList__(url_list)

        if __url_list is None:
            return None

        self = object.__new__(cls)
        self.url_list = __url_list

        return self

    def __init__(self, url_list: Path):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        for line_str in self.url_list:
            if line_str.startswith("</"):
                stream_url = None
                raise StopIteration
            if line_str.startswith("<"):
                stream_url = None
                continue
            else:
                stream_url, *more = line_str.split(",")
                if stream_url is not None:
                    stream_url = stream_url.strip()

            return stream_url

        else:
            raise StopIteration


class __UrlList__:
    def __new__(cls, url_list: Path):
        if url_list is None:
            log.error("The stream list file is None")
            return None

        if os.path.isfile(url_list) is not True:
            log.error(f"{url_list} file is not found")
            return None

        return object.__new__(cls)

    def __init__(self, url_list: Path):
        self.localhost_ip = get_ip()
        self.file = open(url_list)

    def __iter__(self):
        return self

    def __next__(self):
        for self.line in self.file:
            line_str = self.line.strip()
            # Empty lines
            # Comment lines starts with "#"
            # Scheduling group starts with "<"
            if line_str != "" and not line_str.startswith("#"):

                one_url = line_str.replace("localhost", str(self.localhost_ip))

                return one_url

            else:
                # These are the comments in the stream_url.list file
                pass
        else:
            self.file.close()
            raise StopIteration


def _urls_parse_args(parser):
    parser.add_argument(
        "--stream-url-list",
        default=None,
        help="The name of the file with the list of stream urls. Default: %(default)s",
    )


def main():
    parser = ArgumentParser(description="BrainFrame Apps files, dirs, args")
    _urls_parse_args(parser)
    args = parser.parse_args()

    url_list = UrlList(args.stream_url_list)
    if url_list:
        for stream_url in url_list:
            log.debug(stream_url)

    return


if __name__ == "__main__":
    main()
