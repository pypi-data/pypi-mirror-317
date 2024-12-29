#
# Copyright (c) 2021 Dilili Labs, Inc.  All rights reserved. Contains Dilili Labs Proprietary Information. RESTRICTED COMPUTER SOFTWARE.  LIMITED RIGHTS DATA.
#
import json
import os
import sys
from argparse import ArgumentParser

from brainframe.api import BrainFrameAPI, bf_errors
from brainframe_apps.command_utils import by_name, command, subcommand_parse_args
from brainframe_apps.list_stream import get_stream_persistent_id, list_stream_parse_args
from brainframe_apps.logger_factory import log


def delete_stream(api, stream_persistent_id=None):
    streams = api.get_stream_configurations()
    stream_id = None
    stream = None

    try:
        for stream in streams:

            if stream_persistent_id is not None:
                # only delete the matching streams
                if str(get_stream_persistent_id(stream)) == stream_persistent_id:
                    api.delete_stream_configuration(stream.id, 5)
                    stream_id = stream.id
                    log.debug(
                        f"    {stream.id}: {stream.name} {stream_persistent_id} deleted"
                    )
            else:
                # delete all streams
                api.delete_stream_configuration(stream.id, 5)
                stream_id = stream.id
                log.debug(
                    f"    {stream.id}: {stream.name} {stream_persistent_id} deleted"
                )

        if stream_id is None:
            log.warning("    Stream not found")

    except (bf_errors.ServerNotReadyError, json.decoder.JSONDecodeError):
        log.error(
            f"    {stream.id}: {stream.name} {stream_persistent_id} delete stream failed"
        )
    return stream


@command("delete_stream")
def delete_stream_main():
    parser = ArgumentParser(
        description="This tool deletes video streams of the BrainFrame server."
    )
    list_stream_parse_args(parser)
    args = subcommand_parse_args(parser)

    # Connect to the BrainFrame Server
    server_url = args.server_url if args.server_url else f"http://{args.server_url}"
    log.debug(
        f"{os.path.basename(sys.argv[0])} Waiting for BrainFrame server at {server_url}"
    )
    api = BrainFrameAPI(server_url)
    try:
        api.wait_for_server_initialization(timeout=15)
    except (TimeoutError, bf_errors.ServerNotReadyError):
        log.error(f"BrainFrame server connection timeout")
        return

    stream = delete_stream(api, args.stream_url)

    if stream is None:
        print("\nNo stream found")


if __name__ == "__main__":
    by_name["delete_stream"]()
