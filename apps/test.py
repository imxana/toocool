# for http and https test

from flask import request, json, jsonify, render_template

def register(app):

    # print the request info
    @app.route('/api/test/', methods=['GET', 'POST'])
    @app.route('/api/test/<key>', methods=['GET', 'POST'])
    def api_test(key='world'):
        if key == 'api':
            msg = {
                'METHOD'   : request.method,
                'HOST'     : request.host,
                'PATH'     : request.path,
                # 'ENVIRON'  : {},
                'HEADERS'  : {},
                'DATA'     : request.data.decode(),
                'REMOTE_ADDR': request.remote_addr,
                'ARGS'     : request.args,
                'FORM'     : request.form,
                'VALUES'   : request.values,
                'JSON'     : request.json,
                'COOKIES'  : request.cookies,
            }
            for k,v in request.environ.items():
                if 'ENVIRON' in msg:
                    msg['ENVIRON'][k] = str(v)

            for k,v in request.headers.items():
                if 'HEADERS' in msg:
                    msg['HEADERS'][k] = str(v)

            # json format
            smsg = json.dumps(msg, indent=2)

            # set the font red
            rmsg = "\033[31m\nCurl Test OK.\n----------------------------------------------------------------------\n\n%s\n\033[00m"%smsg

            # Print msg in Server
            print(rmsg)


            # if use curl to send request, return shell format
            if 'HEADERS' in msg:
                ua = msg['HEADERS'].get('User-Agent')
                if not bool(ua):
                    return render_template('test/request.html', req=None)
                elif ua.startswith('curl'):
                    return rmsg

            # return '<pre>%s</pre>'%smsg
            return render_template('test/request.html', req=smsg)

        return render_template('test/hello.html', name=key)
        # return 'hello %s'%api






