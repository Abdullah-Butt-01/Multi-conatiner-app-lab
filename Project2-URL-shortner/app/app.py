from flask import Flask, request, redirect  # Flash -> creates web app, request -> reads data sent by user, redirect -> sends the user to another URL
import redis # connect to redis databse
import string # provides letters and digits
import random # generate random codes
import os # read enviroment variables

app = Flask(__name__) # creating web server application

# connecting to redis
redis_host = os.getenv("REDIS_HOST", "redis") # read EnvVar
r = redis.Redis(host=redis_host, port=6379, decode_responses=True) # execute redis commands

#function to generate short code (Total 62 characters; a-z, A-Z, 0-9)
def generate_code(length=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length)) # random choice


@app.route("/", methods=["GET"]) # home route
def home():
    return """
    <h2>URL Shortener</h2>
    <form action="/shorten" method="post">
        <input name="url" placeholder="Enter URL">
        <button type="submit">Shorten</button>
    </form>
    """


@app.route("/shorten", methods=["POST"])
def shorten():
    original_url = request.form["url"] # get user input
    short_code = generate_code() # generate code

    r.set(short_code, original_url) # save mapping in redis (key-value)
 
    #Store the code in a Redis list
    r.rpush("all_codes", short_code)

    return f"Short URL: http://localhost:5000/{short_code}"


@app.route("/<code>") # redirect route
def redirect_url(code): 
    original_url = r.get(code) # search for URL

    if original_url:
        return redirect(original_url)
    else:
        return "URL not found"

#Adding route to see all URLs
@app.route("/all", methods=["GET"])
def all_urls():
    codes = r.lrange("all_codes", 0, -1)  # get all short codes
    result = "<h2>All Shortened URLs</h2><ul>"
    for code in codes:
        url = r.get(code)
        result += f"<li><a href='/{code}'>/{code}</a> → {url}</li>"
    result += "</ul>"
    return result

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
