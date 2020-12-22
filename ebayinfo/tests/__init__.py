from ebayinfo.tests.utils import getMarketsDict

# ### on ebay category version update, ###
# ### change these constants and the table below to test ###

# select * from markets order by "iEbaySiteID" ;
#
# ### on ebay category version update, ###
# ### change the constants above and this table to test ###
# query might help:
# select "cMarket", "cCountry", "iEbaySiteID", "iCategoryVer" from  markets order by "iEbaySiteID" ;

# this info is put into the test database by sMarketsTable() in ./utils_test.py
# for testing, core/tests/base.py puts markets in test database
# suggest enhancement: use the table below instead of hard coding in core/tests/base.py

sMarketsTable = \
'''
  cMarket   | cCountry | cLanguage | iEbaySiteID | bHasCategories | iCategoryVer | cCurrencyDef | cUseCategoryID | iUtcPlusOrMinus
------------+----------+-----------+-------------+----------------+--------------+--------------+----------------+-----------------
 EBAY-US    | US       | en-US     |           0 | t              |          124 | USD          |                |              -8
 EBAY-ENCA  | CA       | en-CA     |           2 | t              |          122 | CAD          |                |              -8
 EBAY-GB    | GB       | en-GB     |           3 | t              |          115 | GBP          |                |               0
 EBAY-AU    | AU       | en-AU     |          15 | t              |          116 | AUD          |                |              10
 EBAY-AT    | AT       | de-AT     |          16 | t              |           93 | EUR          |                |               1
 EBAY-FRBE  | BE       | fr-BE     |          23 | f              |           88 | EUR          | EBAY-FR        |               1
 EBAY-FR    | FR       | fr-FR     |          71 | t              |          112 | EUR          |                |               1
 EBAY-DE    | DE       | de-DE     |          77 | t              |          125 | EUR          |                |               1
 EBAY-MOTOR | US       | en-US     |         100 | t              |           75 | USD          |                |              -8
 EBAY-IT    | IT       | it-IT     |         101 | t              |          104 | EUR          |                |               1
 EBAY-NLBE  | BE       | nl-BE     |         123 | f              |           92 | EUR          |                |               1
 EBAY-NL    | NL       | nl-NL     |         146 | t              |           86 | EUR          | EBAY-NL        |               1
 EBAY-ES    | ES       | es-ES     |         186 | t              |           89 | EUR          |                |               1
 EBAY-CH    | CH       | de-CH     |         193 | t              |           94 | CHF          |                |               1
 EBAY-HK    | HK       | zh-Hant   |         201 | t              |           27 | HKD          |                |               8
 EBAY-IN    | IN       | en-IN     |         203 | t              |           65 | INR          |                |               5
 EBAY-IE    | IE       | en-IE     |         205 | t              |           73 | EUR          |                |               1
 EBAY-MY    | MY       | en-MY     |         207 | t              |           38 | MYR          |                |               8
 EBAY-FRCA  | CA       | fr-CA     |         210 | f              |           75 | CAD          |                |              -8
 EBAY-PH    | PH       | en-PH     |         211 | t              |           38 | PHP          |                |               8
 EBAY-PL    | PL       | pl-PL     |         212 | t              |           57 | PLN          |                |               1
 EBAY-SG    | SG       | en-SG     |         216 | t              |           37 | SGD          |                |               8
 EBAY-SE    | SE       | sv-SE     |         218 | f              |           11 | SEK          |                |               1
'''
sPriorMarketsTable = \
'''
  cMarket   | cCountry | cLanguage | iEbaySiteID | bHasCategories | iCategoryVer | cCurrencyDef | cUseCategoryID | iUtcPlusOrMinus
------------+----------+-----------+-------------+----------------+--------------+--------------+----------------+-----------------
 EBAY-US    | US       | en-US     |           0 | t              |          123 | USD          |                |              -8
 EBAY-ENCA  | CA       | en-CA     |           2 | t              |          121 | CAD          |                |              -8
 EBAY-GB    | GB       | en-GB     |           3 | t              |          114 | GBP          |                |               0
 EBAY-AU    | AU       | en-AU     |          15 | t              |          115 | AUD          |                |              10
 EBAY-AT    | AT       | de-AT     |          16 | t              |           92 | EUR          |                |               1
 EBAY-FRBE  | BE       | fr-BE     |          23 | f              |           87 | EUR          |                |               1
 EBAY-FR    | FR       | fr-FR     |          71 | t              |          111 | EUR          |                |               1
 EBAY-DE    | DE       | de-DE     |          77 | t              |          124 | EUR          |                |               1
 EBAY-MOTOR | US       | en-US     |         100 | t              |           75 | USD          |                |              -8
 EBAY-IT    | IT       | it-IT     |         101 | t              |          103 | EUR          |                |               1
 EBAY-NLBE  | BE       | nl-BE     |         123 | f              |           88 | EUR          |                |               1
 EBAY-NL    | NL       | nl-NL     |         146 | t              |           83 | EUR          |                |               1
 EBAY-ES    | ES       | es-ES     |         186 | t              |           88 | EUR          |                |               1
 EBAY-CH    | CH       | de-CH     |         193 | t              |           93 | CHF          |                |               1
 EBAY-HK    | HK       | zh-Hant   |         201 | t              |           26 | HKD          |                |               8
 EBAY-IN    | IN       | en-IN     |         203 | t              |           65 | INR          |                |               5
 EBAY-IE    | IE       | en-IE     |         205 | t              |           72 | EUR          |                |               1
 EBAY-MY    | MY       | en-MY     |         207 | t              |           37 | MYR          |                |               8
 EBAY-FRCA  | CA       | fr-CA     |         210 | f              |           74 | CAD          |                |              -8
 EBAY-PH    | PH       | en-PH     |         211 | t              |           37 | PHP          |                |               8
 EBAY-PL    | PL       | pl-PL     |         212 | t              |           56 | PLN          |                |               1
 EBAY-SG    | SG       | en-SG     |         216 | t              |           36 | SGD          |                |               8
 EBAY-SE    | SE       | sv-SE     |         218 | f              |           11 | SEK          |                |               1
 '''

dMarketsCurrent             = getMarketsDict( sMarketsTable )

EBAY_CURRENT_VERSION_SG     = dMarketsCurrent[ 216 ].iCategoryVer
EBAY_CURRENT_VERSION_US     = dMarketsCurrent[   0 ].iCategoryVer
EBAY_CURRENT_VERSION_GB     = dMarketsCurrent[   3 ].iCategoryVer
EBAY_CURRENT_VERSION_Mo     = dMarketsCurrent[ 100 ].iCategoryVer # short for Motor
EBAY_CURRENT_VERSION_ENCA   = dMarketsCurrent[   2 ].iCategoryVer

dMarketsPrevious            = getMarketsDict( sPriorMarketsTable )

prior_EBAY_CURRENT_VERSION_SG = dMarketsPrevious[ 216 ].iCategoryVer
prior_EBAY_CURRENT_VERSION_US = dMarketsPrevious[   0 ].iCategoryVer
prior_EBAY_CURRENT_VERSION_GB = dMarketsPrevious[   3 ].iCategoryVer


# select "id","iCategoryID","name","iLevel","iParentID","bLeafCategory","iTreeVersion","iEbaySiteID_id"
# from ebay_categories where "iEbaySiteID_id" = 2 and "iCategoryID" = 64627;

# CAVEAT! if you add a category from a new market, you must add the root to GetEbayCategoriesWebTestSetUp!!!

sEbayCategoryDump = \
'''
  id  | iCategoryID |           name                | iLevel | iParentID | bLeafCategory | iTreeVersion | iEbaySiteID_id
------+-------------+--------------------------+--------+-----------+---------------+--------------+------------+----
  771 |       12576 | Business & Industrial         |      1 |     12576 | f             |          117 |          0
22882 |           1 | Collectables                  |      1 |         1 | f             |          108 |          3
19191 |       20081 | Antiques                      |      1 |     20081 | f             |          108 |          3
    2 |       20081 | Antiques                      |      1 |     20081 | f             |          117 |          0
 4569 |           1 | Collectibles                  |      1 |         1 | f             |          117 |          0
 3380 |       11450 | Clothing, Shoes & Accessories |      1 |     11450 | f             |          117 |          0
 9620 |         293 | Consumer Electronics          |      1 |       293 | f             |          117 |          0
17669 |         220 | Toys & Hobbies                |      1 |       220 | f             |          117 |          0
16964 |       64482 | Sports Mem, Cards & Fan Shop  |      1 |     64482 | f             |          117 |          0
13707 |         281 | Jewelry & Watches             |      1 |       281 | f             |          117 |          0
  540 |         550 | Art                           |      1 |       550 | f             |          117 |          0
14311 |         619 | Musical Instruments & Gear    |      1 |       619 | f             |          117 |          0
18739 |        1249 | Video Games & Consoles        |      1 |      1249 | f             |          117 |          0
 3164 |         625 | Cameras & Photo               |      1 |       625 | f             |          117 |          0
29513 |         293 | Sound & Vision                |      1 |       293 | f             |          112 |          3
129982|         293 | Consumer Electronics          |      1 |       293 | f             |          119 |          2

14477 |      180010 | Pianos, Keyboards & Organs    |      2 |       619 | f             |          117 |          0
 9656 |       32852 | TV, Video & Home Audio        |      2 |       293 | f             |          117 |          0
  548 |         551 | Paintings                     |      2 |       550 | t             |          117 |          0
 4570 |          34 | Advertising                   |      2 |         1 | f             |          117 |          0
 8481 |        1446 | Religion & Spirituality       |      2 |         1 | f             |          117 |          0
  417 |      100927 | Periods & Styles              |      2 |     20081 | f             |          117 |          0
19525 |      100927 | Periods/Styles                |      2 |     20081 | f             |          108 |          3
  432 |       20094 | Science & Medicine (Pre-1930) |      2 |     20081 | f             |          117 |          0
 5547 |       66502 | Arcade, Jukeboxes & Pinball   |      2 |         1 | f             |          117 |          0
 5745 |         898 | Casino                        |      2 |         1 | f             |          117 |          0
   20 |        4707 | Architectural & Garden        |      2 |     20081 | f             |          117 |          0
 8858 |         593 | Tobacciana                    |      2 |         1 | f             |          117 |          0
 1166 |       92074 | Electrical & Test Equipment   |      2 |     12576 | f             |          117 |          0
 9290 |         597 | Vanity, Perfume & Shaving     |      2 |         1 | f             |          117 |          0
 9325 |       69851 | Vintage, Retro, Mid-Century   |      2 |         1 | f             |          117 |          0
24923 |       69851 | Vintage & Retro Collectables  |      2 |         1 | f             |          108 |          3
 3882 |      175759 | Vintage                       |      2 |     11450 | f             |          117 |          0
 6664 |         137 | Disneyana                     |      2 |         1 | f             |          117 |          0
 8455 |       29832 | Radio, Phonograph, TV, Phone  |      2 |         1 | f             |          117 |          0
 9872 |      183077 | Vintage Electronics           |      2 |       293 | f             |          117 |          0
17116 |       50123 | Vintage Sports Memorabilia    |      2 |     64482 | f             |          117 |          0
14066 |       48579 | Vintage & Antique Jewelry     |      2 |       281 | f             |          117 |          0
17915 |         233 | Games                         |      2 |       220 | f             |          117 |          0
 9629 |       15052 | Portable Audio & Headphones   |      2 |       293 | f             |          117 |          0
14502 |      180014 | Pro Audio Equipment           |      2 |       619 | f             |          117 |          0
18742 |       54968 | Video Game Accessories        |      2 |      1249 | f             |          117 |          0
 3209 |       69323 | Film Photography              |      2 |       625 | f             |          117 |          0
29668 |      175740 | Vintage Sound & Vision        |      2 |       293 | f             |          112 |          3
130232|      183077 | Vintage Electronics           |      2 |       293 | f             |          119 |          2

 9679 |       14961 | TV, Video & Audio Accessories |      3 |     32852 | f             |          117 |          0
 3230 |       15250 | Slide & Movie Projection      |      3 |     69323 | f             |          117 |          0
 9710 |       71582 | TV, Video & Audio Parts       |      3 |     32852 | f             |          117 |          0
14491 |      181224 | Parts & Accessories           |      3 |    180010 | f             |          117 |          0
 9899 |      183079 | Other Vintage Electronics     |      3 |    183077 | t             |          117 |          0
 9661 |       14969 | Home Audio Stereos, Components|      3 |     32852 | f             |          117 |          0
 8479 |      171194 | Price Guides & Publications   |      3 |     29832 | t             |          117 |          0
 5021 |      165266 | Other Collectible Ads         |      3 |        34 | t             |          117 |          0
 8462 |         931 | Radios                        |      3 |     29832 | f             |          117 |          0
19527 |       69471 | Art Deco                      |      3 |    100927 | t             |          108 |          3
24929 |       72397 | Bakelite                      |      3 |     69851 | t             |          108 |          3
  419 |       69471 | Art Deco                      |      3 |    100927 | t             |          117 |          0
 8515 |      165688 | Islam                         |      3 |      1446 | f             |          117 |          0
 5555 |       13720 | Jukeboxes                     |      3 |     66502 | f             |          117 |          0
 5759 |       35743 | Chips                         |      3 |       898 | f             |          117 |          0
 5785 |       10909 | Dice                          |      3 |       898 | t             |          117 |          0
   32 |       37911 | Hardware                      |      3 |      4707 | f             |          117 |          0
  449 |      163035 | Scientific Instruments        |      3 |     20094 | f             |          117 |          0
 8879 |         951 | Lighters                      |      3 |       593 | f             |          117 |          0
 1370 |      181939 | Test, Measurement & Inspection|      3 |     92074 | f             |          117 |          0
 9311 |       35986 | Shaving                       |      3 |       597 | f             |          117 |          0
 9331 |       72397 | Bakelite                      |      3 |     69851 | t             |          117 |          0
 3883 |      182059 | Vintage Accessories           |      3 |    175759 | f             |          117 |          0
 6665 |         139 | Vintage (Pre-1968)            |      3 |       137 | f             |          117 |          0
 9873 |      175740 | Vintage Audio & Video         |      3 |    183077 | f             |          117 |          0
17933 |        7317 | Game Pieces, Parts            |      3 |       233 | t             |          117 |          0
17152 |       50133 | Other Vintage Sports Mem      |      3 |     50123 | t             |          117 |          0
14067 |         500 | Costume                       |      3 |     48579 | f             |          117 |          0
17916 |        2550 | Board & Traditional Games     |      3 |       233 | f             |          117 |          0
14503 |      168129 | Acoustical Treatments         |      3 |    180014 | t             |          117 |          0
14523 |      119019 | Vintage Pro Audio Equipment   |      3 |    180014 | t             |          117 |          0
 9630 |      112529 | Headphones                    |      3 |     15052 | t             |          117 |          0
 4979 |       13623 | Merchandise & Memorabilia     |      3 |        34 | f             |          117 |          0
14504 |      163896 | Amplifiers                    |      3 |    180014 | t             |          117 |          0
18746 |      171814 | Cables & Adapters             |      3 |     54968 | t             |          117 |          0
 8480 |       29833 | Other Vintage Radio, TV, Phone|      3 |     29832 | t             |          117 |          0
29683 |      175741 | Vintage Parts & Accessories   |      3 |    175740 | f             |          112 |          3
130233|      175740 | Vintage Audio & Video         |      3 |    183077 | f             |          119 |          2

 5003 |       10804 | Signs                         |      4 |     13623 | f             |          117 |          0
 9881 |       67807 | Vintage Preamps & Tube Preamps|      4 |    175740 | t             |          117 |          0
 8464 |         934 | Manuals                       |      4 |       931 | t             |          117 |          0
 8467 |         932 | Transistor Radios             |      4 |       931 | t             |          117 |          0
 5559 |       13723 | Replacement Parts             |      4 |     13720 | t             |          117 |          0
 5770 |      150119 | Poker Chips                   |      4 |     35743 | t             |          117 |          0
 5771 |       63757 | Sets                          |      4 |     35743 | f             |          117 |          0
 5779 |       73484 | Storage & Supplies            |      4 |     35743 | f             |          117 |          0
   36 |      162933 | Drawer Pulls                  |      4 |     37911 | t             |          117 |          0
  450 |      163036 | Barometers                    |      4 |    163035 | t             |          117 |          0
 8915 |         595 | Other Collectible Lighters    |      4 |       951 | t             |          117 |          0
 1429 |      181968 | Test Meters & Detectors       |      4 |    181939 | f             |          117 |          0
 8517 |      165690 | Prayer Beads                  |      4 |    165688 | t             |          117 |          0
 9313 |       35988 | Mugs, Brushes                 |      4 |     35986 | t             |          117 |          0
 3884 |       74962 | Bags, Handbags & Cases        |      4 |    182059 | t             |          117 |          0
 3903 |      182063 | Umbrellas & Parasols          |      4 |    182059 | t             |          117 |          0
 6684 |         140 | Other Vintage Disneyana       |      4 |       139 | t             |          117 |          0
 8465 |        7275 | Parts & Tubes                 |      4 |       931 | t             |          117 |          0
 8468 |       38032 | Tube Radios                   |      4 |       931 | f             |          117 |          0
 9882 |       50595 | Vintage Radios                |      4 |    175740 | t             |          117 |          0
14081 |       58560 | Art Nouveau/Art Deco 1895-1935|      4 |       500 | f             |          117 |          0
17917 |       19100 | Vintage Manufacture           |      4 |      2550 | t             |          117 |          0
 9878 |       73368 | Vintage Amplifiers & Tube Amps|      4 |    175740 | t             |          117 |          0
 9888 |      175741 | Vintage Parts & Accessories   |      4 |    175740 | f             |          117 |          0
 9662 |       14970 | Amplifiers & Preamps          |      4 |     14969 | t             |          117 |          0
 9669 |       48647 | Record Players/Home Turntables|      4 |     14969 | t             |          117 |          0
 9683 |       14964 | Audio Cables & Interconnects  |      4 |     14961 | t             |          117 |          0
 9711 |      122649 | Amplifier Parts & Components  |      4 |     71582 | t             |          117 |          0
 9672 |       81741 | Other Home Stereo Components  |      4 |     14969 | t             |          117 |          0
 9887 |       73382 | Vintage Tuners & Tube Tuners  |      4 |    175740 | t             |          117 |          0
14500 |       21766 | Other Parts & Accessories     |      4 |    181224 | t             |          117 |          0
 3231 |       15252 | Movie Projectors              |      4 |     15250 | t             |          117 |          0
 9884 |       50597 | Vintage Speakers              |      4 |    175740 | t             |          117 |          0
 1468 |      181998 | Testers & Calibrators         |      4 |    181939 | f             |          117 |          0
 1467 |        4678 | Other Test Meters & Detectors |      4 |    181968 | t             |          117 |          0
29689 |       64627 | Valves & Vacuum Tubes         |      4 |    175741 | t             |          112 |          3
130248|      175741 | Vintage Parts & Accessories   |      4 |    175740 | f             |          119 |          2

 1478 |      170062 | Tube Testers                  |      5 |    181998 | t             |          117 |          0
 9893 |       67815 | Vintage Transformers          |      5 |    175741 | t             |          117 |          0
 9895 |      168088 | Other Vintage A/V Parts & Accs|      5 |    175741 | t             |          117 |          0
 5004 |       37840 | Original                      |      5 |     10804 | f             |          117 |          0
 9894 |       64627 | Vintage Tubes & Tube Sockets  |      5 |    175741 | t             |          117 |          0
 1434 |       50960 | Electric Circuit & Multimeters|      5 |    181968 | f             |          117 |          0
 1431 |       73160 | Capacitance & ESR Meters      |      5 |    181968 | t             |          117 |          0
 5778 |       63760 | Other Casino Chip Sets        |      5 |     63757 | t             |          117 |          0
 5781 |       73486 | Trays, Racks                  |      5 |     73484 | t             |          117 |          0
 8470 |       38034 | 1930-49                       |      5 |     38032 | t             |          117 |          0
14091 |       10967 | Other Art Deco Costume Jewelry|      5 |     58560 | t             |          117 |          0
 1436 |       58277 | Multimeters                   |      6 |     50960 | t             |          117 |          0
 5006 |       10806 | 1930-69                       |      6 |     37840 | t             |          117 |          0
 9891 |       39996 | Vintage Manuals               |      5 |    175741 | t             |          117 |          0
130254|       64627 | Vintage Tubes & Tube Sockets  |      5 |    175741 | t             |          119 |          2

219227|        6000 | eBay Motors                   |      1 |      6000 | f             |           75 |        100
220511|        6028 | Parts & Accessories           |      2 |      6000 | f             |           75 |        100
221826|       10073 | Vintage Car & Truck Parts     |      3 |      6028 | f             |           75 |        100
221907|       80741 | Radio & Speaker Systems       |      4 |     10073 | t             |           75 |        100


'''
# ### last row (Radio & Speaker Systems) & ###
# ###        Tube Testers row (1478)       ###
# ###               tested in              ###
# ### TestHeirarchiesAreTheyCompleteWebTest.test_are_heirarchies_complete() ###

'''
'''

# actually for 'EBAY-US' as of 2017-12
sExampleCategoryVersion = \
  '''<?xml version="1.0" encoding="UTF-8"?>
    <GetCategoriesResponse xmlns="urn:ebay:apis:eBLBaseComponents">
        <Timestamp>2017-12-12T04:45:28.766Z</Timestamp>
        <Ack>Success</Ack>
        <Version>1041</Version>
        <Build>E1041_CORE_APICATALOG_18587827_R1</Build>
        <UpdateTime>2017-06-13T02:06:57.000Z</UpdateTime>
        <CategoryVersion>117</CategoryVersion>
        <ReservePriceAllowed>true</ReservePriceAllowed>
        <MinimumReservePrice>0.0</MinimumReservePrice>
    </GetCategoriesResponse>'''

sExampleCategoryList = \
 '''<?xml version="1.0" encoding="UTF-8"?>
<GetCategoriesResponse xmlns="urn:ebay:apis:eBLBaseComponents">
    <Timestamp>2017-12-27T21:26:23.376Z</Timestamp>
    <Ack>Success</Ack>
    <Version>1041</Version>
    <Build>E1041_CORE_APICATALOG_18587827_R1</Build>
    <CategoryArray>
        <Category>
            <BestOfferEnabled>true</BestOfferEnabled>
            <AutoPayEnabled>true</AutoPayEnabled>
            <CategoryID>20081</CategoryID>
            <CategoryLevel>1</CategoryLevel>
            <CategoryName>Antiques</CategoryName>
            <CategoryParentID>20081</CategoryParentID>
        </Category>
        <Category>
            <BestOfferEnabled>true</BestOfferEnabled>
            <AutoPayEnabled>true</AutoPayEnabled>
            <CategoryID>37903</CategoryID>
            <CategoryLevel>2</CategoryLevel>
            <CategoryName>Antiquities</CategoryName>
            <CategoryParentID>20081</CategoryParentID>
        </Category>
        <Category>
            <BestOfferEnabled>true</BestOfferEnabled>
            <AutoPayEnabled>true</AutoPayEnabled>
            <CategoryID>37908</CategoryID>
            <CategoryLevel>3</CategoryLevel>
            <CategoryName>The Americas</CategoryName>
            <CategoryParentID>37903</CategoryParentID>
            <LeafCategory>true</LeafCategory>
        </Category>
        <Category>
            <BestOfferEnabled>true</BestOfferEnabled>
            <AutoPayEnabled>true</AutoPayEnabled>
            <CategoryID>162922</CategoryID>
            <CategoryLevel>3</CategoryLevel>
            <CategoryName>Byzantine</CategoryName>
            <CategoryParentID>37903</CategoryParentID>
            <LeafCategory>true</LeafCategory>
        </Category>
        <Category>
            <BestOfferEnabled>true</BestOfferEnabled>
            <AutoPayEnabled>true</AutoPayEnabled>
            <CategoryID>162923</CategoryID>
            <CategoryLevel>3</CategoryLevel>
            <CategoryName>Celtic</CategoryName>
            <CategoryParentID>37903</CategoryParentID>
            <LeafCategory>true</LeafCategory>
        </Category>
        <Category>
            <BestOfferEnabled>true</BestOfferEnabled>
            <AutoPayEnabled>true</AutoPayEnabled>
            <CategoryID>37905</CategoryID>
            <CategoryLevel>3</CategoryLevel>
            <CategoryName>Egyptian</CategoryName>
            <CategoryParentID>37903</CategoryParentID>
            <LeafCategory>true</LeafCategory>
        </Category>
        <Category>
            <BestOfferEnabled>true</BestOfferEnabled>
            <AutoPayEnabled>true</AutoPayEnabled>
            <CategoryID>162916</CategoryID>
            <CategoryLevel>3</CategoryLevel>
            <CategoryName>Far Eastern</CategoryName>
            <CategoryParentID>37903</CategoryParentID>
            <LeafCategory>true</LeafCategory>
        </Category>
        <Category>
            <BestOfferEnabled>true</BestOfferEnabled>
            <AutoPayEnabled>true</AutoPayEnabled>
            <CategoryID>37906</CategoryID>
            <CategoryLevel>3</CategoryLevel>
            <CategoryName>Greek</CategoryName>
            <CategoryParentID>37903</CategoryParentID>
            <LeafCategory>true</LeafCategory>
        </Category>

    </CategoryArray>
    <CategoryCount>19188</CategoryCount>
    <UpdateTime>2017-06-13T02:06:57.000Z</UpdateTime>
    <CategoryVersion>117</CategoryVersion>
    <ReservePriceAllowed>true</ReservePriceAllowed>
    <MinimumReservePrice>0.0</MinimumReservePrice>
</GetCategoriesResponse>
'''
