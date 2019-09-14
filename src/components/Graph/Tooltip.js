import React from 'react'
import './Tooltip.css'

export default ({hoveredCirc, scales}) => {
  const { xScale, yScale } = scales
  const styles = {
    left: `${xScale(hoveredCirc[0]) - 30}px`,
    top: `${yScale(hoveredCirc[1] + 50)}px`
  }

  return (
    <div className="Tooltip" style={styles}>
      <table>
        <tbody>
          <tr>
            <th colSpan="2">{hoveredCirc[0]}</th>
          </tr>
          <tr>
            <td colSpan="2">{hoveredCirc[1]}</td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}
