import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.queries import all_artists, all_labels, all_releases, get_releases_from_before_seventies, all_releases_from_artist

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(('localhost', PORT), requestHandler=RequestHandler) as server:
        server.register_introspection_functions()

        def signal_handler(signum, frame):
            print("received signal")
            server.server_close()

            # perform clean up, etc. here...
            print("exiting, gracefully")
            sys.exit(0)

        # signals
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)


        # register functions
        server.register_function(all_artists, 'get_artists')
        server.register_function(all_labels, 'get_labels')
        server.register_function(all_releases, 'get_releases')
        server.register_function(all_releases_from_artist, 'get_releases_from_artist')
        server.register_function(get_releases_from_before_seventies, 'get_releases_from_before_seventies')

        # start the server
        print(f"Starting the RPC Server in port {PORT}...")
        server.serve_forever()
