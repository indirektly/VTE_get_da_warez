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
        c.close()

    VT_results = searchVTandDownload(args.api, args.search, args.directory)



    if(args.extra != "x"):
        mystery(args.extra, VT_results["file_names"])
    



def searchVTandDownload(api_key, search_statement):
    vt_client = vt.Client(api_key)
    print("a")



    # Test search: p%253A5%2520type%253Adocument%2520s%253A1
    # test = c.iterator("/intelligence/search?query=p%253")
    # test4 = c.get_json("/intelligence/search?query=p%253")
    # test4['data']
    #
    # Data Needed: (Hashes of MD5 and SHA1), (File_type), Simple Disposition, Overall Engine Disposition
    # t["data"][i]["attributes"]["last_analysis_stats"]

    VTE_JSON_results = vt_client.get_json("/intelligence/search?query=" + search_statement)
    samples_found = {}
    for i in range(len(VTE_JSON_results["data"])):
        temp = {}
        temp["md5"] = VTE_JSON_results["data"][i]["attributes"]["md5"]
        temp["sha1"] = VTE_JSON_results["data"][i]["attributes"]["sha1"]
        temp["sha256"] = VTE_JSON_results["data"][i]["attributes"]["sha256"]
        if((VTE_JSON_results["data"][i]["attributes"]["last_analysis_stats"]["malicious"] > 0) or (VTE_JSON_results["data"][i]["attributes"]["last_analysis_stats"]["suspicious"])):
            temp["Simple_Disposition"] = "malicious"
        else:
            temp["Simple_Disposition"] = "benign"
        temp["Overall_Disposition"] = VTE_JSON_results["data"][i]["attributes"]["last_analysis_stats"]
        samples_found[temp["sha256"]] = temp

    
    # client.download_file("44d88612fea8a8f36de82e1278abb02f", f)
    def downloadFiles(samples_found):
        print("a")


def mysteryTask(samples_found):
    print("a")


if(__name__ == '__main__'):
    main()