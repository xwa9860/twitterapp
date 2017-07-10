import * as d3 from 'd3';
import React from 'react';
import cloud from 'd3-cloud';
import fetch from 'isomorphic-fetch';

class WordCloud extends React.Component {
  constructor(props) {
    super(props);

    this.fill = null;
    this.svg = null;
  }

  draw(words) {
    const cloud = this.svg.selectAll('g text').data(words, function(d) {
      return d.text;
    });

    //Entering words
    cloud
      .enter()
      .append('text')
      .style('font-family', 'Impact')
      .style('fill', (d, i) => this.fill(i))
      .attr('text-anchor', 'middle')
      .attr('font-size', 1)
      .text(function(d) {
        return d.text;
      });

    //Entering and existing words
    cloud
      .transition()
      .duration(600)
      .style('font-size', function(d) {
        return d.size + 'px';
      })
      .attr('transform', function(d) {
        return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')';
      })
      .style('fill-opacity', 1);

    //Exiting words
    cloud
      .exit()
      .transition()
      .duration(200)
      .style('fill-opacity', 1e-6)
      .attr('font-size', 1)
      .remove();
  }

  update(words) {
    cloud()
      .size([500, 500])
      .words(words)
      .padding(5)
      .rotate(function() {
        return ~~(Math.random() * 2) * 90;
      })
      .font('Impact')
      .fontSize(function(d) {
        return d.size;
      })
      .on('end', words => this.draw(words))
      .start();
  }

  fetchWords() {
    fetch('/words').then(response => response.json()).then(json => {
      this.update(json.result);
      setTimeout(() => this.fetchWords(), 1000);
    });
  }

  componentDidMount() {
    this.fill = d3.scaleOrdinal(d3.schemeCategory20);
    this.svg = d3
      .select('.word-cloud-container')
      .append('svg')
      .attr('width', 500)
      .attr('height', 500)
      .append('g')
      .attr('transform', 'translate(250,250)');
    this.fetchWords();
  }

  render() {
    return <div className="word-cloud-container" />;
  }
}

export default WordCloud;
