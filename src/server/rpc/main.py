import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.queries import all_artists, all_labels, all_releases, get_releases_from_before_seventies, \
    all_releases_from_artist, get_genres, all_releases_from_genre, get_countries, all_releases_from_country, \
    get_labels, get_artists, all_releases_from_label

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(('0.0.0.0', PORT), requestHandler=RequestHandler) as server:
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

        # artists
        server.register_function(get_artists, 'get_artists')
        server.register_function(all_releases_from_artist, 'get_releases_from_artist')

        # releases
        server.register_function(all_releases, 'get_releases')

        server.register_function(get_releases_from_before_seventies, 'get_releases_from_before_seventies')

        # genres
        server.register_function(get_genres, 'get_genres')
        server.register_function(all_releases_from_genre, 'get_releases_by_genre')

        # countries
        server.register_function(get_countries, 'get_countries')
        server.register_function(all_releases_from_country, 'get_releases_by_country')

        # labels
        server.register_function(get_labels, 'get_labels')
        server.register_function(all_releases_from_label, 'get_releases_by_label')

        # start the server
        print(f"Starting the RPC Server in port {PORT}...")
        server.serve_forever()
