

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




sResponse2ndCategoryItem = \
'''{"findItemsByKeywordsResponse":
  [{"ack":["Success"],"version":["1.13.0"],"timestamp":["2018-03-03T23:04:24.581Z"],
    "searchResult":
      [{"@count":"1",
        "item":
          [ { "itemId":["202430076409"],
              "title":["Classic Western Electric KS-15874-L2 Cardmatic Tube Tester Made By Hickok Great!"],
              "globalId":["EBAY-US"],
              "subtitle":["Totally Complete Outfit!  Really NIce!"],
              "primaryCategory":[{"categoryId":["170062"],"categoryName":["Tube Testers"]}],
              "secondaryCategory":[{"categoryId":["7275"],"categoryName":["Parts & Tubes"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mgpbjxNWrOrRHjbTm5iC75w\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Classic-Western-Electric-KS-15874-L2-Cardmatic-Tube-Tester-Made-Hickok-Great-\/202430076409"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["61021"],"location":["Dixon,IL,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"154.06"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"154.06"}],
              "bidCount":["5"],
              "sellingState":["Active"],
              "timeLeft":["P4DT1H0M15S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-09-08T00:24:25.000Z"],
              "endTime":["2018-09-13T00:24:25.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["14"]}],"returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

              }]

           }],

        "paginationOutput":[{"pageNumber":["1"],"entriesPerPage":["100"],"totalPages":["1"],"totalEntries":["2374"]}],
        "itemSearchURL":["http:\/\/www.ebay.com\/sch\/i.html?_nkw=catalin&_ddo=1&_ipg=100&_pgn=1"]
   }
 ]
}'''
