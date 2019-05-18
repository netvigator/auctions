def application(environ,start_response):
    import os
    #os.environ['PYTHONPATH'] = '/home/Common/pyPacks'
    status = '200 OK'
    html = (
        '<html>\n'
        '<body>\n'
        '<h1>mod_wsgi Test Page</h1>\n'
        '<h3>wsgi environmental variables</h3>\n'
        '<table align=left>\n'
        '<tr><th align=left>variable</th><th>&nbsp;&nbsp;</th><th align=left>value</th></tr>'
        '%s\n'
        '</table>\n'
        '<p>\n'
        '<div style = "clear:both;"></div>\n'
        '<hr>\n'
        '<h3>OS environmental variables</h3>\n'
        '<table align=left>\n'
        '<tr><th align=left>variable</th><th>&nbsp;&nbsp;</th><th align=left>value</th></tr>'
        '%s\n'
        '</table>\n'
        '</body>\n'
        '</html>\n' )
    #
    lVarsOS     = []
    lVarsWSGI   = []
    #
    for k,v in os.environ.items():
        lVarsOS.append(
            '<tr><td>%s</td><td>&nbsp;&nbsp;</td><td>%s</td></tr>' %
            ( k, v ) )
    lVarsOS.sort()
    sRowsOS = '\n'.join( lVarsOS )
    #
    for k,v in    environ.items():
        if k in os.environ and os.environ[k] == v:
            pass
        else:
            lVarsWSGI.append(
                '<tr><td>%s</td><td>&nbsp;&nbsp;</td><td>%s</td></tr>' %
                ( k, v ) )
    lVarsWSGI.sort()
    sRowsWSGI = '\n'.join( lVarsWSGI )
    response_header = [('Content-type','text/html')]
    sReturn = html % ( sRowsWSGI, sRowsOS )
    bReturn = str.encode( sReturn )
    #bReturn = str.encode( html )
    start_response(status,response_header)
    return [ bReturn ]

