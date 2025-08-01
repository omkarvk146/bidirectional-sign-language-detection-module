import React, { useState } from 'react';

const InputBox = ({ inputText, setInputText, onTranslate }) => {
  const [isListening, setIsListening] = useState(false);

  const handleVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Sorry, your browser does not support Speech Recognition.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();
    setIsListening(true);

    recognition.onresult = event => {
      const transcript = event.results[0][0].transcript;
      setInputText(transcript);
      setIsListening(false);
    };

    recognition.onerror = event => {
      alert('Error occurred in recognition: ' + event.error);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };
  };

  return (
    <div style={{ marginBottom: 20 }}>
      <input
        type="text"
        placeholder="Speak or type here..."
        value={inputText}
        onChange={e => setInputText(e.target.value)}
        style={{ padding: 10, width: 300, marginRight: 10 }}
      />
      <button onClick={onTranslate} style={{ padding: 10 }}>
        Translate
      </button>
      <button
        onClick={handleVoiceInput}
        style={{
          padding: 10,
          marginLeft: 10,
          backgroundColor: isListening ? 'lightgreen' : 'lightblue',
        }}
        disabled={isListening}
      >
        {isListening ? 'Listening...' : '🎙️ Speak'}
      </button>
    </div>
  );
};

export default InputBox;
