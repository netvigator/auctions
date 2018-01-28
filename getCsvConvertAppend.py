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
from os             import environ, listdir
from os.path        import join
from sys            import path

from Dir.Get        import sTempDir
from String.Output  import ReadableNo
from Time.Output    import sayGMT
from Utils.Config   import getConfDict
from Utils.Config   import getBoolOffYesNoTrueFalse as getBool

import django


path.append('~/Devel/auctions')

environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

django.setup()


# as import scripts are implemented, import the models here
#from auctionshoppingbot.auctionbot.models \
#   import Brand, Type, Model, BrandType

from brands.models      import Brand
from categories.models  import Category, BrandCategory
from models.models      import Model
from core.user_one      import oUserOne


dConvertConf        = getConfDict('getCsvConvertAppend.conf')

sCsvPath            = dConvertConf['main']['csvpath']
bCrashOnErrors      = getBool(
                      dConvertConf['main']['crashonerrors'] )
sModelPicsPath      = dConvertConf['main']['cmodelpicspath']

sGMT = sayGMT( sBetween = '_' )
#
sErrorFile          = join( sTempDir, 'conversion_errors_%s.txt'  % sGMT )


oHongKongTime = timezone('Asia/Bangkok')


oBrands     = Brand.objects
oCategories = Category.objects
oModels     = Model.objects

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
    #
    oBrand = Brand()
    #
    oBrand.cTitle        = oRow['CFULLNAME']
    oBrand.bWanted       = not getBool(oRow['LNOTWANTED'])
    oBrand.bAllOfInterest=     getBool(oRow['LALLOFINTEREST'])
    oBrand.iStars        = int( float( oRow['NSTARS'] ) )
    oBrand.cComment      = oRow['CCOMMENTS']
    oBrand.cNationality  = _getNationality( oRow['CNATIONALITY'] )
    oBrand.cExcludeIf    = ''
    oBrand.iLegacyKey    = int( oRow['BRANDINTEGER'] )
    oBrand.tLegacyCreate = getTimeStampGotString( oRow['TCREATE'] )
    oBrand.tLegacyModify = getTimeStampGotString( oRow['TMODIFY'] )
    oBrand.iUser         = oUserOne
    #
    return oBrand


def _Category( oRow ):
    #
    #from auctionshoppingbot.auctionbot.models import Type
    #
    oT                  = Category()
    #
    oT.cTitle           = oRow['CDESCRIBE']
    oT.cKeyWords        = oRow['CKEYWORDS'].replace( '/', ',' )
    #oT.bKeyWordRequired= getBool(oRow['LKEYWORDSREQUIRED'])
    oT.iStars           = int( float( oRow['NSTARS'] ) )
    oT.bAllOfInterest   = getBool(oRow['LALLOFINTEREST'])
    oT.bWantPair        = getBool(oRow['LWANTPAIR'])
    oT.bAccessory       = getBool(oRow['LACCESSORY'])
    oT.bComponent       = getBool(oRow['LCOMPONENT'])
    oT.bsupercede       = getBool(oRow['LSUPERCEDE'])
    oT.iLegacyKey       = int( oRow['TYPEINTEGER'] )
    oT.iLegacyFamily    = int( oRow['FAMILYINTEGER'] )
    oT.tLegacyCreate    = getTimeStampGotString( oRow['TCREATE'] )
    oT.tLegacyModify    = getTimeStampGotString( oRow['TMODIFY'] )
    #
    oT.iUser            = oUserOne
    #
    return oT



def _CategoryFamily():
    #
    oAllCategories = Category.objects.all()
    #
    for oT in oAllCategories:
        #
        iLegacyFamily = oT.iLegacyFamily
        #
        if iLegacyFamily > 0:
            #
            oMainCategory = (
                Category.objects.filter( iLegacyKey = iLegacyFamily ).first() )
            #
            oT.iFamily = oMainCategory
            #
            oT.save()
            #
            # not working 2017-11-12
            #
        #
    #

# oCategories  = Category.objects

def _Model( oRow ):
    #
    # from auctionshoppingbot.auctionbot.models import Model
    #
    oM                  = Model()
    #
    oM.cTitle           = oRow['CMODELNO']
    if getBool( oRow['LKEYWORDSREQUIRED'] ):
        oM.cKeyWords        = oRow['CKEYWORDS']
    #oM.bKeyWordRequired=     getBool( oRow['LKEYWORDSREQUIRED'] )
    #oM.bSplitDigitsOK  =     getBool( oRow['LSPLITDIGITSOK'] )
    oM.iStars           = int( float( oRow['NSTARS'] ) )
    oM.bGenericModel    =     getBool( oRow['LGENERICMODEL'] )
    oM.bSubModelsOK     = not getBool( oRow['LNOMODELVARIATIONS'] )
    oM.bMustHaveBrand   =     getBool( oRow['LMUSTHAVEBRAND'] )
    oM.bWanted          = not getBool( oRow['LNOTINTEREST'] )
    oM.bGetPictures     = not getBool( oRow['LNOPICTURES'] )
    oM.bGetDescription  = not getBool( oRow['LNODESCRIPTION'] )
    oM.cComment         = oRow['CCOMMENTS'] + oRow['MCOMMENTS'] 
    oM.iLegacyKey       = oRow['MODELINTEGER']
    oM.ilegacybrand     = oRow['BRANDINTEGER']
    oM.ilegacytype      = oRow['TYPEINTEGER']
    oM.tLegacyCreate    = getTimeStampGotString( oRow['TCREATE'] )
    oM.tLegacyModify    = getTimeStampGotString( oRow['TMODIFY'] )
    #
    oM.iBrand           = oBrands.filter(iLegacyKey =oM.ilegacybrand).first()
    oM.iCategory        = oCategories.filter( iLegacyKey =oM.ilegacytype ).first()
    #
    oM.iUser            = oUserOne
    #
    return oM


tLegacyModelPicCols = (
    'MPICFILESPEC',   'MFILESPECBIG',   'MFILESPECWIDE',
    'MFILESPECHALF1', 'MFILESPECHALF2', 'MFILESPECLR' )

tNewModelPicCols = (
    'cFileSpec1', 'cFileSpec2', 'cFileSpec3', 'cFileSpec4', 'cFileSpec5' )

dModelPicNames  = {}

def _ModelPics( oRow ):
    #
    if len( dModelPicNames ) == 0:
        #
        lModelPics = listdir( sModelPicsPath )
        #
        for sFileName in lModelPics:
            #
            dModelPicNames[ sFileName.upper() ] = sFileName
            #
        #
    #
    iRowLegacyKey   = oRow['MODELINTEGER']
    #
    oTargetModel = (
        Model.objects.filter( iLegacyKey = iRowLegacyKey ).first() )
    #
    lGotPics = []
    #
    for sColName in tLegacyModelPicCols:
        #
        cThisPic = oRow[ sColName ]
        #
        if cThisPic and len( cThisPic ) > 2:
            #
            lGotPics.append( cThisPic )
            #
        #
    #
    if lGotPics:
        #
        def getNextColName():
            #
            for sColName in tNewModelPicCols:
                #
                yield sColName
                
            #
        #
        genNextColName = getNextColName()
        #
        for sThisPic in lGotPics:
            #
            if sThisPic in dModelPicNames:
                #
                sPutInCol = next( genNextColName )
                #
                setattr( oTargetModel, sPutInCol, dModelPicNames[ sThisPic ] )
                #
            #
        #
        oReturn = oTargetModel
        #
    else:
        #
        oReturn = None
        #
    #
    return oReturn

            
        
            


def _BrandCategory( oRow ):
    #
    #from auctionshoppingbot.auctionbot.models import BrandType
    from categories.models import BrandCategory
    #
    oBC            = BrandCategory()
    #
    try:
        #
        oBC.iBrand = oBrands.filter(iLegacyKey =oRow['BRANDINTEGER']).first()
        #
    except ValueError:
        #
        if bCrashOnErrors: raise
        #
        # print(
        #     'not finding a brand row for legacy key "%s"!!!' %
        #     oRow['BRANDINTEGER'] )
        #
    try:
        #
        oBC.iCategory = oCategories.filter(
            iLegacyKey =oRow['TYPEINTEGER'] ).first()
        #
    except ValueError:
        #
        if bCrashOnErrors: raise
        #
        # print(
        #     'not finding a type row for legacy key "%s"!!!' %
        #     oRow['TYPEINTEGER'] )
        #
    #
    oBC.tLegacyCreate   = ( getTimeStampGotString( oRow['TCREATE'] ) )
    #
    oBC.iUser       = oUserOne
    #
    return oBC


tSeparator = ( '', '\n' )


def ExcludeThis( oCsvRow, oTable, cColName ):
    #
    cLook4Key = oCsvRow[ cColName ]
    #
    if isinstance( cLook4Key, type( None ) ):
        #
        return None
        #
    #
    oTableRow = oTable.filter( iLegacyKey = int( cLook4Key ) ).first()
    #
    try:
        #
        iExcludeAlready = int( bool( oTableRow.cExcludeIf ) )
        #
        if not iExcludeAlready: oTableRow.cExcludeIf = ''
        #
        oTableRow.cExcludeIf += (
                tSeparator[iExcludeAlready] + oCsvRow['CEXCLUDEIF'] )
        #
    except AttributeError:
        #
        oTableRow = None
        #
    #
    return oTableRow


'''
def _CategoryExclude( oRow ):
    #
    # ExcludeThis( oRow, Category )
    #
    oCategory = oCategories.filter(
        iLegacyKey = int( oRow['TYPEINTEGER'] ) ).first()
    #
    iExcludeAlready = int( bool( oCategory.cExcludeIf ) )
    #
    oCategory.cExcludeIf += tSeparator[ iExcludeAlready ] + oRow['CEXCLUDEIF']
    #
    oCategory.save()
'''


def _CategoryExclude( oRow):
    #
    return ExcludeThis( oRow, oCategories, 'TYPEINTEGER' )

def _BrandExclude( oRow ):
    #
    if oRow["BRANDINTEGER"].endswith( '.' ):
        #
        oRow["BRANDINTEGER"] = oRow["BRANDINTEGER"][:-1]
        #
    return ExcludeThis( oRow, oBrands, "BRANDINTEGER" )

def _ModelExclude( oRow ):
    #
    return ExcludeThis( oRow, oModels, "MODELINTEGER" )



dTables = dict(
    brands          = ['BRANDS.CSV',        _Brand          ],
    categories      = ['TYPES.CSV',         _Category, _CategoryFamily ],
    models          = ['MODELS.CSV',        _Model          ],
    BrandCategories = ['BRANDTYPES.CSV',    _BrandCategory  ],
    categoryExclude = ['TYPEEXCLUDE.CSV',   _CategoryExclude],
    brandExclude    = ['BRANDEXCLUDE.CSV',  _BrandExclude   ],
    modelExclude    = ['MODELEXCLUDE.CSV',  _ModelExclude   ],
    modelPics       = ['MODELS.CSV',        _ModelPics      ],
    )
'''
    brandsNotWanted = ['BRANDEXCLUDE.CSV',  _BrandsNotWanted],
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
    print( 'counting lines in %s ...' % sCsvFile )
    #
    oCsvFile    = getFileObject( sCsvPath, sCsvFile )
    #
    iCsvLines = -1
    #
    try:
        for oCsvRow in oCsvFile: 
            iCsvLines += 1
            oPriorRow = oCsvRow
    except UnicodeDecodeError:
        print( 'Unicode error on line %s' % str( iCsvLines ) )
        print( 'Prior row: %s' % oPriorRow )
        raise
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
        if oCsvRow is None: continue
        #
        oNewRow = doTable( oCsvRow )
        #
        if oNewRow is None: 
            iSeq += 1
            continue
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
        print(
            '\nnote that we enountered %s error%s coverting the %s data!\n' %
            ( iErrors, Plural( iErrors ), sTable ) )
        #






def doTables( lTables ):
    #
    for sTable in lTables:
        #
        if sTable not in dTables:
            #
            print( 'no such table as "%s"!' % sTable )
            #
            continue
        #
        if len( dTables[ sTable ] ) < 2:
            #
            print( 'no coversion script for "%s" yet!' % sTable )
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
