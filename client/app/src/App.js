import React, { Component } from 'react';
import axios from 'axios'
import './App.css';
import MatchesDisplay from './components/MatchesDisplay'
import Description from './components/description'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      pattern: "",
      stringToMatchInput: "",
      stringToMatch: "",
      result: false,
      match: false,
      matches: [],
      currentMatch: '',
      matchRanges: [],
      invalidRegMessage: '',
      invalidStrMessage: '',
    }
    this.onChange = this.onChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
    this.checkRegex = this.checkRegex.bind(this);
    this.handleMatchResult = this.handleMatchResult.bind(this);
    this.checkForEmptyFields = this.checkForEmptyFields.bind(this);
    this.checkLegal = this.checkLegal.bind(this);
  }

  checkForEmptyFields(pattern, string){
    if(pattern === ''){
      this.setState({ invalidRegMessage: 'Pattern cant be empty'})
    } else {
      this.setState({ invalidRegMessage: ''})
    }
    if(string === ''){
      this.setState({ invalidStrMessage: 'String cant be empty'})
    } else {
      this.setState({ invalidStrMessage: ''})
    }
    if(pattern === '' || string === '')
      return true
    return false
  }

  checkLegal(pattern, string){
    axios.post('http://localhost:5000/checkLegalRegex', {
      pattern: pattern
    })
      .then(res => {
        if(res.data.result.length != 0){
          this.setState({
              invalidRegMessage: res.data.result[0],
              match: false,
              matches: []
          })
          console.log(res.data.result[0])
        } else {
          this.setState({
            invalidRegMessage: '',
            stringToMatch: string,
            matches: [],
            match: true
          }, this.checkRegex)
        }
      })
  }

  onSubmit(e) {
    e.preventDefault()
    const { pattern, stringToMatchInput } = this.state

    if(this.checkForEmptyFields(pattern, stringToMatchInput) === true)
      return

    if(this.checkLegal(pattern, stringToMatchInput) === false)
      return

  }

  checkRegex(){
    axios.post('http://localhost:5000/findMatches', {
      pattern: this.state.pattern,
      stringToMatch: this.state.stringToMatch
    })
      .then(res => {
        this.setState({ matchRanges: res.data.result })
        this.handleMatchResult(res.data.result)
      })
  }

  handleMatchResult(foundMatches){
    const { stringToMatch } = this.state
    const words = stringToMatch.split(' ')
    if(foundMatches.length == 0){
      this.setState({ result: false })
    }
    else{
      let matches = []
      let i = 0
      for (let wordRanges of foundMatches){
        for (let range of wordRanges){
          matches.push(words[i].substr(range[0], range[1]-range[0]))
        }
        ++i;
      }
      this.setState({
        result: true,
        matches
      })

    }
  }

  onChange(e) {
    this.setState({ [e.target.name]: e.target.value})
  }


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
              <span style={{color: 'crimson'}}>
                {this.state.invalidRegMessage}
              </span>
        </div>
        <div className='tc fl w-50 pt3'>
            <h2>String to Match:</h2>
          <p>
            <input
              className='textInput pa3 ba b--green bg-lightest-blue'
              type="text"
              name="stringToMatchInput"
              value={this.state.stringToMatchInput}
              onChange={this.onChange}
              />
          </p>
          <span style={{color: 'crimson'}}>
            {this.state.invalidStrMessage}
          </span>
        </div>
        <div className="tc fl w-100">
          <p>
          <input
            className="ph3 pv2 input-reset ba b--black bg-lightest-blue grow pointer f5 dib"
            type="submit"
            value="Find Match"
            />
          </p>
        </div>
        </form>

        {this.state.match &&
          <MatchesDisplay
            stringToMatch={this.state.stringToMatch}
            match={this.state.match}
            matchRanges={this.state.matchRanges}
            matches={this.state.matches}
          />
       }
       <Description />

      </div>
    );
  }
}

export default App;
