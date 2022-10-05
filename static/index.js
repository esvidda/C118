//Crear la variable date - (fecha).
var date =  new Date()
let display_date= "Fecha:" + date.toLocaleDateString()

//Cargar HTML DOM.
$(document).ready(function(){
    $("#display_date").html(display_date)
    $('#save_button').prop('disabled', true);
})
//Definir la variable para almacenar la emoción predecida.
let predicted_emotion;

//HTML-->JavaScript--->Flask.
//Flask--->JavaScript--->HTML.

//Selector jQuery y la acción click.

$(function () {
    $("#predict_button").click(function () {
        //Llamada a AJAX 
        let input_data={
            "text": $("#text").val()
        }
        console.log(input_data)

        $.ajax({
            type: 'POST',
            url: "/predict-emotion",
            data: JSON.stringify(input_data),
            dataType: "json",
            contentType: 'application/json',
            success: function (result)
            
              {
                
                // Resultado recibido de Flask ----->JavaScript
                predicted_emotion = result.data.predicted_emotion
                emo_url = result.data.predicted_emotion_img_url

                // Mostrar resultado usando JavaScript----->HTML
                $("#prediction").html(predicted_emotion)
                $('#prediction').css("display", "block");

                $("#emo_img_url").attr('src', emo_url);
                $('#emo_img_url').css("display", "block");

                $('#save_button').prop('disabled', false);

            },
            //Función error 
             error: function (result) {
                alert(result.responseJSON.message)
             }
        });
    });
    $("#save_button").click(function () {
        save_data={
            "date":display_date,
            "text":$("#text").val(),
            "emotion":predicted_emotion


        }
        $.ajax({
            type:'POST',
            url:"/save-entry",
            data:JSON.stringify(save_data),
            dataType:"json",
            contentType:'application/json',
            success: function(){
                alert("tu entrada ha sido guardada exitosamente")
                window.location.reload()

            },
            error: function (result) {
                alert(result.responseJSON.message)
            }
        })
    })

})
