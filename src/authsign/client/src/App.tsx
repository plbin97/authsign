import React from 'react';
import Signin from './features/signin/Signin'
import Signup from "./features/signup/Signup";
import './App.css';

class App extends React.Component<any, any> {
  render() {
    return (
        <div>
          <Signup />
        </div>
    );
  }
}

export default App;
