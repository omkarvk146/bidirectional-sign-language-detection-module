import React, { useState } from 'react';
import InputBox from './InputBox';
import ResultDisplay from './ResultDisplay';
import Navbar from './Navbar';
import './VoiceToSign.css';

const VoiceToSign = () => {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState(null);

  const availableGifs = [
    'any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
    'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office',
    'do you have money', 'do you want something to drink', 'do you want tea or coffee', 'do you watch TV',
    'dont worry', 'flower is beautiful', 'good afternoon', 'good evening', 'good morning', 'good night',
    'good question', 'had your lunch', 'happy journey', 'hello what is your name',
    'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing', 'i am fine',
    'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre',
    'i love to shop', 'i had to say something but i forgot', 'i have headache', 'i like pink colour',
    'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker', 'my name is john', 'nice to meet you',
    'no smoking please', 'open the door', 'please call me later', 'please clean the room',
    'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime',
    'shall I help you', 'shall we go together tommorow', 'sign language interpreter', 'sit down',
    'stand up', 'take care', 'there was traffic jam', 'wait I am thinking', 'what are you doing',
    'what is the problem', 'what is todays date', 'what is your father do', 'what is your job',
    'what is your mobile number', 'what is your name', 'whats up', 'when is your interview',
    'when we will go', 'where do you stay', 'where is the bathroom', 'where is the police station',
    'you are wrong', 'address', 'agra', 'ahemdabad', 'all', 'april', 'assam', 'august', 'australia',
    'badoda', 'banana', 'banaras', 'banglore', 'bihar', 'bridge', 'cat', 'chandigarh', 'chennai',
    'christmas', 'church', 'clinic', 'coconut', 'crocodile', 'dasara', 'deaf', 'december', 'deer',
    'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass', 'grapes', 'gujrat', 'hello',
    'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'karnataka', 'kerala', 'krishna',
    'litre', 'mango', 'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october',
    'orange', 'pakistan', 'pass', 'police station', 'post office', 'pune', 'punjab', 'rajasthan',
    'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'southafrica', 'story', 'sunday',
    'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa',
    'village', 'voice', 'wednesday'
  ];

  const onTranslate = () => {
    if (!inputText.trim()) {
      alert('Please enter or speak some text first.');
      return;
    }

    const normalizedInput = inputText.toLowerCase().trim();

    // Match full phrase from the input
    const matchedGif = availableGifs.find(phrase => normalizedInput.includes(phrase));

    if (matchedGif) {
      setResult({ type: 'gif', value: matchedGif });
    } else {
      setResult({ type: 'letters', value: normalizedInput.split('') });
    }
  };

  return (
    <>
      <Navbar />
      <div className="voice-to-sign-container">
        <h1 className="voice-to-sign-title">Voice to Sign</h1>
        <InputBox
          inputText={inputText}
          setInputText={setInputText}
          onTranslate={onTranslate}
          className="input-box"
        />
        <ResultDisplay result={result} className="result-display" />
      </div>
    </>
  );
};

export default VoiceToSign;
