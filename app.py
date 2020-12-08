from flask import request, jsonify, Flask
from pymongo import MongoClient
from bson.objectid import ObjectId

from flask_cors import CORS
# pycharm terminal -> pip install -U flask-cors

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://yoonchaiyoung:9452@18.222.215.81", 27017)
db = client.music_love

# 전체 음악 TOP100 목록 보여주기
@app.route("/music/list", methods=["GET"])
def music_list():
    music_lst = list(db.music.find({}))

    def pre_processing(music):
        music['_id'] = str(music['_id'])
        return music

    music_lst = [pre_processing(music) for music in music_lst]

    return jsonify({'result': music_lst})


# 내가 좋아하는 음악 리스트에 추가
@app.route("/music/love/<oid>", methods=["GET"])
def music_love(oid):
    music_love_list = db.user_music.find_one({"music_love": oid})

    if not music_love_list:
        db.user_music.insert_one({"music_love": oid})

    music_love_list = list(db.user_music.find({}, {"_id": False}))

    return jsonify({"result": music_love_list})


# 내가 좋아하는 음악 리스트에서 삭제
@app.route("/music/notlove/<oid>", methods=["GET"])
def music_notlove(oid):
    db.user_music.delete_one({"music_love": oid})

    music_love_list = list(db.user_movie.find({}, {"_id": False}))

    return jsonify({"result": music_love_list})


# 내가 좋아하는 음악 리스트 확인
@app.route("/music/user_love", methods=["GET"])
def music_user_love():
    music_lst = list(db.user_music.find({}, {"_id": False}))

    def pre_processing(music):
        music["_id"] = str(music["_id"])
        return music

    music_love_list = [ObjectId(music["music_love"]) for music in music_lst]

    music_detail_info = db.music.find({"_id": {"$in": music_love_list}})

    music_lst = [pre_processing(music) for music in music_detail_info]
    return jsonify({"result": music_lst})

if __name__ == "__main__":
    print("Server Start! ❤❤")
    app.run("0.0.0.0", 5000, debug=True)
