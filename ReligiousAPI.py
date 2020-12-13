from datetime import datetime
import requests

class ReligiousAPI():

    def parseTimingsJson(self,responseJson):
        result = dict()
        data = responseJson["data"]
        for item in data:
            key = int(item["date"]["gregorian"]["day"])
            result[key] = {}
            fields = ["Fajr","Sunrise","Dhuhr","Asr","Sunset","Maghrib","Isha","Imsak","Midnight"]
            for field in fields:
                result[key][field] = item["timings"][field]

        return result


    def getTimingsJson(self,city,country,day,year=None,month=None):
        if year == None or month == None:
            year = datetime.now().year
            month = datetime.now().month

        response = requests.get(
            'http://api.aladhan.com/v1/calendarByCity',
            params={'city':city,'country':country,'month':month,'year':year,'method':7}
        )

        timingEntries = self.parseTimingsJson(response.json())
        
        return timingEntries[day]



if __name__ == "__main__":
   
    r = ReligiousAPI()
    print(r.getTimingsJson("Tehran","Iran",3))
            