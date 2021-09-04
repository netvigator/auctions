'''
all secrets are in Secrets.ini
do not want to repeat them somewere (more DRY)
therefore must get all secrets from Secrets.ini
'''

from subprocess             import run

from config.settings.base   import DATABASES

from pyPks.Time.Output      import getNowIsoDateTimeFileNameSafe


POSTGRES_USER       = DATABASES['default']['USER'    ]
POSTGRES_PASSWORD   = DATABASES['default']['PASSWORD']
DATABASE_HOST       = DATABASES['default']['HOST'    ]
DATABASE_PORT       = DATABASES['default']['PORT'    ]


sURI = 'postgresql://%s:%s@%s:%s/auctions' % (
    POSTGRES_USER, POSTGRES_PASSWORD, DATABASE_HOST, DATABASE_PORT )

tDump = ( 'pg_dump', sURI, '-Fc' )

def do_backup():
    #
    sNow = getNowIsoDateTimeFileNameSafe()[:16]
    #
    sFile = "/tmp/auctions-database-%s.backup" % sNow
    #
    fDump = open( sFile, "w" )
    #
    oResult = run( tDump, stdout = fDump )
    #
    fDump.close()
    #
    return oResult.returncode, oResult.stderr



