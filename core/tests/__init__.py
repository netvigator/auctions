

sEbayErrorResponse = \
    '''{"errorMessage":
        [{"error":
            [{"errorId":["10006"],
              "domain":["Security"],
              "severity":["Error"],
              "category":["System"],
              "message":["Rate limiter system error"],
              "subdomain":["RateLimiter"],
                    "parameter":[{"@name":"Param1","__value__":"Transport outbound I\/O exception in RateLimiterServiceV1: java.util.concurrent.ExecutionException: java.util.concurrent.TimeoutException: Did not receive response within 100 milliseconds, at service location: http:\/\/ngrlsvc.vip.ebay.com\/ngrlsvc\/v1\/RateLimiterService\/isRateLimited"}]}]}]}'''
#
# http://ngrlsvc.vip.ebay.com/ngrlsvc/v1/RateLimiterService/isRateLimited