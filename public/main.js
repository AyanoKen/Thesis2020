function listen(){
  let recognition = new webkitSpeechRecognition();
  recognition.interimResults = true;
  recognition.onresult = function(event){
    if(event.results.length > 0){
      document.getElementById("text").innerHTML = "<strong>Is this what you said:</strong> " + event.results[0][0].transcript

      document.getElementById("speech").value = event.results[0][0].transcript
    }
  }
  recognition.start();
}
