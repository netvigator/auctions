'''
all secrets are in Secrets.ini
do not want to repeat them somewere (more DRY)
therefore must get all secrets from Secrets.ini
'''
from os                     import environ

from subprocess             import run

from config.settings.base   import DATABASES

from pyPks.Time.Output      import getNowIsoDateTimeFileNameSafe


POSTGRES_USER       = DATABASES['default']['USER'    ]
POSTGRES_PASSWORD   = DATABASES['default']['PASSWORD']
DATABASE_HOST       = DATABASES['default']['HOST'    ]
DATABASE_PORT       = DATABASES['default']['PORT'    ]

POSTGRES_ADMIN      = DATABASES['default']['ADMIN'   ]
POSTGRES_ADMIN_PW   = DATABASES['default']['ADMIN_PW']

sURI = 'postgresql://%s:%s@%s:%s/auctions' % (
    POSTGRES_USER, POSTGRES_PASSWORD, DATABASE_HOST, DATABASE_PORT )

tDump = ( 'pg_dump', sURI, '-Fc' )

sAdmin = 'postgresql://%s:%s@%s:%s/auctions' % (
    POSTGRES_ADMIN, POSTGRES_ADMIN_PW, DATABASE_HOST, DATABASE_PORT )

tVacuum = ( 'vacuumdb', '-z', sAdmin )
#
sBackUpDir = environ["BACKUP_DIR"]
#
sNow = getNowIsoDateTimeFileNameSafe()[:16]
#
sFile = "%sauctions-database-%s.backup" % ( sBackUpDir, sNow )
#
def do_backup():
    #
    if POSTGRES_ADMIN:
        #
        oVacuum = run( tVacuum )
        #
    #
    fDump = open( sFile, "w" )
    #
    oResult = run( tDump, stdout = fDump )
    #
    fDump.close()
    #
    return oResult.returncode, oResult.stderr


