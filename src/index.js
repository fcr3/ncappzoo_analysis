import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import AppWrapper from './AppWrapper';
import * as serviceWorker from './serviceWorker';
import {BrowserRouter} from 'react-router-dom'

import {createStore, applyMiddleware, compose} from 'redux';
import reducer from './redux/reducer';
import {Provider} from 'react-redux';
import thunk from 'redux-thunk'

const store = createStore(
  reducer,
  compose(
    applyMiddleware(thunk)
  )
);

ReactDOM.render(
  <Provider store={store}>
    <BrowserRouter>
      <AppWrapper />
    </BrowserRouter>
  </Provider>
, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
