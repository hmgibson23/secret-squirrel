import gensim, logging, sys
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL = None

## Logger magic
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


@app.route('/check', methods=['POST'])
def check():
	vector = checkProximity(request.json["word"])
	return jsonify(vector)

@app.route('/query', methods=['GET'])
def query():
	searchword = request.args.get('word', '')
	vector = checkProximity(searchword)
	return jsonify(vector)

def loadModel(filename):
    return gensim.models.Word2Vec.load_word2vec_format(filename, binary=True)

def checkProximity(phrase):
    return MODEL.most_similar(positive=phrase.split())


def setup(argv):
    if len(argv) != 2:
        print("./word-2-vec-service <training-set>")
        sys.exit(1)

        global MODEL
    MODEL = loadModel(argv[1])




if __name__ == "__main__":
    setup(sys.argv)
    app.run()
