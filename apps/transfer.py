# coding=utf-8
from flask import request, jsonify, g


def register_front(app):

    @app.route('/defaultstyles/')
    def defaultstyles():
        """获取系统所有风格信息"""
        styles = []
        styles.append({
            'styleName':'123',
            'styleId':123,
            'styleImgUrl':'iii'
            })
        return jsonify(styles)


    @app.route('/process/human-mask-picture/')
    def human_mask_picture():
        """风格转化结果图处理-获取人像遮罩图"""
        originImgUrl = request.values.get('originImgUrl', '')

        return jsonify({
            'maskImgUrl':'iii'
            })

    @app.route('/users/<userId>/styletransfer', methods=['POST'])
    def users_styletransfer(userId):
        """
        风格转化—系统风格
        风格转化—自定义风格
        """
        styleId = request.values.get('styleId ', '')
        originImgUrl = request.values.get('originImgUrl', '')

        return jsonify({
            'processImgUrl':'iii'
            })

    @app.route('/process/mask/', methods=['POST'])
    def process_mask():
        """风格转化结果图处理-遮罩"""
        originImgUrl = request.values.get('originImgUrl', '')
        resultImgUrl = request.values.get('resultImgUrl', '')
        maskImgUrl = request.values.get('maskImgUrl', '')

        return jsonify({
            'processImgUrl': 'iii'
        })

    @app.route('/process/colorpreserve/', methods=['POST'])
    def process_colorpreserve():
        originImgUrl = request.values.get('originImgUrl', '')
        resultImgUrl = request.values.get('resultImgUrl', '')
        colorMaskImgUrl = request.values.get('colorMaskImgUrl', '')

        return jsonify({
            'processImgUrl': 'iii'
        })



def register_calculate(app):
    import random
    tasks = []
    done = []


    @app.route('/tasks/add/')
    def add_task():
        tasks.append({'id':random.randint(10001, 99999)})
        return jsonify({
            'code':1
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
            return jsonify(tasks.pop())
        return jsonify('Empty')


    @app.route('/tasks/callback/', methods=['POST'])
    def task_cb():
        """callback from qiniu"""
        qiniu_setting = qiniu_setting = {
            'access_key' : 'iQ3ndG5uRpwdeln_gcrH3iiZ7E3KbMdJVkdYV9Im',
            'secret_key' : 'AGsp6K7fu1NsH2DnsPi7hW3qa3JXb4dtfeGvkm-A',
            'bucket_name' : 'image',
            'bucket_domain' : 'https://oi3qt7c8d.qnssl.com/',
            'callbakUrl' : 'http://139.129.24.151/tasks/callback',
            'callbackBody' : 'filename:$(fname)'
        }
        filename = request.values.get('filename', '')
        url  = qiniu_setting + filename

        return  url
