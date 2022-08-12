import React from 'react'

import './App.css'
import { Counter } from './features/counter/Counter'

class App extends React.Component<any, any> {
  render () {
    return (
        <div>
          <Counter/>
        </div>
    )
  }
}

export default App
