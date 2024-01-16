import time
from functools import wraps
import geopandas as gpd
import uvicorn
from shapely.geometry import Point
from fiona.drvsupport import supported_drivers
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette import status
from fastapi import Request
from locationcachefile import location_cache, location_cache_lock, load_location_cache
from geopy.geocoders import Nominatim

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from os import  getenv

from fastapi_limiter import FastAPILimiter

supported_drivers['KML'] = 'rw'
gdf = gpd.read_file('SEPTARegionalRailStations2016.kml')
location_cache.update(load_location_cache())




async def find_nearest_point(latitude, longitude):
    # print(gdf)
    print(location_cache)
    with location_cache_lock:
        currentkey = Point(latitude, longitude)
        print("current", currentkey, location_cache)
        if currentkey in location_cache:
            print("Okay I am here", location_cache)
            return location_cache[currentkey]

        point = Point(latitude, longitude)
        gdf['distance'] = gdf['geometry'].distance(point)
        # print(gdf)
        # print(gdf.columns)
        nearest_point = gdf.loc[gdf['distance'].idxmin()]
        result = nearest_point['Name']
        location_cache[point] = result
        print(location_cache, "Name here")
        return result


# print(find_nearest_point(-75.76, 40.0))


def get_address(latitude, longitude):
    geolocator = Nominatim(user_agent="nearest")

    location = geolocator.reverse(( longitude,latitude), language="en")
    address = location.address if location and location.address else None
    return address


# print(find_nearest_point(40.0, -75.76))

def ratelimiter(maximumcalls: int, time_frame: int):
    def decorator(func):
        call = []

        @wraps(func)
        async def wrapper(request:Request, *args, **kwargs):
            current_time = time.time()
            calls_in_timeframe = [current_call for current_call in call if current_call > current_time - time_frame]

            if len(calls_in_timeframe) >= maximumcalls:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate Limit Exceeded")
            call.append(current_time)
            return await func(request, *args, **kwargs)

        return wrapper
    return decorator


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the appropriate origin or origins
    allow_credentials=True,
    allow_methods=["*"],  # Set this to the appropriate HTTP methods
    allow_headers=["*"],  # Set this to the appropriate headers
)

@app.get("/nearestlocation")
@ratelimiter(maximumcalls=10, time_frame=60)
async def get_nearest_location(request:Request,latitude: float, longitude: float):
    try:
        result = await find_nearest_point(longitude,latitude)
        address = get_address(longitude,latitude)
        return JSONResponse(content={
            "latitude": latitude,
            "longitude": longitude,
            "nearest_point": result,
            "Address": address})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(getenv("PORT",8000))
    uvicorn.run("app.main:",host="0.0.0.0",port=port,reload=True)
