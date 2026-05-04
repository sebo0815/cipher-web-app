from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

"""
 This is a simple Caesar cipher encryption function. 
 I wrote this as a project for my certification. I am still open for job offers, so if your company
 is searching for a python developer, please contact me. I am also open for freelance work.
 Sebastian Schneider:  sebodeveloper@gmail.com
"""
def caesar(text, shift, encrypt=True):

    if not isinstance(shift, int):
        return 'Shift must be an integer value.'

    if shift < 1 or shift > 25:
        return 'Shift must be an integer between 1 and 25.'

    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    if not encrypt:
        shift = -shift
    
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    translation_table = str.maketrans(
        alphabet + alphabet.upper(),
        shifted_alphabet + shifted_alphabet.upper()
    )

    encrypted_text = text.translate(translation_table)
    return encrypted_text


def encrypt(text, shift):
    return caesar(text, shift)


def decrypt(text, shift):
    return caesar(text, shift, encrypt=False)

# ===== FLASK =====

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/encrypt", methods=["POST"])
def do_encrypt():
    data = request.get_json()

    text = data.get("text", "")
    shift = data.get("shift", 0)

    try:
        shift = int(shift)
    except:
        return jsonify({"error": "Shift muss eine Zahl sein"}), 400

    result = encrypt(text, shift)

    # Falls dein Code eine Fehlermeldung zurückgibt
    if "Shift must" in result:
        return jsonify({"error": result}), 400

    return jsonify({"result": result})


# OPTIONAL: Entschlüsselung
@app.route("/decrypt", methods=["POST"])
def do_decrypt():
    data = request.get_json()

    text = data.get("text", "")
    shift = int(data.get("shift", 0))

    result = decrypt(text, shift)

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)