from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://surya:surya@cluster0.ovgnl6x.mongodb.net/?retryWrites=true&w=majority')
db = client.dbadmin

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_rec = request.form['bucket_in']
    count = db.bucket.count_documents({})
    num = count+1
    doc = {
        'num' : num,
        'bucket' : bucket_rec,
        'done' : 0
    }

    db.bucket.insert_one(doc)
    return jsonify({'msg': 'Data tersimpan!!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_rec = request.form['num_in']
    db.bucket.update_one(
        {'num' : int(num_rec)},
        {'$set': {'done' : 1}}
    )
    return jsonify({'msg': 'Ditandai sebagai selesai!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': buckets_list})

@app.route("/delete", methods = ['POST'])
def delete_bucket():
    num_rec = request.form['num_in']
    db.bucket.delete_one({'num' : int(num_rec)})
    return jsonify({'msg' : 'Sukses hapus data'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)