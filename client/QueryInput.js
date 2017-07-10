import React from 'react';

class QueryInput extends React.Component {
  render() {
    return (
      <div>
        <input
          ref={c => {
            this.input = c;
          }}
          placeholder="Keyword..."
        />
        <button
          className="btn btn-default"
          onClick={() => {
            this.props.onChange(this.input.value);
          }}
        >
          Submit
        </button>
      </div>
    );
  }
}

export default QueryInput;
