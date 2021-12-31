import sys, os, multiprocessing
import json, re
from scrapper import ScrapeWebsite
import concurrent.futures as ft
from multiprocessing import Process, current_process

def generateInputData(stry):
    inputs = []

    if '-' in stry:
        kaweys = stry.strip().split("-")
    else:
        kaweys = [stry]
        
    for h in kaweys:
        g = h.split("*")
        inputs.append(g)

    print("generated")
    return inputs


def initiateScrapping(data):
    try:
        print(data)
        proc_name = current_process().name
        print("Initializing Scrapper...... for " + proc_name + " \n")
        
        print("Received " + str(len(data)) + " Parameters")
        province = data[0]
        city = data[1]
        ad_type = "w"
        keywordInput = data[2]
        print(province + ", " + city + ", " + ad_type + ", " + keywordInput)
        argss = (province, city, ad_type, keywordInput.split(","))
        app         = ScrapeWebsite(province, city, proc_name)
        total_command_line_arguments = len(argss)
        result = app.startScrape(argss)
        print("ok")
        return ""
    except Exception as e:
        print(e)
        return


# def main (ratta):
#     data = ratta
#     parameters = generateInputData(data)
#     print(len(parameters))
#     if __name__ == 'initScrapper':
#         print("yep")
#         multiprocessing.freeze_support()
#         pool = multiprocessing.Pool(processes=len(parameters))
#         results = pool.map(initiateScrapping, parameters)
#         print("here")
#         pool.join()
#         pool.close()  
#     print("done")
#     return data


if __name__ == '__main__':
    print(sys.argv)
    procs = []
    if len(sys.argv) > 1:
        data = sys.argv[1]
        print(data)
        parameters = generateInputData(data)
        print(parameters)
        for index, number in enumerate(parameters):
            proc = Process(target=initiateScrapping, args=(number,))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()
        
        sys.exit()
    else:
        sys.exit(1)

    
    
   