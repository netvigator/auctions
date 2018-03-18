
# put USA first, it should be pk = 1
sMarketsTable = \
'''
  cMarket   | cCountry | cLanguage | iEbaySiteID | bHasCategories | iCategoryVer | cCurrencyDef | cUseCategoryID | iUtcPlusOrMinus 
------------+----------+-----------+-------------+----------------+--------------+--------------+----------------+-----------------
 EBAY-US    | US       | en-US     |           0 | t              |          117 | USD          |                |              -8
 EBAY-ENCA  | CA       | en-CA     |           2 | t              |              | CAD          |                |              -8
 EBAY-GB    | GB       | en-GB     |           3 | t              |          108 | GBP          |                |               0
 EBAY-AU    | AU       | en-AU     |          15 | t              |              | AUD          |                |              10
 EBAY-AT    | AT       | de-AT     |          16 | t              |              | EUR          |                |               1
 EBAY-FRBE  | BE       | fr-BE     |          23 | f              |              | EUR          |                |               1
 EBAY-FR    | FR       | fr-FR     |          71 | t              |              | EUR          |                |               1
 EBAY-DE    | DE       | de-DE     |          77 | t              |              | EUR          |                |               1
 EBAY-MOTOR | US       | en-US     |         100 | t              |              | USD          |                |              -8
 EBAY-IT    | IT       | it-IT     |         101 | t              |              | EUR          |                |               1
 EBAY-NLBE  | BE       | nl-BE     |         123 | f              |              | EUR          |                |               1
 EBAY-NL    | NL       | nl-NL     |         146 | t              |              | EUR          |                |               1
 EBAY-ES    | ES       | es-ES     |         186 | t              |              | EUR          |                |               1
 EBAY-CH    | CH       | de-CH     |         193 | t              |              | CHF          |                |               1
 EBAY-HK    | HK       | zh-Hant   |         201 | t              |              | HKD          |                |               8
 EBAY-IN    | IN       | en-IN     |         203 | t              |              | INR          |                |               5
 EBAY-IE    | IE       | en-IE     |         205 | t              |              | EUR          |                |               1
 EBAY-MY    | MY       | en-MY     |         207 | t              |              | MYR          |                |               8
 EBAY-FRCA  | CA       | fr-CA     |         210 | f              |              | CAD          |                |              -8
 EBAY-PH    | PH       | en-PH     |         211 | t              |              | PHP          |                |               8
 EBAY-PL    | PL       | pl-PL     |         212 | t              |              | PLN          |                |               1
 EBAY-SG    | SG       | en-SG     |         216 | t              |           30 | SGD          |                |               8
 EBAY-SE    | SE       | sv-SE     |         218 | f              |              | SEK          |                |               1
 '''
 
 
 
sCategoryDump = \
'''
  id  | iCategoryID |           name                | iLevel | iParentID | bLeafCategory | iTreeVersion | iMarket_id | iSupercededBy | lft  | rght | tree_id | level | parent_id 
------+-------------+--------------------------+--------+-----------+---------------+--------------+------------+---------------+------+------+---------+-------+-----------
  771 |       12576 | Business & Industrial         |      1 |     12576 | f             |          117 |          0 |               | 1540 | 6325 |       2 |     1 |         1
22882 |           1 | Collectables                  |      1 |         1 | f             |          108 |          3 |               | 7384 |11499 |       1 |     1 |     19190
19191 |       20081 | Antiques                      |      1 |     20081 | f             |          108 |          3 |               |    2 |  685 |       1 |     1 |     19190
    2 |       20081 | Antiques                      |      1 |     20081 | f             |          117 |          0 |               |   2 |  1077 |       2 |     1 |         1
 4569 |           1 | Collectibles                  |      1 |         1 | f             |          117 |          0 |               | 9136 |18683 |       2 |     1 |         1
 3380 |       11450 | Clothing, Shoes & Accessories |      1 |     11450 | f             |          117 |          0 |               | 6758 | 8025 |       2 |     1 |         1
 9620 |         293 | Consumer Electronics          |      1 |       293 | f             |          117 |          0 |               |19238 |19817 |       2 |     1 |         1
17669 |         220 | Toys & Hobbies                |      1 |       220 | f             |          117 |          0 |               |36170 |38245 |       2 |     1 |         1
16964 |       64482 | Sports Mem, Cards & Fan Shop  |      1 |     64482 | f             |          117 |          0 |               |34760 |35223 |       2 |     1 |         1
13707 |         281 | Jewelry & Watches             |      1 |       281 | f             |          117 |          0 |               |28246 |29431 |       2 |     1 |         1

24923 |       69851 | Vintage & Retro Collectables  |      2 |         1 | f             |          108 |          3 |               |11469 |11484 |       1 |     2 |     22882
19525 |      100927 | Periods/Styles                |      2 |     20081 | f             |          108 |          3 |               |  525 |  536 |       1 |     2 |     19191
 8481 |        1446 | Religion & Spirituality       |      2 |         1 | f             |          117 |          0 |               |16959 |17100 |       2 |     2 |      4569
  417 |      100927 | Periods & Styles              |      2 |     20081 | f             |          117 |          0 |               |  833 |  850 |       2 |     2 |         2
  432 |       20094 | Science & Medicine (Pre-1930) |      2 |     20081 | f             |          117 |          0 |               |  865 |  910 |       2 |     2 |         2
 5547 |       66502 | Arcade, Jukeboxes & Pinball   |      2 |         1 | f             |          117 |          0 |               |11091 |11136 |       2 |     2 |      4569
 5745 |         898 | Casino                        |      2 |         1 | f             |          117 |          0 |               |11487 |11604 |       2 |     2 |      4569
   20 |        4707 | Architectural & Garden        |      2 |     20081 | f             |          117 |          0 |               |   37 |  116 |       2 |     2 |         2
 8858 |         593 | Tobacciana                    |      2 |         1 | f             |          117 |          0 |               |17713 |17858 |       2 |     2 |      4569
 1166 |       92074 | Electrical & Test Equipment   |      2 |     12576 | f             |          117 |          0 |               | 2329 | 3004 |       2 |     2 |       771
 9290 |         597 | Vanity, Perfume & Shaving     |      2 |         1 | f             |          117 |          0 |               |18577 |18646 |       2 |     2 |      4569
 9325 |       69851 | Vintage, Retro, Mid-Century   |      2 |         1 | f             |          117 |          0 |               |18647 |18664 |       2 |     2 |      4569
 3882 |      175759 | Vintage                       |      2 |     11450 | f             |          117 |          0 |               | 7463 | 7656 |       2 |     2 |      3380
 6664 |         137 | Disneyana                     |      2 |         1 | f             |          117 |          0 |               |13325 |13626 |       2 |     2 |      4569
 8455 |       29832 | Radio, Phonograph, TV, Phone  |      2 |         1 | f             |          117 |          0 |               |16907 |16958 |       2 |     2 |      4569
 9872 |      183077 | Vintage Electronics           |      2 |       293 | f             |          117 |          0 |               |19725 |19780 |       2 |     2 |      9620
17116 |       50123 | Vintage Sports Memorabilia    |      2 |     64482 | f             |          117 |          0 |               |35147 |35220 |       2 |     2 |     16964
14066 |       48579 | Vintage & Antique Jewelry     |      2 |       281 | f             |          117 |          0 |               |28965 |29274 |       2 |     2 |     13707
17915 |         233 | Games                         |      2 |       220 | f             |          117 |          0 |               |36661 |36876 |       2 |     2 |     17669
 
19527 |       69471 | Art Deco                      |      3 |    100927 | t             |          108 |          3 |               |  528 |  529 |       1 |     3 |     19525
24929 |       72397 | Bakelite                      |      3 |     69851 | t             |          108 |          3 |               |11480 |11481 |       1 |     3 |     24923
  419 |       69471 | Art Deco                      |      3 |    100927 | t             |          117 |          0 |               |  836 |  837 |       2 |     3 |       417
 8515 |      165688 | Islam                         |      3 |      1446 | f             |          117 |          0 |               |17026 |17037 |       2 |     3 |      8481
 5555 |       13720 | Jukeboxes                     |      3 |     66502 | f             |          117 |          0 |               |11106 |11117 |       2 |     3 |      5547
 5759 |       35743 | Chips                         |      3 |       898 | f             |          117 |          0 |               |11514 |11563 |       2 |     3 |      5745
 5785 |       10909 | Dice                          |      3 |       898 | t             |          117 |          0 |               |11566 |11567 |       2 |     3 |      5745
   32 |       37911 | Hardware                      |      3 |      4707 | f             |          117 |          0 |               |   60 |   85 |       2 |     3 |        20
  449 |      163035 | Scientific Instruments        |      3 |     20094 | f             |          117 |          0 |               |  902 |  909 |       2 |     3 |       432
 8879 |         951 | Lighters                      |      3 |       593 | f             |          117 |          0 |               |17754 |17827 |       2 |     3 |      8858
 1370 |      181939 | Test, Measurement & Inspection|      3 |     92074 | f             |          117 |          0 |               | 2738 | 2981 |       2 |     3 |      1166
 9311 |       35986 | Shaving                       |      3 |       597 | f             |          117 |          0 |               |18624 |18639 |       2 |     3 |      9290
 9331 |       72397 | Bakelite                      |      3 |     69851 | t             |          117 |          0 |               |18658 |18659 |       2 |     3 |      9325
 3883 |      182059 | Vintage Accessories           |      3 |    175759 | f             |          117 |          0 |               | 7548 | 7595 |       2 |     3 |      3882
 6665 |         139 | Vintage (Pre-1968)            |      3 |       137 | f             |          117 |          0 |               |13586 |13625 |       2 |     3 |      6664
 8462 |         931 | Radios                        |      3 |     29832 | f             |          117 |          0 |               |16924 |16947 |       2 |     3 |      8455
 9873 |      175740 | Vintage Audio & Video         |      3 |    183077 | f             |          117 |          0 |               |19728 |19775 |       2 |     3 |      9872
17933 |        7317 | Game Pieces, Parts            |      3 |       233 | t             |          117 |          0 |               |36696 |36697 |       2 |     3 |     17915
17152 |       50133 | Other Vintage Sports Mem      |      3 |     50123 | t             |          117 |          0 |               |35168 |35169 |       2 |     3 |     17116
14067 |         500 | Costume                       |      3 |     48579 | f             |          117 |          0 |               |28966 |29097 |       2 |     3 |     14066
17916 |        2550 | Board & Traditional Games     |      3 |       233 | f             |          117 |          0 |               |36662 |36667 |       2 |     3 |     17915
 
 5559 |       13723 | Replacement Parts             |      4 |     13720 | t             |          117 |          0 |               |11115 |11116 |       2 |     4 |      5555
 5770 |      150119 | Poker Chips                   |      4 |     35743 | t             |          117 |          0 |               |11535 |11536 |       2 |     4 |      5759
 5771 |       63757 | Sets                          |      4 |     35743 | f             |          117 |          0 |               |11539 |11554 |       2 |     4 |      5759
 5779 |       73484 | Storage & Supplies            |      4 |     35743 | f             |          117 |          0 |               |11555 |11562 |       2 |     4 |      5759
   36 |      162933 | Drawer Pulls                  |      4 |     37911 | t             |          117 |          0 |               |   67 |   68 |       2 |     4 |        32
  450 |      163036 | Barometers                    |      4 |    163035 | t             |          117 |          0 |               |  903 |  904 |       2 |     4 |       449
 8915 |         595 | Other Collectible Lighters    |      4 |       951 | t             |          117 |          0 |               |17785 |17786 |       2 |     4 |      8879
 1429 |      181968 | Test Meters & Detectors       |      4 |    181939 | f             |          117 |          0 |               | 2903 | 2980 |       2 |     4 |      1370
 8517 |      165690 | Prayer Beads                  |      4 |    165688 | t             |          117 |          0 |               |17031 |17032 |       2 |     4 |      8515
 9313 |       35988 | Mugs, Brushes                 |      4 |     35986 | t             |          117 |          0 |               |18627 |18628 |       2 |     4 |      9311
 3884 |       74962 | Bags, Handbags & Cases        |      4 |    182059 | t             |          117 |          0 |               | 7549 | 7550 |       2 |     4 |      3883
 3903 |      182063 | Umbrellas & Parasols          |      4 |    182059 | t             |          117 |          0 |               | 7589 | 7590 |       2 |     4 |      3883
 6684 |         140 | Other Vintage Disneyana       |      4 |       139 | t             |          117 |          0 |               |13605 |13606 |       2 |     4 |      6665
 8465 |        7275 | Parts & Tubes                 |      4 |       931 | t             |          117 |          0 |               |16931 |16932 |       2 |     4 |      8462
 8468 |       38032 | Tube Radios                   |      4 |       931 | f             |          117 |          0 |               |16937 |16946 |       2 |     4 |      8462
 9882 |       50595 | Vintage Radios                |      4 |    175740 | t             |          117 |          0 |               |19763 |19764 |       2 |     4 |      9873
14081 |       58560 | Art Nouveau/Art Deco 1895-1935|      4 |       500 | f             |          117 |          0 |               |28967 |28988 |       2 |     4 |     14067
17917 |       19100 | Vintage Manufacture           |      4 |      2550 | t             |          117 |          0 |               |36665 |36666 |       2 |     4 |     17916

 1434 |       50960 | Electric Circuit & Multimeters|      5 |    181968 | f             |          117 |          0 |               | 2912 | 2921 |       2 |     5 |      1429
 1431 |       73160 | Capacitance & ESR Meters      |      5 |    181968 | t             |          117 |          0 |               | 2906 | 2907 |       2 |     5 |      1429
 5778 |       63760 | Other Casino Chip Sets        |      5 |     63757 | t             |          117 |          0 |               |11552 |11553 |       2 |     5 |      5771
 5781 |       73486 | Trays, Racks                  |      5 |     73484 | t             |          117 |          0 |               |11560 |11561 |       2 |     5 |      5779
 8470 |       38034 | 1930-49                       |      5 |     38032 | t             |          117 |          0 |               |16938 |16939 |       2 |     5 |      8468
14091 |       10967 | Other Art Deco Costume Jewelry|      5 |     58560 | t             |          117 |          0 |               |28980 |28981 |       2 |     5 |     14081

 1436 |       58277 | Multimeters                   |      6 |     50960 | t             |          117 |          0 |               | 2915 | 2916 |       2 |     6 |      1434


'''

