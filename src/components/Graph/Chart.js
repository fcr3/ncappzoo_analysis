import React, { Component } from 'react'
import { scaleBand, scaleLinear } from 'd3-scale'

// import data from '../../data'
import Axes from './Axes'
import Circles from './Circles'
import Lines from './Lines'
import ResponsiveWrapper from './ResponsiveWrapper'
import Tooltip from './Tooltip'
import './Chart.css'

class Chart extends Component {
  constructor(props) {
    super(props)
    this.xScale = scaleBand()
    this.yScale = scaleLinear()

    this.state = {
      hoveredCirc: null,
      data: this.props.data
    }
  }

  render() {
    const margins = { top: 30, right: 10, bottom: 50, left: 60 }
    const svgDimensions = {
      width: Math.max(this.props.parentWidth, 600),
      height: 500
    }

    const data = this.state.data
    const maxValue = Math.max(...data.map(d => d[1]))

    const xScale = this.xScale
      .padding(0)
      .domain(data.map(d => d[0]))
      .range([margins.left, svgDimensions.width - margins.right])

    const yScale = this.yScale
      .domain([0, maxValue])
      .range([svgDimensions.height - margins.bottom, margins.top])

    return (
      <div className="Chart">
        <svg width={svgDimensions.width} height={svgDimensions.height}>
          <Axes
            scales={{ xScale, yScale }}
            margins={margins}
            svgDimensions={svgDimensions}
          />
          <Lines
            scales={{ xScale, yScale }}
            data={data}
          />
          <Circles
            scales={{ xScale, yScale }}
            data={data}
            hoveredCirc={this.state.hoveredCirc}
            onMouseOverCallback={datum => this.setState({hoveredCirc: datum})}
            onMouseOutCallback={datum => this.setState({hoveredCirc: null})}
          />
        </svg>
        { this.state.hoveredCirc ?
          <Tooltip
            hoveredCirc={this.state.hoveredCirc}
            scales={{ xScale, yScale }}
          /> :
          null
        }
      </div>
    )
  }
}

export default ResponsiveWrapper(Chart);
