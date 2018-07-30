import React, { Component } from 'react';
import axios from 'axios'
import './App.css';
import MatchesDisplay from './components/MatchesDisplay'

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
      matchRanges: []
    }
    this.onChange = this.onChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
    this.checkRegex = this.checkRegex.bind(this);
    this.handleMatchResult = this.handleMatchResult.bind(this);
  }

  onSubmit(e) {
    e.preventDefault()
    this.setState({
      stringToMatch: this.state.stringToMatchInput,
      matches: [],
      match: true
    }, this.checkRegex)
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
          ++i;
        }
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

        <div className="fl w-50 ph4 pv5">
          <h2>Special Characters Supported</h2>
          <h2>*<span>0 or more repetitions of the preceding RE</span></h2>
          <h2>+<span>1 or more repetitions of the preceding RE</span></h2>
          <h2>?<span>0 or 1 repetitions of the preceding RE</span></h2>
          <h2>()<span>Matches RE within parenthesis, and indicates start and end of a group</span></h2>
          <h2>{'{X}'}<span>Matches the preceding RE with exactly X number of repetitions</span></h2>
          <h2>{'{X,}'}<span>Matches the preceding RE with at least X repetitions, or more</span></h2>
          <h2>{'{X,Y}'}<span>Matches the preceding RE with at least'X repetitions but no more than Y</span></h2>
          <p>
          </p>
        </div>

      </div>
    );
  }
}

export default App;
