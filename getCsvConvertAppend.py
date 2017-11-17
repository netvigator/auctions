#!/usr/bin/env python
# -*- coding: utf-8 -*-
#### !/usr/bin/pythonTest
#
# get CSV Convert to new data format Append to Auctions
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# The GNU General Public License is available from:
#   The Free Software Foundation, Inc.
#   51 Franklin Street, Fifth Floor
#   Boston MA 02110-1301 USA
#
#   http://www.gnu.org/licenses/gpl.html
#
# Copyright 2017 Rick Graves
#
'''


'''

from csv            import DictReader
from pytz           import timezone
from os             import environ
from os.path        import join
from sys            import exit, path

from six            import print_ as print3

from Dir.Get        import sTempDir
from String.Output  import ReadableNo
from Time.Output    import sayGMT
from Utils.Config   import getConfDict
from Utils.Config   import getBoolOffYesNoTrueFalse as getBool

import django


path.append('~/Devel/auctions')

environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

django.setup()


#if not environ.get( 'DJANGO_SETTINGS_MODULE' ):
    ##
    #exit(
        #"\nyou forgot to set the 'DJANGO_SETTINGS_MODULE' "
        #"environmental variable!\n" )
    ##

from django.contrib.auth import get_user_model

User = get_user_model()

# as import scripts are implemented, import the models here
#from auctionshoppingbot.auctionbot.models \
#   import Brand, Type, Model, BrandType

from brands.models import Brand


dConvertConf        = getConfDict('getCsvConvertAppend.conf')

sCsvPath            = dConvertConf['main']['csvpath']
bCrashOnErrors      = getBool( dConvertConf['main']['crashonerrors'] )

sGMT = sayGMT( sBetween = '_' )
#
sErrorFile          = join( sTempDir, 'conversion_errors_%s.txt'  % sGMT )


oHongKongTime = timezone('Asia/Bangkok')

oUserOne = User.objects.filter( id = 1 ).first()

if not oUserOne:
    #
    oUser = User()
    #
    oUser.cnamegiven    = 'Rick'
    oUser.cnamefamily   = 'Graves'
    oUser.cemail        = 'gravesricharde@yahoo.com'
    oUser.cusername     = 'aardvigator'
    oUser.cpasswordhash = 'tba'
    #
    oUser.save()
    #
    oUserOne = oUser


oBrands = Brand.objects


def getTimeStampGotString( sTimeStamp ):
    #
    from django.utils.timezone import make_aware
    #
    from Time.Convert import getDateTimeObjFromString
    #
    if sTimeStamp.startswith( '0000-00-00' ):
        #
        oDateTime = None
        #
    else:
        #
        oDateTime = getDateTimeObjFromString( sTimeStamp )
        #
        oDateTime = make_aware( oDateTime, timezone = oHongKongTime )
        #
    #
    return oDateTime



def _getNationality( s ):
    #
    sReturn = s
    #
    if s == 'A': sReturn = 'US'
    #
    return sReturn


def _Brand( oRow ):
    #
    # from auctionshoppingbot.auctionbot.models import Brand
    from brands.models import Brand
    #
    oBrand = Brand()
    #
    oBrand.ctitle        = oRow['CFULLNAME']
    oBrand.bwanted       = not getBool(oRow['LNOTWANTED'])
    oBrand.ballofinterest=     getBool(oRow['LALLOFINTEREST'])
    oBrand.istars        = int( float( oRow['NSTARS'] ) )
    oBrand.ccomment      = oRow['CCOMMENTS']
    oBrand.cnationality  = _getNationality( oRow['CNATIONALITY'] )
    oBrand.cexcludeif    = ''
    oBrand.ilegacykey    = int( oRow['BRANDINTEGER'] )
    oBrand.tlegacycreate = getTimeStampGotString( oRow['TCREATE'] )
    oBrand.tlegacymodify = getTimeStampGotString( oRow['TMODIFY'] )
    oBrand.iuser         = oUserOne
    #
    return oBrand


def _Category( oRow ):
    #
    #from auctionshoppingbot.auctionbot.models import Type
    #
    from categories.models import Category
    #
    oT                  = Category()
    #
    oT.ctitle           = oRow['CDESCRIBE']
    oT.ckeywords        = oRow['CKEYWORDS'].replace( '/', ',' )
    oT.bkeywordrequired = getBool(oRow['LKEYWORDSREQUIRED'])
    oT.istars           = int( float( oRow['NSTARS'] ) )
    oT.ballofinterest   = getBool(oRow['LALLOFINTEREST'])
    oT.bwantpair        = getBool(oRow['LWANTPAIR'])
    oT.baccessory       = getBool(oRow['LACCESSORY'])
    oT.bcomponent       = getBool(oRow['LCOMPONENT'])
    oT.bsupercede       = getBool(oRow['LSUPERCEDE'])
    oT.ilegacykey       = int( oRow['TYPEINTEGER'] )
    oT.ilegacyfamily    = int( oRow['FAMILYINTEGER'] )
    oT.tlegacycreate    = getTimeStampGotString( oRow['TCREATE'] )
    oT.tlegacymodify    = getTimeStampGotString( oRow['TMODIFY'] )
    #
    oT.iuser            = oUserOne
    #
    return oT



def _CategoryFamily():
    #
    from categories.models import Category
    #
    oAllCategories = Category.objects.all()
    #
    for oT in oAllCategories:
        #
        iLegacyFamily = oT.ilegacyfamily
        #
        if iLegacyFamily > 0:
            #
            oMainCategory = (
                Category.objects.filter( ilegacykey = iLegacyFamily ).first() )
            #
            oT.ifamily = oMainCategory
            #
            oT.save()
            #
            # not working 2017-11-12
            #
        #
    #

oCategories  = Category.objects

def _Model( oRow ):
    #
    # from auctionshoppingbot.auctionbot.models import Model
    from models import Model
    #
    oM                  = Model()
    #
    oM.ctitle           = oRow['CMODELNO']
    oM.ckeywords        = oRow['CKEYWORDS']
    oM.bkeywordrequired =     getBool( oRow['LKEYWORDSREQUIRED'] )
    oM.bsplitdigitsok   =     getBool( oRow['LSPLITDIGITSOK'] )
    oM.istars           = int( float( oRow['NSTARS'] ) )
    oM.bgenericmodel    =     getBool( oRow['LGENERICMODEL'] )
    oM.bsubmodelsok     = not getBool( oRow['LNOMODELVARIATIONS'] )
    oM.bmusthavebrand   =     getBool( oRow['LMUSTHAVEBRAND'] )
    oM.bwanted          = not getBool( oRow['LNOTINTEREST'] )
    oM.bgetpictures     = not getBool( oRow['LNOPICTURES'] )
    oM.bgetdescription  = not getBool( oRow['LNODESCRIPTION'] )
    oM.ccomment         = oRow['CCOMMENTS'] + oRow['MCOMMENTS'] 
    oM.ilegacykey       = oRow['MODELINTEGER']
    oM.ilegacybrand     = oRow['BRANDINTEGER']
    oM.ilegacytype      = oRow['TYPEINTEGER']
    oM.tlegacycreate    = getTimeStampGotString( oRow['TCREATE'] )
    oM.tlegacymodify    = getTimeStampGotString( oRow['TMODIFY'] )
    #
    oM.ibrand           = oBrands.filter(ilegacykey =oM.ilegacybrand).first()
    oM.itype            = oTypes.filter( ilegacykey =oM.ilegacytype ).first()
    #
    oM.iuser            = oUserOne
    #
    return oM


'''

from csv import DictReader
oFile = open( '/home/Common/Auctions_CSVs_2017-02-18/BRANDTYPES.CSV' )
oReader = DictReader( oFile )
oReader.__next__()
{'': None, 'TMODIFY': '0000-00-00_00:00:00', 'BRANDINTEGER': '6741', 'TYPEINTEGER': '3170', 'TCREATE': '2000-12-26_21:30:51'}
{'TCREATE': '2000-12-26_21:30:51', 'TYPEINTEGER': '3170', 'BRANDINTEGER': '6741', 'TMODIFY': '0000-00-00_00:00:00', '': None}

def _BrandType( oRow ):
    #
    #from auctionshoppingbot.auctionbot.models import BrandType
    from models import BrandType
    #
    oBT                 = BrandType()
    #
    try:
        #
        oBT.ibrand      = oBrands.filter(ilegacykey =oRow['BRANDINTEGER']).first()
        #
    except ValueError:
        #
        if bCrashOnErrors: raise
        #
        # print3(
        #     'not finding a brand row for legacy key "%s"!!!' %
        #     oRow['BRANDINTEGER'] )
        #
    try:
        #
        oBT.itype       = oTypes.filter( ilegacykey =oRow['TYPEINTEGER'] ).first()
        #
    except ValueError:
        #
        if bCrashOnErrors: raise
        #
        # print3(
        #     'not finding a type row for legacy key "%s"!!!' %
        #     oRow['TYPEINTEGER'] )
        #
    #
    oBT.tlegacycreate   = ( getTimeStampGotString( oRow['TCREATE'] ) )
    #
    oBT.iuser       = oUserOne
    #
    return oBT

'''
dTables = dict(
    brands      = ['BRANDS.CSV',    _Brand      ],
    categories  = ['TYPES.CSV',     _Category,  _CategoryFamily ],
    )
'''
    models      = ['MODELS.CSV',    _Model      ],
    brandtypes  = ['BRANDTYPES.CSV',_BrandType  ] )
'''

def _putErrorMsg( sTable, oNewRow, sMsg ):
    #
    from File.Write     import openAppendClose
    #
    sOut = '%s\n%s\n%s\n\n' % ( sTable, str( oNewRow.__dict__ ), sMsg )
    #
    openAppendClose( sOut, sErrorFile, bSayBytes = False )
    #


def doOneTable( sTable ):
    #
    from sys                import stdout
    #
    from six                import next as getNext
    #
    from File.Get           import getFileObject
    from String.Output      import Plural
    from Utils.Progress     import TextMeter, DummyMeter
    #
    from django.db.utils    import IntegrityError
    
    oProgressMeter  = DummyMeter()
    #
    if stdout.isatty():
        #
        oProgressMeter = TextMeter()
        #
    #
    sCsvFile    = dTables[sTable][0]
    doTable     = dTables[sTable][1]
    #
    doMore      = None
    #
    if len( dTables[sTable] ) > 2:
        doMore  = dTables[sTable][2]
    #
    print3( 'counting lines in %s ...' % sCsvFile )
    #
    oCsvFile    = getFileObject( sCsvPath, sCsvFile )
    #
    iCsvLines = -1
    #
    for sLine in oCsvFile: iCsvLines += 1
    #
    oCsvFile    = getFileObject( sCsvPath, sCsvFile )
    #
    oCsvReader  = DictReader( oCsvFile )
    #
    sLineB4     = ''
    sOnLeft     = 'stepping thru %s lines' % ReadableNo( iCsvLines )
    #
    oProgressMeter.start( iCsvLines, sOnLeft, sLineB4 )
    #
    iSeq        = 0
    iErrors     = 0
    #
    for oCsvRow in oCsvReader:
        #
        oNewRow = doTable( oCsvRow )
        #
        try:
            #
            oNewRow.save()
            #
        except IntegrityError as e:
            #
            if bCrashOnErrors:
                raise
            else:
                #
                _putErrorMsg( sTable, oNewRow, "Error {0}".format(str(e)) )
                iErrors += 1
                #
            #
        #
        iSeq    += 1
        #
        oProgressMeter.update( iSeq )
        #
    #
    oProgressMeter.end( iCsvLines )
    #
    if doMore:
        #
        doMore()
        #
    #
    if iErrors:
        #
        print3(
            '\nnote that we enountered %s error%s coverting the %s data!\n' %
            ( iErrors, Plural( iErrors ), sTable ) )
        #
    
    
    
    
    

def doTables( lTables ):
    #
    for sTable in lTables:
        #
        if sTable not in dTables:
            #
            print3( 'no such table as "%s"!' % sTable )
            #
            continue
        #
        if len( dTables[ sTable ] ) < 2:
            #
            print3( 'no coversion script for "%s" yet!' % sTable )
            continue
            #
        #
        doOneTable( sTable )
        #
    #


if __name__ == "__main__":
    #
    from sys            import argv
    #
    from Utils.Result   import sayTestResult
    #
    lProblems = []
    #
    #
    if len( argv ) >= 2:
        #
        doTables( argv[1:] )
        #
    #
    sayTestResult( lProblems )
