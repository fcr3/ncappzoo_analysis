import React, { Component } from 'react'

export default class Lines extends Component {
  render() {
    const { scales, data } = this.props
    const { xScale, yScale } = scales

    const lines = []
    data.forEach((datum, i) => {
        if (i === 0) {
          return
        }

        const datum1 = [xScale(data[i - 1][0]), yScale(data[i - 1][1])]
        const datum2 = [xScale(datum[0]), yScale(datum[1])]

        lines.push((
          <line
           x1={datum1[0]}
           y1={datum1[1]}
           x2={datum2[0]}
           y2={datum2[1]}
           key={i}
           style={{stroke: '#3371c5', strokeWidth: '2'}}
          />
        ))
    })

    return (
      <g>{lines}</g>
    )
  }
}
