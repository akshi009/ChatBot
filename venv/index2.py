# gemini
from google import genai
import os
from dotenv import load_dotenv
import time
from flask import Flask,render_template,request,session

load_dotenv()
app = Flask(__name__)
client = genai.Client(api_key=os.getenv('GEMINI_API'))
app.secret_key = os.getenv('SECRET_KEY')
@app.route("/", methods=["GET", "POST"])

def chat():
    # global history
    if "history" not in session:
        session["history"]=[]
    if request.method == "POST":
        try:
            message = request.form.get("question")
            if message == "exit":
                session["history"]=[]
                return render_template(
                     "index.html",
                     chat="Chat ended."
                 )
            gemini_history = []
            for item in session["history"]:
                gemini_history.append({"role": "user", "parts": [{"text": item["user"]}]})
                gemini_history.append({"role": "model", "parts": [{"text": item["bot"]}]})
            chat = client.chats.create( model='gemini-2.5-flash',history=gemini_history)
            res=chat.send_message(message)
            answer = res.text
            session["history"] = session["history"] + [{"user": message, "bot": answer}]
        except Exception as e:
            session["history"] = session["history"] + [{"user": message, "bot": f"Error: {e}"}]
            time.sleep(2)
    return render_template('index.html',chat=session["history"])
             
    #     for attempt in range(1):
    #         try:
    #             message = request.form.get("question", "").strip()
    #             response = client.models.generate_content(
    #                 model='gemini-2.5-flash',
    #                 contents=message
    #             )

    #             history.append({
    #                 "user":message,
    #                 "bot":response.text
    #             })

    #             session["history"]=history
    #             return render_template("index.html",chat=session["history"])

    #         except Exception as e:
    #             return render_template("index.html",chat=f"Attempt {attempt + 1} failed: {e}")
    #             time.sleep(2)
    # return render_template("index.html",chat="some error!")

    # if request.method == "POST":
    #     message = request.form.get("question", "").strip()
    #     if message.lower() == "exit":
    #         return render_template("index.html",chat="Chat ended.")
    #     response = client.models.generate_content(
    #         model='gemini-2.5-flash',
    #         contents=message
    #     )
    #     answer = response.text
    # return render_template("index.html", chat=answer)

       
            

        # Upload

# upload=client.files.upload(file='asset/resume.png')
# chat = client.models.generate_content( 
#     model='gemini-3.1-flash-lite',
#     contents=['What Skills Should I Learn To Get a Package of 1cr in 6 Months',upload]
# )
# print(chat.text)
        # return render_template('index.html',chat=chat.text)

if (__name__=="__main__"):
    app.run(debug=True,port=8080)

