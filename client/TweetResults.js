import React from 'react';
import fetch from 'isomorphic-fetch';

class TweetResults extends React.Component {
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
      <ul className="list-group">
        {this.state.tweets.map(tweet =>
          <li className="list-group-item" key={tweet.tid}>
            {tweet.tweet}
          </li>
        )}
      </ul>
    );
  }
}

export default TweetResults;
