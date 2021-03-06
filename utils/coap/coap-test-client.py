# Copyright 2017 IoT-Lab Team
# Contributor(s) : see AUTHORS file
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import logging
import asyncio
import argparse
from aiocoap import Context, Message, POST

logging.basicConfig(level=logging.INFO)


@asyncio.coroutine
def alive_message(args):
    path = args.path
    payload = args.payload,
    server = args.server

    protocol = yield from Context.create_client_context()

    if path == "alive":
        request = Message(code=POST, payload="Alive".encode('utf-8'))
        request.set_request_uri('coap://{}/{}'.format(server, path))
    else:
        request = Message(code=POST, payload=payload.encode('utf-8'))
        request.set_request_uri('coap://{}/server'.format(server))

    try:
        yield from protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)


def main():
    parser = argparse.ArgumentParser(description="Test CoAP client")
    parser.add_argument('--server', type=str, default="localhost",
                        help="Server host.")
    parser.add_argument('--path', type=str, default="alive",
                        help="CoAP resource path")
    parser.add_argument('--payload', type=str, default="",
                        help="CoAP resource payload")
    args = parser.parse_args()
    asyncio.get_event_loop().run_until_complete(alive_message(args))

if __name__ == "__main__":
    main()
