from urllib import response
from flask import Flask, render_template, url_for, request, jsonify
from text_sentiment_prediction import *

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/predict-emotion', methods=["POST"])
def predict_emotion():
    
    # Obtener el texto ingresado del requerimiento POST.
    input_text= request.json.get("text")
    
    if not input_text:
        # Respuesta para enviar si input_text está indefinido.
        response= {
            "status": "error",
            "mesage": "Por favor, ingresa algún texto para predecir tu emoción"
        }
        return jsonify(response)
    else:
        # Respuesta para enviar si input_text no está indefinido.
        predicted_emotion,predicted_emotion_img_url = predict(input_text)

        response= {
            "status": "success",
            "data": {
                "predicted_emotion": predicted_emotion,
                "predicted_emotion_img_url": predicted_emotion_img_url
            }
        }

        # Enviar respuesta.         
        return jsonify(response)
@app.route("/save-entry", methods=["POST"])
def save_entry():
    date = request.json.get("date")           
    emotion = request.json.get("emotion")
    save_text = request.json.get("text")

    entry= date+","+save_text+","+emotion+","
    file_handler=open('./static/data_files/data_entry.csv','a')
    file_handler.write(entry+'\n')
    return jsonify("Success")

    

app.run(debug=True)



    