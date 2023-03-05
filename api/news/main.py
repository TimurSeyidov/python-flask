import flask

from core.models import db_session
from core.models.News import News
from flask import jsonify, make_response, abort, request

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/news', methods=['GET'])
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    return jsonify({
        'news': [item.to_dict(
            only=('title', 'content', 'user.name')
        ) for item in news]
    })


@blueprint.route('/api/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        abort(404)
    return jsonify(
        {
            'news': news.to_dict(only=(
                'title', 'content', 'user_id', 'is_private'))
        }
    )


@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        abort(400)
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        abort(400)
    db_sess = db_session.create_session()
    news = News(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(news)
    db_sess.commit()
    return make_response(jsonify({'success': 'OK'}), 201)


@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        abort(404)
    db_sess.delete(news)
    db_sess.commit()
    return make_response(jsonify({'success': 'OK'}), 202)
