import React, { Component } from 'react';
import axios from 'axios'
import './App.css';

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      pattern: "",
      stringToMatch: "",
      result: false,
      match: false
    }
    this.onChange = this.onChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
  }

  onSubmit(e) {
    e.preventDefault()
    axios.post('http://localhost:5000/findMatches', {
      pattern: this.state.pattern,
      stringToMatch: this.state.stringToMatch
    })
      .then(res => {
        console.log(res.data.result)
      })
  }

  onChange(e) {
    this.setState({ [e.target.name]: e.target.value})
  }
  onSubmit
  render() {
    return (
      <div>
        <div className='tc'>
         <h1 className='f1'>Regex Validator</h1>
        </div>
        <form onSubmit={this.onSubmit}>
        <div className='tc fl w-50 pv3'>
            <h2>Pattern:</h2>
              <p>
              <input
                className='textInput pa3 ba b--green bg-lightest-blue'
                type="text"
                name="pattern"
                value={this.state.pattern}
                onChange={this.onChange}
                />
              </p>
        </div>
        <div className='tc fl w-50 pt3'>
            <h2>String to Match:</h2>
          <p>
            <input
              className='textInput pa3 ba b--green bg-lightest-blue'
              type="text"
              name="stringToMatch"
              value={this.state.stringToMatch}
              onChange={this.onChange}
              />
          </p>
        </div>
        <div className="tc fl w-100">
          <input
            className="ph3 pv2 input-reset ba b--black bg-lightest-blue grow pointer f5 dib"
            type="submit"
            value="Find Match"
            />
        </div>
        </form>
        {this.state.result && <div><p>Result = {this.state.match}</p></div>}
      </div>
    );
  }
}

export default App;
