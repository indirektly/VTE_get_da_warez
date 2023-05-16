import vt
import argparse
from mystery_task import mystery


def main(args):
    parser = argparse.ArgumentParser(
        prog="VTE File retriever",
        description="This is used to get VT Enterprise files from a search and download them to be used for ~reasons~",
    )

    # VT Enterprise/Premium API key
    parser.add_argument("-a", "--vt_api", required=True, help="The API key")
    # VTE Search Query
    parser.add_argument("-s", "--search", required=True, help="The Search query that you would perform in VT Enterprise")
    # The directory to save the files to.        
    parser.add_argument("-d", "--directory" default=".", help="The directory to save the file samples from the search")
    # Redis DB ip:port combo for saving metadata
    parser.add_argument("-r", "--redis", default="x", help="Redis port:ip details to send the metadata")
    # Do the extra mystery task
    parser.add_argument("-e", "--extra", default="x")
    args = parser.parse_args()
    

    if(args.api == "creds.txt"):
        with open("samples/vt_creds.txt", "r") as c:
            args.api = c.readline()

    VT_results = searchVTandDownload(args.api, args.search, args.directory)



    if(args.extra != "x"):
        mystery(args.extra, VT_results["file_names"])
    



def searchVTandDownload(search_statement):
    vt_client = vt.Client()
    print("a")

    # Test search: p%253A5%2520type%253Adocument%2520s%253A1
    # test = c.iterator("/intelligence/search?query=p%253")
    # test4 = c.get_json("/intelligence/search?query=p%253")
    # test4['data']
    def searchVTE(search):
        print("a")
    def downloadFiles(searchResults):
        print("a")


def mysteryTask(filename):
    print("a")


if(__name__ == '__main__'):
    main()