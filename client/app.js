import React from 'react';
import ReactDOM from 'react-dom';
import TweetResults from './TweetResults';
import WordCloudNeg from './WordCloudNeg';
import WordCloudPos from './WordCloudPos';

class TwitterApp extends React.Component {
  render() {
    return (
      <div>
        <TweetResults />
        <WordCloudNeg />
        <WordCloudPos />
      </div>
    );
  }
}

ReactDOM.render(<TwitterApp />, document.getElementById('appContainer'));
