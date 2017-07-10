import React from 'react';
import ReactDOM from 'react-dom';
import TweetResults from './TweetResults';
import WordCloud from './WordCloud';

class TwitterApp extends React.Component {
  render() {
    return (
      <div>
        <TweetResults />
        <WordCloud />
      </div>
    );
  }
}

ReactDOM.render(<TwitterApp />, document.getElementById('appContainer'));
