# claude
import anthropic
import os
from dotenv import load_dotenv
from flask import Flask,render_template,request,session

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

client = anthropic.Anthropic(
    api_key = os.getenv("ANTHROPIC")
)
@app.route("/", methods=["GET", "POST"])
def chat():
    if "conversation" not in session:
        session["conversation"]=[]
    if "history" not in session:
        session["history"]=[]
    if request.method == "POST":
        question=request.form.get("question")
        # user= input("=>")
        conversation=session["conversation"]
        conversation.append({"role":"user","content":question})
        if question.lower()=='exit':
            session["conversation"] = []
            session["history"] = []
            return render_template("index.html", chat=[])
        else:
            res=client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1000,
                messages=conversation
            )
            ans = res.content[0].text
            conversation.append({"role":"assistant","content":ans})
            session["conversation"]=conversation

            session["history"].append({
            "user": question,
            "bot": ans
        })
            return render_template("index.html", chat=session["history"])
    return render_template("index.html", chat=session["history"])

if __name__ == "__main__":
    app.run(debug=True, port=5000)