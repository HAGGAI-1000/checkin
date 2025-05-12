from flask import Flask, request, make_response
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body", "")
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>You said: {incoming_msg}</Message>
</Response>"""
    response = make_response(twiml_response)
    response.headers["Content-Type"] = "application/xml"
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
