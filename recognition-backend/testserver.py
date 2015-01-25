# Shows your WSGI environ
def application(environ, start_response):
    start_response('200 OK', [ ('Content-type', 'text/plain') ])
    for k in sorted(environ):
        yield '%-30s:  %r\n'%(k,environ[k])

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('', 3030, application)
    srv.serve_forever()

