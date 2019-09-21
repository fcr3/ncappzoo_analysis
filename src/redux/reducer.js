import {FETCH_TOKEN} from './actions';

const initialState = {
  token: null
}

export default function reducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_TOKEN:
      console.log("reached")
      return {token: action.token}
    default:
      return state;
   }
}
