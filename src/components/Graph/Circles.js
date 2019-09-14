import React, { Component } from 'react'

export default class Circles extends Component {
  render() {
    const { scales, data } = this.props
    const { xScale, yScale } = scales

    const circles = (
      data.map((datum, i) => {
        return (
          <circle
           cx={xScale(datum[0])}
           cy={yScale(datum[1])}
           r={6}
           key={i}
           onMouseOver={() => this.props.onMouseOverCallback(datum)}
           onMouseOut={() => this.props.onMouseOutCallback(null)}
          />
        )
      })
    )

    return (
      <g>{circles}</g>
    )
  }
}
