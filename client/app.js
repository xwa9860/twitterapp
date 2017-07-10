import React from 'react';
import ReactDOM from 'react-dom';

import QueryInput from './QueryInput';

class TwitterApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: ''
    };
  }
  render() {
    return (
      <div>
        <QueryInput onChange={query => this.setState({ query })} />
        <div>
          Output: {this.state.query}
        </div>
      </div>
    );
  }
}

ReactDOM.render(<TwitterApp />, document.getElementById('appContainer'));
