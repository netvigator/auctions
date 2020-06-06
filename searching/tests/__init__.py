iRecordStepsForThis = None or 383183181329


# sItemHitLog is just a starter, the file is ItemHitsLog.log
sItemHitLog = \
'''
tTimeEnd            | iItemNumb    | iHitStars
2018-03-07 20:59:24 | 132521748790 | 175
2018-03-23 21:29:45 | 401354589892 | 200
2018-03-10 11:46:09 | 372238175241 | 270
'''

#### categories for testing are in searching/tests/base.py ###

#### if you add a vacuum tube brand, ###
####  you need a BrandCategory row   ###
####    code is in base.py     ###

sBrands = \
'''
      cTitle       | iStars | cExcludeIf | cKeyWords  | cLookFor  |
-------------------+--------+------------+------------+------------
 ACRO              |      9 |            |            | Acrosound
 Acoustic Research |      7 |            |            |
 Addison           |      7 |            |            |
 Allied            |      5 |            |            |
 Altec-Lansing     |     10 |            |            | Altec
 Ampex             |      5 |            |            |
 Amperex (Bugle Boy) |    9 |            | BB\\rBugle Boy |
 Amperex           |      8 |            |            |
 Amperex (gold pins)|     9 | Amperex PQ | gold pin   |
 Amperex PQ        |      9 |            |            |
 Arvin             |      7 |            |            |
 Astronic          |      2 |            |            |
 Audio Research    |      5 |            |            |
 Bell              |      4 |            |            |
 Bendix            |      7 |            |            |
 Bogen             |      1 |            |            |
 Brociner          |      6 |            |            |
 Brook             |      8 |            |            |
 Coronado          |      7 |            |            |
 Crosley           |      3 |            |            |
 Cunningham        |      8 |            |            |
 DeWald            |      4 |            |            |
 DuKane            |      7 |            |            |
 Dynaco            |      5 |            |            | Dyna\\rDynakit
 EICO              |      7 |            |            |
 Electro-Voice     |      7 |            |            | EV
 Emerson           |      6 |            |            |
 Fada              |      8 |            |            |
 Fairchild         |      8 |            |            |
 Fisher            |      9 |            |            |
 Garod             |      5 |            |            | Garol
 GE                |      5 |            |            | General Electric
 GE (5 Star)       |      8 |            | 5 Star     | General Electric
 GEC (Genalex)     |      9 |            |            | Genalex\\rGenelex
 Genalex (Gold Lion)|    10 |            | Gold Lion  | Genelex
 Grommes           |      5 |            |            |
 Harman-Kardon     |      7 |            |            |
 Heathkit          |      8 |            |            | Heath
 Hickok            |      8 |            |            |
 Interelectronics  |      3 |            |            |
 JBL               |      7 |            |            |
 Jensen            |      8 |            |            |
 Kadette           |      6 |            |            |
 Ken-Rad           |      8 |            |            |
 KLH               |      8 |            |            |
 Klangfilm         |      6 |            |            |
 Klipsch           |      8 |            |            | Klipschorn
 Knight            |      4 |            |            |
 Lafayette         |      7 |            |            |
 Langevin          |      8 |            |            |
 Lansing           |      9 |            |            | Jim Lansing\\rJames B. Lansing
 Leak              |      7 |            |            |
 Lorenz            |      5 |            |            |
 Luxman            |      6 |            |            |
 Marantz           |     10 | Speaker\\rAV9000\\rreplica | |
 Matsushita        |      4 |            |            |
 Marconi           |      7 |            |            |
 Mazda             |      5 |            |            |
 McIntosh          |      6 |            |            |
 MFA               |      8 |            |            |
 Motorola          |      7 |            |            |
 Mullard           |      9 | IEC        |            |
 Mullard 10M       |      9 |            |            | 10M
 Mullard IEC       |      5 |            |            | IEC Mullard
 National          |      7 |            |            |
 PACO              |      2 |            |            |
 Philips           |      7 |            |            |
 Pilot             |      8 |            |            |
 Quad              |      5 |            |            |
 Radford           |      7 |            |            |
 Radio Craftsmen   |      8 |            |            |
 Raytheon          |      7 |            |            |
 RCA               |      7 |            |            |
 Regency           |      5 |            |            |
 Sargent-Rayment   |      4 |            |            |
 Scott, H.H.       |      8 |            |            | Scott\\rH.H. Scott
 Sentinel          |      6 |            |            |
 Sherwood          |      5 |            |            |
 Siemens           |      4 |            |            |
 Silvertone        |      3 |            |            |
 Spartan           |      8 |            |            |
 Stromberg-Carlson |      5 |            |            |
 Stark             |      5 |            |            |
 Supreme           |      5 |            |            |
 Sylvania          |      6 |            |            |
 Tannoy            |      7 |            |            |
 Telefunken        |      6 |            |            |
 Tung-Sol          |      7 |            |            |
 University        |      5 |            |            |
 UTC               |      8 |            |            |
 Valvo             |      5 |            |            |
 Western Electric  |      9 | Western Electric Era |  |
 Westinghouse      |      5 |            |            |
'''

# ### if you add a vacuum tube brand, ###
# ###  you need a BrandCategory row   ###
# ###    code is in base.py     ###

# 6SN7GTA\\r6SN7GTB

# ### note column delimiter | must have a space on one side or the other
sModels = \
'''
       cTitle       | cKeyWords | iStars | bSubModelsOK |      Brand        | Category     | cLookFor    | cExcludeIf   | bGenericModel | bMustHaveBrand |
--------------------+-----------+--------+--------------+-------------------+--------------+-------------+--------------+---------------+----------------+
 10                 |           |      9 | f            |                   |  Vacuum Tube |             | Lot of 10\\rLot of (10)\\r^10\\r10,000 | t
 12SN7              |           |      7 | t            |                   |  Vacuum Tube | 12SN7-GT    |              | t
 12AT7              |           |      3 | f            |                   |  Vacuum Tube |             |              | t
 12AT7 (Bugle Boy)  | Bugle Boy\\rBB | 7 | f          | Amperex (Bugle Boy) |  Vacuum Tube |             |              | f
 12AU7A             |           |      5 | t            |                   |  Vacuum Tube |             | 5814A        | t
 12AU7WA            |           |      4 | t            |                   |  Vacuum Tube |             |              | t
 12AX7 (GE)         |           |      9 | f            | GE                |  Vacuum Tube |             |              | f
 12AX7              |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 12AX7A             |           |      6 | f            |                   |  Vacuum Tube |             | 7025         | t
 7025 (12AX7A)      |           |      7 | t            |                   |  Vacuum Tube |             |              | t
 12AX7-WA           |           |      7 | t            |                   |  Vacuum Tube |             |              | t
 12AX7-WA (Philips) |           |      8 | t            | Philips           |  Vacuum Tube |             |              | f
 2A3                |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 2A3 (RCA SP)       | mono plate |    10 | f            | RCA               |  Vacuum Tube |             |              | f
 45                 |           |      8 | f            |                   |  Vacuum Tube | Type 45\\rUX-245\\rGX-245 | | t
 300B (etched base) | etched\\rengraved | 9 | t         | Western Electric  |  Vacuum Tube |             |              | f
 300B (no kws)      |           |      8 | t            | Western Electric  |  Vacuum Tube |             |              | f
 417A               |           |      7 | f            |                   |  Vacuum Tube |             |              | t
 5814A              |           |      7 | f            |                   |  Vacuum Tube |             |              | t
 5842               |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 5881               |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 5R4GA              |           |      4 | t            |                   |  Vacuum Tube |             |              | t
 5R4GYB             |           |      6 | t            |                   |  Vacuum Tube |             |              | t
 5R4WGA             |           |      4 | t            |                   |  Vacuum Tube |             |              | t
 6SN7GT (Sylvania)  |           |      8 | f            | Sylvania          |  Vacuum Tube |             |              | f
 6SN7GT             |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 6SN7GTB            |           |      6 | t            |                   |  Vacuum Tube |             |              | t
 6CA7               |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 6DJ8               |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 6DJ8 (Bugle Boy)   | Bugle Boy\\rBB | 7 | f          | Amperex (Bugle Boy) |  Vacuum Tube |             |              | f
 6922               |           |      5 | f            |                   |  Vacuum Tube |             |              | t
 6922 (Amperex Gold)| gold\\rGP |      7 | f           | Amperex (gold pins)|  Vacuum Tube |             |              | f
 6BH6               |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 6AU6A              |           |      6 | f            |                   |  Vacuum Tube | 6AU6        |              | t
 6BQ5               |           |      7 | f            |                   |  Vacuum Tube |             |              | t
 6189               |           |      3 | t            |                   |  Vacuum Tube |             |              | t
 6V6G (GE)          |           |      8 | f            | GE                |  Vacuum Tube |             |              | f
 6V6G (Sylvania)    | Sylvania\\rSilvertone | 8 | f     | Sylvania          |  Vacuum Tube |             |              | f
 6V6G               |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 6V6 (metal can)    |           |      2 | f            |                   |  Vacuum Tube |             |              | t
 6V6GTA             |           |      6 | t            |                   |  Vacuum Tube |             |              | t
 6V6GTA (RCA)       |           |      7 | f            | RCA               |  Vacuum Tube |             |              | f
 6V6GT (Mazda)      |           |      8 | f            | Mazda             |  Vacuum Tube |             |              | f
 6L6 (metal can)    |           |      4 | f            |                   |  Vacuum Tube |             |              | t
 6L6G               |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 6L6GA              |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 6L6GB              |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 6L6GC              |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 6L6WGB             |           |      8 | t            |                   |  Vacuum Tube |             |              | t
 7DJ8               |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 6201               |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 6550               |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 6550A              |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 6550 (Tung-Sol)    |           |     10 | f            | Tung-Sol          |  Vacuum Tube |             |              | f
 6550-VI            |           |      9 | f            |                   |  Vacuum Tube |             |              | t
 7308               |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 7308 (Amperex PQ)  |           |      9 | f            | Amperex PQ        |  Vacuum Tube |             |              | f
 83                 |           |      6 | f            |                   |  Vacuum Tube | VT-83       |              | t
 211                |           |      9 | f            |                   |  Vacuum Tube | VT-4C       |              | t
 8417               |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 AD1                |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 AZ1                |           |      5 | f            |                   |  Vacuum Tube |             |              | t
 CCa (= 6922)       |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 CV2492             |           |      7 | f            |                   |  Vacuum Tube |             |              | t
 CV2493             |           |      7 | f            |                   |  Vacuum Tube |             |              | t
 CV4108             |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 CV5358             |           |      7 | f            |                   |  Vacuum Tube |             |              | t
 CV5472             |           |      7 | f            |                   |  Vacuum Tube |             |              | t
 E188CC             |           |      7 | f            |                   |  Vacuum Tube |             |              | t
 E88CC              |           |      4 | f            |                   |  Vacuum Tube |             |              | t
 ECC88              |           |      7 | f            |                   |  Vacuum Tube |             |              | t
 EL34               |           |      5 | f            |                   |  Vacuum Tube |             |              | t
 EL34 (metal base)  | metal base|      9 | f            |                   |  Vacuum Tube |             |              | t
 EL34 (MB Mullard)  | metal base|     10 | f            | Mullard           |  Vacuum Tube |             |              | f
 EL34 (MB Amp BB)   | metal base|     10 | f          | Amperex (Bugle Boy) |  Vacuum Tube |             |              | f
 EF86               |           |      7 | f            |                   |  Vacuum Tube |             |              | t
 EF86 (Amperex BB)  |           |      9 | f          | Amperex (Bugle Boy) |  Vacuum Tube |             |              | f
 PCC88              |           |      7 | f            |                   |  Vacuum Tube |             |              | t
 EL84               |           |      7 | f            |                   |  Vacuum Tube |             |              | t
 KT-66              |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 VT-25 (10Y)        |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 VT-107 (6V6 metal) |           |      3 | f            |                   |  Vacuum Tube |             |              | t
 VT-107A (6V6GT)    |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 VT-107B (6V6G)     |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 TV-7               |           |      5 | f            | Supreme           |  Tube Tester |             |
 8-77               |           |      7 | f            | Stark             |  Tube Tester |             |
 100 (amp)          |           |      9 | f            | Fisher            |    Amplifier |             | X-100\\rTX-100\\r100%
 100 (speaker)      |           |      5 | f            | Fisher            |Speaker System|             | X-100\\rTX-100\\r100%
 1005B              |           |      6 | t            | Altec-Lansing     |         Horn |             |
 287F               |           |      9 | f            | Altec-Lansing     |  Theater Amp |             |
 288-8F             |           |      7 | t            | Altec-Lansing     |       Driver |             |
 288                |           |      7 | f            | Altec-Lansing     |       Driver |             |
 311-90             |           |      9 | f            | Altec-Lansing     |         Horn |             |
 414E               |           |      5 | t            | Altec-Lansing     |       Driver |             |
 415                |           |     10 | f            | Altec-Lansing     |       Driver |             |
 415C               |           |      4 | t            | Altec-Lansing     |       Driver |             | 415
 416A               |           |      7 | f            | Altec-Lansing     |       Driver |             |
 416Z               |           |      5 | t            | Altec-Lansing     |       Driver |             |
 421                |           |      5 | f            | Altec-Lansing     |       Driver |             | 421A         |
 421A               |           |      5 | t            | Altec-Lansing     |       Driver |             |
 440C               |           |      5 | t            | Altec-Lansing     |       Preamp |             |
 445A               |           |      8 | f            | Altec-Lansing     |       Preamp |             |
 511A               |           |      6 | f            | Altec-Lansing     |         Horn |             |
 515A               |           |      7 | t            | Altec-Lansing     |       Driver | 515         | 515B\\r515C  |
 542                |           |      6 | f            | Altec-Lansing     |         Horn |             |
 601a (driver)      |           |      8 | t            | Altec-Lansing     |       Driver |             |
 601B (enclosure)   |           |      7 | t            | Altec-Lansing     |Speaker Enclosure|          |
 602A               |           |      6 | t            | Altec-Lansing     |       Driver |             |
 604                |           |     10 | f            | Altec-Lansing     |       Driver |             |
 604D               |           |      8 | f            | Altec-Lansing     |       Driver |             |
 604E               |           |     10 | f            | Altec-Lansing     |       Driver |             |
 604-8G             |           |      7 | f            | Altec-Lansing     |       Driver |             |
 605A (driver)      |           |      8 | t            | Altec-Lansing     |       Driver |             |
 605A (enclosure)   |           |     10 | t            | Altec-Lansing     |Speaker Enclosure|          |
 606                |           |     10 | f            | Altec-Lansing     |Speaker Enclosure|          |
 620                |           |      8 | f            | Altec-Lansing     |Speaker Enclosure|          |
 755                |           |      7 | f            | Altec-Lansing     |       Driver | 755A        | 755C\\r755E
 755C               |           |      7 | t            | Altec-Lansing     |       Driver |             | 755\\r755A\\r755E
 755E               |           |      7 | f            | Altec-Lansing     |       Driver |             |
 803A (driver)      |           |      7 | t            | Altec-Lansing     |       Driver |             | horn         |
 803B (horn)        |           |      7 | t            | Altec-Lansing     |         Horn |             |
 804A (horn)        |           |      6 | t            | Altec-Lansing     |         Horn |             |
 806A               |           |      7 | t            | Altec-Lansing     |       Driver |             |
 808-8A             |           |      5 | t            | Altec-Lansing     |       Driver |             |
 873A (Barcelona)   |           |      7 | f            | Altec-Lansing     |Speaker System| Barcelona   |
 846B (Valencia)    |           |      7 | f            | Altec-Lansing     |Speaker System| Valencia    |
 848A (Flamenco)    |           |      7 | f            | Altec-Lansing     |Speaker System| Flamenco    |
 875A (Granada)     |           |      7 | f            | Altec-Lansing     |Speaker System| Granada     |
 890                |           |      7 | f            | Altec-Lansing     |Speaker Enclosure| Bolero   |
 811B               |           |      6 | t            | Altec-Lansing     |         Horn |             |
 A-433A             |           |      8 | t            | Altec-Lansing     |       Preamp |             |
 A-5                |           |      8 | f            | Altec-Lansing     |Speaker System|             |
 A-7                |           |      6 | f            | Altec-Lansing     |Speaker System|             |
 A7-500-II          |           |      6 | f            | Altec-Lansing     |Speaker System| Magnificent |
 N-500B             |           |      6 | t            | Altec-Lansing     |    Crossover |             |
 N-800E             |           |      6 | t            | Altec-Lansing     |    Crossover |             |
 N-1500A            |           |      6 | t            | Altec-Lansing     |    Crossover |             |
 N-1600A            |           |      6 | t            | Altec-Lansing     |    Crossover |             |
 N-3000A            |           |      6 | t            | Altec-Lansing     |    Crossover |             |
 N-3900A            |           |      6 | t            | Altec-Lansing     |    Crossover |             |
 603-b              |           |      7 | t            | Altec-Lansing     |       Driver |             |
 1569A              |           |      9 | t            | Altec-Lansing     |  Theater Amp |             |
 150-4B             |           |      9 | t            | Lansing           |       Driver |             |
 Designers Handbook | Radiotron |      6 | f            | RCA               |         Book | Designer's Handbook |
 X-100-B            |           |      4 | t            | Fisher            |Integrated Amp|             |
 XP-1A              |           |      4 | t            | Fisher            |Speaker System|             |
 XP-2B              |           |      4 | t            | Fisher            |Speaker System| XP-3        |
 XP-3B              |           |      4 | t            | Fisher            |Speaker System| XP-3        |
 XP-4B              |           |      4 | t            | Fisher            |Speaker System| XP-4        |
 XP-5B              |           |      4 | t            | Fisher            |Speaker System| XP-5        |
 XP-6A              |           |      4 | t            | Fisher            |Speaker System|             |
 XP-7A              |           |      4 | t            | Fisher            |Speaker System|             |
 XP-8A              |           |      4 | t            | Fisher            |Speaker System| XP-8        |
 XP-9B              |           |      4 | t            | Fisher            |Speaker System| XP-9        |
 XP-55B             |           |      4 | t            | Fisher            |Speaker System| XP-55       |
 HF-61A             |           |      6 | t            | EICO              |       Preamp |             |
 HF-85              |           |      7 | f            | EICO              |       Preamp |             |
 ST-84              |           |      7 | f            | EICO              |       Preamp |             |
 80-C               |           |      7 | f            | Fisher            |       Preamp |             |
 80-R               |           |      7 | f            | Fisher            |        Tuner |             |
 90-C               |           |      9 | f            | Fisher            |       Preamp |             |
 PR-6               |           |      5 | f            | Fisher            |       Preamp |             |
 PR-66              |           |      5 | f            | Fisher            |       Preamp |             |
 C-20               |           |      6 | f            | McIntosh          |       Preamp |             |
 C-11               |           |      7 | f            | McIntosh          |       Preamp |             |
 122                |           |      8 | f            | Scott, H.H.       |       Preamp |             |
 C-350              |           |      8 | f            | Radio Craftsmen   |       Preamp |             |
 HF-65              |           |      7 | f            | EICO              |       Preamp |             |
 PC-1               |           |      9 | f            | Electro-Voice     |       Preamp |             |
 210PA              |           |      6 | f            | Grommes           |       Preamp |             |
 212                |           |      5 | f            | Grommes           |       Preamp |             |
 AP-426             |           |      5 | f            | Stromberg-Carlson |       Preamp |             |
 Citation IV        |           |      9 | f            | Harman-Kardon     |       Preamp |             |
 Citation III-X     |           |      8 | f            | Harman-Kardon     |        Tuner |             |
 SP-2               |           |      5 | f            | Heathkit          |       Preamp |             |
 Point 1            |           |      8 | f            | Leak              |       Preamp |             |
 AE-2               |           |      7 | f            | McIntosh          |       Preamp |             |
 C-104              |           |      5 | f            | McIntosh          |       Preamp |             |
 PAM-1              |           |      4 | f            | Dynaco            |       Preamp |             |
 PAS-2              |           |      4 | f            | Dynaco            |       Preamp |             |
 PAS-3              |           |      7 | f            | Dynaco            |       Preamp |             | PAS-2
 PAS-3X             |           |      9 | f            | Dynaco            |       Preamp |             |
 Stereo 70          |           |      7 | f            | Dynaco            |    Amplifier | St 70       |
 A-25               |           |      8 | t            | Dynaco            |Speaker System|             |
 A-50               |           |      6 | t            | Dynaco            |Speaker System|             |
 SP-6               |           |      9 | f            | Audio Research    |       Preamp |             |
 SP-8               |           |      9 | f            | Audio Research    |       Preamp |             |
 S1001              |           |      6 | f            | ACRO              |       Preamp |             |
 116B               |           |      9 | t            | Langevin          |       Preamp |             |
 PR-100A            |           |      8 | t            | Bogen             |       Preamp |             |
 Consolette         |           |      6 | f            | Interelectronics  |       Preamp |             |
 400-C              |           |      7 | f            | Fisher            |       Preamp |             | 400-CX
 130                |           |      8 | f            | Scott, H.H.       |       Preamp |             |
 Citation I         |           |      8 | f            | Harman-Kardon     |       Preamp |             | Sixteen
 WA-P2              |           |      5 | f            | Heathkit          |       Preamp |             |
 W-3M               |           |      9 | f            | Heathkit          |    Amplifier |             |
 EA-3               |           |      4 | f            | Heathkit          |Integrated Amp|             |
 KT-600A            |           |      9 | t            | Lafayette         |       Preamp |             |
 C-4                |           |      4 | f            | McIntosh          |       Preamp |             |
 C-108H             |           |      4 | t            | McIntosh          |       Preamp |             |
 CL-35              |           |      7 | f            | Luxman            |       Preamp |             |
 Luminescence       |           |      9 | f            | MFA               |       Preamp |             |
 SC2                |           |      7 | f            | Radford           |       Preamp |             |
 C-32               |           |      7 | f            | Luxman            |       Preamp |             |
 50-C               |           |      7 | f            | Fisher            |       Preamp |             |
 CL-32              |           |      8 | f            | Luxman            |       Preamp |             |
 C-8                |           |      4 | f            | McIntosh          |       Preamp |             | C-8S
 2                  |           |      6 | f            | Acoustic Research |Speaker System| AR-2        | LST-2\\r2 way\\r(2)
 2a                 |           |      6 | f            | Acoustic Research |Speaker System| AR-2a       |
 2x                 |           |      7 | f            | Acoustic Research |Speaker System| AR-2x       |
 2ax                |           |      8 | f            | Acoustic Research |Speaker System| AR-2ax      |
 AS-21              |           |      8 | f            | Heathkit          |Speaker System|             |
 SP-1               |           |      9 | f            | Audio Research    |       Preamp |             |
 SP-2               |           |      9 | f            | Audio Research    |       Preamp |             |
 SP-3               |           |      9 | f            | Audio Research    |       Preamp |             |
 SP-3A1             |           |      9 | f            | Audio Research    |       Preamp |             |
 SP-11              |           |      9 | f            | Audio Research    |       Preamp |             |
 SP-12              |           |      9 | f            | Audio Research    |       Preamp |             |
 4B                 |           |      7 | f            | Brook             |       Preamp |             | Bryston
 10C3               |           |      8 | t            | Brook             |    Amplifier |             |
 12A3               |           |      8 | f            | Brook             |       Preamp |             |
 3G                 |           |      7 | t            | Brook             |       Preamp |             |
 7                  |           |      9 | f            | Brook             |       Preamp |             | Marantz
 A100               |           |      5 | f            | Brociner          |       Preamp |             |
 A100PV             |           |      5 | f            | Brociner          |       Preamp |             |
 A1005              |           |      5 | f            | Brociner          |       Preamp |             |
 CA-2               |           |      5 | f            | Brociner          |       Preamp |             |
 Mark 30C           |           |      5 | t            | Brociner          |       Preamp |             |
 ST-94              |           |      7 | f            | EICO              |       Preamp |             |
 Varislope Mono     |           |      7 | f            | Leak              |       Preamp |             | Stereo
 Horizon 5          |           |      6 | t            | National          |       Preamp |             |
 SP-215             |           |     10 | f            | Pilot             |       Preamp |             |
 LC-21              |           |      8 | f            | Scott, H.H.       |       Preamp |             |
 Quad 22            |           |      8 | f            | Quad              |       Preamp |             |
 C-8S               |           |      5 | f            | McIntosh          |       Preamp |             |
 SV-1               |           |      8 | f            | RCA               |       Preamp |             |
 121-C              |           |      9 | t            | Scott, H.H.       |       Preamp |             |
 C-22               |           |      7 | f            | McIntosh          |       Preamp |             | CM
 SP-210             |           |      8 | f            | Pilot             |       Preamp |             |
 Verislope 3        |           |      8 | f            | Leak              |       Preamp | Verislope\\rVarislope\\rVeriscope\\rVariscope | Mono
 240                |           |      9 | f            | Fairchild         |       Preamp |             |
 245                |           |      9 | f            | Fairchild         |       Preamp |             |
 620                |           |     10 | f            | Fairchild         |    Amplifier |             |
 QC II              |           |      8 | f            | Quad              |       Preamp |             |
 400-CX             |           |     10 | f            | Fisher            |       Preamp |             | 400-CX-2
 350-P              |           |      8 | f            | Regency           |       Preamp |             | AD1/350
 350                |           |      3 | f            | Ampex             |       Preamp |             | AD1/350
 Quad 33            |           |      2 | f            | Quad              |       Preamp |             |
 Audio Consolette   |           |     10 | f            | Marantz           |       Preamp |           1 | 1 pc\\r45\\rDD 5.1\\rDLB\\rWC-1\\rMA500\\rPMD\\r1050\\r200\\rQuad Adapter\\rSQ\\rVan Alstine\\rChannel\\rRecorder
 7                  |           |     10 | f            | Marantz           |       Preamp |             | 7 pcs\\rBrook\\r7T\\rSC-7\\rSG-7\\rfaceplate
 2                  |           |     10 | f            | Marantz           |    Amplifier | Model Two\\rModel 2 |
 400-CX (4 button)  |           |      8 | f            | Fisher            |       Preamp |             | 400-CX-2
 400-CX-2           |           |     10 | f            | Fisher            |       Preamp |             |
 FM-1000            |           |     10 | f            | Fisher            |        Tuner |             |
 R-200              |           |      8 | f            | Fisher            |        Tuner |             |
 SA-1000            |           |     10 | f            | Fisher            |    Amplifier |             |
 mirror             |           |      8 | f            | Spartan           |        Radio |             |
 RC350              |           |      8 | f            | RCA               |        Radio |             |
 126                |           |      8 | f            | Garod             |        Radio |             |
 R5A1               |           |      7 | f            | Addison           |        Radio |             |
 50XC               |           |      7 | f            | Motorola          |        Radio |             |
 1465               |           |      8 | f            | Crosley           |        Radio |             |
 66X8               |           |      8 | f            | RCA               |        Radio |             |
 43-8190            |           |      8 | f            | Coronado          |        Radio |             |
 AX-235             |           |      8 | f            | Emerson           |        Radio |             |
 A5                 |           |      8 | f            | Addison           |        Radio |             |
 526-C              |           |      7 | t            | Bendix            |        Radio |             |
 E38                |           |      5 | f            | Lafayette         |        Radio |             |
 51x16 S            |           |      6 | f            | Motorola          |        Radio |             |
 284-N              |           |      7 | t            | Sentinel          |        Radio |             |
 R5A3               |           |      9 | f            | Addison           |        Radio |             |
 51x16              |           |      6 | f            | Motorola          |        Radio |             |
 A-502              |           |      8 | f            | DeWald            |        Radio |             |
 L-570              |           |      8 | f            | GE                |        Radio |             |
 1B55L              |           |      8 | t            | Garod             |        Radio |             |
 557                |           |      8 | f            | Spartan           |        Radio |             |
 L-622              |           |      8 | f            | GE                |        Radio |             |
 3284               |           |      5 | f            | Silvertone        |        Radio |             |
 P38                |           |      4 | f            | Fada              |        Radio |             |
 BT245              |           |      8 | f            | Emerson           |        Radio |             |
 558                |           |      8 | f            | Spartan           |        Radio |             |
 66X9               |           |      6 | f            | RCA               |        Radio |             |
 EP-375             |           |      9 | f            | Emerson           |        Radio |             |
 A-501              |           |      7 | f            | DeWald            |        Radio |             |
 H136               |           |      8 | f            | Westinghouse      |        Radio |             |
 V-3468             |           |      8 | f            | Westinghouse      |        Radio |             |
 Bluebird           |           |      8 | f            | Spartan           |        Radio |             |
 520                |           |      7 | f            | Emerson           |        Radio |             |
 1450               |           |      8 | f            | Garod             |        Radio |             |
 B501               |           |      7 | f            | DeWald            |        Radio |             |
 A2A                |           |      7 | t            | Addison           |        Radio |             |
 BM258              |           |      6 | t            | Emerson           |        Radio |             |
 50-X-C3            |           |      7 | t            | Motorola          |        Radio |             |
 50-XC4             |           |      9 | t            | Motorola          |        Radio |             |
 532                |           |      8 | f            | Arvin             |        Radio |             |
 H126               |           |      8 | f            | Westinghouse      |        Radio |             |
 6AU-1              |           |      9 | t            | Garod             |        Radio |             |
 AU-190             |           |      8 | f            | Emerson           |        Radio |             |
 2A                 |           |      8 | f            | Addison           |        Radio |             |
 700                |           |     10 | f            | Fada              |        Radio |             |
 K25                |           |      7 | f            | Kadette           |        Radio |             |
 711                |           |      8 | f            | Fada              |        Radio |             |
 53X                |           |      8 | f            | Fada              |        Radio |             |
 652                |           |      0 | f            | Fada              |        Radio |             |
 400                |           |      7 | f            | Emerson           |        Radio |             |
 537                |           |      8 | f            | Spartan           |        Radio |             |
 F55                |           |      8 | f            | Fada              |        Radio |             |
 51C                |           |      8 | t            | Motorola          |        Radio |             |
 5                  |           |      9 | f            | Addison           |        Radio |             | 5 NOS\\r5 ea\\r5 each\\r5 pack\\r5 pair\\r5 pcs\\rbox of 5\\rqty 5
 115                | Catalin   |      8 | f            | Fada              |        Radio |             |
 136                | Catalin   |      9 | f            | Fada              |        Radio |             |
 116                | Catalin   |      8 | f            | Fada              |        Radio |             |
 845                |           |      6 | f            | Fada              |        Radio |             |
 1000               | Catalin   |      9 | f            | Fada              |        Radio |             | 115
 511                |           |      8 | f            | Emerson           |        Radio |             |
 5F60               |           |      9 | f            | Fada              |        Radio |             |
 L 56               |           |      8 | f            | Fada              |        Radio |             |
 5F50               |           |      7 | f            | Fada              |        Radio |             |
 526-MC             |           |      5 | f            | Bendix            |        Radio |             |
 248-NI             |           |     10 | f            | Sentinel          |        Radio |             |
 235                |           |      7 | f            | Emerson           |        Radio | Little Miracle |
 H-222              |           |      7 | f            | Jensen            |       Driver |             |
 A-402              |           |      8 | f            | Jensen            |    Crossover |             |
 A-61               |           |      7 | f            | Jensen            |    Crossover |             |
 M1131              |           |      6 | f            | Jensen            |        Choke |             |
 RP-302A            |           |      6 | t            | Jensen            |       Driver |             |
 RP-201             |           |      8 | t            | Jensen            |       Driver |             |
 P15-LS             |           |      5 | t            | Jensen            |       Driver |             |
 Imperial           |           |      9 | f            | Jensen            |Speaker System|             |
 15" Silver         |           |      7 | f            | Tannoy            |       Driver |             |
 GRF                |           |      7 | f            | Tannoy            |Speaker Enclosure|          |
 539-A              |           |      5 | f            | Hickok            |  Tube Tester |             |
 539-B              |           |      9 | f            | Hickok            |  Tube Tester |             |
 539-C              |           |      5 | f            | Hickok            |  Tube Tester |             |
 600A               |           |      5 | t            | Hickok            |  Tube Tester |             |
 6000A              |           |      6 | t            | Hickok            |  Tube Tester |             |
 75                 |           |     10 | f            | JBL               |       Driver | 075         |
 76                 |           |      6 | f            | JBL               |       Driver | 076         |
 175                |           |     10 | f            | JBL               |       Driver |             |
 LE-175             |           |      8 | f            | JBL               |       Driver |             |
 275                |           |     10 | f            | JBL               |       Driver |             |
 D-130              |           |      7 | f            | JBL               |       Driver | 130         |
 D-130A             |           |      7 | f            | JBL               |       Driver | 130A        |
 D-130B             |           |      7 | f            | JBL               |       Driver | 130B        |
 LE5-5              |           |      5 | t            | JBL               |       Driver |             |
 LE14A              |           |      8 | f            | JBL               |       Driver |             |
 1217-1290          |           |      7 | f            | JBL               |         Horn |             |
 H5040              |           |      7 | f            | JBL               |         Horn |             |
 N2400              |           |      6 | f            | JBL               |    Crossover |             |
 N2600              |           |      6 | f            | JBL               |    Crossover |             |
 N500               |           |      6 | f            | JBL               |    Crossover |             |
 C38 (Baron)        |           |      8 | f            | JBL               |Speaker Enclosure| Baron    | S-38\\rBookshelf\\rN-38
 C45 (Metregon)     |           |      6 | f            | JBL               |Speaker Enclosure| Metregon |
 L220 (Oracle)      |           |      6 | f            | JBL               |Speaker System|             |
 CA-5               |           |      5 | f            | Hickok            |    Accessory |             |
 CA-3               |           |      5 | t            | Hickok            |    Accessory |             | CA-5
 Heresy (H700)      |           |      6 | f            | Klipsch           |Speaker System|             |
 K-22               |           |      6 | f            | Klipsch           |       Driver |             |
 K-55-V             |           |      6 | f            | Klipsch           |       Driver |             |
 K-77               |           |      6 | f            | Klipsch           |       Driver |             |
 K-700              |           |      6 | f            | Klipsch           |         Horn |             |
 KS-15874           |           |      9 | f            | Western Electric  |  Tube Tester |             |
 755A               |           |      8 | t            | Western Electric  |       Driver |             |
 T-35B              |           |      6 | t            | University        |       Driver |             |
 T-350B             |           |      7 | t            | University        |       Driver |             |
 LK-72              |           |      5 | f            | Scott, H.H.       |Integrated Amp|             |
 240                |           |      9 | f            | Scott, H.H.       |    Amplifier |             |
 240                |           |      6 | f            | Pilot             |Integrated Amp|             |
 Patrician          |           |      9 | f            | Electro-Voice     |Speaker System|             |
 Regency            |           |      7 | f            | Electro-Voice     |Speaker System|             |
 18WK               |           |      8 | f            | Electro-Voice     |       Driver |             |
 T-25-A             |           |      7 | t            | Electro-Voice     |       Driver |             |
 T-35B              |           |      7 | t            | Electro-Voice     |       Driver |             |
 T-350B             |           |      7 | t            | Electro-Voice     |       Driver |             |
 T-250              |           |      7 | t            | Electro-Voice     |       Driver |             |
 828-HFB            |           |      6 | t            | Electro-Voice     |       Driver |             |
 6HD                |           |      5 | f            | Electro-Voice     |         Horn |             |
 8HD                |           |      5 | f            | Electro-Voice     |         Horn |             |
 X36                |           |      6 | f            | Electro-Voice     |    Crossover |             |
 TO-300             |           |      7 | f            | ACRO              |Output Transformer|         |
 meter              |           |      3 | f            |                   |    Component |             |
 1                  |           |      6 | f            | Acoustic Research |Speaker System| AR-1\\rOne  |Tower\\rGES Acoustic\\rHC-1\\rSUB\\r1 pair\\rOne Only\\rone pair\\rone owner\\rone previous owner\\r1 of\\rone of\\rMC.1\\rAthena\\rHome Theater\\ronly One
 nine               |           |      9 | f            | KLH               |Speaker System|             |
 IT-28              |           |      5 | f            | Heathkit          |Capacitor Checker|          | Capacitor Tester\rCapacitance Checker\rCapacitance Tester
 '''
#      cTitle       | cKeyWords | iStars | bSubModelsOK |      Brand        | Category     | cLookFor    | cExcludeIf   | bGenericModel | bMustHaveBrand |


dSearchResult = \
{'autoPay': 'false',
 'condition': {'conditionDisplayName': 'New', 'conditionId': '1000'},
 'country': 'US',
 'galleryURL': 'http://thumbs3.ebaystatic.com/m/mutHoe85kv1_SUEGG3k1yBw/140.jpg',
 'globalId': 'EBAY-US',
 'isMultiVariationListing': 'false',
 'itemId': '282330751118',
 'listingInfo': {
     'bestOfferEnabled': 'true',
    'buyItNowAvailable': 'false',
    'endTime': '2018-02-13T00:34:26.000Z',
    'gift': 'false',
    'listingType': 'Auction',
    'startTime': '2017-01-19T00:34:26.000Z',
    'watchCount': '19'},
 'location': 'Staten Island,NY,USA',
 'paginationOutput': {
     'entriesPerPage': '100',
    'pageNumber': '1',
    'thisEntry': '1',
    'totalEntries': '1320',
    'totalPages': '14'},
 'paymentMethod': 'PayPal',
 'postalCode': '10303',
 'primaryCategory': {'categoryId': '73160','categoryName': 'Capacitance & ESR Meters'},
 'returnsAccepted': 'true',
 'sellingStatus': {
    'convertedCurrentPrice': {'@currencyId': 'USD','__value__': '27.99'},
    'currentPrice': {'@currencyId': 'USD', '__value__': '27.99'},
    'sellingState': 'Active',
    'timeLeft': 'P13DT6H33M56S'},
    'shippingInfo': {'expeditedShipping': 'false',
  'handlingTime': '1',
  'oneDayShippingAvailable': 'false',
  'shipToLocations': 'Worldwide',
  'shippingServiceCost': {'@currencyId': 'USD', '__value__': '0.0'},
  'shippingType': 'Free'},
 'title': 'Digital Capacitance Tester Capacitor Meter Auto Range Multimeter Checker 470mF',
 'topRatedListing': 'true',
 'viewItemURL': 'http://www.ebay.com/itm/Digital-Capacitance-Tester-Capacitor-Meter-Auto-Range-MultimeterChecker-470mF-/282330751118'
 }

#### do not add new test items above, add them below ###
#### do not add new test items above, add them below ###
#### do not add new test items above, add them below ###

iExampleResponseCount = 5

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
          { "itemId":["253313715173" ],"isMultiVariationListing":["false" ],
              "topRatedListing":["false" ],
              "globalId":["EBAY-US" ],
              "title":["Simpson 360-2 Digital Volt-Ohm Milliammeter Operator's Manual" ],
              "country":["US" ],
              "shippingInfo":[{
                "expeditedShipping":["false" ],
                "shippingType":["Calculated" ],
                "handlingTime":["3" ],
                "shipToLocations":["Worldwide" ],
                "oneDayShippingAvailable":["false" ]}],
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

            },{ "itemId":["233420619849"],
                "title":["6GM8 / ECC86 Vacuum Tube, New Tested "],
                "globalId":["EBAY-US"],
                "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
                "secondaryCategory":[{"categoryId":["80741"],"categoryName":["Radio & Speaker Systems"]}],
                "galleryURL":["https://thumbs2.ebaystatic.com/m/mES0laZ3ya2KZIT9Jp4TPFg/140.jpg"],
                "viewItemURL":["https://www.ebay.com/itm/6GM8-ECC86-Vacuum-Tube-New-Tested-/233420619849"],
                "paymentMethod":["PayPal"],"autoPay":["false"],
                "postalCode":["239**"],"location":["Clarksville,VA,USA"],"country":["US"],
                "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
                "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.95"}],
                "bidCount":["0"],"sellingState":["Active"],
                "timeLeft":["P4DT20H53M9S"]}],
                "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
                "startTime":["2019-12-01T19:16:01.000Z"],
                "endTime":["2019-12-08T19:16:01.000Z"],
                "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["true"],
                "condition":[{"conditionId":["1500"],"conditionDisplayName":["Open box"]}],
                "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["132401762082" ],"isMultiVariationListing":["false" ],
              "topRatedListing":["false" ],
              "globalId":["EBAY-US" ],
              "title":["Simpson 360 Digital Multi Meter Volt Ohm Milliameter Working" ],
              "country":["US" ],
              "shippingInfo":[{
                "expeditedShipping":["false" ],
                "handlingTime":["2" ],
                "shippingServiceCost":[{"@currencyId": "USD", "__value__": "0.0"}],
                "oneDayShippingAvailable":["false" ],
                "shipToLocations":["Worldwide" ],
                "shippingType":["Free" ] } ],
              "galleryURL":["http://thumbs3.ebaystatic.com/m/mc2iTJIYDZVO0Nh-w2n1Tzw/140.jpg" ],
              "autoPay":["false" ],
              "location":["Bellmore,NY,USA" ],
              "postalCode":["11710" ],
              "returnsAccepted":["false" ],
              "viewItemURL":["http://www.ebay.com/itm/Simpson-360-Digital-Multi-Meter-Volt-Ohm-Milliameter-Working-/132401762082" ],
              "sellingStatus":[{
                "currentPrice":[{ "@currencyId": "USD", "__value__": "79.99" } ],
                "timeLeft":["P1DT6H52M48S" ],
                "convertedCurrentPrice":[{ "@currencyId": "USD", "__value__": "79.99"}],
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

            },{"itemId":["253303813311" ],"isMultiVariationListing":["false" ],
              "topRatedListing":["false" ],
              "globalId":["EBAY-US" ],
              "title":["SIMPSON 360-2 RUNII DIGITAL OHM -VOLT METER #12286" ],
              "country":["US" ],
              "shippingInfo":[
                { "expeditedShipping":["true" ],
                "handlingTime":["3" ],
                "shippingServiceCost":[{ "@currencyId": "USD", "__value__": "0.0" }],
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

            },{"itemId":["253295991282" ],"isMultiVariationListing":["false" ],
              "topRatedListing":["false" ],
              "globalId":["EBAY-US" ],
              "title":["Simpson 360 Multimeter" ],
              "country":["US" ],
              "shippingInfo":[
                { "expeditedShipping":["false" ],
                "handlingTime":["2" ],
                "shippingServiceCost":[{ "@currencyId": "USD", "__value__": "10.0" }],
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
                "endTime":["2018-01-04T14:01:02.000Z" ] } ]

                } ],
          "@count": "5" }
      ],
      "version":["1.13.0" ] } ]
}'''
#### do not add new test items above, add them below ###
#### do not add new test items above, add them below ###
#### do not add new test items above, add them below ###

# ###      if you add an item whose title includes a double quote,       ###
# ### you must manually convert a signle backslash to a double backslash ###
# ###      also first item is tested in core.test_utils_ebay             ###

# helpful useful regex re for splitting item info: .(?=,")

sResponseItems2Test = \
'''{"findItemsByKeywordsResponse":
  [{"ack":["Success"],"version":["1.13.0"],"timestamp":["2018-03-03T23:04:24.581Z"],
    "searchResult":
      [{"@count":"100",
        "item": [
           { "itemId":["122990519283"],
             "title":["Garol 6AU-1 Catalin Radio "],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
             "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mqcfM87dPUKfbuWlIpUTi-w\/140.jpg"],
             "viewItemURL":["http:\/\/www.ebay.com\/itm\/Garol-6AU-1-Catalin-Radio-\/122990519283"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["15085"],"location":["Trafford,PA,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"563.88"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"563.88"}],"bidCount":["14"],"sellingState":["Active"],"timeLeft":["P0DT3H38M14S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2018-02-27T02:42:38.000Z"],
             "endTime":["2018-03-04T02:42:38.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["44"]}],"returnsAccepted":["true"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["true"]

         },{ "itemId":["193480815469"],
             "title":["Antique FADA vintage Catalin tube radio model Dip-Top 711 working price reduced"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["38034"],"categoryName":["1930-49"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mqJjsVU-D1s347x-WJyHbYQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Antique-FADA-vintage-Catalin-tube-radio-model-Dip-Top-711-working-price-reduced-\/193480815469"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["301**"],"location":["Acworth,GA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"30.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"355.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"355.0"}],
             "bidCount":["11"],"sellingState":["Active"],"timeLeft":["P2DT23H4M31S"]}],"listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-05-24T21:16:10.000Z"],
             "endTime":["2020-05-31T21:15:10.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["40"]}],"returnsAccepted":["false"],
             "galleryPlusPictureURL":["https:\/\/galleryplus.ebayimg.com\/ws\/web\/193480815469_1_0_1.jpg"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["233597629477"],
             "title":["2A3 Single Mono Plate RCA Cunningham"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/m-tV-EBfayw4qaGNZhJ741Q\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/2A3-Single-Mono-Plate-RCA-Cunningham-\/233597629477"],
             "paymentMethod":["PayPal","VisaMC"],"autoPay":["false"],
             "location":["Hong Kong"],"country":["HK"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"30.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"0.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"0.99"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P2DT5H44M19S"]}],"listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-05-24T03:57:01.000Z"],
             "endTime":["2020-05-31T03:57:01.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["7"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["7000"],"conditionDisplayName":["For parts or not working"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["264741220720"],
             "title":["1  excellent mil spec general electric 12ax7wa \/ 12ax7 tube  # K 69"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs1.ebaystatic.com\/m\/malOZ5WH8GFiipSCgTasBwQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/1-excellent-mil-spec-general-electric-12ax7wa-12ax7-tube-K-69-\/264741220720"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["457**"],"location":["Belpre,OH,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"7.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["5"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],
             "bidCount":["1"],"sellingState":["Active"],"timeLeft":["P0DT3H44M29S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2020-05-24T01:56:25.000Z"],"endTime":["2020-05-29T01:56:25.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["2"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["174290984997"],
             "title":["10 vntg 12AX7A ~ Raytheon ~Black Plate~ Tube lot TV-7 & Hi-Fi Tested 12AX7   rca"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/m_yHMS3VSLkaC1ZzA7veGZg\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/10-vntg-12AX7A-Raytheon-Black-Plate-Tube-lot-TV-7-Hi-Fi-Tested-12AX7-rca-\/174290984997"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "location":["USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"9.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"59.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"59.99"}],
             "bidCount":["7"],"sellingState":["Active"],"timeLeft":["P2DT13H37M1S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-05-22T12:00:05.000Z"],
             "endTime":["2020-05-25T12:00:05.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["12"]}],"returnsAccepted":["true"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["true"]

         },{ "itemId":["174291344087"],
             "title":["7308 Audiophile Vacuum Tube Very Rare Superb Sound - CV4108 E188CC Raytheon Amp"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/m5sP0epErlCpCMHpDhqVhig\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/7308-Audiophile-Vacuum-Tube-Very-Rare-Superb-Sound-CV4108-E188CC-Raytheon-Amp-\/174291344087"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["902**"],"location":["Redondo Beach,CA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"13.79"}],"shippingType":["FlatDomesticCalculatedInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"99.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"99.99"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P9DT17H14M2S"]}],"listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-05-22T15:37:24.000Z"],
             "endTime":["2020-06-01T15:37:24.000Z"],
             "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["1500"],"conditionDisplayName":["Open box"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["133401627353"],
             "title":["Matched Pair EL34 6CA7 Bugle Boy (Mullard) Metal Base Tubes SY1 57C 1957"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mRdOIaW84CBGMma5mgb443w\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Matched-Pair-EL34-6CA7-Bugle-Boy-Mullard-Metal-Base-Tubes-SY1-57C-1957-\/133401627353"],
             "paymentMethod":["CashOnPickup","PayPal"],"autoPay":["false"],
             "postalCode":["974**"],"location":["Eugene,OR,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"6.75"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"499.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"499.0"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P1DT0H2M37S"]}],"listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-05-03T22:02:50.000Z"],
             "endTime":["2020-05-10T22:02:50.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["9"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["1500"],"conditionDisplayName":["Open box"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["184284149755"],
             "title":["Electro Voice EV Vintage FiberGlass 8HD Horn Pair Speaker T10 T25 T250 A"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/m0TIUkJlMwsBfU9B74FGJAQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Electro-Voice-EV-Vintage-FiberGlass-8HD-Horn-Pair-Speaker-T10-T25-T250-\/184284149755"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["463**"],"location":["Westville,IN,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"74.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"74.99"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P5DT15H33M28S"]}],"listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"97.49"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"97.49"}],
             "startTime":["2020-05-08T13:32:08.000Z"],
             "endTime":["2020-05-15T13:32:08.000Z"],
             "listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["2"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["153920100946"],
             "title":["Jensen Vintage 16 Ohm A-402 Crossover Network Pair Speaker RP302 Imperial "],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/m9blZu8Fe2c3f2fxComLaLQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Jensen-Vintage-16-Ohm-A-402-Crossover-Network-Pair-Speaker-RP302-Imperial-\/153920100946"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["463**"],"location":["Westville,IN,USA"],"country":["US"],"shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"299.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"299.99"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P2DT16H38M29S"]}],"listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"389.99"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"389.99"}],
             "startTime":["2020-05-05T14:37:04.000Z"],
             "endTime":["2020-05-12T14:37:04.000Z"],
             "listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["5"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["353067866152"],
             "title":["1 vintage factory built Jensen PR-100 Imperial speaker  p15ll  rp-302  rp-201"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs1.ebaystatic.com\/m\/mtqsZlbiB3swQFbbM1v3rYQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/1-vintage-factory-built-Jensen-PR-100-Imperial-speaker-p15ll-rp-302-rp-201-\/353067866152"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["467**"],"location":["New Haven,IN,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"3000.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"3000.0"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P1DT2H32M9S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-05-04T00:30:44.000Z"],
             "endTime":["2020-05-11T00:30:44.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["17"]}],"returnsAccepted":["true"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["184281669249"],
             "title":["Electro Voice EV Vintage 16 Ohm X36 Crossover Network Pair Speaker T35 T350 B "],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mvw0gkYWVk6xgN9Jhb3rY8A\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Electro-Voice-EV-Vintage-16-Ohm-X36-Crossover-Network-Pair-Speaker-T35-T350-B-\/184281669249"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["463**"],"location":["Westville,IN,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"74.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"74.99"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P3DT17H4M46S"]}],"listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"97.49"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"97.49"}],
             "startTime":["2020-05-06T15:06:33.000Z"],
             "endTime":["2020-05-13T15:06:33.000Z"],
             "listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["3"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["293562589789"],
             "title":["JBL M31 (looks Like D130) Needs are-Coned"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mOCSR5ghYCGE7W--74xFB-g\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/JBL-M31-looks-Like-D130-Needs-are-Coned-\/293562589789"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["430**"],"location":["Newark,OH,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"60.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"60.0"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P3DT17H1M46S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"80.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"80.0"}],
             "startTime":["2020-04-28T19:34:51.000Z"],
             "endTime":["2020-05-05T19:34:51.000Z"],
             "listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["2"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["7000"],"conditionDisplayName":["For parts or not working"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["362980614720"],
             "title":["VT25  Western Electric Tube Valve matched pair NOS NIB not 300B 2a3 45 211"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs1.ebaystatic.com\/m\/m2THCudwB30JKVh43mQgveg\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/VT25-Western-Electric-Tube-Valve-matched-pair-NOS-NIB-not-300B-2a3-45-211-\/362980614720"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "location":["Taiwan"],"country":["TW"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"15.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"299.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"299.0"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P0DT5H57M47S"]}],"listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-04-27T08:31:37.000Z"],
             "endTime":["2020-05-02T08:31:37.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["10"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["1000"],"conditionDisplayName":["New"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["233573519366"],
             "title":["Westinghouse 6550 vintage tube"],
             "globalId":["EBAY-ENCA"],"primaryCategory":[{"categoryId":["64627"],
             "categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/mF3ji-T_pgJESpwOyKm_MKg\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Westinghouse-6550-vintage-tube-\/233573519366"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["L8P2H5"],"location":["Canada"],"country":["CA"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"CAD","__value__":"20.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"14.4"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P1DT21H24M50S"]}],"listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-04-29T00:00:47.000Z"],
             "endTime":["2020-05-04T00:00:47.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["4"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["184168518275"],
             "title":["****Jensen Vintage 16 Ohm A-402 Crossover Network Speaker RP302 Imperial "],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mSRnSjej5JT6R9ROD1pIdAg\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Jensen-Vintage-16-Ohm-A-402-Crossover-Network-Speaker-RP302-Imperial-\/184168518275"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["097**"],"location":["APO,  Armed Forces Europe,  The Middle East,  & Canada.,  USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"15.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"125.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"125.0"}],"sellingState":["Active"],"timeLeft":["P19DT3H6M29S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-02-12T23:44:37.000Z"],
             "endTime":["2020-05-12T23:44:37.000Z"],
             "listingType":["StoreInventory"],"gift":["false"],"watchCount":["7"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["283709382058"],
             "title":["Vintage Altec 875A Granada Horn Speaker Pair - Barcelona Valencia Family"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/mxL5vSAk5xmZDSQ-s-p0XZQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Vintage-Altec-875A-Granada-Horn-Speaker-Pair-Barcelona-Valencia-Family-\/283709382058"],
             "paymentMethod":["PayPal","VisaMC","AmEx","Discover"],"autoPay":["false"],
             "postalCode":["941**"],"location":["San Francisco,CA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"1990.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"1990.0"}],
             "sellingState":["Active"],"timeLeft":["P19DT22H52M58S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-12-13T19:29:26.000Z"],
             "endTime":["2020-05-13T19:29:26.000Z"],
             "listingType":["StoreInventory"],"gift":["false"],"watchCount":["155"]}],
             "returnsAccepted":["false"],"isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["133392165411"],
             "title":["Western Electric 300B tube >engraved base<"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/m-waC1FAtPYSse4hQYYaWlA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Western-Electric-300B-tube-engraved-base-\/133392165411"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["481**"],"location":["Germany"],"country":["DE"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["4"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"1525.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"1525.0"}],
             "bidCount":["23"],"sellingState":["Active"],"timeLeft":["P7DT14H45M0S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-04-21T11:27:57.000Z"],
             "endTime":["2020-05-01T11:27:57.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["11"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["1500"],"conditionDisplayName":["Open box"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["174253058987"],
             "title":["British Made Mullard 7DJ8 PCC88 Tube Valve -6DJ8 ECC88 sub -Warm Old School hifi"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mhU31HbfWCOC_nPygU3mPMQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/British-Made-Mullard-7DJ8-PCC88-Tube-Valve-6DJ8-ECC88-sub-Warm-Old-School-hifi-\/174253058987"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["902**"],"location":["Redondo Beach,CA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"14.5"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"59.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"59.99"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P2DT22H28M37S"]}],"listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-04-16T19:10:36.000Z"],
             "endTime":["2020-04-26T19:10:36.000Z"],
             "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["254574295997"],
             "title":["IEC Mullard 6922 \/ E88CC \/ 6DJ8 Gold Pin Tube"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/me997L6uSDbIYwZ5kDT-F9g\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/IEC-Mullard-6922-E88CC-6DJ8-Gold-Pin-Tube-\/254574295997"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["301**"],"location":["Kennesaw,GA,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"60.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"60.0"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P3DT5H19M13S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-04-20T02:01:07.000Z"],
             "endTime":["2020-04-27T02:01:07.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["352961821505"],
             "title":["1 altec 287F amplifier meter panel "],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["67815"],"categoryName":["Vintage Transformers"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/m5F3UlEGH3-Gsx01G33X0qA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/1-altec-287F-amplifier-meter-panel-\/352961821505"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "location":["USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"15.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"199.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"199.99"}],
             "sellingState":["Active"],"timeLeft":["P16DT3H35M56S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-02-06T03:13:47.000Z"],
             "endTime":["2020-05-06T03:13:47.000Z"],
             "listingType":["StoreInventory"],"gift":["false"],"watchCount":["2"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["313048572053"],
             "title":["11 Vintage 60's Western Electric 417A 5842 Bent D Getter Amplifier Tube Bulk Lot"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/m5yXTRCH7Ro7T5UH92kjR1A\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/11-Vintage-60s-Western-Electric-417A-5842-Bent-D-Getter-Amplifier-Tube-Bulk-Lot-\/313048572053"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["981**"],"location":["Seattle,WA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"8.95"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"61.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"61.5"}],"bidCount":["13"],"sellingState":["Active"],"timeLeft":["P5DT1H56M54S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-04-08T00:26:24.000Z"],
             "endTime":["2020-04-15T00:26:24.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["26"]}],"returnsAccepted":["true"],
             "galleryPlusPictureURL":["https:\/\/galleryplus.ebayimg.com\/ws\/web\/313048572053_1_0_1.jpg"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["283830240734"],
             "title":["Vtg 60s ALTEC FLAMENCO 848A Speaker Set Horn 416Z 806A N800F 16ohm Valencia VOTT"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/muZ3DMgOk1mOOE5dSexaztA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Vtg-60s-ALTEC-FLAMENCO-848A-Speaker-Set-Horn-416Z-806A-N800F-16ohm-Valencia-VOTT-\/283830240734"],
             "paymentMethod":["CashOnPickup","PayPal"],"autoPay":["false"],
             "postalCode":["846**"],"location":["Spanish Fork,UT,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"2200.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"2200.0"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P2DT1H18M24S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-03-28T23:20:37.000Z"],
             "endTime":["2020-04-04T23:20:37.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["6"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["174236717488"],
             "title":["Telefunken E88CC\/01 w\/ Mullard label <> audiophono grade 6922 CCA 6DJ8 Gold Pins"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs1.ebaystatic.com\/m\/mcXBeU_-a8ZIRSwT2ign8DQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Telefunken-E88CC-01-w-Mullard-label-audiophono-grade-6922-CCA-6DJ8-Gold-Pins-\/174236717488"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["902**"],"location":["Redondo Beach,CA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"16.49"}],"shippingType":["FlatDomesticCalculatedInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"245.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"245.0"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P7DT20H33M21S"]}],"listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-03-31T18:38:00.000Z"],"endTime":["2020-04-10T18:38:00.000Z"],"listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["1500"],"conditionDisplayName":["Open box"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["313033073507"],
             "title":["VINTAGE ALTEC LANSING 755E speakers - Pair"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mFLVQBgmfHQGNtgrgWW4rrg\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/VINTAGE-ALTEC-LANSING-755E-speakers-Pair-\/313033073507"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["631**"],"location":["Saint Louis,MO,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"1100.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"1100.0"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P5DT7H51M18S"]}],"listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-03-19T21:29:56.000Z"],
             "endTime":["2020-03-29T21:29:56.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["114154224682"],
             "title":["HEATHKIT TUBE AMPLIFIER EA-3   \/ UA-2 \/ UA-1"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/mciSDfgh3FutxyA-pCEetNA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/HEATHKIT-TUBE-AMPLIFIER-EA-3-UA-2-UA-1-\/114154224682"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["934**"],"location":["San Luis Obispo,CA,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"38.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"38.0"}],
             "bidCount":["9"],"sellingState":["Active"],"timeLeft":["P2DT6H42M13S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-03-19T20:20:36.000Z"],
             "endTime":["2020-03-26T20:20:36.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["23"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["7000"],"conditionDisplayName":["For parts or not working"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["174226403478"],
             "title":["4 pcs - RCA 6922 vintage vacuum tube quad - E88CC 6DJ8 CV2492 CCa - valves"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/mtkhUKKLIVWslB85XTDIHsg\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/4-pcs-RCA-6922-vintage-vacuum-tube-quad-E88CC-6DJ8-CV2492-CCa-valves-\/174226403478"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["905**"],"location":["Torrance,CA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"13.5"}],"shippingType":["FlatDomesticCalculatedInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"165.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"165.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P6DT16H27M29S"]}],"listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-03-21T06:07:49.000Z"],
             "endTime":["2020-03-31T06:07:49.000Z"],"listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["324090682443"],
             "title":["GOLD LION KT66 Vacuum tube 1 GENELEX logo MADE in UK M-Osram valve No Reserve"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mX818FRkURdFbbTw7zVbQVA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/GOLD-LION-KT66-Vacuum-tube-1-GENELEX-logo-MADE-UK-M-Osram-valve-No-Reserve-\/324090682443"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["926**"],"location":["Ladera Ranch,CA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"8.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["4"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"69.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"69.0"}],
             "bidCount":["11"],"sellingState":["Active"],"timeLeft":["P5DT18H29M6S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-03-02T19:54:54.000Z"],
             "endTime":["2020-03-09T19:54:54.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["10"]}],"returnsAccepted":["true"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["383441473993"],
             "title":["BROOK 10C Tube Amplifier   Western Electric Fairchild 620 300B 2A3   Tested 10C3"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mC3dPpoXHK24a_3dCG86xqw\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/BROOK-10C-Tube-Amplifier-Western-Electric-Fairchild-620-300B-2A3-Tested-10C3-\/383441473993"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["294**"],"location":["Charleston,SC,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"1660.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"1660.0"}],
             "bidCount":["2"],"sellingState":["Active"],"timeLeft":["P0DT19H49M42S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-02-28T23:35:03.000Z"],
             "endTime":["2020-02-29T23:35:03.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["9"]}],"returnsAccepted":["true"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["254524704215"],
             "title":["15 x EL84 Telefunken Valvo Siemens Lorenz 6BQ5 old version Made in West Germany"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mNHguNcTo4Qc6wHCmFNod_w\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/15-x-EL84-Telefunken-Valvo-Siemens-Lorenz-6BQ5-old-version-Made-West-Germany-\/254524704215"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["448**"],
             "location":["Germany"],"country":["DE"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"15.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"34.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"34.99"}],
             "bidCount":["3"],"sellingState":["Active"],"timeLeft":["P5DT23H17M39S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-02-28T03:05:26.000Z"],
             "endTime":["2020-03-06T03:05:26.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["7"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["153839648277"],
             "title":["Vintage Dynaco A-50 speakers A50 A25 A-25"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mwLVkh2_AT6F9ksgjK6vFhw\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Vintage-Dynaco-A-50-speakers-A50-A25-A-25-\/153839648277"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["200**"],"location":["Washington,District Of Columbia,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"299.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"299.99"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P5DT5H58M3S"]}],"listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-02-20T19:02:01.000Z"],
             "endTime":["2020-02-27T19:02:01.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["12"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["174183853047"],
             "title":["1940s Northern Western Electric Altec 604 Duplex Speaker in Original 605 Cabinet"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mym4r6FVk16o_w7w8iq5qQA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/1940s-Northern-Western-Electric-Altec-604-Duplex-Speaker-Original-605-Cabinet-\/174183853047"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["V7E3V7"],"location":["Canada"],"country":["CA"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"800.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"5888.88"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"5888.88"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P5DT7H25M34S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-02-07T00:36:06.000Z"],
             "endTime":["2020-02-14T00:36:06.000Z"],
             "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["174177597476"],
             "title":["AC 100A Meter Split Core Transformer  "],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["4678"],"categoryName":["Other Test Meters & Detectors"]}],
             "galleryURL":["https:\/\/thumbs1.ebaystatic.com\/m\/meLmnsTlalojdJ8PvNbUaOw\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/AC-100A-Meter-Split-Core-Transformer-\/174177597476"],
             "paymentMethod":["PayPal","VisaMC","AmEx","Discover"],"autoPay":["false"],
             "postalCode":["117**"],"location":["Saint James,NY,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"8.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["10"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"10.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"10.0"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P5DT12H31M16S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-02-01T06:26:46.000Z"],
             "endTime":["2020-02-08T06:26:46.000Z"],
             "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["1500"],"conditionDisplayName":["New \u2013 Open box"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["274222992683"],
             "title":["AZ1 Valvo Pair! Mesh Plate Tube Valve Röhre Big Ballon Klangfilm AD1 Tested Good"],
             "globalId":["EBAY-GB"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Valves & Vacuum Tubes"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mhuuD1v60XOndrcE9SwWBwQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/AZ1-Valvo-Pair-Mesh-Plate-Tube-Valve-Rohre-Big-Ballon-Klangfilm-AD1-Tested-Good-\/274222992683"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "location":["Latvia"],"country":["LV"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"13.12"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"GBP","__value__":"39.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"52.46"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P6DT9H11M11S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-24T09:02:23.000Z"],
             "endTime":["2020-01-31T09:02:23.000Z"],"listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["164044315855"],
             "title":["FISHER 80-R TUBE TUNER &PRE   vg shape \/ untested  ( 1 ea )"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["67807"],"categoryName":["Vintage Preamps & Tube Preamps"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mHrP-V_Tk3U5rkciwI6_2ag\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/FISHER-80-R-TUBE-TUNER-PRE-vg-shape-untested-1-ea-\/164044315855"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["928**"],"location":["Anaheim,CA,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"49.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"49.99"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P5DT2H7M0S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-23T01:57:03.000Z"],"returnsAccepted":["false"],
             "endTime":["2020-01-30T01:57:03.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["283752371216"],
             "title":["4x EL34 power tubes  RFT ( SIEMENS ) - NOS  - EL 34 "],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs1.ebaystatic.com\/m\/mX8KksB3cQAuzkFsR5Km-yw\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/4x-EL34-power-tubes-RFT-SIEMENS-NOS-EL-34-\/283752371216"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "location":["Germany"],"country":["DE"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"20.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"229.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"229.0"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P8DT9H10M59S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-23T09:01:49.000Z"],
             "endTime":["2020-02-02T09:01:49.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["312954104297"],
             "title":["4x KT61 ( 6AG6 G ) tubes HALTRON ( M.O.V. ) - NOS (~  6V6G \/ EL33 \/  EL3 ) KT 61"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mUCUHZ0OGJg1ot2vgc-7oVA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/4x-KT61-6AG6-G-tubes-HALTRON-M-O-V-NOS-6V6G-EL33-EL3-KT-61-\/312954104297"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "location":["Germany"],"country":["DE"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"20.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"219.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"219.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P8DT8H57M32S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-23T08:48:36.000Z"],
             "endTime":["2020-02-02T08:48:36.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["312953984914"],
             "title":["2x  E82CC \/ 6189  VALVO \/  SIEMENS tubes -  NOS ( ECC802S \/ 12AU7WA ) -  E 82 CC"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/mjUMYje6sxrIb3vq_OkTeYw\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/2x-E82CC-6189-VALVO-SIEMENS-tubes-NOS-ECC802S-12AU7WA-E-82-CC-\/312953984914"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "location":["Germany"],"country":["DE"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"15.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"89.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"89.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P8DT8H20M4S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-23T08:11:11.000Z"],
             "endTime":["2020-02-02T08:11:11.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["164044313206"],
             "title":["DYNACO ST 70  ORIGINAL CAGE (with meter) VG SHAPE ( 1 EA )"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/mqiJpYtUAsWCCxLKuKYYx0g\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/DYNACO-ST-70-ORIGINAL-CAGE-with-meter-VG-SHAPE-1-EA-\/164044313206"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["928**"],"location":["Anaheim,CA,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"49.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"49.99"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P5DT2H4M8S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-23T01:53:18.000Z"],
             "endTime":["2020-01-30T01:53:18.000Z"],
             "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["283743905366"],
             "title":["2x  ECC88 \/ 6DJ8   TELEFUNKEN  <> tubes  - NOS  -  ( ~  7DJ8 \/ PCC88 )  MILITARY"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/m7erU0_LT3JT9nnCfetRyPw\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/2x-ECC88-6DJ8-TELEFUNKEN-tubes-NOS-7DJ8-PCC88-MILITARY-\/283743905366"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "location":["Germany"],"country":["DE"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"15.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"179.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"179.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P7DT12H34M22S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-16T09:09:40.000Z"],
             "endTime":["2020-01-26T09:09:40.000Z"],
             "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["174147736580"],
             "title":["Valvo Heerlen E88CC NOS Grey Shield CCa 6DJ8 6922 CV2492 CV2493 CV5358 CV5472"],
             "globalId":["EBAY-US"],"subtitle":["Prod. in'60th, Grey Shield, Stage Getter, Goldpins"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs1.ebaystatic.com\/m\/mwWK-iC4YCrl7v1O4gk7fcA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Valvo-Heerlen-E88CC-NOS-Grey-Shield-CCa-6DJ8-6922-CV2492-CV2493-CV5358-CV5472-\/174147736580"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "location":["Germany"],"country":["DE"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"17.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"1.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"1.0"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P8DT13H32M38S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-08T15:33:17.000Z"],
             "endTime":["2020-01-18T15:33:17.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["13"]}],"returnsAccepted":["false"],
             "galleryPlusPictureURL":["https:\/\/galleryplus.ebayimg.com\/ws\/web\/174147736580_1_0_1.jpg"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["174148034585"],
             "title":["4 lot 6201 GE dual triode preamp tube,pin compatible with 12AX7 used,tested,good"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mbv5Zea49EkVkBgtTZJk1Og\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/4-lot-6201-GE-dual-triode-preamp-tube-pin-compatible-12AX7-used-tested-good-\/174148034585"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["530**"],"location":["Johnson Creek,WI,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"25.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"25.0"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P7DT0H59M40S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"50.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"50.0"}],
             "startTime":["2020-01-07T03:00:19.000Z"],
             "endTime":["2020-01-17T03:00:19.000Z"],
             "listingType":["AuctionWithBIN"],"gift":["false"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["174145135158"],
             "title":["NOS General Electric GE 5 Star 5814A 12au7 Vacuum Tube Tested Guaranteed! 3 Mica"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/m18XYCCeasHmNR844kUthLQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/NOS-General-Electric-GE-5-Star-5814A-12au7-Vacuum-Tube-Tested-Guaranteed-3-Mica-\/174145135158"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["982**"],"location":["Point Roberts,WA,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["CalculatedDomesticFlatInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"28.88"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"28.88"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P0DT22H16M26S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-04T00:16:47.000Z"],
             "endTime":["2020-01-11T00:16:47.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["202868417147"],
             "title":["Amperex 12AX7 ECC83 Vintage Tube Pair Bugle Boy Tested NOS (Noise Tested)"],
             "globalId":["EBAY-US"],"subtitle":["Amplitrex AT-1000 tested, a quality audio tube auction!"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mU0xGWE5t73HgN7vgCck17g\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Amperex-12AX7-ECC83-Vintage-Tube-Pair-Bugle-Boy-Tested-NOS-Noise-Tested-\/202868417147"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["894**"],"location":["Sparks,NV,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"5.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"24.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"24.5"}],
             "bidCount":["5"],"sellingState":["Active"],"timeLeft":["P2DT17H26M6S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-05T19:26:01.000Z"],
             "endTime":["2020-01-12T19:26:01.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["24"]}],
             "returnsAccepted":["true"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["true"]

         },{ "itemId":["202867134038"],
             "title":["Mullard 10M Master Series 12AX7 \/ ECC83 10,000 HR Gold Pin Tube Amplitrex Tested"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/mroj-tbk7waMCzS6Hhkne0w\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Mullard-10M-Master-Series-12AX7-ECC83-10-000-HR-Gold-Pin-Tube-Amplitrex-Tested-\/202867134038"],
             "paymentMethod":["PayPal"],"autoPay":["true"],
             "postalCode":["305**"],"location":["Hoschton,GA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"56.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"56.0"}],
             "bidCount":["14"],"sellingState":["Active"],
             "timeLeft":["P1DT14H22M28S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-01T16:22:23.000Z"],
             "endTime":["2020-01-11T16:22:23.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["16"]}],
             "returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["352919421447"],
             "title":["2 1950's Sylvania Black Plate 6SN7GTA 6SN7 Vacuum Tubes Test NOS Guaranteed! #6"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/m1mIlmV6iWikuwomU6BhdwQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/2-1950s-Sylvania-Black-Plate-6SN7GTA-6SN7-Vacuum-Tubes-Test-NOS-Guaranteed-6-\/352919421447"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["982**"],"location":["Point Roberts,WA,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["CalculatedDomesticFlatInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["4"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"68.88"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"68.88"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P0DT22H18M50S"]}],"listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-04T00:18:34.000Z"],
             "endTime":["2020-01-11T00:18:34.000Z"],
             "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["114039185762"],
             "title":["Vintage Altec Lansing N-800-D Dividing Network"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/m10pOGdAAI2z3Vc8A-NStEg\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Vintage-Altec-Lansing-N-800-D-Dividing-Network-\/114039185762"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["974**"],"location":["Springfield,OR,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"19.99"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["5"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"156.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"156.0"}],
             "bidCount":["6"],"sellingState":["Active"],
             "timeLeft":["P1DT22H26M47S"]}],"listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-12-29T22:00:19.000Z"],
             "endTime":["2020-01-05T22:00:19.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["21"]}],
             "returnsAccepted":["false"],"condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["174142861539"],
             "title":["AMPEREX BUGLE BOY EF86\/6267 VACUUM TUBE MESH PLATE"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mN3bzB8twXeNWnPjagIpRRw\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/AMPEREX-BUGLE-BOY-EF86-6267-VACUUM-TUBE-MESH-PLATE-\/174142861539"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["600**"],"location":["McHenry,IL,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"9.95"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"15.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"15.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P4DT15H33M24S"]}],"listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-01T15:07:23.000Z"],
             "endTime":["2020-01-08T15:07:23.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["2"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["324030050981"],
             "title":["2 X ) KLH vintage model nine speaker power supply "],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mhAgmqFICN3O-2-mJYFVp8w\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/2-X-KLH-vintage-model-nine-speaker-power-supply-\/324030050981"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["554**"],"location":["Minneapolis,MN,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"99.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"99.99"}],"bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P5DT13H21M28S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-02T12:55:20.000Z"],
             "endTime":["2020-01-09T12:55:20.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["4"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["164011103887"],
             "title":["Altec 288 B Diaphragms "],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mWtXnMig_lsBzh3NSK6crRg\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Altec-288-B-Diaphragms-\/164011103887"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["972**"],"location":["Portland,OR,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"35.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"99.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"99.0"}],"bidCount":["1"],"sellingState":["Active"],
             "timeLeft":["P0DT5H37M54S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-12-30T05:11:26.000Z"],
             "endTime":["2020-01-04T05:11:26.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["15"]}],
             "returnsAccepted":["false"],"isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["153777954483"],
             "title":["Vintage Stark 8-77 Tube Tester Hickok 6000"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["170062"],"categoryName":["Tube Testers"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mV5zWxKs5AL9Ng1BK2Q0GXA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Vintage-Stark-8-77-Tube-Tester-Hickok-6000-\/153777954483"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["M3B***"],"location":["Canada"],"country":["CA"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"55.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["4"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"102.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"102.5"}],
             "bidCount":["10"],"sellingState":["Active"],
             "timeLeft":["P4DT2H57M21S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-12-29T02:31:06.000Z"],
             "endTime":["2020-01-08T02:31:06.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["31"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["193278712422"],
             "title":["HICKOK 532 \/ 533 \/ 534 \/ 600 MUTUAL CONDUCTANCE TUBE TESTER ROLL CHART ASSEMBLY"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["170062"],"categoryName":["Tube Testers"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/m5GloPEMEBW1F4o7_nox7nw\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/HICKOK-532-533-534-600-MUTUAL-CONDUCTANCE-TUBE-TESTER-ROLL-CHART-ASSEMBLY-\/193278712422"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["486**"],"location":["Midland,MI,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"25.56"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"25.56"}],
             "bidCount":["2"],"sellingState":["Active"],
             "timeLeft":["P2DT15H46M15S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-12-30T15:20:00.000Z"],
             "endTime":["2020-01-06T15:20:00.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],"returnsAccepted":["true"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["174143946146"],
             "title":["Amperex 6922 gold pin tube military edition audio grade gold pins 6DJ8 E88CC"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/msN8H1fW87ppGRAWMjLwFMw\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Amperex-6922-gold-pin-tube-military-edition-audio-grade-gold-pins-6DJ8-E88CC-\/174143946146"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["905**"],"location":["Torrance,CA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"12.99"}],"shippingType":["FlatDomesticCalculatedInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"55.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"55.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P5DT19H32M20S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-01-02T19:08:00.000Z"],
             "endTime":["2020-01-09T19:08:00.000Z"],
             "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["324020037678"],
             "title":["Altec Lansing Model 17 Custom Speakers 620 Cabinets with 604-8G"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/mN9zuHyw9VC9f_g8FgaceGA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Altec-Lansing-Model-17-Custom-Speakers-620-Cabinets-604-8G-\/324020037678"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["570**"],"location":["Tea,SD,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"379.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"379.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P6DT1H37M25S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2019-12-21T23:49:44.000Z"],
             "endTime":["2019-12-28T23:49:44.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["11"]}],
             "returnsAccepted":["true"],"condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["184092262958"],
             "title":["VINTAGE PAIR OF GE 8417 AMP TUBES KZ 188-5"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/mFRj9h_R05DCfrd1VSq1iyA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/VINTAGE-PAIR-GE-8417-AMP-TUBES-KZ-188-5-\/184092262958"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["460**"],"location":["Fishers,IN,USA"],"country":["US"],
             "shippingInfo":[{
                "shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],
                "shippingType":["FreePickup"],
                "shipToLocations":["Worldwide"],
                "expeditedShipping":["false"],
                "oneDayShippingAvailable":["false"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"40.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"40.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P5DT22H29M12S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2019-12-21T20:41:58.000Z"],
             "endTime":["2019-12-28T20:41:58.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],
             "returnsAccepted":["false"],
             "condition":[{"conditionId":["1500"],"conditionDisplayName":["Open box"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["184089371148"],
             "title":["Amperex\/Bugle Boy 12AT7 vacuum tube made in W. Germany"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs1.ebaystatic.com\/m\/mgbaP_7gBLbLZr7_6pozyKA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Amperex-Bugle-Boy-12AT7-vacuum-tube-made-W-Germany-\/184089371148"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["620**"],"location":["Granite City,IL,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"5.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"20.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"20.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P4DT2H0M56S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2019-12-20T00:14:58.000Z"],
             "endTime":["2019-12-27T00:14:58.000Z"],"listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["true"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["153747946010"],
             "title":["ALTEC LANSING 808 8A HORN Driver Symbiotik from HAMMOND B3 Leslie 122 Speaker"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/mMYmKuGIEx2YuQX0RHH4r1Q\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/ALTEC-LANSING-808-8A-HORN-Driver-Symbiotik-HAMMOND-B3-Leslie-122-Speaker-\/153747946010"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["600**"],"location":["Wauconda,IL,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"57.95"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"249.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"249.95"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P5DT4H5M57S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-12-03T03:58:40.000Z"],
             "endTime":["2019-12-13T03:58:40.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["4"]}],
             "returnsAccepted":["false"],"isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["163972543321"],
             "title":["Acrosound TO-300  Output Tranformers, Pair, one mounted on Heathkit W3M Chassis."],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mSPg_dRt3U0UT5vz_T0l9Ww\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Acrosound-TO-300-Output-Tranformers-Pair-one-mounted-Heathkit-W3M-Chassis-\/163972543321"],
             "paymentMethod":["PayPal"],"autoPay":["true"],
             "postalCode":["088**"],"location":["South Amboy,NJ,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"249.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"249.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P2DT14H21M21S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"349.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"349.0"}],
             "startTime":["2019-12-03T14:13:56.000Z"],
             "endTime":["2019-12-10T14:13:56.000Z"],
             "listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["5"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["133251370953"],
             "title":["1x 7308 AMPEREX PQ USA Gold Pin HiFi Amplifier Vacuum Tube - TESTED"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mCCFdNED1217-e2edWxW5mw\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/1x-7308-AMPEREX-PQ-USA-Gold-Pin-HiFi-Amplifier-Vacuum-Tube-TESTED-\/133251370953"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["851**"],"location":["Apache Junction,AZ,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"13.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"13.5"}],
             "bidCount":["5"],"sellingState":["Active"],
             "timeLeft":["P0DT18H15M10S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-11-25T15:56:31.000Z"],
             "endTime":["2019-11-30T15:56:31.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["8"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["123987878353"],
             "title":["Single Altec Lansing 415D 415-D Biflex 15 inch Speaker for Parts or Repair "],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mT7psnhxKh3hv4soR77T9vQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Single-Altec-Lansing-415C-415-C-Biflex-15-inch-Speaker-Parts-Repair-\/123987878353"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["600**"],"location":["Crystal Lake,IL,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"40.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["4"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"15.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"15.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P6DT8H31M43S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-11-25T06:09:45.000Z"],
             "endTime":["2019-12-02T06:09:45.000Z"],"listingType":["Auction"],
             "gift":["false"],"watchCount":["1"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["153723814561"],
             "title":["FISHER R-200 TUBE TUNER~PHENOMENAL SOUND & CONDITION~TELFUNKEN~MULLARD~TUBE AMP"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mrSxQPsHwbbct79Te7B_dBQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/FISHER-R-200-TUBE-TUNER-PHENOMENAL-SOUND-CONDITION-TELFUNKEN-MULLARD-TUBE-AMP-\/153723814561"],
             "paymentMethod":["PayPal"],"autoPay":["true"],
             "postalCode":["951**"],"location":["San Jose,CA,USA"],"country":["US"],
             "shippingInfo":[{
                "shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],
                "shippingType":["FreePickup"],
                "shipToLocations":["Worldwide"],
                "expeditedShipping":["false"],
                "oneDayShippingAvailable":["false"],
                "handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"199.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"199.99"}],
             "bidCount":["1"],"sellingState":["Active"],
             "timeLeft":["P3DT23H52M0S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-11-17T21:04:50.000Z"],
             "endTime":["2019-11-24T21:04:50.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["20"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["323984684424"],
             "title":["Marantz 2 mono amplifier tube 1950's original EL34 amp PICK UP ONLY"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
             "galleryURL":["https:\/\/thumbs1.ebaystatic.com\/m\/mtFOCaCjkFOPURkBi46qyFA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Marantz-2-mono-amplifier-tube-1950s-original-EL34-amp-PICK-UP-ONLY-\/323984684424"],
             "paymentMethod":["CashOnPickup","Discover"],"autoPay":["false"],
             "postalCode":["452**"],"location":["Cincinnati,OH,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],
             "shippingType":["FreePickup"],
             "shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"4500.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"4500.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P4DT23H13M24S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-11-18T20:26:18.000Z"],
             "endTime":["2019-11-25T20:26:18.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["7"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["233407527461"],
             "title":["LOT OF 7 6V6 6V6GT KEN-RAD TUNG-SOL GE RCA TV7 TESTED"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mI3Qm6Qj5Gl0lQc4-VQc7ig\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/LOT-7-6V6-6V6GT-KEN-RAD-TUNG-SOL-GE-RCA-TV7-TESTED-\/233407527461"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["455**"],"location":["Springfield,OH,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"6.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"15.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"15.0"}],
             "bidCount":["3"],"sellingState":["Active"],
             "timeLeft":["P3DT0H38M43S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-11-18T21:52:20.000Z"],
             "endTime":["2019-11-23T21:52:20.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],"returnsAccepted":["true"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["392536575491"],
             "title":["JBL 175 DRIVER 1217-1290 HORN LENS SPEAKER "],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mYJuXDBQZOz6la3hKGXFCvA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/JBL-175-DRIVER-1217-1290-HORN-LENS-SPEAKER-\/392536575491"],
             "paymentMethod":["CashOnPickup","PayPal"],"autoPay":["false"],
             "postalCode":["330**"],"location":["Pompano Beach,FL,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"45.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["5"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"300.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"300.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P4DT7H51M30S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-11-15T03:00:09.000Z"],
             "endTime":["2019-11-22T03:00:09.000Z"],
             "listingType":["Auction"],"gift":["false"],
             "watchCount":["1"]}],"returnsAccepted":["false"],
             "galleryPlusPictureURL":["https:\/\/galleryplus.ebayimg.com\/ws\/web\/392536575491_1_0_1.jpg"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["184032120009"],
             "title":["Altec Lansing Magnificent A7-500-II Speakers pair "],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/m0a1Hqce6_Ma7FBur2qj22w\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Altec-Lansing-Magnificent-A7-500-II-Speakers-pair-\/184032120009"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["330**"],"location":["Hallandale,FL,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],
             "shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"1250.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"1250.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P0DT20H21M42S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2019-11-11T15:30:14.000Z"],
             "endTime":["2019-11-18T15:30:14.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["14"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["193189027590"],
             "title":["Altec Lansing 604D Duplex 15\u201d Single Speaker & N-1600-B Crossover"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/miONH0xBkHYtmSJUx8CBwJA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Altec-Lansing-604D-Duplex-15-Single-Speaker-N-1600-B-Crossover-\/193189027590"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["956**"],"location":["Davis,CA,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["5"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"800.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"800.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P3DT0H37M24S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-11-02T14:15:40.000Z"],
             "endTime":["2019-11-09T14:15:40.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["5"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["153708457263"],
             "title":["ALTEC LANSING 421 A DIA CONE Vintage Bass Musical Instrument Speaker 1 PAIR"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mVckBMHub-1h42wP2RTaVKA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/ALTEC-LANSING-421-DIA-CONE-Vintage-Bass-Musical-Instrument-Speaker-1-PAIR-\/153708457263"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["600**"],"location":["Wauconda,IL,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"67.95"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"299.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"299.95"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P6DT9H31M44S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-11-02T23:10:03.000Z"],
             "endTime":["2019-11-12T23:10:03.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["2"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["133227447968"],
             "title":["Altec Lansing Big A7 Speakers Pair. Early Green Drivers 511b Horn 416A N-500-G"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs1.ebaystatic.com\/m\/mShLMJQ8bune5GoD83DrduA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Altec-Lansing-Big-A7-Speakers-Pair-Early-Green-Drivers-511b-Horn-416A-N-500-G-\/133227447968"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["N8N***"],"location":["Canada"],"country":["CA"],
             "shippingInfo":[{"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"3999.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"3999.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P4DT3H19M18S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2019-11-03T17:00:03.000Z"],
             "endTime":["2019-11-10T17:00:03.000Z"],
             "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["113945886050"],
             "title":["JBL L220 Walnut Excellent with 076 Cats-eye, LE5-9, LE14A Aquaplas Cone all OEM"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/mV1S7g2zHkDygyIeVzPf0QA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/JBL-L220-Walnut-Excellent-076-Cats-eye-LE5-9-LE14A-Aquaplas-Cone-all-OEM-\/113945886050"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["774**"],"location":["Richmond,TX,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],
             "shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"2500.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"2500.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P2DT9H8M54S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"3250.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"3250.0"}],
             "startTime":["2019-11-01T22:47:21.000Z"],
             "endTime":["2019-11-08T22:47:21.000Z"],
             "listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["4"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["123950129789"],
             "title":["Pair of Altec 1569A Theater EL34 Tube Amplifiers (Western Electric Era) Peerless"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mO4GkuCYtYjJp2POZ5ppkWQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Pair-Altec-1569A-Theater-EL34-Tube-Amplifiers-Western-Electric-Era-Peerless-\/123950129789"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["600**"],"location":["Crystal Lake,IL,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"200.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["4"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"1800.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"1800.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P6DT22H7M53S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"2350.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"2350.0"}],
             "startTime":["2019-10-23T20:24:29.000Z"],
             "endTime":["2019-11-02T20:24:29.000Z"],
             "listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["6"]}],
             "returnsAccepted":["false"],"isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["383228212021"],
             "title":["Pair Electro-Voice EV The Patrician Premium System 18Wk, (2)828HF, T25A\/6HD T35"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mP2IjzOioHltNi7n205w8Zg\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Pair-Electro-Voice-EV-Patrician-Premium-System-18Wk-2-828HF-T25A-6HD-T35-\/383228212021"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["600**"],"location":["Crystal Lake,IL,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"2000.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["10"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"15000.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"15000.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P6DT20H49M15S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"19500.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"19500.0"}],
             "startTime":["2019-10-23T19:06:07.000Z"],
             "endTime":["2019-11-02T19:06:07.000Z"],
             "listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["4"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["153684782088"],
             "title":["Vintage Heathkit AS-21 (Legato Compact) Altec 414a's (2) & 804a Drivers \/ Beauty"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs1.ebaystatic.com\/m\/mpfSRzlRS2wM9TTEjdV-DlA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Vintage-Heathkit-AS-21-Legato-Compact-Altec-414as-2-804a-Drivers-Beauty-\/153684782088"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["27608"],"location":["Raleigh,NC,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],
             "shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"500.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"500.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P4DT7H58M28S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-10-14T20:51:04.000Z"],
             "endTime":["2019-10-19T20:51:04.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["233369497398"],
             "title":["Pilot 240 tube integrated amp stereo WORKING ala Fisher Scott"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/mr0dbGK4-GgoqBEJmw635GA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Pilot-240-tube-integrated-amp-stereo-WORKING-ala-Fisher-Scott-\/233369497398"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["53217"],"location":["Milwaukee,WI,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"45.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"360.0"}],
             "convertedCurrentPrice":[{"@currencyId":"USD","__value__":"360.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P4DT13H6M26S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-10-15T01:58:55.000Z"],
             "endTime":["2019-10-20T01:58:55.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["283636126401"],
             "title":[" JBL L220 Oracle Speakers  076 Cat Eye Tweeters, LE14A Woofer, LE5-9 midrange"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mzXvV40uV4jEI_fTC8ilbYQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/JBL-L220-Oracle-Speakers-076-Cat-Eye-Tweeters-LE14A-Woofer-LE5-9-midrange-\/283636126401"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["21539"],"location":["Lonaconing,MD,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],
             "shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"2600.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"2600.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P6DT7H20M36S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-10-07T14:47:42.000Z"],
             "endTime":["2019-10-17T14:47:42.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["4"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["202796135729"],
             "title":["SCOTT LK-72 Tube Amplifier 7199 GE 7591 Mullard 5AR4 Bench Checked and Serviced"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/m01pFLziBNbX_qzSeWs97GA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/SCOTT-LK-72-Tube-Amplifier-7199-GE-7591-Mullard-5AR4-Bench-Checked-and-Serviced-\/202796135729"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["94588"],"location":["Pleasanton,CA,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"299.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"299.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P4DT20H37M33S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2019-10-09T04:04:32.000Z"],
             "endTime":["2019-10-16T04:04:32.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["33"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["143400343473"],
             "title":["Klipsch K-77\/ EV\/ University T35 Tweeters Heresy La Scala Set Made 09\/07\/2012"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/muevptjC4711kmZ34vt9MaA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Klipsch-K-77-EV-University-T35-Tweeters-Heresy-Scala-Set-Made-09-07-2012-\/143400343473"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["48350"],"location":["Davisburg,MI,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"85.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"85.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P6DT8H24M56S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-10-03T02:00:19.000Z"],
             "endTime":["2019-10-10T02:00:19.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],"returnsAccepted":["true"],"isMultiVariationListing":["false"],
             "topRatedListing":["true"]

         },{ "itemId":["383183181329"],
             "title":["Amperex Bugle Boy 6DJ8 ECC88 Vacuum Tube Tested 100%"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mfjAsnwTSE908ASn6GeyuTQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Amperex-Bugle-Boy-6DJ8-ECC88-Vacuum-Tube-Tested-100-\/383183181329"],
             "paymentMethod":["PayPal"],"autoPay":["true"],
             "location":["Canada"],"country":["CA"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"8.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P3DT7H16M25S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"15.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"15.0"}],
             "startTime":["2019-09-30T00:52:19.000Z"],
             "endTime":["2019-10-07T00:52:19.000Z"],"listingType":["AuctionWithBIN"],"gift":["false"]}],"returnsAccepted":["true"],"isMultiVariationListing":["false"],
             "topRatedListing":["false"]

         },{ "itemId":["323923889701"],
             "title":["Fisher FM-1000, 400-CX, SA-1000, stereo component set - vintage tube electronics"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/mDQS9V998VJKBx0P7r3McPQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Fisher-FM-1000-400-CX-SA-1000-stereo-component-set-vintage-tube-electronics-\/323923889701"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["19464"],"location":["Pottstown,PA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],
             "shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"4100.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"4100.0"}],
             "bidCount":["3"],"sellingState":["Active"],
             "timeLeft":["P1DT3H29M33S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-09-22T00:40:15.000Z"],
             "endTime":["2019-09-27T00:40:15.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["53"]}],"returnsAccepted":["true"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],"isMultiVariationListing":["false"],
             "topRatedListing":["false"]

         },{ "itemId":["352786860975"],
             "title":["Vintage Pair of Acoustic Research EARLY AR-2\/AR-2x Speakers PLEASE READ"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/m57dgVBqbJxtkYScsjb_bMg\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Vintage-Pair-Acoustic-Research-EARLY-AR-2-AR-2x-Speakers-PLEASE-READ-\/352786860975"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["48331"],"location":["Farmington,MI,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"85.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["4"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"109.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"109.5"}],
             "bidCount":["3"],"sellingState":["Active"],
             "timeLeft":["P4DT2H33M14S"]}],"listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-09-11T23:22:34.000Z"],
             "endTime":["2019-09-18T23:22:34.000Z"],"listingType":["Auction"],"gift":["false"],
             "watchCount":["5"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["183953915448"],
             "title":["Electro Voice EV Regency Speaker Cabinet Enclosure Empty Vintage Corner Horn "],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
             "galleryURL":["https:\/\/thumbs1.ebaystatic.com\/m\/mHK0AHdI-pgQuT0jLGv66hw\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Electro-Voice-EV-Regency-Speaker-Cabinet-Enclosure-Empty-Vintage-Corner-Horn-\/183953915448"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["46391"],
             "location":["Westville,IN,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],
             "shippingType":["FreePickup"],
             "shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"49.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"49.99"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P5DT23H44M55S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"64.99"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"64.99"}],
             "startTime":["2019-09-13T20:33:56.000Z"],
             "endTime":["2019-09-20T20:33:56.000Z"],
             "listingType":["AuctionWithBIN"],"gift":["false"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["183952461011"],
             "title":["Tung Sol 6SN7GTB 82\/88"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/mzzdsDN1X2eWbdJEkYfn2TQ\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Tung-Sol-6SN7GTB-82-88-\/183952461011"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["49047"],
             "location":["Dowagiac,MI,USA"],"country":["US"],
             "shippingInfo":[{
                "shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],
                "shippingType":["FreePickup"],
                "shipToLocations":["Worldwide"],
                "expeditedShipping":["false"],
                "oneDayShippingAvailable":["false"],
                "handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"10.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"10.0"}],
             "bidCount":["0"],"sellingState":["Active"],
             "timeLeft":["P5DT0H41M31S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2019-09-12T21:31:32.000Z"],
             "endTime":["2019-09-19T21:31:32.000Z"],
             "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["264395445356"],
             "title":["2 RCA Type 83 JAN mil grade rectifier tubes.For Hickok,TV-7 tube testers & more."],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["170062"],"categoryName":["Tube Testers"]}],"secondaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
             "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mLRC8iWJU9BY0KaYooEEu9w\/140.jpg"],
             "viewItemURL":["http:\/\/www.ebay.com\/itm\/2-RCA-Type-83-JAN-mil-grade-rectifier-tubes-For-Hickok-TV-7-tube-testers-more-\/264395445356"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["34234"],
             "location":["Sarasota,FL,USA"],"country":["US"],
             "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],
             "bidCount":["0"],
             "sellingState":["Active"],
             "timeLeft":["P9DT3H33M0S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2019-07-12T02:07:44.000Z"],
             "endTime":["2019-07-22T02:07:44.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["4"]}],"returnsAccepted":["true"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],"isMultiVariationListing":["false"],
             "topRatedListing":["false"]

          },{ "itemId":["293128761816"],
              "title":["VINTAGE LOT ALTEC LANSING N-500-C NETWORK CROSSOVER w\/803B WOOFER SPEAKER+ HORN"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/m2Y7tJD2s1iy1NWonZyFIPw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-LOT-ALTEC-LANSING-N-500-C-NETWORK-CROSSOVER-w-803B-WOOFER-SPEAKER-HORN-\/293128761816"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["92707"],"location":["Santa Ana,CA,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["true"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"699.98"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"699.98"}],
              "bidCount":["0"],"sellingState":["Active"],
              "timeLeft":["P8DT14H17M43S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2019-06-21T17:02:01.000Z"],
              "endTime":["2019-07-01T17:02:01.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["3"]}],"returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{"itemId":["123795331323"],
              "title":["ALTEC 755A Loudspeaker Unit same as Western Electric 755A"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/m9jykf7R3tNKXA-Dg6zJh6w\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/ALTEC-755A-Loudspeaker-Unit-same-Western-Electric-755A-\/123795331323"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "location":["Taiwan"],"country":["TW"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"38.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["5"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"540.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"540.0"}],
              "bidCount":["15"],"sellingState":["Active"],
              "timeLeft":["P4DT21H22M10S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2019-06-07T17:55:54.000Z"],
              "endTime":["2019-06-14T17:55:54.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["41"]}],"returnsAccepted":["true"],
              "galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/123795331323_1_0_1.jpg"],
              "isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["123790646318"],
              "title":["Altec 601A Speaker with N3000A Crossover"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mJw19gfwAj4D08Wx9k2uNXA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Altec-601A-Speaker-N3000A-Crossover-\/123790646318"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["95062"],
              "location":["Santa Cruz,CA,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"249.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"249.0"}],
              "bidCount":["0"],"sellingState":["Active"],
              "timeLeft":["P6DT5H50M27S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2019-06-03T02:07:40.000Z"],
              "endTime":["2019-06-13T02:07:40.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["4"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["223539937147"],
              "title":["Vintage Altec Lansing 601A Duplex speaker Co-axial woofer"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mkYUCr_YypsxGxWSSemBnog\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Altec-Lansing-601A-Duplex-speaker-Co-axial-woofer-\/223539937147"],
              "paymentMethod":["PayPal","VisaMC","AmEx","Discover"],"autoPay":["false"],
              "postalCode":["22182"],"location":["Vienna,VA,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["4"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"99.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"99.0"}],
              "bidCount":["1"],"sellingState":["Active"],
              "timeLeft":["P1DT22H25M1S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2019-06-03T18:41:52.000Z"],
              "endTime":["2019-06-08T18:41:52.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["14"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["173922031351"],
              "title":["JBL JBL early \\"Jim\\" Lansing 150-4B 15\\" AlNiCo Paragon Hartsfield woofer 32 ohm"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mrnJ0EkiQY7_3OS-5tryJug\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/JBL-JBL-early-Jim-Lansing-150-4B-15-AlNiCo-Paragon-Hartsfield-woofer-32-ohm-\/173922031351"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["12144"],
              "location":["Rensselaer,NY,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"202.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"202.5"}],
              "bidCount":["5"],"sellingState":["Active"],
              "timeLeft":["P3DT15H7M25S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2019-06-03T11:24:38.000Z"],
              "endTime":["2019-06-10T11:24:38.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["10"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["401777677255"],
              "title":["Vintage  Altec Lansing Dividing Network Crossover N-3000G, 890B Bolero Speaker "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mw6zn8PUSc4pEnF3uHu7JWA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Altec-Lansing-Dividing-Network-Crossover-N-3000G-890B-Bolero-Speaker-\/401777677255"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["54904"],
              "location":["Oshkosh,WI,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"4.95"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"19.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"19.95"}],
              "bidCount":["0"],"sellingState":["Active"],
              "timeLeft":["P5DT21H7M14S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
              "startTime":["2019-05-31T17:19:27.000Z"],
              "endTime":["2019-06-07T17:19:27.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["192878961826"],
              "title":["Jensen RP-302A Vintage Super Tweeter 16 ohm 1957 Jensen Imperial"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],
              "categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mFAahvarZOHmg7clSWXlgpg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Jensen-RP-302A-Vintage-Super-Tweeter-16-ohm-1957-Jensen-Imperial-\/192878961826"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["49316"],
              "location":["Caledonia,MI,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"165.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"165.0"}],
              "bidCount":["0"],"sellingState":["Active"],
              "timeLeft":["P6DT5H2M45S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"220.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"220.0"}],
              "startTime":["2019-04-03T02:15:10.000Z"],
              "endTime":["2019-04-10T02:15:10.000Z"],
              "listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["2"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["202636634682"],
              "title":["Vintage Acoustic Research SAT 660 Speakers(2)"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],
              "categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/m3umS-mQ2uZGxFZW3o91ycw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Acoustic-Research-SAT-660-Speakers-2-\/202636634682"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["23456"],
              "location":["Virginia Beach,VA,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"44.5"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"21.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"21.99"}],
              "bidCount":["0"],"sellingState":["Active"],
              "timeLeft":["P4DT7H13M45S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
              "startTime":["2019-03-27T02:54:18.000Z"],
              "endTime":["2019-04-01T02:54:18.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],"topRatedListing":["false"]

          },{ "itemId":["133004653920"],
              "title":["VINTAGE ALTEC LANSING 604D DUPLEX SPEAKER, With N-1600B CROSSOVER."],
              "globalId":["EBAY-US"],
              "subtitle":["Near mint condition .. in original 1950s packaging"],
              "primaryCategory":[{"categoryId":["50597"],
              "categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mh3UMGjtjfTEMMB3R2kpP-Q\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-ALTEC-LANSING-604D-DUPLEX-SPEAKER-N-1600B-CROSSOVER-\/133004653920"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["11103"],
              "location":["Astoria,NY,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["CalculatedDomesticFlatInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"1000.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"1000.0"}],
              "bidCount":["0"],"sellingState":["Active"],
              "timeLeft":["P6DT20H52M39S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"1350.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"1350.0"}],
              "startTime":["2019-03-27T16:34:17.000Z"],
              "endTime":["2019-04-03T16:34:17.000Z"],
              "listingType":["AuctionWithBIN"],"gift":["false"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],"topRatedListing":["false"]

          },{ "itemId":["293004871422"],
              "title":["Jbl L65 Jubal Le5-12 Mids Pair Working Nice! See Pictures"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mx1gcC1mBLST_B8i3qWAYpg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Jbl-L65-Jubal-Le5-5-Mids-Pair-Working-Nice-See-Pictures-\/293004871422"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["08096"],
              "location":["Woodbury,NJ,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"100.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"100.0"}],
              "bidCount":["0"],"sellingState":["Active"],
              "timeLeft":["P6DT5H38M58S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
              "startTime":["2019-03-13T02:46:55.000Z"],
              "endTime":["2019-03-20T02:46:55.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["2"]}],
              "returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["254154293727"],
              "title":["vintage klipsch Lascalas"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mHmtp3VufMhrZzkpVJ0QB6A\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/vintage-klipsch-Lascalas-\/254154293727"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["27332"],
              "location":["Sanford,NC,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],
              "shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"650.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"650.0"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P6DT14H4M30S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
              "startTime":["2019-03-07T13:14:25.000Z"],
              "endTime":["2019-03-14T13:14:25.000Z"],
              "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

          },{ "itemId":["254130264753"],
              "title":["The Fisher 105 - 3 Way Speakers \u2013 Cool Latticework Grills - 12\\" Woofers        "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mAvNyg1TCZktrhVJMZZgiyw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Fisher-105-3-Way-Speakers-Cool-Latticework-Grills-12-Woofers-\/254130264753"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["48072"],
              "location":["Berkley,MI,USA"],"country":["US"],
              "shippingInfo":[{
                    "shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],
                    "shippingType":["FreePickup"],
                    "shipToLocations":["Worldwide"],
                    "expeditedShipping":["false"],
                    "oneDayShippingAvailable":["false"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"35.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"35.0"}],
              "bidCount":["0"],"sellingState":["Active"],
              "timeLeft":["P6DT22H11M59S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
              "startTime":["2019-02-18T19:34:33.000Z"],
              "endTime":["2019-02-25T19:34:33.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["323681140009"],
              "title":["Marantz Model 140 Stereo Amp, 3200 Preamp and Model 112 Tuner - Complete Stack!"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mbdj0vd_Up5LY226wdJa1Qw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Marantz-Model-140-Stereo-Amp-3200-Preamp-and-Model-112-Tuner-Complete-Stack-\/323681140009"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["91205"],
              "location":["Glendale,CA,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"600.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"600.0"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P4DT10H51M2S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"1250.0"}],
              "convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"1250.0"}],
              "startTime":["2019-02-05T00:14:28.000Z"],
              "endTime":["2019-02-10T00:14:28.000Z"],
              "listingType":["AuctionWithBIN"],"gift":["false"],
              "watchCount":["14"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["223348187115"],
              "title":["ALTEC Early Model 606 Corner Cabinet 602A 15\\" Duplex Speaker  N3000A "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mRhVzDgV_VpWwAb0mcui0ZQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/ALTEC-Early-Model-606-Corner-Cabinet-602A-15-Duplex-Speaker-N3000A-\/223348187115"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["34684"],
              "location":["Palm Harbor,FL,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"1200.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"1200.0"}],
              "bidCount":["0"],"sellingState":["Active"],
              "timeLeft":["P4DT2H57M42S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
              "startTime":["2019-01-28T02:03:19.000Z"],
              "endTime":["2019-02-07T02:03:19.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["1"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["312436313310"],
              "title":["MARANTZ  MODEL 240 POWER AMPLIFIER, USED, GOOD CONDITION, TESTED"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mnJntjWuIHESgT19YH31S8g\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/MARANTZ-MODEL-240-POWER-AMPLIFIER-USED-GOOD-CONDITION-TESTED-\/312436313310"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["30092"],
              "location":["Norcross,GA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"990.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"990.0"}],
              "bidCount":["0"],"sellingState":["Active"],
              "timeLeft":["P4DT11H24M55S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
              "startTime":["2019-01-21T01:56:09.000Z"],
              "endTime":["2019-01-27T13:56:09.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["1"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["312417181299"],
              "title":["MARANTZ  MODEL 240 POWER AMPLIFIER, USED, GOOD CONDITION"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mnJntjWuIHESgT19YH31S8g\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/MARANTZ-MODEL-240-POWER-AMPLIFIER-USED-GOOD-CONDITION-\/312417181299"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["30092"],
              "location":["Norcross,GA,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"990.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"990.0"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P5DT9H13M4S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
              "startTime":["2019-01-07T01:55:47.000Z"],
              "endTime":["2019-01-13T13:55:47.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["1"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["173696834267"],
              "title":["1 NOS Westinghouse Canada 12au7A 12au7 Vacuum Tube TV7 Tested Guaranteed! NR! "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/m36cuFDIQj7iq7rONooJnPA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/1-NOS-Westinghouse-Canada-12au7A-12au7-Vacuum-Tube-TV7-Tested-Guaranteed-NR-\/173696834267"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["98281"],
              "location":["Point Roberts,WA,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["CalculatedDomesticFlatInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],
              "bidCount":["0"],
              "sellingState":["Active"],"timeLeft":["P6DT16H24M36S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-12-18T03:10:30.000Z"],
              "endTime":["2018-12-25T03:10:30.000Z"],
              "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["372536713027"],
              "title":["VINTAGE RCA 6SN7GTB ELECTRON TUBE NOS"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mIzUnQ-fKZHNift4RgtUP6w\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-RCA-6SN7GTB-ELECTRON-TUBE-NOS-\/372536713027"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["19352"],
              "location":["Lincoln University,PA,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["0"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"14.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"14.5"}],
              "bidCount":["0"],
              "sellingState":["Active"],"timeLeft":["P4DT8H13M14S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"19.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"19.0"}],
              "startTime":["2018-12-15T18:57:57.000Z"],
              "endTime":["2018-12-22T18:57:57.000Z"],
              "listingType":["AuctionWithBIN"],"gift":["false"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["303000959884"],
              "title":["1 6SN7GT SYLVANIA 2-Hole Black Plate HiFi Radio Amplifier Vacuum Tube Code 126"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/my6h7YWII_pfXxwrd4M-MiA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/1-6SN7GT-SYLVANIA-2-Hole-Black-Plate-HiFi-Radio-Amplifier-Vacuum-Tube-Code-126-\/303000959884"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["10981"],
              "location":["Sugar Loaf,NY,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FlatDomesticCalculatedInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P2DT16H34M7S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-12-18T03:19:06.000Z"],
              "endTime":["2018-12-21T03:19:06.000Z"],
              "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["173696832184"],
              "title":["2 Vintage Philips Holland GE  6DJ8 6922 E88CC Vacuum Tubes Tested Guaranteed!"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/m0yOEdrCTe9BPgqxSC_EoZQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/2-Vintage-Philips-Holland-GE-6DJ8-6922-E88CC-Vacuum-Tubes-Tested-Guaranteed-\/173696832184"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["98281"],
              "location":["Point Roberts,WA,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["CalculatedDomesticFlatInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"58.88"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"58.88"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P6DT16H21M47S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-12-18T03:07:28.000Z"],
              "endTime":["2018-12-25T03:07:28.000Z"],
              "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["303000971114"],
              "title":["3 Vintage Matsushita EL34 6CA7 Golden Series Tubes,1950s,Dual Getters,EX sound"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mhRk0qrgHQ1VbSvzq6WKaFQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/3-Vintage-Matsushita-EL34-6CA7-Golden-Series-Tubes-1950s-Dual-Getters-EX-sound-\/303000971114"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["32547"],
              "location":["Fort Walton Beach,FL,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"10.0"}],"shippingType":["FlatDomesticCalculatedInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"168.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"168.0"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P6DT16H50M51S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-12-18T03:36:20.000Z"],
              "endTime":["2018-12-25T03:36:20.000Z"],
              "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["123550734798"],
              "title":["LOT OF 10 pcs 12ax7 ecc83 VACUUM TUBES TESTED GOOD VINTAGE RCA TUNG-SOL RAYTHEON"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mqBJKi745cX526lvoS4IxNA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/LOT-10-pcs-12ax7-ecc83-VACUUM-TUBES-TESTED-GOOD-VINTAGE-RCA-TUNG-SOL-RAYTHEON-\/123550734798"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["97496"],
              "location":["Winston,OR,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"4.36"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["0"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"79.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"79.0"}],
              "sellingState":["Active"],
              "timeLeft":["P4DT22H6M47S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-12-18T00:31:46.000Z"],
              "endTime":["2018-12-23T00:31:46.000Z"],"listingType":["FixedPrice"],"gift":["false"]}],
              "returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]


          },{ "itemId":["192748960622"],
              "title":["4 Qty. 6SN7 GTB Sylvania NIS, NIB"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/m6969Dt0cnZHFMU0LnYPRpQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/4-Qty-6SN7-GTB-Sylvania-NIS-NIB-\/192748960622"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["98248"],
              "location":["Ferndale,WA,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"40.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"40.0"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P6DT10H31M39S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"52.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"52.0"}],
              "startTime":["2018-12-05T23:01:21.000Z"],
              "endTime":["2018-12-12T23:01:21.000Z"],
              "listingType":["AuctionWithBIN"],"gift":["false"]}],"returnsAccepted":["true"],
              "isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["192748949221"],
              "title":["Pair of Fisher XP6 Mid range speakers  5\\""],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/m467hMHEuzsMjLbrMOTVMEQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Pair-Fisher-XP6-Mid-range-speakers-5-\/192748949221"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["05641"],
              "location":["Barre,VT,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"0.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"0.99"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P2DT10H21M54S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"10.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"10.0"}],
              "startTime":["2018-12-05T22:46:58.000Z"],
              "endTime":["2018-12-08T22:46:58.000Z"],
              "listingType":["AuctionWithBIN"],"gift":["false"]}],"returnsAccepted":["true"],
              "isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["352535627937"],
              "title":["1 NOS Sylvania 6V6G 6V6 Vacuum tube Tested Guaranteed! USA Marconi"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/m0ftp77E26fMK9XoEOxOXaQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/1-NOS-Sylvania-6V6G-6V6-Vacuum-tube-Tested-Guaranteed-USA-Marconi-\/352535627937"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["98281"],
              "location":["Point Roberts,WA,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["CalculatedDomesticFlatInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["4"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"28.88"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"28.88"}],
              "bidCount":["0"],"sellingState":["Active"],
              "timeLeft":["P6DT3H47M45S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-12-04T23:35:02.000Z"],
              "endTime":["2018-12-11T23:35:02.000Z"],
              "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
              "isMultiVariationListing":["false"],
              "topRatedListing":["false"]


          },{ "itemId":["312339506602"],
              "title":["Altec 1005B  A7 A4 Voice of the Theatre horn speaker "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/m9Und7wtXmQy5vcaykE6BNw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Altec-1005B-A7-A4-Voice-Theatre-horn-speaker-\/312339506602"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["L7J2L8"],
              "location":["Canada"],"country":["CA"],"shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"120.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["5"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P6DT14H26M8S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
              "startTime":["2018-11-27T02:39:27.000Z"],
              "endTime":["2018-12-04T02:39:27.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["6"]}],
              "returnsAccepted":["true"],
              "galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/312339506602_1_0_1.jpg"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

          },{ "itemId":["113392158472"],
              "title":["ONE RAYTHEON REGISTERED 6L6 6L6GC Vacuum Tube  HICKOK 539C TESTED"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mGUQ5NxPMLfjDiKIvxeelcA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/ONE-RAYTHEON-REGISTERED-6L6-6L6GC-Vacuum-Tube-HICKOK-539C-TESTED-\/113392158472"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["07026"],
              "location":["Garfield,NJ,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"14.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"14.99"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P6DT18H59M29S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-11-22T17:20:26.000Z"],
              "endTime":["2018-11-29T17:20:26.000Z"],
              "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["283272931267"],
              "title":["5 Tube  Tubes EF86 6CF8 Valvo Miniwatt Mullard Tube EF 86 tested"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mZAPDVsJgGXMRVp2X7IS5Lg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/5-Tube-Tubes-EF86-6CF8-Valvo-Miniwatt-Mullard-Tube-EF-86-tested-\/283272931267"],
              "productId":[{"@type":"ReferenceID","__value__":"141057910"}],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "location":["Germany"],
              "country":["DE"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"16.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"49.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"49.0"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P6DT17H32M30S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-11-22T15:52:29.000Z"],
              "endTime":["2018-11-29T15:52:29.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["1"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["382632483507"],
              "title":["FISHER XP7-B speakers TESTED beautiful condition"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mIM4QJMG1AidGt82hcwoPfA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/FISHER-XP7-B-speakers-TESTED-beautiful-condition-\/382632483507"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["14850"],
              "location":["Ithaca,NY,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"149.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"149.99"}],
              "bidCount":["1"],
              "sellingState":["Active"],
              "timeLeft":["P5DT9H37M29S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-11-19T23:25:58.000Z"],
              "endTime":["2018-11-26T23:25:58.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],
              "returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["323589685342"],
              "title":["ONE SPEAKER The Fisher XP 1 Speakers Mid Century "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mQ3ZFTCSvtyA-CY8A15EyuA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/ONE-SPEAKER-Fisher-XP-1-Speakers-Mid-Century-\/323589685342"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["92394"],
              "location":["Victorville,CA,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"40.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"49.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"49.99"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P4DT22H14M59S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-12-08T23:25:16.000Z"],
              "endTime":["2018-12-13T23:25:16.000Z"],
              "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["264048401593"],
              "title":["Pair Vintage THE FISHER XP-7B  Speakers "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mzCZo9JGphropCodLx4xKug\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Pair-Vintage-FISHER-XP-7B-Speakers-\/264048401593"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["21921"],
              "location":["Elkton,MD,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"250.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"250.0"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P2DT2H6M23S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
              "startTime":["2018-11-18T23:41:58.000Z"],
              "endTime":["2018-11-21T23:41:58.000Z"],
              "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["352494035670"],
              "title":["4 Vintage Philips ECG JAN 12AX7WA 7025 12ax7 Vacuum Tubes Tested Guaranteed!"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mjK7ij2AQ4faRT_Aaik45BQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/4-Vintage-Philips-ECG-JAN-12AX7WA-7025-12ax7-Vacuum-Tubes-Tested-Guaranteed-\/352494035670"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["98281"],
              "location":["Point Roberts,WA,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["CalculatedDomesticFlatInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"88.88"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"88.88"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P6DT7H36M59S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-10-23T01:11:36.000Z"],
              "endTime":["2018-10-30T01:11:36.000Z"],
              "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

          },{ "itemId":["332849161811"],
              "title":["The Fisher XP-1 Vintage Speakers *Local Pickup Only*"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/meJraUI67QUjC56uNbF-IDA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Fisher-XP-1-Vintage-Speakers-Local-Pickup-Only-\/332849161811"],
              "charityId":["143709"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["20781"],
              "location":["Hyattsville,MD,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"49.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"49.99"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P5DT4H49M58S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-10-21T22:25:16.000Z"],
              "endTime":["2018-10-28T22:25:16.000Z"],
              "listingType":["Auction"],"gift":["false"]}],
              "returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]


          },{ "itemId":["192675470270"],
              "title":["University Sound Altec Audio Horn Model CIB-A8 w Mount White Tested Clean Used"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mqcfM87dPUKfbuWlIpUTi-w\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/University\/192675470270"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["15085"],
              "location":["Trafford,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"563.88"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"563.88"}],"bidCount":["14"],"sellingState":["Active"],"timeLeft":["P0DT3H38M14S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-02-27T02:42:38.000Z"],
              "endTime":["2018-03-04T02:42:38.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["44"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],"isMultiVariationListing":["false"],
              "topRatedListing":["true"]

          },{ "itemId":["153200191510"],
              "title":["Rare!!! Vintage Altec Lansing 604 8G Studio Monitor Loud Speakers Pair 8 Ohms"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mqcfM87dPUKfbuWlIpUTi-w\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Altec\/153200191510"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["15085"],
              "location":["Trafford,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"563.88"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"563.88"}],"bidCount":["14"],"sellingState":["Active"],"timeLeft":["P0DT3H38M14S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-02-27T02:42:38.000Z"],"endTime":["2018-03-04T02:42:38.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["44"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],"isMultiVariationListing":["false"],
              "topRatedListing":["true"]

           },{"itemId":["173544935496"],
              "title":["2 Metal RCA 6V6 VT-107 Vacuum Tubes Tested Guaranteed!"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/miEzQ8SxUW9cKuHB1wZTNlg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/2-Metal-RCA-6V6-VT-107-Vacuum-Tubes-Tested-Guaranteed-\/173544935496"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["98281"],"location":["Point Roberts,WA,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["CalculatedDomesticFlatInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"39.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"39.99"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P6DT1H2M7S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-09-20T02:44:40.000Z"],
              "endTime":["2018-09-27T02:44:40.000Z"],
              "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["183436307728"],
              "title":["VINTAGE HICKOK MODEL 539B TUBE TESTER with CA-4 Adapter"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["170062"],"categoryName":["Tube Testers"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mnTL60BGlz4zimNqc9CVjOg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-HICKOK-MODEL-539B-TUBE-TESTER-CA-4-Adapter-\/183436307728"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["49814"],"location":["Champion,MI,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"49.99"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"499.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"499.0"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P4DT5H3M32S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-09-16T00:28:34.000Z"],
              "endTime":["2018-09-21T00:28:34.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["15"]}],"returnsAccepted":["false"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["192660195679"],
              "title":["Pair of Fisher XP6 10.5\\" Woofers"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/m-MOEX_hnwnYWaIgdzFtgpw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Pair-Fisher-XP6-10-5-Woofers-\/192660195679"],
              "paymentMethod":["PayPal"],"autoPay":["false"],"postalCode":["05641"],
              "location":["Barre,VT,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.99"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P0DT1H19M14S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"30.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"30.0"}],
              "startTime":["2018-09-16T23:43:54.000Z"],
              "endTime":["2018-09-19T23:43:54.000Z"],
              "listingType":["AuctionWithBIN"],"gift":["false"],
              "watchCount":["2"]}],"returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["192659380750"],
              "title":["Altec A5 Customized with sound nice so more than the original (515\/288\/2405)"],
              "globalId":["EBAY-US"],
              "subtitle":["A  version perfect with sound perfect"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/m_3eUK3d0hoGzu4TeKKtWUQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Altec-A5-Customized-sound-nice-so-more-than-original-515-288-2405-\/192659380750"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "location":["Vietnam"],"country":["VN"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"1792.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"5000.0"}],
              "convertedCurrentPrice":[{"@currencyId":"USD","__value__":"5000.0"}],
              "bidCount":["0"],"sellingState":["Active"],
              "timeLeft":["P6DT9H43M21S"]}],
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
              "startTime":["2018-09-16T05:11:54.000Z"],
              "endTime":["2018-09-23T05:11:54.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["7"]}],"returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["232913976977"],
              "title":["VINTAGE JBL 175 driver with 1217\/1290 HORNS!!SET OF TWO!!!! CLOSE NUMBERS!!!!"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/m5TBfqaVG7aI2yrDrEvgkgQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-JBL-175-driver-1217-1290-HORNS-SET-TWO-CLOSE-NUMBERS-\/232913976977"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["45387"],
              "location":["Yellow Springs,OH,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"400.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"400.0"}],
              "bidCount":["1"],
              "sellingState":["Active"],
              "timeLeft":["P4DT20H38M23S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-09-02T18:47:14.000Z"],
              "endTime":["2018-09-09T18:47:14.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["1"]}],"returnsAccepted":["false"],
              "isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["323437473473"],
              "title":["JBL Metregon 205 - Time Capsule! (130A, 275, N500, H5040)"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/m7ai837pzPZRjykJpFzcF3A\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/JBL-Metregon-205-Time-Capsule-130A-275-N500-H5040-\/323437473473"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["78735"],"location":["Austin,TX,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"5399.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"5399.99"}],
              "bidCount":["0"],"sellingState":["Active"],
              "timeLeft":["P5DT16H47M19S"]}],"listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
              "startTime":["2018-09-09T15:53:34.000Z"],
              "endTime":["2018-09-16T15:53:34.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["13"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["202430076409"],
              "title":["Classic Western Electric KS-15874-L2 Cardmatic Tube Tester Made By Hickok Great!"],
              "globalId":["EBAY-US"],
              "subtitle":["Totally Complete Outfit!  Really NIce!"],
              "primaryCategory":[{"categoryId":["170062"],"categoryName":["Tube Testers"]}],"secondaryCategory":[{"categoryId":["7275"],"categoryName":["Parts & Tubes"]}],
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

           },{"itemId":["323425124965"],
              "title":["Vintage Klipsch Heresy Red cloth Alnico horns, K-22 woofers, K-55V K700, K-77"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mcTIlJWajENQooFcAheZzTw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Klipsch-Heresy-Red-cloth-Alnico-horns-K-22-woofers-K-55V-K700-K-77-\/323425124965"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["98837"],"location":["Moses Lake,WA,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"1250.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"1250.0"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P2DT3H26M18S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"1635.5"}],
              "convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"1635.5"}],
              "startTime":["2018-09-01T23:10:51.000Z"],
              "endTime":["2018-09-08T23:10:51.000Z"],
              "listingType":["AuctionWithBIN"],"gift":["false"],
              "watchCount":["7"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["192633431454"],
              "title":["Spectacular JBL C38 Enclosure 2-Way Speakers D130, 075 & N2400"],
              "globalId":["EBAY-US"],"subtitle":["Mid Century look speakers that will blow the roof off"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/m4S-D5lsR3xfRD7Ise4sQAQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Spectacular-JBL-C38-Enclosure-2-Way-Speakers-D130-075-N2400-\/192633431454"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["44708"],"location":["Canton,OH,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"500.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"500.0"}],
              "bidCount":["14"],"sellingState":["Active"],
              "timeLeft":["P4DT15H4M29S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-08-22T00:15:43.000Z"],
              "endTime":["2018-08-29T00:15:43.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["45"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],"topRatedListing":["false"]


           },{"itemId":["283100002617"],
              "title":["Vintage Hickok 539b Tube Tester with Model CA-5 Universal Adapter"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["170062"],"categoryName":["Tube Testers"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mn4tv3wk4ff_mCAl8BbM73g\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Hickok-539b-Tube-Tester-Model-CA-5-Universal-Adapter-\/283100002617"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["08079"],"location":["Salem,NJ,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"50.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"410.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"410.0"}],
              "bidCount":["11"],
              "sellingState":["Active"],
              "timeLeft":["P3DT5H49M44S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-08-12T15:44:30.000Z"],
              "endTime":["2018-08-19T15:44:30.000Z"],
              "listingType":["Auction"],
              "gift":["false"],"watchCount":["36"]}],"returnsAccepted":["true"],
              "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["202401940540"],
              "title":["JBL D130, 075 & N2600 X-Over"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mOIuVSDe4VN-zG-p6LCpjsw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/JBL-D130-075-N2600-X-Over-\/202401940540"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["10710"],
              "location":["Yonkers,NY,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"218.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"218.5"}],
              "bidCount":["5"],
              "sellingState":["Active"],
              "timeLeft":["P4DT9H40M12S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-08-13T19:34:58.000Z"],
              "endTime":["2018-08-20T19:34:58.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["17"]}],"returnsAccepted":["false"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["263879319271"],
              "title":["Marantz Model 240 Power Stereo Amplifier Vintage 120 Watts Working Silver Amp"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["73368"],"categoryName":["Vintage Amplifiers & Tube Amps"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/m_3PUvMt772FuZo1zKCGPPQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Marantz-Model-240-Power-Stereo-Amplifier-Vintage-120-Watts-Working-Silver-Amp-\/263879319271"],
              "paymentMethod":["PayPal"],"autoPay":["false"],"postalCode":["17055"],"location":["Mechanicsburg,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"299.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"299.99"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P5DT14H35M14S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-08-15T00:29:53.000Z"],
              "endTime":["2018-08-22T00:29:53.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["14"]}],
              "returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["163199461416"],
              "title":["■Vintage Altec 601B Speaker & N-3000B Crossover Network In Cabinet #204781"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mcKbXFbyACk4LGBkautkHjw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-Altec-601B-Speaker-N-3000B-Crossover-Network-Cabinet-204781-\/163199461416"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["90278"],
              "location":["Redondo Beach,CA,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"294.03"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"294.03"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P3DT19H46M20S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-08-13T05:41:31.000Z"],
              "endTime":["2018-08-20T05:41:31.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["2"]}],"returnsAccepted":["true"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["263861079618"],
              "title":["10 PIECE LOT OF ASSORTED RCA TUBES"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mPPUCMZIE64vn9WwzpeR0uQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/10-PIECE-LOT-ASSORTED-RCA-TUBES-\/263861079618"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["11766"],"location":["Mount Sinai,NY,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"39.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"39.95"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P6DT8H16M20S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-08-05T20:53:36.000Z"],
              "endTime":["2018-08-12T20:53:36.000Z"],
              "listingType":["Auction"],"gift":["false"]}],
              "returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["223093061969"],
              "title":["RCA Electron Tubes Vintage Mixed Lot of (10) Tubes w\/ Sleeve NIB NOS"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mnJRYLrnNsXVMJXakQiORbg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/RCA-Electron-Tubes-Vintage-Mixed-Lot-10-Tubes-w-Sleeve-NIB-NOS-\/223093061969"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["28358"],"location":["Lumberton,NC,USA"],"country":["US"],"shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"4.88"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"9.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"9.95"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P4DT13H8M52S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-08-08T00:00:40.000Z"],
              "endTime":["2018-08-13T00:00:40.000Z"],
              "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["153121548106"],
              "title":["VINTAGE TANNOY GRF CORNER CABINET w. 15\\" SILVER DUAL CONCENTRIC DRIVER LSU\/HF\/15"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mmMi8YwkhNGrJcHNUFZvR7g\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/VINTAGE-TANNOY-GRF-CORNER-CABINET-w-15-SILVER-DUAL-CONCENTRIC-DRIVER-LSU-HF-15-\/153121548106"],
              "paymentMethod":["PayPal"],"autoPay":["false"],"postalCode":["80113"],
              "location":["Englewood,CO,USA"],"country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"5200.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"5200.0"}],
              "bidCount":["2"],
              "sellingState":["Active"],
              "timeLeft":["P8DT7H28M50S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-07-31T22:04:29.000Z"],
              "endTime":["2018-08-10T22:04:29.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["22"]}],"returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["283006362761"],
              "title":["ITM#2 Harman Kardon CITATION III X Multiplex FM Stereo Vacuum TUBE TUNER Radio"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["67807"],
              "categoryName":["Vintage Preamps & Tube Preamps"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mRd4PiejZdyF6HKb71_8qyA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/ITM-2-Harman-Kardon-CITATION-III-X-Multiplex-FM-Stereo-Vacuum-TUBE-TUNER-Radio-\/283006362761"],
              "paymentMethod":["PayPal"],
              "autoPay":["false"],
              "postalCode":["90026"],
              "location":["Los Angeles,CA,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"0.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"0.99"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P6DT2H17M22S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-06-13T13:14:41.000Z"],"endTime":["2018-06-20T01:14:41.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["18"]}],
              "returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["113173838358"],
              "title":["Altec Lansing 806a Drivers  w 811 b Horns"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/meZzFAGRfBjJViF62YTgUXA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Altec-Lansing-806a-Drivers-w-811-b-Horns-\/113173838358"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["55347"],
              "location":["Eden Prairie,MN,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"95.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"450.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"450.0"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P5DT0H46M18S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-07-29T02:15:47.000Z"],
              "endTime":["2018-08-05T02:15:47.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["5"]}],
              "returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]



           },{"itemId":["273380279306"],
              "title":["Altec Lansing 288-8K High Frequency Drive MRII 542 Horn"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs3.ebaystatic.com\/m\/mzzZOca3bXrrfnX5YxJMrXA\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Altec-Lansing-288-8K-High-Frequency-Drive-MRII-542-Horn-\/273380279306"],
              "paymentMethod":["CashOnPickup","PayPal"],"autoPay":["false"],
              "postalCode":["48824"],
              "location":["East Lansing,MI,USA"],"country":["US"],
              "shippingInfo":[{"shippingType":["Freight"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"100.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"100.0"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P6DT13H56M13S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-07-30T15:25:42.000Z"],
              "endTime":["2018-08-06T15:25:42.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["2"]}],"returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["232745789325"],
              "title":["Altec 603 B 15\\" Speaker 604 803 Vintage"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],
              "categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/miTrs7xinm0cv51NB6tWCog\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Altec-603-B-15-Speaker-604-803-Vintage-\/232745789325"],
              "paymentMethod":["PayPal"],
              "autoPay":["false"],
              "postalCode":["19044"],
              "location":["Horsham,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],
              "handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"61.0"}],
              "convertedCurrentPrice":[{"@currencyId":"USD","__value__":"61.0"}],
              "bidCount":["5"],
              "sellingState":["Active"],
              "timeLeft":["P2DT20H44M52S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-04-25T00:25:29.000Z"],"endTime":["2018-05-02T00:25:29.000Z"],
              "listingType":["Auction"],
              "gift":["false"],
              "watchCount":["27"]}],
              "returnsAccepted":["false"],
              "isMultiVariationListing":["false"],
              "topRatedListing":["false"]

            },{"itemId":["332618106572"],
              "title":["NIB Matched Quad RCA 6BH6 6661 E90F BLACK Marantz 8B Test STRONG 98-101% NEW NOS"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mbzAx1VlTAKPaAX9FMC5_aw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/NIB-Matched-Quad-RCA-6BH6-6661-E90F-BLACK-Marantz-8B-Test-STRONG-98-101-NEW-NOS-\/332618106572"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["53121"],
              "location":["Elkhorn,WI,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"4.75"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"29.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"29.0"}],"sellingState":["Active"],"timeLeft":["P27DT5H18M54S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-04-12T00:55:39.000Z"],"endTime":["2018-05-12T00:55:39.000Z"],
              "listingType":["FixedPrice"],"gift":["false"]}],
              "returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["183161209931"],
              "title":["1 Pair - JENSEN RP201 Horns + RP201 H-F Unit Compression Drivers - 16 Ohms"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mqVhhyAT4V8qBM45j9jmBIQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/1-Pair-JENSEN-RP201-Horns-RP201-H-F-Unit-Compression-Drivers-16-Ohms-\/183161209931"],
              "paymentMethod":["CashOnPickup","PayPal"],"autoPay":["false"],
              "postalCode":["97224"],
              "location":["Portland,OR,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"380.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"380.0"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P1DT4H33M39S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-04-06T00:02:31.000Z"],"endTime":["2018-04-16T00:02:31.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["12"]}],"returnsAccepted":["true"],"isMultiVariationListing":["false"],"topRatedListing":["true"]

           },{"itemId":["162988530803"],
              "title":["ALTEC LANSING  311-90 Horn for 288 290 291 292 299 drivers "],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mzRY0LYxDsD1ETtl0gj_xOQ\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/ALTEC-LANSING-311-90-Horn-288-290-291-292-299-drivers-\/162988530803"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["35210"],
              "location":["Birmingham,AL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"50.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"399.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"399.99"}],"bidCount":["1"],"sellingState":["Active"],"timeLeft":["P1DT6H36M27S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-04-09T02:05:02.000Z"],"endTime":["2018-04-16T02:05:02.000Z"],
              "listingType":["Auction"],"gift":["false"],"watchCount":["25"]}],"returnsAccepted":["true"],"galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/162988530803_1_0_1.jpg"],"isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["282602694679"],
              "title":["ALTEC LANSING 604E Super 15\\" Duplex Horn Speakers N-1500-A Crossover Pair"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mTRKR64kQS_8hQCnfmSzwnw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/ALTEC-LANSING-604E-Super-15-Duplex-Horn-Speakers-N-1500-A-Crossover-Pair-\/282602694679"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["58701"],
              "location":["Minot,ND,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["Free"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"2200.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"2200.0"}],"sellingState":["Active"],"timeLeft":["P20DT5H24M55S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2017-08-08T00:53:54.000Z"],"endTime":["2018-05-05T00:53:54.000Z"],
              "listingType":["FixedPrice"],"gift":["false"],"watchCount":["51"]}],
              "returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["192509883813"],
              "title":["Vintage THE FISHER 100 SPEAKER SYSTEM ~ Pair Retro Speakers Long Island City NY"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],"categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mqfVuLsXXqLnM1kj8AfComg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-FISHER-100-SPEAKER-SYSTEM-Pair-Retro-Speakers-Long-Island-City-NY-\/192509883813"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["12309"],
              "location":["Schenectady,NY,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["4"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"38.88"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"38.88"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P5DT18H35M17S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"51.88"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"51.88"}],"startTime":["2018-04-13T14:07:11.000Z"],"endTime":["2018-04-20T14:07:11.000Z"],
              "listingType":["AuctionWithBIN"],"gift":["false"]}],
              "returnsAccepted":["false"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["162988285719"],
              "title":["RCA 12SN7GT Electron Radiotron Radio Audio Amp Vacuum Tube Antique TV NOS"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mBi0IeLkbbbJ_lrQVn0Q4Qw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/RCA-12SN7GT-Electron-Radiotron-Radio-Audio-Amp-Vacuum-Tube-Antique-TV-NOS-\/162988285719"],
              "paymentMethod":["PayPal"],
              "autoPay":["true"],
              "postalCode":["15679"],
              "location":["Ruffs Dale,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FlatDomesticCalculatedInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"14.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"14.0"}],"sellingState":["Active"],"timeLeft":["P28DT4H58M34S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-04-08T18:58:48.000Z"],"endTime":["2018-05-08T18:58:48.000Z"],
              "listingType":["StoreInventory"],"gift":["false"]}],
              "returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

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
              "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2018-03-13T01:48:50.000Z"],"endTime":["2018-04-12T01:48:50.000Z"],
              "listingType":["FixedPrice"],"gift":["false"]}],
              "returnsAccepted":["true"],"isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["123046984227"],
              "title":["Tests NOS GE USA 5R4GB 2 Black T Plate Side [] Get HANGING FILAMENT Tube 100+%"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/m9xY_ranr2aV2hVP_LHMZ1g\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Tests-NOS-GE-USA-5R4GA-2-Black-T-Plate-Side-Get-HANGING-FILAMENT-Tube-100-\/123046984227"],
              "paymentMethod":["PayPal"],"autoPay":["true"],
              "postalCode":["01027"],
              "location":["Easthampton,MA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"4.99"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"12.95"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"12.95"}],"sellingState":["Active"],"timeLeft":["P19DT4H26M22S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-03-28T17:57:55.000Z"],"endTime":["2018-04-27T17:57:55.000Z"],
              "listingType":["StoreInventory"],"gift":["false"]}],
              "returnsAccepted":["true"],
              "condition":[{"conditionId":["1000"],"conditionDisplayName":["New"]}],"isMultiVariationListing":["false"],"topRatedListing":["true"]

           },{"itemId":["162988285720"],
              "title":["Tung-Sol 5881 (6L6WGB) amplifier tube. TV-7 test NOS. for Bendix USA SHIPS ONLY"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mBi0IeLkbbbJ_lrQVn0Q4Qw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/RCA-12SN7GT-Electron-Radiotron-Radio-Audio-Amp-Vacuum-Tube-Antique-TV-NOS-\/162988285720"],
              "paymentMethod":["PayPal"],
              "autoPay":["true"],
              "postalCode":["15679"],
              "location":["Ruffs Dale,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FlatDomesticCalculatedInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"14.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"14.0"}],"sellingState":["Active"],"timeLeft":["P28DT4H58M34S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-04-08T18:58:48.000Z"],"endTime":["2018-05-08T18:58:48.000Z"],
              "listingType":["StoreInventory"],"gift":["false"]}],
              "returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

           },{"itemId":["162988285721"],
              "title":["Tung-Sol 6L6WGB 5881 amplifier tube. TV-7 test NOS. for Bendix USA SHIPS ONLY"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mBi0IeLkbbbJ_lrQVn0Q4Qw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/RCA-12SN7GT-Electron-Radiotron-Radio-Audio-Amp-Vacuum-Tube-Antique-TV-NOS-\/162988285721"],
              "paymentMethod":["PayPal"],
              "autoPay":["true"],
              "postalCode":["15679"],
              "location":["Ruffs Dale,PA,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FlatDomesticCalculatedInternational"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"14.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"14.0"}],"sellingState":["Active"],"timeLeft":["P28DT4H58M34S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],"startTime":["2018-04-08T18:58:48.000Z"],"endTime":["2018-05-08T18:58:48.000Z"],
              "listingType":["StoreInventory"],"gift":["false"]}],
              "returnsAccepted":["true"],"isMultiVariationListing":["false"],
              "topRatedListing":["false"]

            },{"itemId":["142842525513"],
               "title":["Lot of 10 Vintage Vacuum Tubes - TUNG-SOL 6AU6A - Tested "],
               "globalId":["EBAY-US"],
               "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
               "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mYUzp63N0ufwx1E7i6fkvOA\/140.jpg"],
               "viewItemURL":["http:\/\/www.ebay.com\/itm\/Lot-10-Vintage-Vacuum-Tubes-TUNG-SOL-6AU6A-Tested-\/142842525513"],
               "paymentMethod":["PayPal"],"autoPay":["false"],
               "postalCode":["51501"],
               "location":["Council Bluffs,IA,USA"],
               "country":["US"],
               "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["4"]}],
               "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"5.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"5.0"}],
               "bidCount":["0"],
               "sellingState":["Active"],
               "timeLeft":["P6DT3H12M26S"]}],
               "listingInfo":[{"bestOfferEnabled":["false"],
               "buyItNowAvailable":["false"],
               "startTime":["2018-06-23T17:00:47.000Z"],
               "endTime":["2018-06-30T17:00:47.000Z"],
               "listingType":["Auction"],
               "gift":["false"]}],
               "returnsAccepted":["true"],
               "isMultiVariationListing":["false"],
               "topRatedListing":["false"]

            },{"itemId":["273340636575"],
               "title":["Supreme TV-7 TUBE TESTER military vintage test western electric 300b"],
               "globalId":["EBAY-US"],
               "primaryCategory":[{"categoryId":["170062"],"categoryName":["Tube Testers"]}],"secondaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
               "galleryURL":["http:\/\/thumbs4.ebaystatic.com\/m\/mUPbClYdYXaa0OwqfcQKGVA\/140.jpg"],
               "viewItemURL":["http:\/\/www.ebay.com\/itm\/military-TV-7-TUBE-TESTER-vintage-WORKING-CONDITION-test-western-electric-300b-\/273340636575"],
               "paymentMethod":["PayPal"],"autoPay":["false"],
               "postalCode":["17101"],
               "location":["Harrisburg,PA,USA"],
               "country":["US"],
               "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"39.8"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
               "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"51.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"51.0"}],
               "bidCount":["5"],
               "sellingState":["Active"],
               "timeLeft":["P7DT19H15M26S"]}],
               "listingInfo":[{"bestOfferEnabled":["false"],
               "buyItNowAvailable":["false"],
               "startTime":["2018-07-06T02:55:36.000Z"],
               "endTime":["2018-07-16T02:55:36.000Z"],
               "listingType":["Auction"],
               "gift":["false"],
               "watchCount":["53"]}],
               "returnsAccepted":["true"],
               "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
               "isMultiVariationListing":["false"],"topRatedListing":["false"]

            },{"itemId":["263776955668"],
               "title":["LOT OF 10 5823 NOS NATIONAL GENERAL ELECTRIC RCA AND AMPEREX"],
               "globalId":["EBAY-US"],
               "primaryCategory":[{"categoryId":["64627"],"categoryName":["Vintage Tubes & Tube Sockets"]}],
               "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mOB9zh8Ul1-mB_H66hDsONg\/140.jpg"],
               "viewItemURL":["http:\/\/www.ebay.com\/itm\/LOT-10-5823-NOS-NATIONAL-GENERAL-ELECTRIC-RCA-AND-AMPEREX-\/263776955668"],
               "paymentMethod":["PayPal"],
               "autoPay":["false"],
               "postalCode":["14004"],
               "location":["Alden,NY,USA"],
               "country":["US"],
               "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["0"]}],
               "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"6.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"6.0"}],
               "bidCount":["0"],
               "sellingState":["Active"],
               "timeLeft":["P6DT23H18M25S"]}],
               "listingInfo":[{"bestOfferEnabled":["false"],
               "buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"28.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"28.0"}],
               "startTime":["2018-06-24T13:05:37.000Z"],
               "endTime":["2018-07-01T13:05:37.000Z"],
               "listingType":["AuctionWithBIN"],
               "gift":["false"]}],
               "returnsAccepted":["true"],
               "isMultiVariationListing":["false"],
               "topRatedListing":["false"]

            },{"itemId":["173375697400"],
               "title":["Pair (2)  '56 Jensen ST-875 \\/ H222 ~ Coaxial Hi-Fi Speaker & H.F. Balance p12 rp"],
               "globalId":["EBAY-US"],
               "subtitle":["Working Pair 12\\" Coaxial Speakers & Balance Controls"],
               "primaryCategory":[{"categoryId":["50597"],
               "categoryName":["Vintage Speakers"]}],
               "galleryURL":["http:\/\/thumbs1.ebaystatic.com\/m\/mBaZSgE-rozcGnSHXpkh9Ag\/140.jpg"],
               "viewItemURL":["http:\/\/www.ebay.com\/itm\/Pair-2-56-Jensen-ST-875-H222-Coaxial-Hi-Fi-Speaker-H-F-Balance-p12-rp-\/173375697400"],
               "paymentMethod":["PayPal"],
               "autoPay":["false"],
               "location":["USA"],
               "country":["US"],
               "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"35.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
               "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"112.5"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"112.5"}],
               "bidCount":["6"],
               "sellingState":["Active"],
               "timeLeft":["P6DT1H3M41S"]}],
               "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
               "startTime":["2018-06-25T00:00:19.000Z"],
               "endTime":["2018-07-02T00:00:19.000Z"],
               "listingType":["Auction"],
               "gift":["false"],
               "watchCount":["21"]}],
               "returnsAccepted":["true"],
               "isMultiVariationListing":["false"],"topRatedListing":["true"]

           },{"itemId":["192577735613"],
              "title":["10 vintage tubes 6AU6 tubes Philips Mullard Super Radiotron tested NIB"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["64627"],
              "categoryName":["Vintage Tubes & Tube Sockets"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/mJvSME4c-rA_rFIZsAFelhg\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/10-vintage-tubes-6AU6-tubes-Philips-Mullard-Super-Radiotron-tested-NIB-\/192577735613"],
              "paymentMethod":["PayPal","MoneyXferAccepted"],"autoPay":["false"],
              "postalCode":["2000"],
              "location":["Australia"],
              "country":["AU"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"AUD","__value__":"20.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"14.84"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P5DT9H1M7S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-06-24T08:09:18.000Z"],
              "endTime":["2018-07-01T08:09:18.000Z"],
              "listingType":["Auction"],
              "gift":["false"],
              "watchCount":["3"]}],
              "returnsAccepted":["true"],
              "galleryPlusPictureURL":["http:\/\/galleryplus.ebayimg.com\/ws\/web\/192577735613_1_1_1.jpg"],
              "condition":[{"conditionId":["3000"],
              "conditionDisplayName":["Used"]}],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

           },{"itemId":["292640430401"],
              "title":["Vintage SET JENSEN IMPERIAL SPEAKER CROSSOVER NETWORK A-61, A-402, M 1131"],
              "globalId":["EBAY-US"],
              "primaryCategory":[{"categoryId":["50597"],
              "categoryName":["Vintage Speakers"]}],
              "galleryURL":["http:\/\/thumbs2.ebaystatic.com\/m\/m9EwLRb7tw7RJxl7yvKTEgw\/140.jpg"],
              "viewItemURL":["http:\/\/www.ebay.com\/itm\/Vintage-SET-JENSEN-IMPERIAL-SPEAKER-CROSSOVER-NETWORK-A-61-A-402-M-1131-\/292640430401"],
              "paymentMethod":["PayPal"],"autoPay":["false"],
              "postalCode":["60016"],
              "location":["Des Plaines,IL,USA"],
              "country":["US"],
              "shippingInfo":[{"shippingType":["Calculated"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["2"]}],
              "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"999.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"999.0"}],
              "bidCount":["0"],
              "sellingState":["Active"],
              "timeLeft":["P1DT12H49M31S"]}],
              "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
              "startTime":["2018-07-14T01:06:44.000Z"],
              "endTime":["2018-07-24T01:06:44.000Z"],
              "listingType":["Auction"],"gift":["false"],
              "watchCount":["6"]}],"returnsAccepted":["false"],
              "isMultiVariationListing":["false"],"topRatedListing":["false"]

              }]

           }],

        "paginationOutput":[{"pageNumber":["1"],"entriesPerPage":["100"],"totalPages":["24"],"totalEntries":["2374"]}],
        "itemSearchURL":["http:\/\/www.ebay.com\/sch\/i.html?_nkw=catalin&_ddo=1&_ipg=100&_pgn=1"]
   }
 ]
}'''

sManualItems2Test = \
'''{"findItemsByKeywordsResponse":
  [{"ack":["Success"],"version":["1.13.0"],"timestamp":["2020-04-29T23:04:24.581Z"],
    "searchResult":
      [{"@count":"4",
        "item": [
           { "itemId":["303545301410"],
             "title":["McIntosh C22 Tube Stereo Preamp Owner's Manual - ORIGINAL- near mint w\/extras!"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["39996"],"categoryName":["Vintage Manuals"]}],
             "galleryURL":["https:\/\/thumbs3.ebaystatic.com\/m\/mFrlcZW5VWRCdJ0Oig21pqA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/McIntosh-C22-Tube-Stereo-Preamp-Owners-Manual-ORIGINAL-near-mint-w-extras-\/303545301410"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["900**"],"location":["Los Angeles,CA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"10.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"13.8"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"13.8"}],"bidCount":["0"],"sellingState":["Active"],"timeLeft":["P3DT5H43M15S"]}],
             "listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["true"],"buyItNowPrice":[{"@currencyId":"USD","__value__":"150.0"}],"convertedBuyItNowPrice":[{"@currencyId":"USD","__value__":"150.0"}],
             "startTime":["2020-04-20T02:27:12.000Z"],
             "endTime":["2020-04-27T02:27:12.000Z"],
             "listingType":["AuctionWithBIN"],"gift":["false"],"watchCount":["1"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["2750"],"conditionDisplayName":["Like New"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["193427753317"],
             "title":["The Fisher X-100-B Stereo Amplifier Service Manual"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["39996"],"categoryName":["Vintage Manuals"]}],
             "galleryURL":["https:\/\/thumbs2.ebaystatic.com\/m\/m0JOlIeCxjwAJh4-DASCWeA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Fisher-X-100-B-Stereo-Amplifier-Service-Manual-\/193427753317"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["021**"],"location":["Brighton,MA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"4.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"12.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"12.99"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P0DT23H17M53S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],
             "startTime":["2020-04-17T20:01:38.000Z"],
             "endTime":["2020-04-24T20:01:38.000Z"],
             "listingType":["Auction"],"gift":["false"],"watchCount":["1"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["5000"],"conditionDisplayName":["Good"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["153883438316"],
             "title":["Heathkit Capacitor Checker Model IT-28 Manual"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["183079"],"categoryName":["Other Vintage Electronics"]}],
             "galleryURL":["https:\/\/thumbs1.ebaystatic.com\/m\/mm1_bIELSVy_V_iNLzUKrgw\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Heathkit-Capacitor-Checker-Model-IT-28-Manual-\/153883438316"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["837**"],"location":["Boise,ID,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["true"],"oneDayShippingAvailable":["false"],"handlingTime":["1"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"15.0"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"15.0"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P2DT21H14M19S"]}],
             "listingInfo":[{"bestOfferEnabled":["true"],"buyItNowAvailable":["false"],"startTime":["2020-03-31T19:16:05.000Z"],"endTime":["2020-04-05T19:16:05.000Z"],"listingType":["Auction"],"gift":["false"],"watchCount":["5"]}],"returnsAccepted":["true"],
             "condition":[{"conditionId":["3000"],"conditionDisplayName":["Used"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

         },{ "itemId":["193390315883"],
             "title":["The Fisher X-100 Stereo Amplifier Service Manual"],
             "globalId":["EBAY-US"],
             "primaryCategory":[{"categoryId":["39996"],"categoryName":["Vintage Manuals"]}],
             "galleryURL":["https:\/\/thumbs4.ebaystatic.com\/m\/m0JOlIeCxjwAJh4-DASCWeA\/140.jpg"],
             "viewItemURL":["https:\/\/www.ebay.com\/itm\/Fisher-X-100-B-Stereo-Amplifier-Service-Manual-\/193390315883"],
             "paymentMethod":["PayPal"],"autoPay":["false"],
             "postalCode":["021**"],"location":["Brighton,MA,USA"],"country":["US"],
             "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"4.0"}],"shippingType":["Flat"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"],"handlingTime":["3"]}],
             "sellingStatus":[{"currentPrice":[{"@currencyId":"USD","__value__":"12.99"}],"convertedCurrentPrice":[{"@currencyId":"USD","__value__":"12.99"}],
             "bidCount":["0"],"sellingState":["Active"],"timeLeft":["P3DT6H18M13S"]}],"listingInfo":[{"bestOfferEnabled":["false"],"buyItNowAvailable":["false"],
             "startTime":["2020-03-20T20:00:28.000Z"],
             "endTime":["2020-03-27T20:00:28.000Z"],
             "listingType":["Auction"],"gift":["false"]}],"returnsAccepted":["false"],
             "condition":[{"conditionId":["5000"],"conditionDisplayName":["Good"]}],
             "isMultiVariationListing":["false"],"topRatedListing":["false"]

              }]

           }],

        "paginationOutput":[{"pageNumber":["1"],"entriesPerPage":["100"],"totalPages":["1"],"totalEntries":["4"]}],
        "itemSearchURL":["http:\/\/www.ebay.com\/sch\/i.html?_nkw=catalin&_ddo=1&_ipg=100&_pgn=1"]
   }
 ]
}'''
# ###      if you add an item whose title includes a double quote,       ###
# ### you must manually convert a signle backslash to a double backslash ###
# ###      also first item is tested in core.test_utils_ebay             ###

# ###    if you add a new item, it will only show up in test_stars.py    ###
# ###     if the category is among the test categories in ebay_info      ###



sLastPageZeroEntries = \
'''{"findItemsAdvancedResponse":
    [  { "ack":["Success"],
         "version":["1.13.0"],
         "timestamp":["2018-05-31T21:26:08.971Z"],
         "searchResult":[{"@count":"0"}],
         "paginationOutput":
            [ { "pageNumber":["15"],
                "entriesPerPage":["100"],
                "totalPages":["15"],
                "totalEntries":["1500"]}],
         "itemSearchURL":["http:\/\/www.ebay.com\/sch\/183077\/i.html?_nkw=magazine&_ddo=1&_ipg=100&_pgn=16"]}]}'''

# CollectableTVs_ID_16
sSuccessButZeroResults = \
'''{"findItemsByCategoryResponse":
    [   {"ack":["Success"],
    "version":["1.13.0"],
    "timestamp":["2018-06-07T23:47:55.652Z"],
    "searchResult":[{"@count":"0"}],
    "paginationOutput":
        [ { "pageNumber":["0"],
            "entriesPerPage":["100"],
            "totalPages":["0"],
            "totalEntries":["0"]}],
    "itemSearchURL":["http:\/\/www.ebay.com\/sch\/73374\/i.html?_ddo=1&_ipg=100&_pgn=10"]}]}'''
