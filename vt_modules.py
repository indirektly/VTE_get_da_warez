import vt

def search_vt(api_key, search_statement):
    vt_client = vt.Client(api_key)
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
            #temp["file_name"] = VTE_JSON_results["data"][i]["attributes"]["meaningful_name"]
            temp["search_used"] = search_statement
            samples_found[temp["sha256"]] = temp
        except:
            print("Issue with:\n\n")
            print(str(VTE_JSON_results["data"][i]))
    vt_client.close()
    return(samples_found)






def download_vt_samples(api_key, sample_dictionary, directory):
    vt_client = vt.Client(api_key)
    for item in sample_dictionary.keys():
        with open(directory + item, "wb") as f:
            vt_client.download_file(item, f)
        f.close()
    vt_client.close()














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
            #temp["file_name"] = VTE_JSON_results["data"][i]["attributes"]["meaningful_name"]
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