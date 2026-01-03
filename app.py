from flask import Flask, render_template, request, redirect, url_for
import random
import string

app = Flask(__name__)

WORDS = [
    ("python", "Popular programming language"),
    ("flask", "Python web framework"),
    ("developer", "Person who writes code"),
    ("programming", "Writing computer instructions"),
    ("hangman", "Word guessing game")
]

def new_game():
    word, hint = random.choice(WORDS)
    return word, hint, [], [], 6

word, hint, correct, wrong, attempts = new_game()

@app.route("/", methods=["GET", "POST"])
def index():
    global word, hint, correct, wrong, attempts

    message = ""
    game_over = False

    if request.method == "POST":
        letter = request.form.get("letter", "").lower()

        if letter and len(letter) == 1 and letter in string.ascii_lowercase:
            if letter in word and letter not in correct:
                correct.append(letter)
            elif letter not in word and letter not in wrong:
                wrong.append(letter)
                attempts -= 1

    display_word = " ".join([c if c in correct else "_" for c in word])

    if "_" not in display_word:
        message = "🎉 YOU WIN!"
        game_over = True

    if attempts <= 0:
        message = f"💀 YOU LOSE! Word was {word.upper()}"
        game_over = True

    return render_template(
        "index.html",
        display_word=display_word,
        attempts=attempts,
        wrong=wrong,
        hint=hint,
        message=message,
        game_over=game_over
    )

@app.route("/restart")
def restart():
    global word, hint, correct, wrong, attempts
    word, hint, correct, wrong, attempts = new_game()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
