from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

#TODO: remove in production (no need to expose source docs)
@app.route('/poem/<int:source_id>', methods=['POST', 'GET'])
def source(source_id):
  if request.method == 'POST':
      #creates a source.
  else:
      show_source()

def show_source():
  return 'Source %d' % source_id

@app.route('/poem/<int:source_id>/<int:poem_id>')
def poem(source_id, poem_id):
  return 'Source %d, poem %d' % source_id, poem_id

if __name__ == "__main__":
    app.debug = True
    app.run()
