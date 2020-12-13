from datetime import datetime
import requests

class WeatherAPI():

    def __init__(self):
        self.appid = "bce69149aa859bc0158f62a8ee0834e0"
        self.standardConditions = ["toofan","barf","baroon","abr","aftab"]#Todo: Replace with persian equivalent
        self.apiWeatherConditions = {#https://openweathermap.org/weather-conditions
            "Thunderstorm":self.standardConditions[0],
            "Squall":self.standardConditions[0],
            "Tornado":self.standardConditions[0],
            "Ash":self.standardConditions[0],
            "Dust":self.standardConditions[0],
            "Sand":self.standardConditions[0],
            "Dust":self.standardConditions[0],
            "Snow":self.standardConditions[1],
            "Drizzle":self.standardConditions[2],
            "Rain":self.standardConditions[2],
            "Mist":self.standardConditions[2],
            "Smoke":self.standardConditions[2],
            "Haze":self.standardConditions[2],
            "Fog":self.standardConditions[2],
            "Clouds":self.standardConditions[3],
            "Clear":self.standardConditions[4],
            }

    def parseForecastJson(self,responseJson):
            result = dict()

            cnt = int(responseJson['cnt'])
            responseList = responseJson['list']
            for i in range(cnt):
                item = responseJson['list'][i]
                result[item['dt']] = {}
                fields = ['temp','temp_min','temp_max','pressure','sea_level','grnd_level','humidity']
                for field in fields:
                    result[item['dt']][field] = item['main'].get(field,'Unkown')
                result[item['dt']]['main_weather'] = self.apiWeatherConditions[item['weather'][0]['main']]
                result[item['dt']]['dt_txt'] = item.get('dt_txt','Unkown')
                result[item['dt']]['wind_speed'] = item['wind'].get('speed','Unkown')
                result[item['dt']]['wind_deg'] = item['wind'].get('deg','Unkown')
            return result


    def parseCurrentJson(self,responseJson):
        result = {}
        fields = ['temp','temp_min','temp_max','pressure','sea_level','grnd_level','humidity']
        for field in fields:
            result[field] = responseJson['main'].get(field,'Unkown')
        result['main_weather'] = self.apiWeatherConditions[responseJson['weather'][0]['main']]
        result['dt_txt'] = responseJson.get('dt_txt','Unkown')#
        result['wind_speed'] = responseJson['wind'].get('speed','Unkown')
        result['wind_deg'] = responseJson['wind'].get('deg','Unkown')
        return result


    def getForecastJson(self,city,utc):
        
        response = requests.get(
            'http://api.openweathermap.org/data/2.5/forecast',
            params={'q':city,'appid':self.appid,'units':'metric'}
        )

        weatherEntries = self.parseForecastJson(response.json())

        #finding nearest entry
        nearest_utc = min(weatherEntries, key=lambda x:abs(x-utc))
        
        return weatherEntries[nearest_utc]


    def getCurrentJson(self,city):
        response = requests.get(
            'http://api.openweathermap.org/data/2.5/weather',
            params={'q':city,'appid':self.appid,'units':'metric'}
        )

        return self.parseCurrentJson(response.json())



if __name__ == "__main__":
    
    wa = WeatherAPI()
    #print(wa.getForecastJson("tehran",int(datetime.now().timestamp())))
    print(wa.getCurrentJson("tehran"))
            