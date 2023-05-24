import vt
import json
import argparse
from vt_modules import search_vt, download_vt_samples
from mystery_task import mystery, mystery2


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
    parser.add_argument("-l", "--stage", default="1", help="Stage of Task wanted to be completed.")
    # Do the extra mystery task
    parser.add_argument("-e", "--extra", default="x")
    args = parser.parse_args()
    
    if(args.vt_api == "creds.txt"):
        with open("samples/vt_creds.txt", "r") as c:
            args.vt_api= c.readline()
        c.close()

    if(args.stage == '1'):
        #VT_results = search_vt(args.vt_api, args.search)
        with open("results.json", "w+") as r:
            temp = json.loads(r.read())
            print(str(temp))
            a = {"a": 1, "b": 2, "c": 4}
            json.dump(a, r)
            quit()
            temp.update(VT_results)
            json.dump(temp, r)
        r.close()
    elif(args.stage == '2'):
        with open("results.json", "w") as r:
            temp = json.loads(r)
            download_vt_samples(args.api_key, temp, args.directory)
        r.close()
        
    elif(args.stage == '3'):
        with open("results.json", "w") as r:
            temp = json.loads(r)
            results = mystery(args.extra, temp)
            temp.update(results)
            json.dump(temp, r)
        r.close()
    
    elif(args.stage == '4'):
        with open("results.json", "w") as r:
            temp = json.loads(r)
            results = mystery2(args.extra, temp)
            temp.update(results)
            json.dump(temp, r)
        r.close()
    

if(__name__ == '__main__'):
    main()