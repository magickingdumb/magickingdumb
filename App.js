import React, { Component } from 'react';
import { View, Button } from 'react-native';
import Voice from 'react-native-voice';
import Tts from 'react-native-tts';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { isListening: false };

    // Initialize voice recognition
    Voice.onSpeechResults = this.onSpeechResults.bind(this);
  }

  componentWillUnmount() {
    Voice.destroy().then(Voice.removeAllListeners);
  }

  onSpeechResults(e) {
    if (e.value && e.value[0].toLowerCase().includes("where is my phone")) {
      Tts.speak("I'm here");
    }
  }

  toggleListening() {
    if (this.state.isListening) {
      Voice.stop();
    } else {
      Voice.start('en-US');
    }

    this.setState({ isListening: !this.state.isListening });
  }

  render() {
    return (
      <View>
        <Button
          onPress={() => this.toggleListening()}
          title={this.state.isListening ? 'FOUND!' : 'Start Listening'}
        />
      </View>
    );
  }
}

export default App;
