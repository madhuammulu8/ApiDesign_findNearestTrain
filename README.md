
## Live Websites

API EndPoint(Deployed in Vercel) : https://api-design-find-nearest-train.vercel.app/nearestlocation?latitude=40.0&longitude=-75.0


## How to run locally
Steps to follow if you want to install this in your local machine
```
Geopandas : pip install geopandas
Geopy: pip install geopy
FastPI:pip install fastapi
Point : pip install shapely

Run Command:

uvicorn main:app --reload
 or
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

```

## ApiDesign_findingNearestTrain(API Practices)

1. Our code will return an API that finds the nearest location based on the latitude and longitude we are entering in the input and returns the nearest rail line Southeastern Pennsylvania Transportation Authority
2. **Not searching the same location, again and again,**:  I am using Dictionary to store the nearest location based on the location we entered, Key is the latitude and longitude we entered and the value is the nearest location so that when a new code executes it will search if lat, long already in the dictionary if it is not then only it will execute the logic (Ex: Dictionary = {<POINT (40 -74)>: 'Trenton Line', <POINT (24 24)>: 'TrentLine'}, Implemented locking to prevent data corruption in a critical section(**dictionary**), In an asynchronous environment, when multiple tasks could be accessing and modifying shared data simultaneously, a lock is used to synchronize access to ensure that only one thread or task can execute critical part code at a time
3. **Cost Effective**: We have implemented caching so it doesn't have to repeat multiple searches and the execution time is saved, It helps in faster response time. It will minimize the API Usage fees, As the number of users increases, the load on external services remains lower due to cached results being served to a portion of the requests.
4. **Sensible responses for anyone from any location**: Using the Nominatim geocoding service, which is known for its global coverage and provides reverse coding, It helps in providing human-readable based on latitude and longitude,( Imp: I am looking into another factor as well)
5. **Reasonably-sized instance of your API able to serve millions of requests per day**:  I have implemented asynchronous function implementation, This allows to handle multiple requests concurrently, especially when involving I/O. "await" is used when calling async functions which enables to perform another task while waiting for certain operation to complete. Using try and except blocks helps prevent applications from crashing due to unexpected errors and ensures appropriate HTTP responses are returned, indicating the error status
6. **Protect your API against malicious users**: Implemented a rate limiter that allows a maximum of 10 requests within 60 seconds, It helps in protecting against a malicious attack such as brute force, API abuse, This is basic protection, We can use simple authentication if we need more protection
7. **DC metro**: https://opendata.dc.gov/datasets/metro-stations-regional/explore?location=38.934919%2C-77.042966%2C11.58#:~:text=Generate%20new%20download-,with,-latest%20data, Just add the .kml file our code perfectly works for this data also without changing any code, **Code is written in a way with minor modifications we can use it for any similar data**.


### Project Results : 

#### API:
<img width="1510" alt="Screenshot 2024-01-16 at 9 16 34 AM" src="https://github.com/madhuammulu8/ApiDesign_findNearestTrain/assets/65707202/3cf0c5b1-d921-4023-8bc6-b9d6526990c9">

#### Fronend:
![image](https://github.com/madhuammulu8/ApiDesign_findNearestTrain/assets/65707202/1a5160f7-36d9-48b5-aead-5b26c638e61b)

Frontend(Deployed in static web app Free Trail Expired): https://equal-coyote.static.domains/

### Google Earth Results
![image](https://github.com/madhuammulu8/ApiDesign_findNearestTrain/assets/65707202/2853e303-3e54-438e-89ae-b3e25c88e372)


### If you access more than 10 times within 60 seconds, It will show Rate Limit Exceeded

<img width="1021" alt="Screenshot 2024-01-11 at 10 25 56 PM" src="https://github.com/madhuammulu8/ApiDesign_findNearestTrain/assets/65707202/6cc2ea8d-1726-4b27-b6bc-87d751eeaa36">

