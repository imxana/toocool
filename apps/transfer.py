# coding=utf-8
from flask import request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
import random

tasks = []
done = []


def register_front(app):

    db = SQLAlchemy(app)
    # users = cur = g.Post.query.all()

    @app.route('/api/user/add/', methods=['GET', 'POST'])
    def signup():
        username = request.values.get('username', '')
        password = request.values.get('password', '')
        email = request.values.get('email', '')

        # cur = g.User.query.filter_by(username='admin').filter_by(password='123')
        ex = g.User.query.filter_by(del_status=False)
        user = ex.filter_by(username=username).first() or ex.filter_by(email=email).first()
        if user:
            return jsonify({ 'code': -2 })

        user = db.User(username=username, email=email, psw=password)
        db.session.add(user)
        db.session.commit()

        return jsonify({ 'code': 1 })
        # return jsonify({'code':[ dict(un=row.username, ps=row.password) for row in cur] })

    @app.route('/api/user/query/', methods=['GET', 'POST'])
    def signin():
        # cur = g.User.query.all()
        username = request.values.get('username', '')
        password = request.values.get('password', '')
        user = g.User.query.filter_by(del_status=False, username=username).first()
        if not user:
            return jsonify({ 'code': -1 })

        fw = [i.to_user.username for i in g.FollowUser.query.filter_by(del_status=False, from_user_id=user.id).all()]
        fd = [i.from_user.username for i in g.FollowUser.query.filter_by(del_status=False, to_user_id=user.id).all()]

        res = {
            'code': 1,
            'username': user.username,
            'email': user.email,
            'login': False,
            'follow_user': fw,
            'followed_user': fd,
        }
        res_secret = {
            'login': True,
            'id': user.id,
        }
        if user and user.password == password:
            res.update(res_secret)

        return jsonify(res)


        # return jsonify({'code':[ dict(un=row.username, ps=row.password) for row in cur] })

    @app.route('/api/user/follow/', methods=['GET', 'POST'])
    def follow_user():
        from_user_name = request.values.get('from_user_name', '')
        to_user_name = request.values.get('to_user_name', '')
        follow_bool = request.values.get('follow_bool', '1')  # 1 or 0

        from_user = g.User.query.filter_by(username=from_user_name).first()
        to_user = g.User.query.filter_by(username=to_user_name).first()
        if not (from_user and to_user):
            return jsonify({ 'code': -1 })

        args = {
            'from_user_id': from_user.id,
            'to_user_id': to_user.id,
        }

        follow = g.FollowUser.query.filter_by(**args).first()
        want_to_follow = bool(int(follow_bool))
        if follow:
            follow.del_status = not want_to_follow
        elif want_to_follow:
            follow = g.FollowUser(**args)
        db.session.add(follow)
        db.session.commit()

        return jsonify({ 'code': 1 })


    @app.route('/api/image/addinfo/', methods=['GET', 'POST'])
    def image_info():
        kwargs = {
            'url': request.values.get('url', ''),
            'filename': request.values.get('filename', ''),
            'param': request.values.get('param', '')
        }
        user_id = request.values.get('user_id', '')
        if user_id:
            kwargs.update({ 'user_id': user_id })

        item = g.Item.query.filter_by(name=filename).first()
        if item:
            return jsonify({'code': '-2'})

        item = g.Item(**kwargs)
        g.db.session.add(item)
        g.db.session.commit()

        return jsonify({ 'code': 1 })


    @app.route('/api/tasks/add/', methods=['GET', 'POST'])
    def add_task():
        """add task to a queue"""
        task = {
            'url': request.values.get('url', ''),
            'type': request.values.get('type', 'model'),
            'model': request.values.get('model', 'mosaic'),
        }
        tasks.append(task)
        return jsonify({ 'code': 1, 'task':task })

    # @app.route('/defaultstyles/')
    # def defaultstyles():
    #     """获取系统所有风格信息"""
    #     styles = []
    #     styles.append({
    #         'styleName':'123',
    #         'styleId':123,
    #         'styleImgUrl':'iii'
    #         })
    #     return jsonify(styles)
    #
    #
    # @app.route('/process/human-mask-picture/')
    # def human_mask_picture():
    #     """风格转化结果图处理-获取人像遮罩图"""
    #     originImgUrl = request.values.get('originImgUrl', '')
    #
    #     return jsonify({
    #         'maskImgUrl':'iii'
    #         })
    #
    # @app.route('/users/<userId>/styletransfer', methods=['POST'])
    # def users_styletransfer(userId):
    #     """
    #     风格转化—系统风格
    #     风格转化—自定义风格
    #     """
    #     styleId = request.values.get('styleId ', '')
    #     originImgUrl = request.values.get('originImgUrl', '')
    #
    #     return jsonify({
    #         'processImgUrl':'iii'
    #         })
    #
    # @app.route('/process/mask/', methods=['POST'])
    # def process_mask():
    #     """风格转化结果图处理-遮罩"""
    #     originImgUrl = request.values.get('originImgUrl', '')
    #     resultImgUrl = request.values.get('resultImgUrl', '')
    #     maskImgUrl = request.values.get('maskImgUrl', '')
    #
    #     return jsonify({
    #         'processImgUrl': 'iii'
    #     })
    #
    # @app.route('/process/colorpreserve/', methods=['POST'])
    # def process_colorpreserve():
    #     originImgUrl = request.values.get('originImgUrl', '')
    #     resultImgUrl = request.values.get('resultImgUrl', '')
    #     colorMaskImgUrl = request.values.get('colorMaskImgUrl', '')
    #
    #     return jsonify({
    #         'processImgUrl': 'iii'
    #     })



def register_calculate(app):

    @app.route('/tasks/add/model/')
    def add_model():
        task = {
            'url':'https://oi3qt7c8d.qnssl.com/res.jpg',
            'type':'model',
            'model':'mosaic',
        }
        tasks.append(task)
        return jsonify(task)

    @app.route('/tasks/add/')
    def add_task():
        ID = random.randint(10001, 99999)
        tasks.append({'id':ID})
        return jsonify({
            'code':1,
            'id':ID
        })

    @app.route('/tasks/query/')
    def task_query():
        return jsonify({
            'tasks':tasks,
            'done':done,
        })

    @app.route('/tasks/pop/')
    def task_pop():
        if tasks:
            return jsonify(tasks.pop(0))
        return jsonify('Empty')


    @app.route('/tasks/callback/', methods=['POST'])
    def task_cb():
        """callback from qiniu"""
        qiniu_setting = {
            'access_key' : 'iQ3ndG5uRpwdeln_gcrH3iiZ7E3KbMdJVkdYV9Im',
            'secret_key' : 'AGsp6K7fu1NsH2DnsPi7hW3qa3JXb4dtfeGvkm-A',
            'bucket_name' : 'image',
            'bucket_domain' : 'https://oi3qt7c8d.qnssl.com/',
            'callbakUrl' : 'http://139.129.24.151/tasks/callback/',
            'callbackBody' : 'filename:$(fname)'
        }
        filename = request.values.get('filename', '')
        imageInfo = request.values.get('imageInfo', '')
        url  = qiniu_setting['bucket_domain'] + filename
        print(filename, url, imageInfo)
        done.append({
            'url':url,
        })

        return  url
