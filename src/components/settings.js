import React, {Component} from 'react'

class Settings extends Component {
  render() {
    const CLIENT_ID = 'b6447698e821e9a7127e'
    const REDIRECT_URI = "http://localhost:3000/";

    return (
      <div>
        <a
          href={`https://github.com/login/oauth/authorize?client_id=${CLIENT_ID}&scope=user&redirect_uri=${REDIRECT_URI}`}
        >
          Let's authenticate!
        </a>
      </div>
    )
  }
}

export default Settings;
