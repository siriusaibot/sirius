#from bs4 import BeautifulSoup
#from urllib.request import urlopen
import wolframalpha
import requests

class TimeAPI():

    def __init__(self):
        self.appid="YJK9QR-AU6PKE33U6"
        self.client = wolframalpha.Client(self.appid)


    def call(self,city):
        res = self.client.query(f"{city} time")
        
        if res['@success'] == 'false':
            return 'unknown'
        else:
            #print(res['pod'][1]["subpod"]["img"]["@alt"])
            for item in res['pod']:
                if item["@title"] == "Result":
                    currentDateTime = item["subpod"]["img"]["@alt"]
                    currentDateTimeList = currentDateTime.split()
                    currentTime = currentDateTimeList[0].split(':')
                    if(currentDateTimeList[1]=="pm"):
                        currentTime[0] = int(currentTime[0])+12
                    return currentTime






if __name__ == "__main__":
    ta = TimeAPI()
    print(ta.call("rasht"))




