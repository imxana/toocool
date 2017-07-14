__author__ = 'xana'


from flask import request, jsonify, g

qiniu_setting = {
    'access_key' : 'iQ3ndG5uRpwdeln_gcrH3iiZ7E3KbMdJVkdYV9Im',
    'secret_key' : 'AGsp6K7fu1NsH2DnsPi7hW3qa3JXb4dtfeGvkm-A',
    'bucket_name' : 'image',
    'bucket_domain' : 'https://oi3qt7c8d.qnssl.com/',
    'callbakUrl' : 'http://139.129.24.151/image/upload',
    'callbackBody' : 'filename:$(fname)&filesize:$(fsize)&param:$(fparam)'
}

def register(app):

    @app.route('/api/image/upload', methods=['POST'])
    def image_upload():
        """
        'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        """
        filename = request.values.get('filename', '')
        param = request.values.get('param', '')
        if filename == '':
            return jsonify({'code': '0'})

        url = qiniu_setting['bucket_domain'] + filename

        item = g.Item.query.filter_by(name=filename).first()
        if item:
            return jsonify({'code': '-2'})

        item = g.Item(name=filename, url=url, param=param)
        g.db.session.add(item)
        g.db.session.commit()

        return jsonify({
            'code': '1',
            'filename': filename,
            'url': url,
            'param': param,
            })

    @app.route('/api/image/query', methods=['GET'])
    def image_query():
        id = request.args.get('id', '')
        name = request.args.get('name', '')

        if not id:
            return jsonify({'code': '0'})

        item = g.Item.query.filter_by(id=id).first()

        if not item:
            return jsonify({'code': '-1'})

        return jsonify({
            'code': '1',
            'id': item.id,
            'url': item.url,
            'param': item.param,
        })
