import redis
from census_data import get_census_data

redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

def get_redis_client():
    """Get Redis client from connection pool"""
    return redis.Redis(connection_pool=redis_pool)

def get_census_data_from_cache(zip_code):
    """Get all census data for a zipcode from cache or fetch from Census API"""
    r = get_redis_client()
    cache_key = f'census_data:{zip_code}'
    cached_value = r.hgetall(cache_key)
    
    if cached_value:
        return {k.decode('utf-8'): v.decode('utf-8') for k,v in cached_value.items()}
        
    census_dict = get_census_data(zip_code)
    if census_dict is not None:
        set_census_data_in_cache(zip_code, census_dict)
        return census_dict
        
    return None

def set_census_data_in_cache(zip_code, census_data):
    """Store all census data for a zipcode in Redis hash"""
    r = get_redis_client()
    cache_key = f'census_data:{zip_code}'
    r.hmset(cache_key, census_data)

