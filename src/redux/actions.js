export const FETCH_TOKEN = "FETCH_TOKEN";

const CLIENT_ID = 'b6447698e821e9a7127e'
const BACKEND_URL = 'http://localhost:9999/authenticate'

function handleFetchToken(token) {
  return {
    type: FETCH_TOKEN,
    token
  }
}

export function fetchToken(code) {
  console.log(`${BACKEND_URL}/${code}`)
  return dispatch => {
    fetch(`${BACKEND_URL}/${code}`)
    .then(response => response.json())
    .then(({ token }) => {
      console.log(token)
      dispatch(handleFetchToken(token));
    });
  };
}
