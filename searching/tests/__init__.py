
iRecordStepsForThis = None


# sItemHitLog is just a starter, the file is ItemHitsLog.log
sItemHitLog = \
'''
tTimeEnd            | iItemNumb    | iHitStars
2018-03-07 20:59:24 | 132521748790 | 175
2018-03-23 21:29:45 | 401354589892 | 200
2018-03-10 11:46:09 | 372238175241 | 270
'''

#### categories for testing are in searching/tests/test_utils.py ###

#### if you add a vacuum tube brand, ###
####  you need a BrandCategory row   ###
####    code is in test_utils.py     ###

sBrands = \
'''
      cTitle       | iStars | cExcludeIf |  cLookFor
-------------------+--------+------------+------------
 ACRO              |      9 |            |
 Addison           |      7 |            |
 Allied            |      5 |            |
 Altec-Lansing     |     10 |            | Altec
 Ampex             |      5 |            |
 Arvin             |      7 |            |
 Astronic          |      2 |            |
 Audio Research    |      5 |            |
 Bell              |      4 |            |
 Bendix            |      7 |            |
 Bogen             |      1 |            |
 Brociner          |      6 |            |
 Brook             |      8 |            |
 Coronado          |      7 |            |
 Crosley           |      3 |            |
 DeWald            |      4 |            |
 DuKane            |      7 |            |
 Dynaco            |      5 |            | Dyna\\rDynakit
 EICO              |      7 |            |
 Electro-Voice     |      7 |            | EV
 Emerson           |      6 |            |
 Fada              |      8 |            |
 Fairchild         |      8 |            |
 Fisher            |      9 |            |
 Garod             |      5 |            | Garol
 GE                |      5 |            | General Electric
 Grommes           |      5 |            |
 Harman-Kardon     |      7 |            |
 Heathkit          |      8 |            | Heath
 Hickok            |      8 |            |
 Interelectronics  |      3 |            |
 JBL               |      7 |            |
 Jensen            |      8 |            |
 Kadette           |      6 |            |
 Klangfilm         |      6 |            |
 Klipsch           |      8 |            | Klipschorn
 Knight            |      4 |            |
 Lafayette         |      7 |            |
 Langevin          |      8 |            |
 Lansing           |      9 |            | Jim Lansing\\rJames B. Lansing
 Leak              |      7 |            |
 Luxman            |      6 |            |
 Marantz           |     10 | Speaker\\rAV9000\\rreplica |
 Matsushita        |      4 |            |
 Marconi           |      7 |            |
 Mazda             |      5 |            |
 McIntosh          |      6 |            |
 MFA               |      8 |            |
 Motorola          |      7 |            |
 Mullard           |      9 |            |
 National          |      7 |            |
 PACO              |      2 |            |
 Philips           |      7 |            |
 Pilot             |      8 |            |
 Quad              |      5 |            |
 Radford           |      7 |            |
 Radio Craftsmen   |      8 |            |
 Raytheon          |      7 |            |
 RCA               |      5 |            |
 Regency           |      5 |            |
 Sargent-Rayment   |      4 |            |
 Scott, H.H.       |      8 |            | Scott\\rH.H. Scott
 Sentinel          |      6 |            |
 Sherwood          |      5 |            |
 Silvertone        |      3 |            |
 Spartan           |      8 |            |
 Supreme           |      5 |            |
 Stromberg-Carlson |      5 |            |
 Sylvania          |      6 |            |
 Tannoy            |      7 |            |
 Tung-Sol          |      6 |            |
 UTC               |      8 |            |
 Western Electric  |      9 |            |
 Westinghouse      |      5 |            |
'''

#### if you add a vacuum tube brand, ###
####  you need a BrandCategory row   ###
####    code is in test_utils.py     ###

#### note column delimiter | must have a space on one side or the other
sModels = \
'''
       cTitle       | cKeyWords | iStars | bSubModelsOK |      Brand        |     Category | cLookFor    | cExcludeIf   | bGenericModel | bMustHaveBrand |
--------------------+-----------+--------+--------------+-------------------+--------------+-------------+--------------+---------------+----------------+
 12SN7              |           |      7 | t            |                   |  Vacuum Tube | 12SN7-GT    |              | t
 6SN7GT (Sylvania)  |           |      8 | f            | Sylvania          |  Vacuum Tube |             |              | f
 6CA7               |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 6DJ8               |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 6922               |           |      5 | f            |                   |  Vacuum Tube |             |              | t
 EL34               |           |      5 | f            |                   |  Vacuum Tube |             |              | t
 6SN7GTB            |           |      6 | t            |                   |  Vacuum Tube |             |              | t
 12AU7A             |           |      5 | t            |                   |  Vacuum Tube |             |              | t
 12AX7              |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 12ax7-wa           |           |      7 | t            |                   |  Vacuum Tube |             |              | t
 12AX7-WA (Philips) |           |      8 | t            | Philips           |  Vacuum Tube |             |              | f             | t
 5R4GA              |           |      4 | t            |                   |  Vacuum Tube |             |              | t
 5R4GYB             |           |      6 | t            |                   |  Vacuum Tube |             |              | t
 5R4WGA             |           |      4 | t            |                   |  Vacuum Tube |             |              | t
 6BH6               |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 6AU6A              |           |      6 | f            |                   |  Vacuum Tube | 6AU6        |              | t
 10                 |           |      9 | f            |                   |  Vacuum Tube |             | Lot of 10\\rLot of (10)\\r^10 | t
 VT-107A (6V6GT)    |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 VT-107B (6V6G)     |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 6V6G (GE)          |           |      8 | f            | GE                |  Vacuum Tube |             |              | f             | t
 6V6G               | Sylvania\\rSilvertone | 8 | f     |                   |  Vacuum Tube |             |
 6V6G               |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 VT-107 (6V6)       |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 6V6 (metal can)    | metal\\rcan |    2 | f            |                   |  Vacuum Tube |             |
 6V6GTA             |           |      6 | t            |                   |  Vacuum Tube |             |              | t
 6V6GTA (RCA)       |           |      7 | f            | RCA               |  Vacuum Tube |             |              | f             | t
 6V6GT (Mazda)      |           |      8 | f            | Mazda             |  Vacuum Tube |             |
 6L6 (metal can)    |           |      4 | f            |                   |  Vacuum Tube |             |              | t
 5881               |           |      6 | f            |                   |  Vacuum Tube |             |              | t
 6L6G               |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 6L6GA              |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 6L6GB              |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 6L6GC              |           |      8 | f            |                   |  Vacuum Tube |             |              | t
 6L6WGB             |           |      8 | t            |                   |  Vacuum Tube |             |              | t
 EF86               |           |      7 | f            |                   |  Vacuum Tube |             |              | t
 TV-7               |           |      5 | f            | Supreme           |  Tube Tester |             |
 100 (amp)          |           |      9 | f            | Fisher            |    Amplifier |             | X-100\\rX-100-B\\rTX-100
 100 (speaker)      |           |      5 | f            | Fisher            |Speaker System|             |
 1005B              |           |      6 | t            | Altec-Lansing     |         Horn |             |
 288-8F             |           |      7 | t            | Altec-Lansing     |       Driver |             |
 288                |           |      7 | f            | Altec-Lansing     |       Driver |             |
 311-90             |           |      9 | f            | Altec-Lansing     |         Horn |             |
 440C               |           |      5 | t            | Altec-Lansing     |       Preamp |             |
 445A               |           |      8 | f            | Altec-Lansing     |       Preamp |             |
 515A               |           |      7 | t            | Altec-Lansing     |       Driver | 515         |
 542                |           |      6 | f            | Altec-Lansing     |         Horn |             |
 601a (driver)      |           |      8 | t            | Altec-Lansing     |       Driver |             |
 601B (enclosure)   |           |      7 | t            | Altec-Lansing     |Speaker Enclosure|          |
 602A               |           |      6 | t            | Altec-Lansing     |       Driver |             |
 604                |           |     10 | f            | Altec-Lansing     |       Driver |             |
 604D               |           |      8 | f            | Altec-Lansing     |       Driver |             |
 604E               |           |     10 | f            | Altec-Lansing     |       Driver |             |
 604-8G             |           |      7 | f            | Altec-Lansing     |       Driver |             |
 606                |           |     10 | f            | Altec-Lansing     |Speaker Enclosure|          |
 755A               |           |      7 | t            | Altec-Lansing     |       Driver |             |
 803A (driver)      |           |      7 | t            | Altec-Lansing     |       Driver |             | horn         |
 803B (horn)        |           |      7 | t            | Altec-Lansing     |         Horn |             |
 806A               |           |      7 | t            | Altec-Lansing     |       Driver |             |
 890                |           |      7 | f            | Altec-Lansing     |Speaker Enclosure| Bolero   |
 811B               |           |      6 | t            | Altec-Lansing     |         Horn |             |
 A-433A             |           |      8 | t            | Altec-Lansing     |       Preamp |             |
 A-5                |           |      8 | f            | Altec-Lansing     |Speaker System|             |
 N-500B             |           |      6 | t            | Altec-Lansing     |    Crossover |             |
 N-1500A            |           |      6 | t            | Altec-Lansing     |    Crossover |             |
 N-1600A            |           |      6 | t            | Altec-Lansing     |    Crossover |             |
 N-3000A            |           |      6 | t            | Altec-Lansing     |    Crossover |             |
 N-3900A            |           |      6 | t            | Altec-Lansing     |    Crossover |             |
 603-b              |           |      7 | t            | Altec-Lansing     |       Driver |             |
 150-4B             |           |      9 | t            | Lansing           |       Driver |             |
 Designers Handbook | Radiotron |      6 | f            | RCA               |         Book | Designer's Handbook |
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
 SP-6               |           |      9 | f            | Audio Research    |       Preamp |             |
 PAS-3              |           |      7 | f            | Dynaco            |       Preamp |             | PAS-2
 SP-8               |           |      9 | f            | Audio Research    |       Preamp |             |
 S1001              |           |      6 | f            | ACRO              |       Preamp |             |
 116B               |           |      9 | t            | Langevin          |       Preamp |             |
 PR-100A            |           |      8 | t            | Bogen             |       Preamp |             |
 Consolette         |           |      6 | f            | Interelectronics  |       Preamp |             |
 400-C              |           |      7 | f            | Fisher            |       Preamp |             | 400-CX
 130                |           |      8 | f            | Scott, H.H.       |       Preamp |             |
 Citation I         |           |      8 | f            | Harman-Kardon     |       Preamp |             | Sixteen
 WA-P2              |           |      5 | f            | Heathkit          |       Preamp |             |
 KT-600A            |           |      9 | t            | Lafayette         |       Preamp |             |
 4B                 |           |      7 | f            | Brook             |       Preamp |             | Bryston
 C-4                |           |      4 | f            | McIntosh          |       Preamp |             |
 C-108H             |           |      4 | t            | McIntosh          |       Preamp |             |
 CL-35              |           |      7 | f            | Luxman            |       Preamp |             |
 Luminescence       |           |      9 | f            | MFA               |       Preamp |             |
 SC2                |           |      7 | f            | Radford           |       Preamp |             |
 C-32               |           |      7 | f            | Luxman            |       Preamp |             |
 50-C               |           |      7 | f            | Fisher            |       Preamp |             |
 CL-32              |           |      8 | f            | Luxman            |       Preamp |             |
 C-8                |           |      4 | f            | McIntosh          |       Preamp |             | C-8S
 2a                 |           |      6 | t            | Audio Research    |Speaker System|             | LST-2\\r2 way\\r(2)
 SP-1               |           |      9 | f            | Audio Research    |       Preamp |             |
 SP-2               |           |      9 | f            | Audio Research    |       Preamp |             |
 SP-3               |           |      9 | f            | Audio Research    |       Preamp |             |
 SP-3A1             |           |      9 | f            | Audio Research    |       Preamp |             |
 SP-11              |           |      9 | f            | Audio Research    |       Preamp |             |
 SP-12              |           |      9 | f            | Audio Research    |       Preamp |             |
 A100               |           |      5 | f            | Brociner          |       Preamp |             |
 12A3               |           |      8 | f            | Brook             |       Preamp |             |
 A100PV             |           |      5 | f            | Brociner          |       Preamp |             |
 A1005              |           |      5 | f            | Brociner          |       Preamp |             |
 CA-2               |           |      5 | f            | Brociner          |       Preamp |             |
 Mark 30C           |           |      5 | t            | Brociner          |       Preamp |             |
 3G                 |           |      7 | t            | Brook             |       Preamp |             |
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
 QC II              |           |      8 | f            | Quad              |       Preamp |             |
 400-CX             |           |     10 | f            | Fisher            |       Preamp |             | 400-CX-2
 350-P              |           |      8 | f            | Regency           |       Preamp |             | AD1/350
 350                |           |      3 | f            | Ampex             |       Preamp |             | AD1/350
 7                  |           |      9 | f            | Brook             |       Preamp |             | Marantz
 Quad 33            |           |      2 | f            | Quad              |       Preamp |             |
 PAS-3X             |           |      9 | f            | Dynaco            |       Preamp |             |
 Audio Consolette   |           |     10 | f            | Marantz           |       Preamp |           1 | 1 pc\\r45\\rDD 5.1\\rDLB\\rWC-1\\rMA500\\rPMD\\r1050\\r200\\rQuad Adapter\\rSQ\\rVan Alstine\\rChannel\\rRecorder
 245                |           |      9 | f            | Fairchild         |       Preamp |             |
 7                  |           |     10 | f            | Marantz           |       Preamp |             | 7 pcs\\rBrook\\r7T\\rSC-7\\rSG-7\\rfaceplate
 2                  |           |     10 | f            | Marantz           |    Amplifier | Model Two\\rModel 2 |
 400-CX (4 button)  |           |      8 | f            | Fisher            |       Preamp |             | 400-CX-2
 400-CX-2           |           |     10 | f            | Fisher            |       Preamp |             |
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
 Imperial           |           |      9 | f            | Jensen            |Speaker System|             |
 15" Silver         |           |      7 | f            | Tannoy            |       Driver |             |
 GRF                |           |      7 | f            | Tannoy            |Speaker System|             |
 539-A              |           |      5 | f            | Hickok            |  Tube Tester |             |
 539-B              |           |      9 | f            | Hickok            |  Tube Tester |             |
 539-C              |           |      5 | f            | Hickok            |  Tube Tester |             |
 75                 |           |     10 | f            | JBL               |       Driver | 075         |
 175                |           |     10 | f            | JBL               |       Driver |             |
 275                |           |     10 | f            | JBL               |       Driver |             |
 D-130              |           |      7 | f            | JBL               |       Driver | 130         |
 D-130A             |           |      7 | f            | JBL               |       Driver | 130A        |
 D-130B             |           |      7 | f            | JBL               |       Driver | 130B        |
 LE5-5              |           |      5 | t            | JBL               |       Driver |             |
 1217-1290          |           |      7 | f            | JBL               |         Horn |             |
 H5040              |           |      7 | f            | JBL               |         Horn |             |
 N2400              |           |      6 | f            | JBL               |    Crossover |             |
 N2600              |           |      6 | f            | JBL               |    Crossover |             |
 N500               |           |      6 | f            | JBL               |    Crossover |             |
 C38 (Baron)        |           |      8 | f            | JBL               |Speaker Enclosure| Baron    | S-38\\rBookshelf\\rN-38
 CA-5               |           |      5 | f            | Hickok            |    Accessory |             |
 CA-3               |           |      5 | t            | Hickok            |    Accessory |             | CA-5
 Heresy (H700)      |           |      6 | f            | Klipsch           |Speaker System|             |
 K-22               |           |      6 | f            | Klipsch           |       Driver |             |
 K-55-V             |           |      6 | f            | Klipsch           |       Driver |             |
 K-77               |           |      6 | f            | Klipsch           |       Driver |             |
 K-700              |           |      6 | f            | Klipsch           |         Horn |             |
 KS-15874           |           |      9 | f            | Western Electric  |  Tube Tester |             |
 755A               |           |      8 | t            | Western Electric  |       Driver |             |
 C45 (Metregon)     |           |      6 | f            | JBL               |Speaker Enclosure| Metregon |
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
  'listingType': 'Auction',
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


#### do not add new test items here, add them below ###
#### do not add new test items here, add them below ###
#### do not add new test items here, add them below ###

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

            },{"itemId":["132401762082" ],"isMultiVariationListing":["false" ],
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

            },{"itemId":["253303813311" ],"isMultiVariationListing":["false" ],
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

            },{"itemId":["253295991282" ],"isMultiVariationListing":["false" ],
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
#### do not add new test items above, add them below ###
#### do not add new test items above, add them below ###
#### do not add new test items above, add them below ###


# ###      if you add an item whose title includes a double quote,       ###
# ### you must manually convert a signle backslash to a double backslash ###
# ###      also first item is tested in core.test_utils_ebay             ###

sResponseItems2Test = \
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
              "shippingInfo":[{"shippingServiceCost":[{"@currencyId":"USD","__value__":"0.0"}],"shippingType":["FreePickup"],"shipToLocations":["Worldwide"],"expeditedShipping":["false"],"oneDayShippingAvailable":["false"]}],
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
