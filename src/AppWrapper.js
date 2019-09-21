import React, {Component} from 'react'
import App from './App'
import {connect} from 'react-redux';
import {fetchToken} from './redux/actions';


class AppWrapper extends Component {
  componentDidMount() {
    if (window.location.href.match(/\?code=(.*)/)) {
      const code = window.location.href.match(/\?code=(.*)/)[1];
      fetchToken(code)
    }
  }

  render() {
    console.log(this.props.token)
    return (
      <App />
    )
  }
}

const mapStateToProps = (reduxState) => {
  return {
    token: reduxState.token
  }
}

export default connect(mapStateToProps, {fetchToken})(AppWrapper);
