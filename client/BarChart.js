import React from 'react';

class BarChart extends React.Component {

  fetchWords() {
    fetch('/words').then(response => response.json()).then(json => {
      this.update(json.result);
      setTimeout(() => this.fetchWords(), 1000);
    });
  }

  componentDidMount() {
    this.fill = d3.scaleOrdinal(d3.schemeCategory20);
    this.svg = d3
      .select('.bar-chart-container')
      .append('svg')
      .attr('width', 1000)
      .attr('height', 500)
      .append('g')
      .attr('transform', 'translate(500,250)');
    this.fetchWords();
  }

  render(){
    return <div className='bar-chart-container'/>;
  }
}

export default BarChart;
