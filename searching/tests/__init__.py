sItemHitLog = \
'''
tTimeEnd            | iItemNumb    | iHitStars
2018-03-07 20:59:24 | 132521748790 | 175
2018-03-23 21:29:45 | 401354589892 | 200
2018-03-10 11:46:09 | 372238175241 | 270
'''

sBrands = \
'''
      cTitle       | iStars | cExcludeIf |  cLookFor  
-------------------+--------+------------+------------
 Marantz           |     10 | Speaker\\rAV9000 | 
 ACRO              |      9 |            | 
 Western Electric  |      9 |            | 
 Radio Craftsmen   |      8 |            | 
 Fairchild         |      8 |            | 
 Pilot             |      8 |            | 
 Langevin          |      8 |            | 
 UTC               |      8 |            | 
 Brook             |      8 |            | 
 EICO              |      7 |            | 
 Lafayette         |      7 |            | 
 Leak              |      7 |            | 
 McIntosh          |      6 |            | 
 Luxman            |      6 |            | 
 Quad              |      5 |            | 
 Ampex             |      5 |            | 
 Sherwood          |      5 |            | 
 Stromberg-Carlson |      5 |            | 
 Audio Research    |      5 |            | 
 Grommes           |      5 |            | 
 Regency           |      5 |            | 
 Bell              |      4 |            | 
 Sargent-Rayment   |      4 |            | 
 Knight            |      4 |            | 
 Interelectronics  |      3 |            | 
 PACO              |      2 |            | 
 Astronic          |      2 |            | 
 MFA               |      8 |            | 
 National          |      7 |            | 
 DuKane            |      7 |            | 
 Brociner          |      6 |            | 
 Altec-Lansing     |     10 |            | 
 Fisher            |      9 |            | 
 Heathkit          |      8 |            | Heath
 Scott, H.H.       |      8 |            | Scott\\rH.H. Scott
 Harman-Kardon     |      7 |            | 
 Electro-Voice     |      7 |            | EV
 Klangfilm         |      6 |            | 
 Dynaco            |      5 |            | Dyna\\rDynakit
 Allied            |      5 |            | 
 Bogen             |      1 |            | 
 Garod             |      5 |            | Garol 
 Addison           |      7 |            | 
 Fada              |      8 |            | 
 Emerson           |      6 |            | 
 DeWald            |      4 |            | 
 Crosley           |      3 |            | 
 RCA               |      6 |            | 
 Radford           |      7 |            | 
 Bendix            |      7 |            | 
 Westinghouse      |      5 |            | 
 GE                |      5 |            | General Electric
 Spartan           |      8 |            | 
 Coronado          |      7 |            | 
 Motorola          |      7 |            | 
 Arvin             |      7 |            | 
 Kadette           |      6 |            | 
 Sentinel          |      6 |            | 
 Silvertone        |      3 |            | 
'''

sModels = \
'''
       cTitle       | cKeyWords | iStars | bSubModelsOK |      Brand        |     Category |  cLookFor   |  cExcludeIf  
--------------------+-----------+--------+--------------+-------------------+--------------+-------------+--------------
 XP-55-B            |           |      4 | t            | Fisher            |Speaker System|             | 
 HF-61A             |           |      6 | t            | EICO              |       Preamp |             | 
 HF-85              |           |      7 | t            | EICO              |       Preamp |             | 
 ST-84              |           |      7 | t            | EICO              |       Preamp |             | 
 80-C               |           |      7 | f            | Fisher            |       Preamp |             | 
 90-C               |           |      9 | f            | Fisher            |       Preamp |             | 
 PR-6               |           |      5 | t            | Fisher            |       Preamp |             | 
 PR-66              |           |      5 | t            | Fisher            |       Preamp |             | 
 C-20               |           |      6 | t            | McIntosh          |       Preamp |             | 
 C-11               |           |      7 | t            | McIntosh          |       Preamp |             | 
 122                |           |      8 | t            | Scott, H.H.       |       Preamp |             | 
 C-350              |           |      8 | t            | Radio Craftsmen   |       Preamp |             | 
 HF-65              |           |      7 | t            | EICO              |       Preamp |             | 
 PC-1               |           |      9 | t            | Electro-Voice     |       Preamp |             | 
 210PA              |           |      6 | t            | Grommes           |       Preamp |             | 
 212                |           |      5 | t            | Grommes           |       Preamp |             | 
 AP-426             |           |      5 | t            | Stromberg-Carlson |       Preamp |             | 
 Citation IV        |           |      9 | t            | Harman-Kardon     |       Preamp |             | 
 SP-2               |           |      5 | t            | Heathkit          |       Preamp |             | 
 440C               |           |      5 | t            | Altec-Lansing     |       Preamp |             | 
 Point 1            |           |      8 | t            | Leak              |       Preamp |             | 
 AE-2               |           |      7 | t            | McIntosh          |       Preamp |             | 
 C-104              |           |      5 | t            | McIntosh          |       Preamp |             | 
 445A               |           |      8 | f            | Altec-Lansing     |       Preamp |             | 
 PAM-1              |           |      4 | t            | Dynaco            |       Preamp |             | 
 PAS-2              |           |      4 | t            | Dynaco            |       Preamp |             | 
 A-433A             |           |      8 | t            | Altec-Lansing     |       Preamp |             | 
 SP-6               |           |      9 | t            | Audio Research    |       Preamp |             | 
 PAS-3              |           |      7 | t            | Dynaco            |       Preamp |             | PAS-2
 SP-8               |           |      9 | t            | Audio Research    |       Preamp |             | 
 S1001              |           |      6 | t            | ACRO              |       Preamp |             | 
 116B               |           |      9 | t            | Langevin          |       Preamp |             | 
 PR-100A            |           |      8 | t            | Bogen             |       Preamp |             | 
 Consolette         |           |      6 | t            | Interelectronics  |       Preamp |             | 
 400-C              |           |      7 | f            | Fisher            |       Preamp |             | 400-CX
 130                |           |      8 | t            | Scott, H.H.       |       Preamp |             | 
 Citation I         |           |      8 | f            | Harman-Kardon     |       Preamp |             | Sixteen
 WA-P2              |           |      5 | t            | Heathkit          |       Preamp |             | 
 KT-600A            |           |      9 | t            | Lafayette         |       Preamp |             | 
 4B                 |           |      7 | t            | Brook             |       Preamp |             | Bryston
 C-4                |           |      4 | t            | McIntosh          |       Preamp |             | 
 C-108H             |           |      4 | t            | McIntosh          |       Preamp |             | 
 CL-35              |           |      7 | t            | Luxman            |       Preamp |             | 
 Luminescence       |           |      9 | t            | MFA               |       Preamp |             | 
 SC2                |           |      7 | t            | Radford           |       Preamp |             | 
 C-32               |           |      7 | t            | Luxman            |       Preamp |             | 
 50-C               |           |      7 | f            | Fisher            |       Preamp |             | 
 CL-32              |           |      8 | t            | Luxman            |       Preamp |             | 
 C-8                |           |      4 | t            | McIntosh          |       Preamp |             | C-8S
 SP-1               |           |      9 | t            | Audio Research    |       Preamp |             | 
 SP-2               |           |      9 | t            | Audio Research    |       Preamp |             | 
 SP-3               |           |      9 | t            | Audio Research    |       Preamp |             | 
 SP-3A1             |           |      9 | t            | Audio Research    |       Preamp |             | 
 SP-11              |           |      9 | t            | Audio Research    |       Preamp |             | 
 SP-12              |           |      9 | t            | Audio Research    |       Preamp |             | 
 A100               |           |      5 | t            | Brociner          |       Preamp |             | 
 12A3               |           |      8 | t            | Brook             |       Preamp |             | 
 A100PV             |           |      5 | t            | Brociner          |       Preamp |             | 
 A1005              |           |      5 | t            | Brociner          |       Preamp |             | 
 CA-2               |           |      5 | t            | Brociner          |       Preamp |             | 
 Mark 30C           |           |      5 | t            | Brociner          |       Preamp |             | 
 3G                 |           |      7 | t            | Brook             |       Preamp |             | 
 ST-94              |           |      7 | t            | EICO              |       Preamp |             | 
 Varislope Mono     |           |      7 | t            | Leak              |       Preamp |             | Stereo
 Horizon 5          |           |      6 | t            | National          |       Preamp |             | 
 SP-215             |           |     10 | t            | Pilot             |       Preamp |             | 
 LC-21              |           |      8 | t            | Scott, H.H.       |       Preamp |             | 
 Quad 22            |           |      8 | t            | Quad              |       Preamp |             | 
 C-8S               |           |      5 | t            | McIntosh          |       Preamp |             | 
 SV-1               |           |      8 | t            | RCA               |       Preamp |             | 
 121-C              |           |      9 | t            | Scott, H.H.       |       Preamp |             | 
 C-22               |           |      7 | t            | McIntosh          |       Preamp |             | CM
 SP-210             |           |      8 | t            | Pilot             |       Preamp |             | 
 Verislope 3        |           |      8 | t            | Leak              |       Preamp | Verislope\\rVarislope\\rVeriscope\\rVariscope | Mono
 240                |           |      9 | t            | Fairchild         |       Preamp |             | 
 QC II              |           |      8 | t            | Quad              |       Preamp |             | 
 400-CX             |           |     10 | f            | Fisher            |       Preamp |             | 400-CX-2
 350-P              |           |      8 | t            | Regency           |       Preamp |             | AD1/350
 350                |           |      3 | t            | Ampex             |       Preamp |             | AD1/350
 7                  |           |      9 | t            | Brook             |       Preamp |             | Marantz
 Quad 33            |           |      2 | t            | Quad              |       Preamp |             | 
 PAS-3X             |           |      9 | f            | Dynaco            |       Preamp |             | 
 Audio Consolette   |           |     10 | t            | Marantz           |       Preamp |           1 | 1 pc\\r45\\rDD 5.1\\rDLB\\rWC-1\\rMA500\\rPMD\\r1050\\r200\\rQuad Adapter\\rSQ\\rVan Alstine\\rChannel\\rRecorder
 245                |           |      9 | t            | Fairchild         |       Preamp |             | 
 7                  |           |     10 | t            | Marantz           |       Preamp |             | 7 pcs\\rBrook\\r7T\\rSC-7\\rSG-7 
 400-CX (4 button)  |           |      8 | t            | Fisher            |       Preamp |             | 400-CX-2
 400-CX-2           |           |     10 | f            | Fisher            |       Preamp |             | 
 mirror             |           |      8 | t            | Spartan           |        Radio |             | 
 RC350              |           |      8 | t            | RCA               |        Radio |             | 
 126                |           |      8 | t            | Garod             |        Radio |             | 
 R5A1               |           |      7 | t            | Addison           |        Radio |             | 
 50XC               |           |      7 | t            | Motorola          |        Radio |             | 
 1465               |           |      8 | t            | Crosley           |        Radio |             | 
 66X8               |           |      8 | t            | RCA               |        Radio |             | 
 43-8190            |           |      8 | t            | Coronado          |        Radio |             | 
 AX-235             |           |      8 | t            | Emerson           |        Radio |             | 
 A5                 |           |      8 | t            | Addison           |        Radio |             | 
 526-C              |           |      7 | t            | Bendix            |        Radio |             | 
 E38                |           |      5 | t            | Lafayette         |        Radio |             | 
 51x16 S            |           |      6 | f            | Motorola          |        Radio |             | 
 284-N              |           |      7 | t            | Sentinel          |        Radio |             | 
 R5A3               |           |      9 | t            | Addison           |        Radio |             | 
 51x16              |           |      6 | f            | Motorola          |        Radio |             | 
 A-502              |           |      8 | t            | DeWald            |        Radio |             | 
 L-570              |           |      8 | t            | GE                |        Radio |             | 
 1B55L              |           |      8 | t            | Garod             |        Radio |             | 
 557                |           |      8 | t            | Spartan           |        Radio |             | 
 L-622              |           |      8 | t            | GE                |        Radio |             | 
 3284               |           |      5 | t            | Silvertone        |        Radio |             | 
 P38                |           |      4 | t            | Fada              |        Radio |             | 
 BT245              |           |      8 | t            | Emerson           |        Radio |             | 
 558                |           |      8 | t            | Spartan           |        Radio |             | 
 66X9               |           |      6 | t            | RCA               |        Radio |             | 
 EP-375             |           |      9 | t            | Emerson           |        Radio |             | 
 A-501              |           |      7 | t            | DeWald            |        Radio |             | 
 H136               |           |      8 | t            | Westinghouse      |        Radio |             | 
 V-3468             |           |      8 | t            | Westinghouse      |        Radio |             | 
 Bluebird           |           |      8 | t            | Spartan           |        Radio |             | 
 520                |           |      7 | t            | Emerson           |        Radio |             | 
 1450               |           |      8 | t            | Garod             |        Radio |             | 
 B501               |           |      7 | t            | DeWald            |        Radio |             | 
 A2A                |           |      7 | t            | Addison           |        Radio |             | 
 BM258              |           |      6 | t            | Emerson           |        Radio |             | 
 50-X-C3            |           |      7 | t            | Motorola          |        Radio |             | 
 50-XC4             |           |      9 | t            | Motorola          |        Radio |             | 
 532                |           |      8 | t            | Arvin             |        Radio |             | 
 H126               |           |      8 | t            | Westinghouse      |        Radio |             | 
 6AU-1              |           |      9 | t            | Garod             |        Radio |             | 
 AU-190             |           |      8 | t            | Emerson           |        Radio |             | 
 2A                 |           |      8 | t            | Addison           |        Radio |             | 
 700                |           |     10 | t            | Fada              |        Radio |             | 
 K25                |           |      7 | t            | Kadette           |        Radio |             | 
 711                |           |      8 | t            | Fada              |        Radio |             | 
 53X                |           |      8 | t            | Fada              |        Radio |             | 
 652                |           |      0 | t            | Fada              |        Radio |             | 
 400                |           |      7 | t            | Emerson           |        Radio |             | 
 537                |           |      8 | t            | Spartan           |        Radio |             | 
 F55                |           |      8 | t            | Fada              |        Radio |             | 
 51C                |           |      8 | t            | Motorola          |        Radio |             | 
 5                  |           |      9 | t            | Addison           |        Radio |             | 5 NOS\\r5 ea\\r5 each\\r5 pack\\r5 pair\\r5 pcs\\rbox of 5\\rqty 5
 115                | Catalin   |      8 | t            | Fada              |        Radio |             | 
 136                | Catalin   |      9 | t            | Fada              |        Radio |             | 
 116                | Catalin   |      8 | t            | Fada              |        Radio |             | 
 845                |           |      6 | t            | Fada              |        Radio |             | 
 1000               | Catalin   |      9 | t            | Fada              |        Radio |             | 115
 511                |           |      8 | t            | Emerson           |        Radio |             | 
 5F60               |           |      9 | t            | Fada              |        Radio |             | 
 L 56               |           |      8 | t            | Fada              |        Radio |             | 
 5F50               |           |      7 | t            | Fada              |        Radio |             | 
 526-MC             |           |      5 | t            | Bendix            |        Radio |             | 
 248-NI             |           |     10 | t            | Sentinel          |        Radio |             | 
 235                |           |      7 | t            | Emerson           |        Radio | Little Miracle | 
'''


dSearchResult = \
{'autoPay': 'false',
 'condition': {'conditionDisplayName': 'New', 'conditionId': '1000'
}, 'country': 'US',
 'galleryURL': 'http://thumbs3.ebaystatic.com/m/mutHoe85kv1_SUEGG3k1yBw/140.jpg',
 'globalId': 'EBAY-US',
 'isMultiVariationListing': 'false',
 'itemId': '282330751118',
 'listingInfo': {'bestOfferEnabled': 'true',
  'buyItNowAvailable': 'false',
  'endTime': '2018-02-13T00:34:26.000Z',
  'gift': 'false',
  'listingType': 'FixedPrice',
  'startTime': '2017-01-19T00:34:26.000Z',
  'watchCount': '19'
}, 'location': 'Staten Island,NY,USA',
 'paginationOutput': {'entriesPerPage': '100',
  'pageNumber': '1',
  'thisEntry': '1',
  'totalEntries': '1320',
  'totalPages': '14'
}, 'paymentMethod': 'PayPal',
 'postalCode': '10303',
 'primaryCategory': {'categoryId': '73160',
  'categoryName': 'Capacitance & ESR Meters'
}, 'returnsAccepted': 'true',
 'sellingStatus': {'convertedCurrentPrice': {'@currencyId': 'USD',
   '__value__': '27.99'
},  'currentPrice': {'@currencyId': 'USD', '__value__': '27.99'
},  'sellingState': 'Active',
  'timeLeft': 'P13DT6H33M56S'
}, 'shippingInfo': {'expeditedShipping': 'false',
  'handlingTime': '1',
  'oneDayShippingAvailable': 'false',
  'shipToLocations': 'Worldwide',
  'shippingServiceCost': {'@currencyId': 'USD', '__value__': '0.0'
},  'shippingType': 'Free'
}, 'title': 'Digital Capacitance Tester Capacitor Meter Auto Range Multimeter Checker 470mF',
 'topRatedListing': 'true',
 'viewItemURL': 'http://www.ebay.com/itm/Digital-Capacitance-Tester-Capacitor-Meter-Auto-Range-MultimeterChecker-470mF-/282330751118'
 }



sExampleResponse = \
'''{
  "findItemsAdvancedResponse":[
    {
      "itemSearchURL":["http://www.ebay.com/sch/58277/i.html?_nkw=Simpson+360&_ddo=1&_ipg=100&_pgn=1" ],
      "paginationOutput":[
        { "totalPages":["1" ],
          "entriesPerPage":["100" ],
          "pageNumber":["1" ],
          "totalEntries":["4" ] } ],
      "ack":["Success" ],
      "timestamp":["2017-12-15T14:18:54.955Z" ],
      "searchResult":[
        { "item":[
          { "itemId":["253313715173" ],
              "isMultiVariationListing":["false" ],
              "topRatedListing":["false" ],
              "globalId":["EBAY-US" ],
              "title":["Simpson 360-2 Digital Volt-Ohm Milliammeter Operator's Manual" ],
              "country":["US" ],
              "shippingInfo":[
                { "expeditedShipping":["false" ],
                "shippingType":["Calculated" ],
                "handlingTime":["3" ],
                "shipToLocations":["Worldwide" ],
                "oneDayShippingAvailable":["false" ] } ],
              "galleryURL":["http://thumbs2.ebaystatic.com/m/m0WO4pWRZTzusBvJHT07rtw/140.jpg" ],
              "autoPay":["false" ],
              "location":["Ruskin,FL,USA" ],
              "postalCode":["33570" ],
              "returnsAccepted":["false" ],
              "viewItemURL":["http://www.ebay.com/itm/Simpson-360-2-Digital-Volt-Ohm-Milliammeter-Operators-Manual-/253313715173" ],
              "sellingStatus":[
                { "currentPrice":[
                    { "@currencyId": "USD", "__value__": "10.0" } ],
                "timeLeft":["P29DT15H3M53S" ],
                "convertedCurrentPrice":[
                    { "@currencyId": "USD", "__value__": "10.0" } ],
                "sellingState":["Active" ] } ],
              "paymentMethod":["PayPal" ],
              "primaryCategory":[
                { "categoryId":["58277" ],
                "categoryName":["Multimeters" ] } ],
              "condition":[
                { "conditionId":["3000" ],
                "conditionDisplayName":["Used" ] } ],
              "listingInfo":[
                { "listingType":["StoreInventory" ],
                "gift":["false" ],
                "bestOfferEnabled":["false" ],
                "startTime":["2017-12-15T05:22:47.000Z" ],
                "buyItNowAvailable":["false" ],
                "endTime":["2018-01-14T05:22:47.000Z" ] } ]

            },{"itemId":["132401762082" ],
              "isMultiVariationListing":["false" ],
              "topRatedListing":["false" ],
              "globalId":["EBAY-US" ],
              "title":["Simpson 360 Digital Multi Meter Volt Ohm Milliameter Working" ],
              "country":["US" ],
              "shippingInfo":[
                { "expeditedShipping":["false" ],
                "handlingTime":["2" ],
                "shippingServiceCost":[
                    { "@currencyId": "USD", "__value__": "0.0" } ],
                "oneDayShippingAvailable":["false" ],
                "shipToLocations":["Worldwide" ],
                "shippingType":["Free" ] } ],
              "galleryURL":["http://thumbs3.ebaystatic.com/m/mc2iTJIYDZVO0Nh-w2n1Tzw/140.jpg" ],
              "autoPay":["false" ],
              "location":["Bellmore,NY,USA" ],
              "postalCode":["11710" ],
              "returnsAccepted":["false" ],
              "viewItemURL":["http://www.ebay.com/itm/Simpson-360-Digital-Multi-Meter-Volt-Ohm-Milliameter-Working-/132401762082" ],
              "sellingStatus":[
                { "currentPrice":[
                    { "@currencyId": "USD", "__value__": "79.99" } ],
                "timeLeft":["P1DT6H52M48S" ],
                "convertedCurrentPrice":[
                    { "@currencyId": "USD", "__value__": "79.99" } ],
                "sellingState":["Active" ] } ],
              "paymentMethod":["PayPal" ],
              "primaryCategory":[
                { "categoryId":["58277" ],
                "categoryName":["Multimeters" ] } ],
              "condition":[
                { "conditionId":["3000" ],
                "conditionDisplayName":["Used" ] } ],
              "listingInfo":[
                { "listingType":["FixedPrice" ],
                "gift":["false" ],
                "bestOfferEnabled":["false" ],
                "watchCount":["5" ],
                "startTime":["2017-11-16T21:11:42.000Z" ],
                "buyItNowAvailable":["false" ],
                "endTime":["2017-12-16T21:11:42.000Z" ] } ]

            },{"itemId":["253303813311" ],
              "isMultiVariationListing":["false" ],
              "topRatedListing":["false" ],
              "globalId":["EBAY-US" ],
              "title":["SIMPSON 360-2 RUNII DIGITAL OHM -VOLT METER #12286" ],
              "country":["US" ],
              "shippingInfo":[
                { "expeditedShipping":["true" ],
                "handlingTime":["3" ],
                "shippingServiceCost":[
                    { "@currencyId": "USD", "__value__": "0.0" } ],
                "oneDayShippingAvailable":["false" ],
                "shipToLocations":["Worldwide" ],
                "shippingType":["FreePickup" ] } ],
              "galleryURL":["http://thumbs4.ebaystatic.com/m/m0SU_J1v1SigYgs-VTlbe6g/140.jpg" ],
              "autoPay":["true" ],
              "location":["Sapulpa,OK,USA" ],
              "postalCode":["74066" ],
              "returnsAccepted":["false" ],
              "viewItemURL":["http://www.ebay.com/itm/SIMPSON-360-2-RUNII-DIGITAL-OHM-VOLT-METER-12286-/253303813311" ],
              "sellingStatus":[
                { "currentPrice":[
                    { "@currencyId": "USD", "__value__": "200.0" } ],
                "timeLeft":["P1DT8H59M46S" ],
                "convertedCurrentPrice":[
                    { "@currencyId": "USD", "__value__": "200.0" } ],
                "bidCount":["0" ],
                "sellingState":["Active" ] } ],
              "paymentMethod":["PayPal" ],
              "primaryCategory":[
                { "categoryId":["58277" ],
                "categoryName":["Multimeters" ] } ],
              "condition":[
                { "conditionId":["3000" ],
                "conditionDisplayName":["Used" ] } ],
              "listingInfo":[
                { "endTime":["2017-12-16T23:18:40.000Z" ],
                "buyItNowPrice":[
                    { "@currencyId": "USD", "__value__": "400.0" } ],
                "gift":["false" ],
                "listingType":["AuctionWithBIN" ],
                "convertedBuyItNowPrice":[
                    { "@currencyId": "USD", "__value__": "400.0" } ],
                "bestOfferEnabled":["false" ],
                "startTime":["2017-12-09T23:18:40.000Z" ],
                "buyItNowAvailable":["true" ] } ]

            },{"itemId":["253295991282" ],
              "isMultiVariationListing":["false" ],
              "topRatedListing":["false" ],
              "globalId":["EBAY-US" ],
              "title":["Simpson 360 Multimeter" ],
              "country":["US" ],
              "shippingInfo":[
                { "expeditedShipping":["false" ],
                "handlingTime":["2" ],
                "shippingServiceCost":[
                    { "@currencyId": "USD", "__value__": "10.0" } ],
                "oneDayShippingAvailable":["false" ],
                "shipToLocations":["Worldwide" ],
                "shippingType":["Flat" ] } ],
              "galleryURL":["http://thumbs3.ebaystatic.com/m/mDzuc_hBdbr66ce2oqz2yxA/140.jpg" ],
              "autoPay":["false" ],
              "location":["Piedmont,SC,USA" ],
              "postalCode":["29673" ],
              "returnsAccepted":["false" ],
              "viewItemURL":["http://www.ebay.com/itm/Simpson-360-Multimeter-/253295991282" ],
              "sellingStatus":[
                { "currentPrice":[
                    { "@currencyId": "USD", "__value__": "39.0" } ],
                "timeLeft":["P19DT23H42M8S" ],
                "convertedCurrentPrice":[
                    { "@currencyId": "USD", "__value__": "39.0" } ],
                "sellingState":["Active" ] } ],
              "paymentMethod":["PayPal" ],
              "primaryCategory":[
                { "categoryId":["58277" ],
                "categoryName":["Multimeters" ] } ],
              "condition":[
                { "conditionId":["7000" ],
                "conditionDisplayName":["For parts or not working" ] } ],
              "listingInfo":[
                { "listingType":["StoreInventory" ],
                "gift":["false" ],
                "bestOfferEnabled":["false" ],
                "startTime":["2017-12-05T14:01:02.000Z" ],
                "buyItNowAvailable":["false" ],
                "endTime":["2018-01-04T14:01:02.000Z" ] } ] } ],
          "@count": "4" }
      ],
      "version":["1.13.0" ] } ]
}'''

sResponseSearchTooBroad = \
'''{"findItemsByKeywordsResponse":
  [{"ack":["Success"],"version":["1.13.0"],"timestamp":["2018-03-03T23:04:24.581Z"],
    "searchResult":
      [{"@count":"100",
        "item":
          [ { "itemId":["122990519283"],
              "title":["Garol 6AU-1 Catalin Radio "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mqcfM87dPUKfbuWlIpUTi-w\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Garol-6AU-1-Catalin-Radio-\/122990519283"],
              "paymentMethod":["PayPal"],
              "autoPay":["false"],
              "postalCode":["15085"],
              "location":["Trafford,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"563.88"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"563.88"}],"bidCount":["14"],"sellingState":["Active"],"timeLeft":["P0DT3H38M14S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-27T02:42:38.000Z"],"endTime":["2018-03-04T02:42:38.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["44"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],
              "topRatedListing":["true"]

           },{"itemId":["253486571279"],
              "title":["Vintage The Fisher XP-55B Speaker System-Pair"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/ml2_sva9LX3ZuyvXvbKCCDQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Fisher-XP-55B-Speaker-System-Pair-\/253486571279"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["95963"],
              "location":["Orland,CA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"70.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"70.0"}],"sellingState":["Active"],"timeLeft":["P3DT12H18M53S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-03-13T01:48:50.000Z"],"endTime":["2018-04-12T01:48:50.000Z"],"listingType":["FixedPrice"],"gift":["false"]}],
              "returnsAccepted":["true"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["372238175241"],
              "title":["VINTAGE 1940s FADA CATALIN BAKELITE RADIO MODEL 1000 CABINET  !!"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/m5xVHnOJXutmBzyPEQBRqLA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-1940s-FADA-CATALIN-BAKELITE-RADIO-MODEL-1000-CABINET-\/372238175241"],
              "paymentMethod":["PayPal"],
              "autoPay":["true"],
              "postalCode":["08831"],
              "location":["Monroe Township,NJ,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["CalculatedDomesticFlatInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"95.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"95.0"}],"sellingState":["Active"],"timeLeft":["P6DT12H41M45S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T11:46:09.000Z"],"endTime":["2018-03-10T11:46:09.000Z"],"listingType":["StoreInventory"],"gift":["false"],"watchCount":["3"]}],
              "returnsAccepted":["false"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["132511862199"],
              "title":["VINTAGE BEAUTIFUL 40s FADA BULLET ART DECO CATALIN BAKELITE ANTIQUE TUBE RADIO "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50595"],"categoryName":["Vintage Radios"]}],
              "secondaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mPZ1LL6TxMOm1JbAk3Gspeg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-BEAUTIFUL-40s-FADA-BULLET-ART-DECO-CATALIN-BAKELITE-ANTIQUE-TUBE-RADIO-\/132511862199"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["08831"],
              "location":["Monroe Township,NJ,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["CalculatedDomesticFlatInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"580.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"580.0"}],"bidCount":["32"],"sellingState":["Active"],"timeLeft":["P0DT3H28M21S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-25T02:32:45.000Z"],"endTime":["2018-03-04T02:32:45.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["83"]}],
              "returnsAccepted":["true"],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

           },{"itemId":["202246769108"],
              "title":["Vtg Red Bakelite\/Catalin Carved Clear\/Black Plastic 2 Umbrella\/Parasol 3 Handles"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "secondaryCategory":[{"categoryId":["182063"],"categoryName":["Umbrellas & Parasols"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mSo7ljD5e-bAvQfxbqB79rg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vtg-Red-Bakelite-Catalin-Carved-Clear-Black-Plastic-2-Umbrella-Parasol-3-Handles-\/202246769108"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["68107"],
              "location":["Omaha,NE,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"19.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"19.99"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P9DT3H48M22S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T02:52:46.000Z"],"endTime":["2018-03-13T02:52:46.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["5"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["132523993393"],
              "title":["Vintage Bakelite\/Catalin Poker Chip & Card Holder~Marbled Butterscotch w\/chips "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mBGE-FHpU8EMf3a8kT9VWaw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Bakelite-Catalin-Poker-Chip-Card-Holder-Marbled-Butterscotch-w-chips-\/132523993393"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["15905"],
              "location":["Johnstown,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"32.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"32.0"}],"bidCount":["3"],"sellingState":["Active"],"timeLeft":["P5DT15H11M15S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T14:15:39.000Z"],"endTime":["2018-03-09T14:15:39.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["5"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

           },{"itemId":["122987310830"],
              "title":["Catalin \/ Bakelite Dominoes. VINTAGE with a Leather Case."],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/meYXAUCeDwFQ6LpoAWvYTPg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Catalin-Bakelite-Dominoes-VINTAGE-Leather-Case-\/122987310830"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["33707"],
              "location":["Saint Petersburg,FL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"6.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"40.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"40.0"}],"sellingState":["Active"],"timeLeft":["P3DT19H30M53S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-02-25T18:35:17.000Z"],"endTime":["2018-03-07T18:35:17.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["282867250157"],
              "title":["Rare Morse Chain co Poole clock Bakelite Catalin Synchronous 1928-29 Deco"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mVMZA0bK2CFyAjJoZhsZdGQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Rare-Morse-Chain-co-Poole-clock-Bakelite-Catalin-Synchronous-1928-29-Deco-\/282867250157"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["20611"],
              "location":["Bel Alton,MD,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"135.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"135.0"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P8DT1H55M46S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"235.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"235.0"}],"startTime":["2018-03-02T01:00:10.000Z"],"endTime":["2018-03-12T01:00:10.000Z"],"listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["9"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["292466597766"],
              "title":["Original CATALIN rod. LARGE. Some call it Bakelite. Burgundy beauty. #787"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/md8dlXbAwFZwGG2nDiABxnQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Original-CATALIN-rod-LARGE-Some-call-Bakelite-Burgundy-beauty-787-\/292466597766"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["10312"],"location":["Staten Island,NY,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"9.95"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"59.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"59.0"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P3DT22H55M37S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-28T22:00:01.000Z"],"endTime":["2018-03-07T22:00:01.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["1000"],"conditionDisplayName":["New"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["112846965430"],
              "title":["Addison 5 Catalin Radio Green Dial Glass Exact Reproduction"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mdTGWm8lbpEXJ09YUPl0aLQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Addison-5-Catalin-Radio-Green-Dial-Glass-Exact-Reproduction-\/112846965430"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["30327"],
              "location":["Atlanta,GA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"3.75"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"30.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"30.0"}],"sellingState":["Active"],"timeLeft":["P29DT4H59M41S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T04:04:05.000Z"],"endTime":["2018-04-02T04:04:05.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/112846965430_1_0_1.jpg"],
              "condition":[{"conditionId":["1000"],"conditionDisplayName":["New"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["202235032315"],
              "title":["Beautiful Emerson Model 520 Catalin radio"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/m3i0-t6HKEL8LuTJJhtdRQg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Beautiful-Emerson-Model-520-Catalin-radio-\/202235032315"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["23005"],
              "location":["Ashland,VA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"30.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["5"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"129.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"129.99"}],"sellingState":["Active"],"timeLeft":["P18DT19H30M28S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-20T18:34:52.000Z"],"endTime":["2018-03-22T18:34:52.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["19"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["273089837651"],
              "title":["Catalin bakelite Poker Chips Set-Yellow Butterscotch 402grams 100 chips in box"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mOnnyO5gcdV-A946015hlcg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Catalin-bakelite-Poker-Chips-Set-Yellow-Butterscotch-402grams-100-chips-box-\/273089837651"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["21623"],
              "location":["Church Hill,MD,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"58.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"58.99"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P4DT3H25M23S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"110.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"110.0"}],"startTime":["2018-03-01T02:30:46.000Z"],"endTime":["2018-03-08T02:29:47.000Z"],"listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["2"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["132521748790"],
              "title":["DeWALD Catalin Harp Model A-501 Radio"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/m65tKyv2ZxnOuI0WLUuyyAg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/DeWALD-Catalin-Harp-Model-A-501-Radio-\/132521748790"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["28270"],
              "location":["Charlotte,NC,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"200.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"200.0"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P3DT21H55M0S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"325.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"325.0"}],"startTime":["2018-02-28T20:59:24.000Z"],"endTime":["2018-03-07T20:59:24.000Z"],"listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["20"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["253420370365"],
              "title":["VTG ANTIQUE ART DECO BAKELITE CATALIN LUCITE JEWELRY BOX TRINKET CIGARETTE"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mpOGAG4bEbP-o1zD-jIpgyw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VTG-ANTIQUE-ART-DECO-BAKELITE-CATALIN-LUCITE-JEWELRY-BOX-TRINKET-CIGARETTE-\/253420370365"],
              "paymentMethod":["CashOnPickup","PayPal"],"autoPay":["false"],
              "postalCode":["95820"],
              "location":["Sacramento,CA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"19.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"19.95"}],"sellingState":["Active"],"timeLeft":["P8DT20H7M2S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-10T19:11:26.000Z"],"endTime":["2018-03-12T19:11:26.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["5"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["332542605606"],
              "title":["Small Green Swirl Catalin or Bakelite Refrigerator Magnet. Quality Made."],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mdyVIlfXg_OsHokZ_UDu-8Q\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Small-Green-Swirl-Catalin-Bakelite-Refrigerator-Magnet-Quality-Made-\/332542605606"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["33408"],
              "location":["North Palm Beach,FL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"6.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"6.0"}],"sellingState":["Active"],"timeLeft":["P4DT1H56M12S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-06T01:00:36.000Z"],"endTime":["2018-03-08T01:00:36.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["2"]}],
              "returnsAccepted":["false"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/332542605606_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["382396316470"],
              "title":["VINTAGE CATALIN  ALPHABET LETTERS --67 TOTAL"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mthIl6RzIvR6RdUJhlknh-g\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-CATALIN-ALPHABET-LETTERS-67-TOTAL-\/382396316470"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["60013"],
              "location":["Cary,IL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"4.85"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"14.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"14.95"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P4DT21H35M21S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-01T20:39:45.000Z"],"endTime":["2018-03-08T20:39:45.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183104744162"],
              "title":["Antique Vintage Old Amber Bakelite Catalin Yellow Dice Beads Faturan Block 2824g"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mN9rBMlZsqip2FFB0D4CCWQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Vintage-Old-Amber-Bakelite-Catalin-Yellow-Dice-Beads-Faturan-Block-2824g-\/183104744162"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44339"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"28.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P5DT20H31M48S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T19:36:12.000Z"],"endTime":["2018-03-09T19:36:12.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["2"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["332551135853"],
              "title":["Quality-Made Business Calling Card Holder. Catalin or Bakelite.  Art Deco Style."],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mthtZzlp_3EPke7eWYoccBg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Quality-Made-Business-Calling-Card-Holder-Catalin-Bakelite-Art-Deco-Style-\/332551135853"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["33408"],
              "location":["North Palm Beach,FL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"4.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"42.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"42.0"}],"sellingState":["Active"],"timeLeft":["P10DT2H11M12S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-12T01:15:36.000Z"],"endTime":["2018-03-14T01:15:36.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["10"]}],
              "returnsAccepted":["false"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/332551135853_1_0_1.jpg"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["142699330480"],
              "title":["VINTAGE BAKELITE\/CATALIN FOLDING CRIBBAGE BOARD W\/PEGS,ICE TEA COLOR,1940'S"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mg70-M7jDYhfhz6VIH7oN_g\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-BAKELITE-CATALIN-FOLDING-CRIBBAGE-BOARD-W-PEGS-ICE-TEA-COLOR-1940S-\/142699330480"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["97062"],
              "location":["Tualatin,OR,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"44.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"44.95"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P1DT4H23M32S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-23T03:27:56.000Z"],"endTime":["2018-03-05T03:27:56.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["2"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["372236489965"],
              "title":[" VINTAGE NOS PAIR 1 1\/8\\\" CHERRY AMBER CATALIN OR BAKELITE DICE IOB 76.6 G TW "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "secondaryCategory":[{"categoryId":["7317"],"categoryName":["Game Pieces, Parts"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mYa1T_m7Wt678hFF6dRJgRQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-NOS-PAIR-1-1-8-CHERRY-AMBER-CATALIN-BAKELITE-DICE-IOB-76-6-G-TW-\/372236489965"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["08107"],
              "location":["Oaklyn,NJ,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"3.99"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"39.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"39.99"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P4DT19H43M0S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-01T18:47:24.000Z"],"endTime":["2018-03-08T18:47:24.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["253446988728"],
              "title":["Vintage EXCELLENT Galloping Golf Bakelite Catalin Dice Game In Leather Case"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mERcjgL3jEHHcD99-MwHJwg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-EXCELLENT-Galloping-Golf-Bakelite-Catalin-Dice-Game-Leather-Case-\/253446988728"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["85750"],
              "location":["Tucson,AZ,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"4.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"15.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"15.0"}],"sellingState":["Active"],"timeLeft":["P21DT19H16M26S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-23T18:20:50.000Z"],"endTime":["2018-03-25T18:20:50.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["3"]}],
              "returnsAccepted":["true"],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["332557814246"],
              "title":["Business Calling Card Holder. Catalin or Bakelite. Quality Made. Art Deco Style."],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mOL_OPjDb1isSQS7AF6a5xg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Business-Calling-Card-Holder-Catalin-Bakelite-Quality-Made-Art-Deco-Style-\/332557814246"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["33408"],
              "location":["North Palm Beach,FL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"3.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"38.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"38.0"}],"sellingState":["Active"],"timeLeft":["P17DT2H13M36S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-19T01:18:00.000Z"],"endTime":["2018-03-21T01:18:00.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["7"]}],
              "returnsAccepted":["false"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/332557814246_1_0_1.jpg"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183104670611"],
              "title":["Antique Vintage Old Amber Bakelite Catalin Yellow White Dice Beads Faturan Block"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mRXMyRQCrTfNVHoGFkZQYjQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Vintage-Old-Amber-Bakelite-Catalin-Yellow-White-Dice-Beads-Faturan-Block-\/183104670611"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44339"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"18.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"10.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"10.5"}],"bidCount":["2"],"sellingState":["Active"],"timeLeft":["P5DT19H58M43S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T19:03:07.000Z"],"endTime":["2018-03-09T19:03:07.000Z"],"listingType":["Auction" ],"gift":["false"],"watchCount":["3"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183100580502"],
              "title":["Authentic Old Vintage German Bakelite Catalin Rods Blocks Rare Veined 590g"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["165690"],"categoryName":["Prayer Beads"]}],
              "secondaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/m15Cd9vSZryZwLNqrxVzpog\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Authentic-Old-Vintage-German-Bakelite-Catalin-Rods-Blocks-Rare-Veined-590g-\/183100580502"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "location":["Lithuania"],
              "country":["LT"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"12.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.0"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P3DT19H21M41S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-28T18:26:05.000Z"],"endTime":["2018-03-07T18:26:05.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["16"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/183100580502_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183100583400"],
              "title":["Authentic Old Vintage German Bakelite Catalin Rods Blocks Rare Veined 482g"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["165690"],"categoryName":["Prayer Beads"]}],
              "secondaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/m7PHAP4538SJQE7cM0LlRvg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Authentic-Old-Vintage-German-Bakelite-Catalin-Rods-Blocks-Rare-Veined-482g-\/183100583400"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "location":["Lithuania"],
              "country":["LT"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"12.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"22.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"22.5"}],"bidCount":["12"],"sellingState":["Active"],"timeLeft":["P3DT19H26M3S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-28T18:30:27.000Z"],"endTime":["2018-03-07T18:30:27.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["17"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/183100583400_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["232678777465"],
              "title":["Vintage Butterscotch Bakelite\/Catalin Bird Napkin Ring 1930s"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mS5ucqB9CEyOfUWdxjJV62Q\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Butterscotch-Bakelite-Catalin-Bird-Napkin-Ring-1930s-\/232678777465"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["98382"],
              "location":["Sequim,WA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"14.22"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"14.22"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P0DT23H16M44S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-25T22:21:08.000Z"],"endTime":["2018-03-04T22:21:08.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["4"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["391992779536"],
              "title":["3 Art Deco Green Butterscotch Amber Bakelite Catalin Phenolic Handle"],
              "globalId":["EBAY-GB"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/m54kOJCw0MjS4NHG8V71VvQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/3-Art-Deco-Green-Butterscotch-Amber-Bakelite-Catalin-Phenolic-Handle-\/391992779536"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "location":["United Kingdom"],
              "country":["GB"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["10"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"GBP","__value__":"450.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"619.7"}],"sellingState":["Active"],"timeLeft":["P6DT14H1M9S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T13:05:33.000Z"],"endTime":["2018-03-10T13:05:33.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["9"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["112848108338"],
              "title":["Vintage Bakelite Red Catalin Androck Strainer 12\\" USA Stainless Steel Wire Mesh"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/myUfIOwm6qtvocJxVR2Mctw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Bakelite-Red-Catalin-Androck-Strainer-12-USA-Stainless-Steel-Wire-Mesh-\/112848108338"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44067"],
              "location":["Northfield,OH,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"19.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"19.99"}],"sellingState":["Active"],"timeLeft":["P29DT20H45M29S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T19:49:53.000Z"],"endTime":["2018-04-02T19:49:53.000Z"],"listingType":["StoreInventory"],"gift":["false"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/112848108338_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["323093306380"],
              "title":["CATALIN BAKELITE  LOT OF 34 PIECES   Deco Caps KNOBS 1 3\/4 inches "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mkb_x82_Nn8ctoG4DOy5CbQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/CATALIN-BAKELITE-LOT-34-PIECES-Deco-Caps-KNOBS-1-3-4-inches-\/323093306380"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["01040"],
              "location":["Holyoke,MA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"149.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"149.99"}],"sellingState":["Active"],"timeLeft":["P20DT17H38M15S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-22T16:42:39.000Z"],"endTime":["2018-03-24T16:42:39.000Z"],"listingType":["StoreInventory"],"gift":["false"],"watchCount":["4"]}],
              "returnsAccepted":["false"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183104681993"],
              "title":["Antique Vintage Old Amber Bakelite Catalin Yellow Dice Beads Faturan Block 363gr"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mIpklA-xj7p5Xbm-MUo7shg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Vintage-Old-Amber-Bakelite-Catalin-Yellow-Dice-Beads-Faturan-Block-363gr-\/183104681993"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44339"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"18.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P5DT20H0M46S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T19:05:10.000Z"],"endTime":["2018-03-09T19:05:10.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["222862364643"],
              "title":["LOT OF 30 MARBLEIZED AMBER BAKELITE\/CATALIN BACKGAMMON PIECES. 4 SIZES 260 GRAMS"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/m1GQswUZhuv2-Od5oXn617A\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/LOT-30-MARBLEIZED-AMBER-BAKELITE-CATALIN-BACKGAMMON-PIECES-4-SIZES-260-GRAMS-\/222862364643"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["M1J2Z6"],
              "location":["Canada"],
              "country":["CA"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"19.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["5"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"49.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"49.95"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P4DT18H57M18S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"69.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"69.0"}],"startTime":["2018-03-01T18:01:42.000Z"],"endTime":["2018-03-08T18:01:42.000Z"],"listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["2"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["183100574760"],
              "title":["Authentic Old Vintage German Bakelite Catalin Rods Blocks Rare Veined 480g"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["165690"],"categoryName":["Prayer Beads"]}],
              "secondaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mAn6Qdvqsj5eeUr0NQpym2w\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Authentic-Old-Vintage-German-Bakelite-Catalin-Rods-Blocks-Rare-Veined-480g-\/183100574760"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "location":["Lithuania"],
              "country":["LT"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"12.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"10.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"10.5"}],"bidCount":["4"],"sellingState":["Active"],"timeLeft":["P3DT19H18M27S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-28T18:22:51.000Z"],"endTime":["2018-03-07T18:22:51.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["16"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/183100574760_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183100578429"],
              "title":["Authentic Old Vintage German Bakelite Catalin Rods Blocks Rare Veined 468g"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["165690"],"categoryName":["Prayer Beads"]}],
              "secondaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/m0wRRzFOev8yR1m-48ekNCA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Authentic-Old-Vintage-German-Bakelite-Catalin-Rods-Blocks-Rare-Veined-468g-\/183100578429"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "location":["Lithuania"],
              "country":["LT"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"12.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.5"}],"bidCount":["2"],"sellingState":["Active"],"timeLeft":["P3DT19H19M49S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-28T18:24:13.000Z"],"endTime":["2018-03-07T18:24:13.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["17"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/183100578429_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["273074865833"],
              "title":["bakelite catalin art deco"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mG7Ux1i4YMCHh8CcRU0USTQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/bakelite-catalin-art-deco-\/273074865833"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "location":["Slovakia"],
              "country":["SK"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"8.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"26.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"26.0"}],"sellingState":["Active"],"timeLeft":["P16DT16H3M56S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-18T15:08:20.000Z"],"endTime":["2018-03-20T15:08:20.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["19"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/273074865833_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["273047508323"],
              "title":["4 CATALIN FURNITURE HANDLES VINTAGE ART DECO BAKELITE AMBER 63 Grams 2.75\\" & 4\\""],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mihXCQI3W3KWbL39Pb_6d3A\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/4-CATALIN-FURNITURE-HANDLES-VINTAGE-ART-DECO-BAKELITE-AMBER-63-Grams-2-75-4-\/273047508323"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["17112"],
              "location":["Harrisburg,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"5.5"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"55.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"55.0"}],"sellingState":["Active"],"timeLeft":["P27DT14H0M46S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-01-30T13:05:10.000Z"],"endTime":["2018-03-31T13:05:10.000Z"],"listingType":["StoreInventory"],"gift":["false"],"watchCount":["5"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["362252683340"],
              "title":["VINTAGE MAHJONG SET - APPLE JUICE CATALIN RESIN - UNUSED - NRMINT 1930'S"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["19100"],"categoryName":["Vintage Manufacture"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mTpC84fCXcINn1p74rmtN8w\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-MAHJONG-SET-APPLE-JUICE-CATALIN-RESIN-UNUSED-NRMINT-1930S-\/362252683340"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["94070"],
              "location":["San Carlos,CA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"22.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"33.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"33.0"}],"bidCount":["21"],"sellingState":["Active"],"timeLeft":["P1DT3H16M3S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-26T02:20:27.000Z"],"endTime":["2018-03-05T02:20:27.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["27"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183100582130"],
              "title":["Authentic Old Vintage German Bakelite Catalin Rods Blocks Rare Veined 384g"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["165690"],"categoryName":["Prayer Beads"]}],
              "secondaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mEzqYIk3Y3j2x-pT3TLd0iw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Authentic-Old-Vintage-German-Bakelite-Catalin-Rods-Blocks-Rare-Veined-384g-\/183100582130"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "location":["Lithuania"],
              "country":["LT"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"12.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"11.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"11.5"}],"bidCount":["4"],"sellingState":["Active"],"timeLeft":["P3DT19H23M50S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-28T18:28:14.000Z"],"endTime":["2018-03-07T18:28:14.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["16"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/183100582130_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["183104747518"],
              "title":["Antique Vintage Old Amber Bakelite Catalin Orange Dice Beads Block 2815gr"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mwHf-Wd7L-9bJCAvabUOujg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Vintage-Old-Amber-Bakelite-Catalin-Orange-Dice-Beads-Block-2815gr-\/183104747518"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44339"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"28.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P5DT20H35M48S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T19:40:12.000Z"],"endTime":["2018-03-09T19:40:12.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183104699744"],
              "title":["Antique Vintage Old Amber Bakelite Catalin Black Cherry Dice Beads Faturan Block"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mrndNwJLBWlWAE13-OhnH2A\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Vintage-Old-Amber-Bakelite-Catalin-Black-Cherry-Dice-Beads-Faturan-Block-\/183104699744"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44339"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"28.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"27.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"27.0"}],"bidCount":["10"],"sellingState":["Active"],"timeLeft":["P5DT20H18M40S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T19:23:04.000Z"],"endTime":["2018-03-09T19:23:04.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["15"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183104746092"],
              "title":["Antique Vintage Old Amber Bakelite Catalin Turquoise Dice Beads Faturan Block"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/muj0isSQsHCrSL8gk8nmZkQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Vintage-Old-Amber-Bakelite-Catalin-Turquoise-Dice-Beads-Faturan-Block-\/183104746092"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44339"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"28.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P5DT20H33M47S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T19:38:11.000Z"],"endTime":["2018-03-09T19:38:11.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["282864936201"],
              "title":["Large bakelite skull catalin swirled colors end of day rat rod hot rod"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mjcWAnPdMdP178oXhMhO74A\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Large-bakelite-skull-catalin-swirled-colors-end-day-rat-rod-hot-rod-\/282864936201"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["98424"],
              "location":["Tacoma,WA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"400.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"400.0"}],"sellingState":["Active"],"timeLeft":["P1DT4H42M9S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-02-28T03:46:33.000Z"],"endTime":["2018-03-05T03:46:33.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["192452462001"],
              "title":["NEW SEALED CARDINAL GLEAMING CATALIN DOMINOES GAME SET VINTAGE 28 DOMINOS"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mR0a-TKez340j9T-Xwwtd5w\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/NEW-SEALED-CARDINAL-GLEAMING-CATALIN-DOMINOES-GAME-SET-VINTAGE-28-DOMINOS-\/192452462001"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["92557"],
              "location":["Moreno Valley,CA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"27.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"27.99"}],"sellingState":["Active"],"timeLeft":["P8DT12H7M44S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-02-10T11:12:08.000Z"],"endTime":["2018-03-12T11:12:08.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/192452462001_1_0_1.jpg"],
              "condition":[{"conditionId":["1000"],"conditionDisplayName":["New"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["192470136271"],
              "title":["Box Full 1940s BAKELITE Catalin Poker Chips 50 Butterscotch 25 Red 25 Green NICE"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mW5xeXdvRiHTqGDLo-D1IuA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Box-Full-1940s-BAKELITE-Catalin-Poker-Chips-50-Butterscotch-25-Red-25-Green-NICE-\/192470136271"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["94114"],
              "location":["San Francisco,CA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"140.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"140.0"}],"sellingState":["Active"],"timeLeft":["P27DT11H47M34S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-03-01T10:51:58.000Z"],"endTime":["2018-03-31T10:51:58.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["282867825374"],
              "title":["Old Vintage CHERRY Amber Bakelite Catalin marbled rod block faturan 48g"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mfyzM6WZJd-O8j0z-E5K2Jg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Old-Vintage-CHERRY-Amber-Bakelite-Catalin-marbled-rod-block-faturan-48g-\/282867825374"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["97228"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"22.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["10"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"499.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"499.0"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P5DT13H29M15S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T12:33:39.000Z"],"endTime":["2018-03-09T12:33:39.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["2"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["362258497448"],
              "title":["VTG RETRO GENERAL ELECTRIC GE L-512 TUBE RADIO CATALIN HANDLE BAKELITE SHELL"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mxJuUnigGb_O4vqkhWcKcUg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VTG-RETRO-GENERAL-ELECTRIC-GE-L-512-TUBE-RADIO-CATALIN-HANDLE-BAKELITE-SHELL-\/362258497448"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["46304"],
              "location":["Chesterton,IN,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["5"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"24.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"24.99"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P6DT20H57M51S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T20:02:15.000Z"],"endTime":["2018-03-10T20:02:15.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["282864937449"],
              "title":["Large bakelite skull catalin swirled colors end of day rat rod hot rod"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mzkZ7BQ1sEd2J1kvKf4aRMQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Large-bakelite-skull-catalin-swirled-colors-end-day-rat-rod-hot-rod-\/282864937449"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["98424"],
              "location":["Tacoma,WA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"400.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"400.0"}],"sellingState":["Active"],"timeLeft":["P1DT4H43M6S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-02-28T03:47:30.000Z"],"endTime":["2018-03-05T03:47:30.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["382397798449"],
              "title":["POKER CHIPS SET  LOWE CARD GAME BOX  CATALIN BAKELITE VTG ANTIQUE"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["63760"],"categoryName":["Other Casino Chip Sets"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mFkEDBqh5NjSDQDWyraCOEw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/POKER-CHIPS-SET-LOWE-CARD-GAME-BOX-CATALIN-BAKELITE-VTG-ANTIQUE-\/382397798449"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["16701"],
              "location":["Bradford,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"18.9"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"230.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"230.0"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P9DT2H33M39S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T01:38:03.000Z"],"endTime":["2018-03-13T01:38:03.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["2"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["282858547870"],
              "title":["Emerson radio BA199 Working Bakelite Catalin"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mYxqjZnCuuClZ1lbpIfs0Vw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Emerson-radio-BA199-Working-Bakelite-Catalin-\/282858547870"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["20611"],
              "location":["Bel Alton,MD,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"75.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"75.0"}],"bidCount":["6"],"sellingState":["Active"],"timeLeft":["P1DT1H56M18S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"175.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"175.0"}],"startTime":["2018-02-23T01:00:42.000Z"],"endTime":["2018-03-05T01:00:42.000Z"],"listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["16"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["282863028569"],
              "title":["Large Bakelite  catalin Amber Dice "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mC8woYgiYHJwPq03GS-fEDA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Large-Bakelite-catalin-Amber-Dice-\/282863028569"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["86179"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"12.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["10"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"150.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"150.5"}],"bidCount":["31"],"sellingState":["Active"],"timeLeft":["P4DT16H52M22S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-26T15:56:46.000Z"],"endTime":["2018-03-08T15:56:46.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["20"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/282863028569_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["352290963265"],
              "title":["Bakelite Catalin 2.72\\" x 10.25\\" long 865 grams huge rod tube mottled brown USA"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/myEttsCf2lpYvKIcARuc7Fg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Bakelite-Catalin-2-72-x-10-25-long-865-grams-huge-rod-tube-mottled-brown-USA-\/352290963265"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["34788"],
              "location":["Leesburg,FL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["10"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"800.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"800.0"}],"sellingState":["Active"],"timeLeft":["P23DT22H7M39S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-25T21:12:03.000Z"],"endTime":["2018-03-27T21:12:03.000Z"],"listingType":["FixedPrice"],"gift":["false"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["273091141755"],
              "title":["4 \u201cRDC\u201d BAKELITE CATALIN MINT MAH JONGG MAHJONGG TILES Your Pick"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["19100"],"categoryName":["Vintage Manufacture"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mPf0L5HgJTzX8QiUfOfjB2A\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/4-RDC-BAKELITE-CATALIN-MINT-MAH-JONGG-MAHJONGG-TILES-Your-Pick-\/273091141755"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["11234"],
              "location":["Brooklyn,NY,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"19.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"19.0"}],"sellingState":["Active"],"timeLeft":["P27DT22H40M42S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-01T21:45:06.000Z"],"endTime":["2018-03-31T21:45:06.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["2"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["273084559811"],
              "title":[" A Rare Art Deco Phenolic Catalin Dressing Table set, trinket boxes on a tray"],
              "globalId":["EBAY-GB"],
              "primaryCategory":[{"categoryId":["69471"],"categoryName":["Art Deco"]}],
              "secondaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mTeIBK8JEa0mvz0bfrQrq0g\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Rare-Art-Deco-Phenolic-Catalin-Dressing-Table-set-trinket-boxes-tray-\/273084559811"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "location":["United Kingdom"],
              "country":["GB"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"26.85"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"GBP","__value__":"249.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"344.26"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P0DT14H29M0S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-25T13:33:24.000Z"],"endTime":["2018-03-04T13:33:24.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["16"]}],
              "returnsAccepted":["true"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183104724243"],
              "title":["Antique Vintage Old Amber Bakelite Catalin Blue Dice Beads Faturan Block 2541g"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mRrHEHfIueSKAtlIK0WrHJQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Vintage-Old-Amber-Bakelite-Catalin-Blue-Dice-Beads-Faturan-Block-2541g-\/183104724243"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44339"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"28.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"12.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"12.5"}],"bidCount":["3"],"sellingState":["Active"],"timeLeft":["P5DT20H27M45S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T19:32:09.000Z"],"endTime":["2018-03-09T19:32:09.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183104668667"],
              "title":["Antique Vintage Old Amber Bakelite Catalin Red Cherry Dice Beads Faturan Block"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mhZF_lP8fJ1Hu2TphDNPMZQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Vintage-Old-Amber-Bakelite-Catalin-Red-Cherry-Dice-Beads-Faturan-Block-\/183104668667"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44339"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"18.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P5DT19H57M18S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T19:01:42.000Z"],"endTime":["2018-03-09T19:01:42.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183104696572"],
              "title":["Antique Vintage Old Amber Bakelite Catalin Red Cherry Dice Beads Faturan Block"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mrhtOQdsdgy392WWMzK8UiQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Vintage-Old-Amber-Bakelite-Catalin-Red-Cherry-Dice-Beads-Faturan-Block-\/183104696572"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44339"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"28.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P5DT20H14M41S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T19:19:05.000Z"],"endTime":["2018-03-09T19:19:05.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["332552628112"],
              "title":["Bakelite Catalin rod 1.12\\" by 9-1\/4\\" apple juice 190 gr Katalin USA"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/m0V-IS8UP9sd1qMNwnkjmWg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Bakelite-Catalin-rod-1-12-9-1-4-apple-juice-190-gr-Katalin-USA-\/332552628112"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["34788"],
              "location":["Leesburg,FL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["10"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"190.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"190.0"}],"sellingState":["Active"],"timeLeft":["P10DT17H45M15S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-12T16:49:39.000Z"],"endTime":["2018-03-14T16:49:39.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["5"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["323112905602"],
              "title":["Wurlitzer 850 850A Jukebox Original Catalin Pilaster Plastic Set"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["13723"],"categoryName":["Replacement Parts"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/menpeOpkirTdiQSJhuCl7Wg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Wurlitzer-850-850A-Jukebox-Original-Catalin-Pilaster-Plastic-Set-\/323112905602"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["30327"],
              "location":["Atlanta,GA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"155.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"155.0"}],"sellingState":["Active"],"timeLeft":["P29DT15H27M48S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T14:32:12.000Z"],"endTime":["2018-04-02T14:32:12.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/323112905602_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["332572082444"],
              "title":["Mid Century Bakelite Catalin Red Rabbit Napkin Holder Yellow Apple Juice Eyes"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mX5MgmB4EamzbcM2yAigDyA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Mid-Century-Bakelite-Catalin-Red-Rabbit-Napkin-Holder-Yellow-Apple-Juice-Eyes-\/332572082444"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["76458"],
              "location":["Jacksboro,TX,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"24.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"24.95"}],"sellingState":["Active"],"timeLeft":["P27DT20H47M58S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-01T19:52:22.000Z"],"endTime":["2018-03-31T19:52:22.000Z"],"listingType":["StoreInventory"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/332572082444_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["332566887402"],
              "title":["Bakelite Catalin Child's bracelet tube in marbelized green 373 grams USA"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mI5QHxqz-DhmJTBHGuTUbzg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Bakelite-Catalin-Childs-bracelet-tube-marbelized-green-373-grams-USA-\/332566887402"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["34788"],
              "location":["Leesburg,FL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["10"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"550.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"550.0"}],"sellingState":["Active"],"timeLeft":["P23DT2H55M24S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-02-25T01:59:48.000Z"],"endTime":["2018-03-27T01:59:48.000Z"],"listingType":["FixedPrice"],"gift":["false"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["252785840595"],
              "title":["Set 10 Art Deco Carved Catalin Or Bakelite Place Card Holder Austria Enamel Gilt"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mPvEGa9Mv9DYVlYORKYNxvQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Set-10-Art-Deco-Carved-Catalin-Bakelite-Place-Card-Holder-Austria-Enamel-Gilt-\/252785840595"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["55109"],
              "location":["Saint Paul,MN,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FlatDomesticCalculatedInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"799.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"799.95"}],"sellingState":["Active"],"timeLeft":["P17DT20H4M4S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2017-02-24T19:08:28.000Z"],"endTime":["2018-03-21T19:08:28.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["11"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/252785840595_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["332546961703"],
              "title":["Bakelite Catalin rod 1-1\/2\\" x 6-3\/4\\" polished Prystal green 294 gr USA vintage"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mqN1kOUA1FQaZBjARFV_Q0Q\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Bakelite-Catalin-rod-1-1-2-x-6-3-4-polished-Prystal-green-294-gr-USA-vintage-\/332546961703"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["34788"],
              "location":["Leesburg,FL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["10"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"350.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"350.0"}],"sellingState":["Active"],"timeLeft":["P5DT13H1M25S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-02-07T12:05:49.000Z"],"endTime":["2018-03-09T12:05:49.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["4"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["112847922741"],
              "title":["LARGE VTG SOLID BAKELITE CATALIN PHENOLIC KNOB HANDLE GRIP PULL FINIAL POMMEL"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mK5PmMMeub5Uy-wmLFJEqcg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/LARGE-VTG-SOLID-BAKELITE-CATALIN-PHENOLIC-KNOB-HANDLE-GRIP-PULL-FINIAL-POMMEL-\/112847922741"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["90068"],
              "location":["Los Angeles,CA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"4.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"19.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"19.99"}],"sellingState":["Active"],"timeLeft":["P6DT18H21M51S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T17:26:15.000Z"],"endTime":["2018-03-10T17:26:15.000Z"],"listingType":["FixedPrice"],"gift":["false"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["122979796906"],
              "title":["Addison 5, Radio, Catalin, Parts, 45 ounces, Jewelry"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/m5HCfm08gA6XGvSAM12GzQw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Addison-5-Radio-Catalin-Parts-45-ounces-Jewelry-\/122979796906"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["32137"],
              "location":["Palm Coast,FL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"135.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"135.0"}],"sellingState":["Active"],"timeLeft":["P19DT16H30M14S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-02-21T15:34:38.000Z"],"endTime":["2018-03-23T15:34:38.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["2"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["302653378838"],
              "title":["Vintage Antique Old amber  Bakelite Catalin faturan Ball block rar 2984gr"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mS2U_fQOc12aTYSr0IJpoeQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Antique-Old-amber-Bakelite-Catalin-faturan-Ball-block-rar-2984gr-\/302653378838"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["42242"],
              "location":["Poland"],
              "country":["PL"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"50.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["10"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"250.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"250.0"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P0DT18H27M47S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-27T17:32:11.000Z"],"endTime":["2018-03-04T17:32:11.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["2"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["362253944495"],
              "title":["VINTAGE MAH JONG BAKELITE CATALIN"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["19100"],"categoryName":["Vintage Manufacture"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mbw0BiOI_NzqdclmkqXn83A\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-MAH-JONG-BAKELITE-CATALIN-\/362253944495"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["94070"],
              "location":["San Carlos,CA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"22.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"11.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"11.5"}],"bidCount":["8"],"sellingState":["Active"],"timeLeft":["P2DT5H1M36S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-27T04:06:00.000Z"],"endTime":["2018-03-06T04:06:00.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["13"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["302653367361"],
              "title":["Vintage Antique Old amber  Bakelite Catalin faturan Ball block rar 1130gr"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mR9kbiNX2AkbXECm51XWCAQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Antique-Old-amber-Bakelite-Catalin-faturan-Ball-block-rar-1130gr-\/302653367361"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["42242"],
              "location":["Poland"],
              "country":["PL"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"20.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["10"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"70.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"70.0"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P0DT18H12M10S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-27T17:16:34.000Z"],"endTime":["2018-03-04T17:16:34.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["4"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183104691495"],
              "title":["Antique Vintage Old Amber Bakelite Catalin Green Dice Beads Faturan Block 2672g"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mUeWle5L1U9gmgNhCcKn28g\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Vintage-Old-Amber-Bakelite-Catalin-Green-Dice-Beads-Faturan-Block-2672g-\/183104691495"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44339"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"28.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P5DT20H8M48S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T19:13:12.000Z"],"endTime":["2018-03-09T19:13:12.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183104694661"],
              "title":["Antique Vintage Old Amber Bakelite Catalin Brown Dice Beads Faturan Block 1977g"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mmkRr-C9floHFQrefRzWdKA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Vintage-Old-Amber-Bakelite-Catalin-Brown-Dice-Beads-Faturan-Block-1977g-\/183104694661"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44339"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"28.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P5DT20H12M41S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T19:17:05.000Z"],"endTime":["2018-03-09T19:17:05.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["192470649439"],
              "title":["Catalin or Lucite Ex Original Pair of Knobs"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["7275"],"categoryName":["Parts & Tubes"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mHaZxJPUS5ojaBlbxYS8enA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Catalin-Lucite-Ex-Original-Pair-Knobs-\/192470649439"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["18444"],
              "location":["Moscow,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"4.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"14.75"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"14.75"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P5DT0H0M7S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-01T23:04:31.000Z"],"endTime":["2018-03-08T23:04:31.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],
              "returnsAccepted":["true"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183104698242"],
              "title":["Antique Vintage Old Amber Bakelite Catalin Green Dice Beads Faturan Block 2545g"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mlt5qZNXO2ylxhmbrhcTstw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Vintage-Old-Amber-Bakelite-Catalin-Green-Dice-Beads-Faturan-Block-2545g-\/183104698242"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44339"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"28.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P5DT20H16M46S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T19:21:10.000Z"],"endTime":["2018-03-09T19:21:10.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183104704582"],
              "title":["Antique Vintage Old Amber Bakelite Catalin Brown Dice Beads Faturan Block 2021g"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mkyqeH37xkvSSTvSYwrEp9g\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Vintage-Old-Amber-Bakelite-Catalin-Brown-Dice-Beads-Faturan-Block-2021g-\/183104704582"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44339"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"28.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P5DT20H24M45S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T19:29:09.000Z"],"endTime":["2018-03-09T19:29:09.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["162919176989"],
              "title":["LOOSE BEADS OLD DARK CHERRY OTTOMAN AMBER BAKELITE CATALİN FATURAN BEADS"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["10967"],"categoryName":["Other Art Deco Costume Jewelry"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mdnw7R9m5dodA6cwUMJYiCg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/LOOSE-BEADS-OLD-DARK-CHERRY-OTTOMAN-AMBER-BAKELITE-CATAL-N-FATURAN-BEADS-\/162919176989"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["06473"],
              "location":["North Haven,CT,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"8.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"8.5"}],"bidCount":["5"],"sellingState":["Active"],"timeLeft":["P1DT2H14M48S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-26T01:19:12.000Z"],"endTime":["2018-03-05T01:19:12.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["11"]}],
              "returnsAccepted":["false"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["401354589892"],
              "title":["Emerson \\"Little Miracle\\" Marbled Green White and Yellow Catalin Tube Radio AX235"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "secondaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mfGHQ2d784sxmbjuARC8DwQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Emerson-Little-Miracle-Marbled-Green-White-and-Yellow-Catalin-Tube-Radio-AX235-\/401354589892"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["60010"],
              "location":["Barrington,IL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"2124.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"2124.95"}],"sellingState":["Active"],"timeLeft":["P19DT22H25M21S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2017-06-26T21:29:45.000Z"],"endTime":["2018-03-23T21:29:45.000Z"],"listingType":["StoreInventory"],"gift":["false"],"watchCount":["21"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["122999012619"],
              "title":["gf Bakelite Catalin Reddish-Brown Swirl Poker Chip Holder 4\\" x 5\\""],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/msmUYt-2ae16ABC6cZMjhnQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/gf-Bakelite-Catalin-Reddish-Brown-Swirl-Poker-Chip-Holder-4-x-5-\/122999012619"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["98604"],
              "location":["Battle Ground,WA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"6.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"24.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"24.95"}],"sellingState":["Active"],"timeLeft":["P29DT17H29M15S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T16:33:39.000Z"],"endTime":["2018-04-02T16:33:39.000Z"],"listingType":["StoreInventory"],"gift":["false"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["372045072006"],
              "title":["ANTIQUE ART DECO MARBLED AMBER & BLACK BAKELITE CATALIN DESK DOUBLE STAMP BOX"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mOwKl1fH372TQT8iDkQwyNw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/ANTIQUE-ART-DECO-MARBLED-AMBER-BLACK-BAKELITE-CATALIN-DESK-DOUBLE-STAMP-BOX-\/372045072006"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["32174"],
              "location":["Ormond Beach,FL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"499.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"499.0"}],"sellingState":["Active"],"timeLeft":["P8DT21H43M33S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2017-08-14T20:48:57.000Z"],"endTime":["2018-03-12T20:47:57.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["6"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/372045072006_1_0_1.jpg"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["312074903524"],
              "title":["Catalin Bakelite Ever Ready Shaving Brush Set In Rubber With Zel Catalin Case"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["35988"],"categoryName":["Mugs, Brushes"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mHpwRWtra3iNikiy0kFogOQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Catalin-Bakelite-Ever-Ready-Shaving-Brush-Set-Rubber-Zel-Catalin-Case-\/312074903524"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["55406"],
              "location":["Minneapolis,MN,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"5.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"19.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"19.0"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P0DT0H30M52S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-24T23:35:16.000Z"],"endTime":["2018-03-03T23:35:16.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["8"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["302653369590"],
              "title":["Vintage Antique Old amber  Bakelite Catalin faturan Ball block rar 882gr"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/m-m0LNtoWZ0Gu3bY239HUwg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Antique-Old-amber-Bakelite-Catalin-faturan-Ball-block-rar-882gr-\/302653369590"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["42242"],
              "location":["Poland"],
              "country":["PL"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"20.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["10"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"70.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"70.0"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P0DT18H15M48S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-27T17:20:12.000Z"],"endTime":["2018-03-04T17:20:12.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183084437878"],
              "title":["Antique Cherry Amber Bakelite Swirl Cube Faturan Catalin Cube Square Dice"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mDCpLeReXz6FHfHFZ7uViCg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Antique-Cherry-Amber-Bakelite-Swirl-Cube-Faturan-Catalin-Cube-Square-Dice-\/183084437878"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["06018"],
              "location":["Canaan,CT,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FlatDomesticCalculatedInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"300.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"300.0"}],"sellingState":["Active"],"timeLeft":["P17DT20H23M23S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-19T19:27:47.000Z"],"endTime":["2018-03-21T19:27:47.000Z"],"listingType":["StoreInventory"],"gift":["false"],"watchCount":["7"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["192470100960"],
              "title":["Vintage 1940s Deco BAKELITE Catalin Poker Chip Caddy Butterscoth Amber 200 CHIPS"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/m2tXIEH-Z7yt-pXul0kIInQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-1940s-Deco-BAKELITE-Catalin-Poker-Chip-Caddy-Butterscoth-Amber-200-CHIPS-\/192470100960"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["94114"],
              "location":["San Francisco,CA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"425.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"425.0"}],"sellingState":["Active"],"timeLeft":["P27DT11H0M43S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-03-01T10:05:07.000Z"],"endTime":["2018-03-31T10:05:07.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["192471465856"],
              "title":["Bakelite\/Catalin Real Marblette Poker Chips, 2 Green Dice, Turntable\/Holder-Box"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["63760"],"categoryName":["Other Casino Chip Sets"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/m0nf1as4edaKA80mMI8zt0Q\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Bakelite-Catalin-Real-Marblette-Poker-Chips-2-Green-Dice-Turntable-Holder-Box-\/192471465856"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["45056"],
              "location":["Oxford,OH,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"6.9"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"19.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"19.99"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P5DT22H40M19S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-02T21:44:43.000Z"],"endTime":["2018-03-09T21:44:43.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["11"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["183095562479"],
              "title":["vintage Thorens (?) table lighter with green bakelite\/catalin base"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["595"],"categoryName":["Other Collectible Lighters"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mrORXIcyXro9TSZzx-pygHg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/vintage-Thorens-table-lighter-green-bakelite-catalin-base-\/183095562479"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["78748"],
              "location":["Austin,TX,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"5.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"22.72"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"22.72"}],"bidCount":["9"],"sellingState":["Active"],"timeLeft":["P0DT20H46M33S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-25T19:50:57.000Z"],"endTime":["2018-03-04T19:50:57.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["27"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["142707264033"],
              "title":["Vintage 1933 Champions Basketball Trophy Green Marble Bakelite\/Catalin? Cool !"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50133"],"categoryName":["Other Vintage Sports Mem"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mNHEha7PUQu3r_COeYrzpDA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-1933-Champions-Basketball-Trophy-Green-Marble-Bakelite-Catalin-Cool-\/142707264033"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["54452"],
              "location":["Merrill,WI,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"9.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"14.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"14.99"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P4DT16H53M23S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-01T15:57:47.000Z"],"endTime":["2018-03-08T15:57:47.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["9"]}],
              "returnsAccepted":["true"],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["122964406400"],
              "title":["Motorola S Grill Catalin Radio"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mTDTGrQ9LAAD8SvzqV6RrPA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Motorola-S-Grill-Catalin-Radio-\/122964406400"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["15085"],
              "location":["Trafford,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"2500.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"2500.0"}],"sellingState":["Active"],"timeLeft":["P10DT20H2M42S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-12T19:07:06.000Z"],"endTime":["2018-03-14T19:07:06.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["17"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["202247971131"],
              "title":["20 MISC. VTG ART DECO PULLS BAKELITE CATALIN METAL 1 LOT"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["162933"],"categoryName":["Drawer Pulls"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mrcCu9G2Xh_Wso-Ul7hgfXg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/20-MISC-VTG-ART-DECO-PULLS-BAKELITE-CATALIN-METAL-1-LOT-\/202247971131"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["90068"],
              "location":["Los Angeles,CA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"9.6"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"19.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"19.99"}],"sellingState":["Active"],"timeLeft":["P6DT23H43M7S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T22:47:31.000Z"],"endTime":["2018-03-10T22:47:31.000Z"],"listingType":["FixedPrice"],"gift":["false"]}],
              "returnsAccepted":["false"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/202247971131_1_0_1.jpg"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["232682730454"],
              "title":["27 VINTAGE EXTRA THICK MINI BAKELITE CATALIN BLONDE DOMINOES WITH BOX RARE"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mAgPkqOLxps3nFNNQ_gHecA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/27-VINTAGE-EXTRA-THICK-MINI-BAKELITE-CATALIN-BLONDE-DOMINOES-BOX-RARE-\/232682730454"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["80544"],
              "location":["Niwot,CO,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"125.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"125.0"}],"sellingState":["Active"],"timeLeft":["P27DT5H52M58S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-01T04:57:22.000Z"],"endTime":["2018-03-31T04:57:22.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["282346720543"],
              "title":["VINTAGE 10 CATALIN BACKGAMMON Marbleize Brown 1 3\/16\\" (30mm)Diameter by BAKELITE"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mutufZc2Z1uGAHN5uF6Ej8w\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-10-CATALIN-BACKGAMMON-Marbleize-Brown-1-3-16-30mm-Diameter-BAKELITE-\/282346720543"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["90036"],
              "location":["Los Angeles,CA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"3.9"}],"shippingType":["FlatDomesticCalculatedInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"26.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"26.0"}],"sellingState":["Active"],"timeLeft":["P24DT23H0M47S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2017-02-01T22:05:11.000Z"],"endTime":["2018-03-28T22:05:11.000Z"],"listingType":["StoreInventory"],"gift":["false"],"watchCount":["79"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/282346720543_1_1_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["162924174185"],
              "title":["EX!DISNEY1930's\\"MICKEY MOUSE\\" BUTTERSCOTCH VS. CATALIN PLASTIC PENCIL SHARPENER"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["140"],"categoryName":["Other Vintage Disneyana"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mcHJlqjBW7hqfSzB5aPCtYQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/EX-DISNEY1930s-MICKEY-MOUSE-BUTTERSCOTCH-VS-CATALIN-PLASTIC-PENCIL-SHARPENER-\/162924174185"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["95258"],
              "location":["Woodbridge,CA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"69.3"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"69.3"}],"sellingState":["Active"],"timeLeft":["P27DT7H52M35S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-01T06:56:59.000Z"],"endTime":["2018-03-31T06:56:59.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["5"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["122999391845"],
              "title":["Vintage 1920s 1930s Leather Clutch Purse Bakelite Catalin Flip Handle Art Deco"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["74962"],"categoryName":["Bags, Handbags & Cases"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/m9-9jUIZ_cV0LeR7uHsvI5g\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-1920s-1930s-Leather-Clutch-Purse-Bakelite-Catalin-Flip-Handle-Art-Deco-\/122999391845"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["15904"],
              "location":["Johnstown,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"4.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"4.99"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P6DT23H8M57S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T22:13:21.000Z"],"endTime":["2018-03-10T22:13:21.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["false"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["382389203283"],
              "title":["Vintage Butterscotch Yellow Bakelite  Catalin Round Poker Chip Holder,Rack,Tray"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["73486"],"categoryName":["Trays, Racks"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mU1TMndnNArcdjZ4QGk-s2Q\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Butterscotch-Yellow-Bakelite-Catalin-Round-Poker-Chip-Holder-Rack-Tray-\/382389203283"],
              "paymentMethod":["PayPal","VisaMC","AmEx","Discover"],"autoPay":["false"],"postalCode":["12534"],
              "location":["Hudson,NY,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"14.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"24.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"24.99"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P0DT23H9M12S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-22T22:13:36.000Z"],"endTime":["2018-03-04T22:13:36.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["8"]}],
              "returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/382389203283_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["372226281258"],
              "title":["Red Garol 6AU-1 Catalin Radio"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mrzxpsifvaN0r0ZaXpPSuPg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Red-Garol-6AU-1-Catalin-Radio-\/372226281258"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["15085"],
              "location":["Trafford,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"1500.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"1500.0"}],"sellingState":["Active"],"timeLeft":["P16DT18H15M16S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-18T17:19:40.000Z"],"endTime":["2018-03-20T17:19:40.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["22"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["323100715891"],
              "title":["Set of 2 Vintage 1940's Cherry Red Bakelite\/Catalin Bangles"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mfK3uqIa2RPQ8GH27qsVeLQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Set-2-Vintage-1940s-Cherry-Red-Bakelite-Catalin-Bangles-\/323100715891"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["95688"],
              "location":["Vacaville,CA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"3.75"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"22.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"22.0"}],"sellingState":["Active"],"timeLeft":["P24DT1H3M7S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-02-26T00:07:31.000Z"],"endTime":["2018-03-28T00:07:31.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["122988148187"],
              "title":["Maroon Fada L-56 Catalin Radio"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mvGASzGMzLsC3r_KHPOwJfA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Maroon-Fada-L-56-Catalin-Radio-\/122988148187"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["15085"],
              "location":["Trafford,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"2000.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"2000.0"}],"sellingState":["Active"],"timeLeft":["P24DT2H2M2S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-26T01:06:26.000Z"],"endTime":["2018-03-28T01:06:26.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["8"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["372220754011"],
              "title":["Green RCA Tulip Grill Catalin Radio"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mEDG3FfdeMmdTJ4UaG1EeKA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Green-RCA-Tulip-Grill-Catalin-Radio-\/372220754011"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["15085"],
              "location":["Trafford,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"1500.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"1500.0"}],"sellingState":["Active"],"timeLeft":["P10DT20H2M13S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-12T19:06:37.000Z"],"endTime":["2018-03-14T19:06:37.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["14"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["142707635529"],
              "title":["Vintage Backgammon Set BAKELITE\/CATALIN 1.5\\" x 3\/8\\" Brown Swirl RARE COLOR Combo"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["19100"],"categoryName":["Vintage Manufacture"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mY2up__wlaBUE5JcU4UDusg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Backgammon-Set-BAKELITE-CATALIN-1-5-x-3-8-Brown-Swirl-RARE-COLOR-Combo-\/142707635529"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["80537"],
              "location":["Loveland,CO,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"112.49"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"112.49"}],"sellingState":["Active"],"timeLeft":["P27DT22H52M43S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-03-01T21:57:07.000Z"],"endTime":["2018-03-31T21:57:07.000Z"],"listingType":["StoreInventory"],"gift":["false"],"watchCount":["2"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["122986954753"],
              "title":["Crosley Split Grill Catalin Radio"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mPDWDcPdMNSwCOKfVJhX31Q\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Crosley-Split-Grill-Catalin-Radio-\/122986954753"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["15085"],
              "location":["Trafford,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"2200.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"2200.0"}],"sellingState":["Active"],"timeLeft":["P23DT16H50M51S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-25T15:55:15.000Z"],"endTime":["2018-03-27T15:55:15.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["18"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["122988142735"],
              "title":["RARE Fada 188 All American Catalin Radio"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mlAez3vglThdW75BBjQeAiA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/RARE-Fada-188-All-American-Catalin-Radio-\/122988142735"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["15085"],
              "location":["Trafford,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"10000.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"10000.0"}],"sellingState":["Active"],"timeLeft":["P24DT1H56M13S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-26T01:00:37.000Z"],"endTime":["2018-03-28T01:00:37.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["11"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]

            },{"itemId":["253425443084"],
              "title":["95 Vintage Bakelite\/Catalin Poker Chips, Red and Yellow w Original Box"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["150119"],"categoryName":["Poker Chips"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/m7zz4eT7Lm7jR3QRZLQ592Q\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/95-Vintage-Bakelite-Catalin-Poker-Chips-Red-and-Yellow-w-Original-Box-\/253425443084"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["02865"],
              "location":["Lincoln,RI,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"11.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"74.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"74.99"}],"sellingState":["Active"],"timeLeft":["P11DT20H5M55S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-13T19:10:19.000Z"],"endTime":["2018-03-15T19:10:19.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["4"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["302653382980"],
              "title":["Vintage Antique Old amber  Bakelite Catalin faturan Ball block rar 2879gr"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["72397"],"categoryName":["Bakelite"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/m-v63ElEX1eWpqpjed6iKfw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Antique-Old-amber-Bakelite-Catalin-faturan-Ball-block-rar-2879gr-\/302653382980"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["42242"],
              "location":["Poland"],
              "country":["PL"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"50.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["10"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"250.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"250.0"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P0DT18H32M0S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-27T17:36:24.000Z"],"endTime":["2018-03-04T17:36:24.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["162927217862"],
              "title":["Vintage Catalin Bakelite Galloping Bowling Dice 3\/4\\"  Case And Score Sheets.rare"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["10909"],"categoryName":["Dice"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mketMlZ1Eu0w8jwf5D9UMjA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Catalin-Bakelite-Galloping-Bowling-Dice-3-4-Case-And-Score-Sheets-rare-\/162927217862"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["06032"],
              "location":["Farmington,CT,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"3.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"2.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"2.0"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P9DT3H58M59S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T03:03:23.000Z"],"endTime":["2018-03-13T03:03:23.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["6"]}],
              "returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["183157500032"],
              "title":["KENWOOD Basic C1 Pre-Amp - NEEDS REPAIR - SOLD AS IS"],
              "globalId":["EBAY-ENCA"],
              "primaryCategory":[{"categoryId":["67807"],"categoryName":["Vintage Preamps & Tube Preamps"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/m3if_N_Ep7pS7UHSAtkcLgA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/KENWOOD-Basic-C1-Pre-Amp-NEEDS-REPAIR-SOLD-\/183157500032"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["B0K1X0"],
              "location":["Canada"],
              "country":["CA"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"CAD","__value__":"50.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"39.13"}],"sellingState":["Active"],"timeLeft":["P24DT9H39M38S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-04-01T17:17:44.000Z"],"endTime":["2018-05-01T17:17:44.000Z"],"listingType":["FixedPrice"],"gift":["false"],"watchCount":["9"]}],
              "returnsAccepted":["false"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["372237637649"],
              "title":["GREEN CATALIN TAYLOR BAROMETER"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["163036"],"categoryName":["Barometers"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mH1wgXnW89Ek0SksRu2HC7A\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/GREEN-CATALIN-TAYLOR-BAROMETER-\/372237637649"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["80918"],
              "location":["Colorado Springs,CO,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"12.5"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["5"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"59.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"59.99"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P6DT22H16M1S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-03T21:20:25.000Z"],"endTime":["2018-03-10T21:20:25.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["false"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["122988243137"],
              "title":["95 Vtg Bakelite Catalin Swirl Poker Chips 1-1\/2\\" across x 1\/8\\" thick Beautiful"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["150119"],"categoryName":["Poker Chips"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mz4F-zq_wX3gSt4nGGmHNLw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/95-Vtg-Bakelite-Catalin-Swirl-Poker-Chips-1-1-2-across-x-1-8-thick-Beautiful-\/122988243137"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["53805"],
              "location":["Boscobel,WI,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"11.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"11.5"}],"bidCount":["4"],"sellingState":["Active"],"timeLeft":["P1DT2H45M49S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-26T01:50:13.000Z"],"endTime":["2018-03-05T01:50:13.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["9"]}],
              "returnsAccepted":["true"],
              "galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/122988243137_1_0_1.jpg"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["true"]}]}],

        "paginationOutput":[{"pageNumber":["1"],"entriesPerPage":["100"],"totalPages":["24"],"totalEntries":["2374"]}],
        "itemSearchURL":["http:\/\/www.ebay.com\/sch\/i.html?_nkw=catalin&_ddo=1&_ipg=100&_pgn=1"]
   }
 ]
}'''


