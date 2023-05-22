import vt
import json
import argparse
from mystery_task import mystery


def main():
    parser = argparse.ArgumentParser(
        prog="VTE File retriever",
        description="This is used to get VT Enterprise files from a search and download them to be used for ~reasons~",
    )

    # VT Enterprise/Premium API key
    parser.add_argument("-a", "--vt_api", required=True, help="The API key")
    # VTE Search Query
    parser.add_argument("-s", "--search", required=True, help="The Search query that you would perform in VT Enterprise")
    # The directory to save the files to.        
    parser.add_argument("-d", "--directory", default="./", help="The directory to save the file samples from the search")
    # Redis DB ip:port combo for saving metadata
    parser.add_argument("-r", "--redis", default="x", help="Redis port:ip details to send the metadata")
    # Do the extra mystery task
    parser.add_argument("-e", "--extra", default="x")
    args = parser.parse_args()
    
    if(args.vt_api == "creds.txt"):
        with open("samples/vt_creds.txt", "r") as c:
            args.vt_api= c.readline()
        c.close()


    VT_results = searchVTandDownload(args.vt_api, args.search, args.directory)

    if(args.extra != "x"):
        mystery(args.extra, VT_results)
    

    with open("results.json", "w") as r:
        temp = json.loads(r)
        temp.update(VT_results)
        final_results = json.dumps(temp)
        r.write(final_results)
    r.close()



def searchVTandDownload(api_key, search_statement, directory):
    vt_client = vt.Client(api_key)



    # Test search: p%253A5%2520type%253Adocument%2520s%253A1
    # Final search: p%3A5%20type%3Adocument%20s%3A1
    # test = c.iterator("/intelligence/search?query=p%253")
    # test4 = c.get_json("/intelligence/search?query=p%253")
    # test4['data']
    #
    # Data Needed: (Hashes of MD5 and SHA1), (File_type), Simple Disposition, Overall Engine Disposition
    # t["data"][i]["attributes"]["last_analysis_stats"]

    VTE_JSON_results = vt_client.get_json("/intelligence/search?query=" + search_statement)

    samples_found = {}
    for i in range(len(VTE_JSON_results["data"])):
        try:
            temp = {}
            # Hashes
            temp["md5"] = VTE_JSON_results["data"][i]["attributes"]["md5"]
            temp["sha1"] = VTE_JSON_results["data"][i]["attributes"]["sha1"]
            temp["sha256"] = VTE_JSON_results["data"][i]["attributes"]["sha256"]
            
            # Dispositions
            if(
                (VTE_JSON_results["data"][i]["attributes"]["last_analysis_stats"]["malicious"] > 0) 
                or (
                VTE_JSON_results["data"][i]["attributes"]["last_analysis_stats"]["suspicious"])):
                temp["simple_disposition"] = "malicious"
            else:
                temp["simple_disposition"] = "benign"
            temp["overall_disposition"] = VTE_JSON_results["data"][i]["attributes"]["last_analysis_stats"]
            
            # Meta data
            temp["file_type"] = VTE_JSON_results["data"][i]["attributes"]["type_description"]
            temp["file_name"] = VTE_JSON_results["data"][i]["attributes"]["meaningful_name"]
            temp["search_used"] = search_statement
            samples_found[temp["sha256"]] = temp
        except:
            print("Issue with:\n\n")
            print(str(VTE_JSON_results["data"][i]))


    # Download the samples
    for item in samples_found:
        with open(directory + item, "wb") as f:
            vt_client.download_file(item, f)
        f.close()
        

    vt_client.close()
    return(samples_found)

def mysteryTask(samples_found):
    print("a")


if(__name__ == '__main__'):
    main()