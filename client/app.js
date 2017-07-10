import React from 'react';
import ReactDOM from 'react-dom';
import fetch from 'isomorphic-fetch';

class TwitterApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tweets: []
    };
  }

  componentDidMount() {
    fetch('/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ keyword: 'nuclear' })
    })
      .then(response => response.text())
      .then(text => console.log(`start fetching job ${text}`));
    this.fetchTweets();
  }

  fetchTweets() {
    fetch('/results')
      .then(response => response.json())
      .then(json => {
        this.setState({ tweets: json.result });
        setTimeout(() => this.fetchTweets(), 1000);
      })
      .catch(err => console.log(err));
  }

  render() {
    return (
      <div>
        {this.state.tweets.map(tweet =>
          <div key={tweet.tid}>
            {tweet.tweet}
          </div>
        )}
      </div>
    );
  }
}

ReactDOM.render(<TwitterApp />, document.getElementById('appContainer'));
