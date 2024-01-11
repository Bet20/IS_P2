import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.queries import all_artists, all_labels, all_releases, count_releases, \
    all_release_titles, releases_from_artist_by_name, artist_name_by_id, releases_from_artist_by_id, \
    releases_from_label_by_name, releases_from_label_by_id, label_by_id, label_by_name, count_labels, count_artists, \
    count_releases_before_year, count_releases_after_year, count_releases_from_country, count_releases_from_genre, \
    count_releases_from_style, count_releases_from_label, count_releases_from_artist, files_list, soft_delete_document

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


        server.register_function(all_releases)
        server.register_function(count_releases)
        server.register_function(all_artists)
        server.register_function(all_release_titles)
        server.register_function(releases_from_artist_by_name)
        server.register_function(artist_name_by_id)
        server.register_function(releases_from_artist_by_id)
        server.register_function(releases_from_label_by_name)
        server.register_function(releases_from_label_by_id)
        server.register_function(all_labels)
        server.register_function(label_by_id)
        server.register_function(label_by_name)
        server.register_function(count_labels)
        server.register_function(count_artists)
        server.register_function(count_releases_before_year)
        server.register_function(count_releases_after_year)
        server.register_function(soft_delete_document)

        # start the server
        print(f"Starting the RPC Server in port {PORT}...")
        server.serve_forever()
