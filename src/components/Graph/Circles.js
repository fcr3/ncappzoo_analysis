import React, { Component } from 'react'

export default class Circles extends Component {
  constructor(props) {
    super(props)
    this.state = {
      hoveredCirc: null
    }
  }

  render() {
    const { scales, data, hoveredCirc } = this.props
    const { xScale, yScale } = scales

    const circles = (
      data.map((datum, i) => {
        if (datum === hoveredCirc) {
          return (
            <circle
             cx={xScale(datum[0])}
             cy={yScale(datum[1])}
             r={6}
             key={i}
             style={{fill: 'white', stroke: '#3371c5', strokeWidth: '3'}}
             onMouseOver={() => this.props.onMouseOverCallback(datum)}
             onMouseOut={() => this.props.onMouseOutCallback(null)}
            />
          )
        }
        return (
          <circle
           cx={xScale(datum[0])}
           cy={yScale(datum[1])}
           r={5}
           key={i}
           style={{fill: '#3371c5', stroke: '#3371c5'}}
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
