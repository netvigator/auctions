
#
sMarketsTable = \
'''
  cMarket   | cCountry | cLanguage | iEbaySiteID | bHasCategories | iCategoryVer | cCurrencyDef | cUseCategoryID | iUtcPlusOrMinus 
------------+----------+-----------+-------------+----------------+--------------+--------------+----------------+-----------------
 EBAY-US    | US       | en-US     |           0 | t              |          118 | USD          |                |              -8
 EBAY-ENCA  | CA       | en-CA     |           2 | t              |          116 | CAD          |                |              -8
 EBAY-GB    | GB       | en-GB     |           3 | t              |          109 | GBP          |                |               0
 EBAY-AU    | AU       | en-AU     |          15 | t              |          109 | AUD          |                |              10
 EBAY-AT    | AT       | de-AT     |          16 | t              |           87 | EUR          |                |               1
 EBAY-FRBE  | BE       | fr-BE     |          23 | f              |           82 | EUR          |                |               1
 EBAY-FR    | FR       | fr-FR     |          71 | t              |          106 | EUR          |                |               1
 EBAY-DE    | DE       | de-DE     |          77 | t              |          119 | EUR          |                |               1
 EBAY-MOTOR | US       | en-US     |         100 | t              |           74 | USD          |                |              -8
 EBAY-IT    | IT       | it-IT     |         101 | t              |           98 | EUR          |                |               1
 EBAY-NLBE  | BE       | nl-BE     |         123 | f              |           83 | EUR          |                |               1
 EBAY-NL    | NL       | nl-NL     |         146 | t              |           78 | EUR          |                |               1
 EBAY-ES    | ES       | es-ES     |         186 | t              |           83 | EUR          |                |               1
 EBAY-CH    | CH       | de-CH     |         193 | t              |           88 | CHF          |                |               1
 EBAY-HK    | HK       | zh-Hant   |         201 | t              |           21 | HKD          |                |               8
 EBAY-IN    | IN       | en-IN     |         203 | t              |           65 | INR          |                |               5
 EBAY-IE    | IE       | en-IE     |         205 | t              |           67 | EUR          |                |               1
 EBAY-MY    | MY       | en-MY     |         207 | t              |           32 | MYR          |                |               8
 EBAY-FRCA  | CA       | fr-CA     |         210 | f              |           69 | CAD          |                |              -8
 EBAY-PH    | PH       | en-PH     |         211 | t              |           32 | PHP          |                |               8
 EBAY-PL    | PL       | pl-PL     |         212 | t              |           51 | PLN          |                |               1
 EBAY-SG    | SG       | en-SG     |         216 | t              |           31 | SGD          |                |               8
 EBAY-SE    | SE       | sv-SE     |         218 | f              |           11 | SEK          |                |               1
 '''
 

# select "id","iCategoryID","name","iLevel","iParentID","bLeafCategory","iTreeVersion","iMarket_id" 
 
sCategoryDump = \
'''
  id  | iCategoryID |           name                | iLevel | iParentID | bLeafCategory | iTreeVersion | iMarket_id 
------+-------------+--------------------------+--------+-----------+---------------+--------------+------------+----
  771 |       12576 | Business & Industrial         |      1 |     12576 | f             |          118 |          0 
22882 |           1 | Collectables                  |      1 |         1 | f             |          108 |          3 
19191 |       20081 | Antiques                      |      1 |     20081 | f             |          108 |          3 
    2 |       20081 | Antiques                      |      1 |     20081 | f             |          118 |          0 
 4569 |           1 | Collectibles                  |      1 |         1 | f             |          118 |          0 
 3380 |       11450 | Clothing, Shoes & Accessories |      1 |     11450 | f             |          118 |          0 
 9620 |         293 | Consumer Electronics          |      1 |       293 | f             |          118 |          0 
17669 |         220 | Toys & Hobbies                |      1 |       220 | f             |          118 |          0 
16964 |       64482 | Sports Mem, Cards & Fan Shop  |      1 |     64482 | f             |          118 |          0 
13707 |         281 | Jewelry & Watches             |      1 |       281 | f             |          118 |          0 
  540 |         550 | Art                           |      1 |       550 | f             |          118 |          0

  548 |         551 | Paintings                     |      2 |       550 | t             |          118 |          0
 4570 |          34 | Advertising                   |      2 |         1 | f             |          118 |          0
 8481 |        1446 | Religion & Spirituality       |      2 |         1 | f             |          118 |          0 
  417 |      100927 | Periods & Styles              |      2 |     20081 | f             |          118 |          0 
19525 |      100927 | Periods/Styles                |      2 |     20081 | f             |          108 |          3
  432 |       20094 | Science & Medicine (Pre-1930) |      2 |     20081 | f             |          118 |          0 
 5547 |       66502 | Arcade, Jukeboxes & Pinball   |      2 |         1 | f             |          118 |          0 
 5745 |         898 | Casino                        |      2 |         1 | f             |          118 |          0 
   20 |        4707 | Architectural & Garden        |      2 |     20081 | f             |          118 |          0 
 8858 |         593 | Tobacciana                    |      2 |         1 | f             |          118 |          0 
 1166 |       92074 | Electrical & Test Equipment   |      2 |     12576 | f             |          118 |          0 
 9290 |         597 | Vanity, Perfume & Shaving     |      2 |         1 | f             |          118 |          0 
 9325 |       69851 | Vintage, Retro, Mid-Century   |      2 |         1 | f             |          118 |          0 
24923 |       69851 | Vintage & Retro Collectables  |      2 |         1 | f             |          108 |          3
 3882 |      175759 | Vintage                       |      2 |     11450 | f             |          118 |          0 
 6664 |         137 | Disneyana                     |      2 |         1 | f             |          118 |          0 
 8455 |       29832 | Radio, Phonograph, TV, Phone  |      2 |         1 | f             |          118 |          0 
 9872 |      183077 | Vintage Electronics           |      2 |       293 | f             |          118 |          0 
17116 |       50123 | Vintage Sports Memorabilia    |      2 |     64482 | f             |          118 |          0 
14066 |       48579 | Vintage & Antique Jewelry     |      2 |       281 | f             |          118 |          0 
17915 |         233 | Games                         |      2 |       220 | f             |          118 |          0 
 
 8479 |      171194 | Price Guides & Publications   |      3 |     29832 | t             |          117 |          0
 5021 |      165266 | Other Collectible Ads         |      3 |        34 | t             |          118 |          0
 8462 |         931 | Radios                        |      3 |     29832 | f             |          118 |          0
19527 |       69471 | Art Deco                      |      3 |    100927 | t             |          108 |          3 
24929 |       72397 | Bakelite                      |      3 |     69851 | t             |          108 |          3 
  419 |       69471 | Art Deco                      |      3 |    100927 | t             |          118 |          0 
 8515 |      165688 | Islam                         |      3 |      1446 | f             |          118 |          0 
 5555 |       13720 | Jukeboxes                     |      3 |     66502 | f             |          118 |          0 
 5759 |       35743 | Chips                         |      3 |       898 | f             |          118 |          0 
 5785 |       10909 | Dice                          |      3 |       898 | t             |          118 |          0 
   32 |       37911 | Hardware                      |      3 |      4707 | f             |          118 |          0 
  449 |      163035 | Scientific Instruments        |      3 |     20094 | f             |          118 |          0 
 8879 |         951 | Lighters                      |      3 |       593 | f             |          118 |          0 
 1370 |      181939 | Test, Measurement & Inspection|      3 |     92074 | f             |          118 |          0 
 9311 |       35986 | Shaving                       |      3 |       597 | f             |          118 |          0 
 9331 |       72397 | Bakelite                      |      3 |     69851 | t             |          118 |          0 
 3883 |      182059 | Vintage Accessories           |      3 |    175759 | f             |          118 |          0 
 6665 |         139 | Vintage (Pre-1968)            |      3 |       137 | f             |          118 |          0 
 9873 |      175740 | Vintage Audio & Video         |      3 |    183077 | f             |          118 |          0 
17933 |        7317 | Game Pieces, Parts            |      3 |       233 | t             |          118 |          0 
17152 |       50133 | Other Vintage Sports Mem      |      3 |     50123 | t             |          118 |          0 
14067 |         500 | Costume                       |      3 |     48579 | f             |          118 |          0 
17916 |        2550 | Board & Traditional Games     |      3 |       233 | f             |          118 |          0 

 8464 |         934 | Manuals                       |      4 |       931 | t             |          118 |          0
 8467 |         932 | Transistor Radios             |      4 |       931 | t             |          118 |          0
 5559 |       13723 | Replacement Parts             |      4 |     13720 | t             |          118 |          0 
 5770 |      150119 | Poker Chips                   |      4 |     35743 | t             |          118 |          0 
 5771 |       63757 | Sets                          |      4 |     35743 | f             |          118 |          0 
 5779 |       73484 | Storage & Supplies            |      4 |     35743 | f             |          118 |          0 
   36 |      162933 | Drawer Pulls                  |      4 |     37911 | t             |          118 |          0 
  450 |      163036 | Barometers                    |      4 |    163035 | t             |          118 |          0 
 8915 |         595 | Other Collectible Lighters    |      4 |       951 | t             |          118 |          0 
 1429 |      181968 | Test Meters & Detectors       |      4 |    181939 | f             |          118 |          0 
 8517 |      165690 | Prayer Beads                  |      4 |    165688 | t             |          118 |          0 
 9313 |       35988 | Mugs, Brushes                 |      4 |     35986 | t             |          118 |          0 
 3884 |       74962 | Bags, Handbags & Cases        |      4 |    182059 | t             |          118 |          0 
 3903 |      182063 | Umbrellas & Parasols          |      4 |    182059 | t             |          118 |          0 
 6684 |         140 | Other Vintage Disneyana       |      4 |       139 | t             |          118 |          0 
 8465 |        7275 | Parts & Tubes                 |      4 |       931 | t             |          118 |          0 
 8468 |       38032 | Tube Radios                   |      4 |       931 | f             |          118 |          0 
 9882 |       50595 | Vintage Radios                |      4 |    175740 | t             |          118 |          0 
14081 |       58560 | Art Nouveau/Art Deco 1895-1935|      4 |       500 | f             |          118 |          0 
17917 |       19100 | Vintage Manufacture           |      4 |      2550 | t             |          118 |          0 

 1434 |       50960 | Electric Circuit & Multimeters|      5 |    181968 | f             |          118 |          0 
 1431 |       73160 | Capacitance & ESR Meters      |      5 |    181968 | t             |          118 |          0 
 5778 |       63760 | Other Casino Chip Sets        |      5 |     63757 | t             |          118 |          0 
 5781 |       73486 | Trays, Racks                  |      5 |     73484 | t             |          118 |          0 
 8470 |       38034 | 1930-49                       |      5 |     38032 | t             |          118 |          0 
14091 |       10967 | Other Art Deco Costume Jewelry|      5 |     58560 | t             |          118 |          0 

 1436 |       58277 | Multimeters                   |      6 |     50960 | t             |          118 |          0 


'''

