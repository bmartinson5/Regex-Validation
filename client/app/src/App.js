import React, { Component } from 'react';
import axios from 'axios'
import './App.css';

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
    this.displayMatches = this.displayMatches.bind(this);
    this.checkRegex = this.checkRegex.bind(this);
    this.sendStrings = this.sendStrings.bind(this);
    this.handleMatchResult = this.handleMatchResult.bind(this);
    this.highlightString = this.highlightString.bind(this);
  }

  onSubmit(e) {
    e.preventDefault()
    this.setState({
      stringToMatch: this.state.stringToMatchInput,
      matches: [],
      match: true
    }, this.checkRegex)
  }

  sendStrings(){
    let strings = this.state.stringToMatch.split(" ")
    for (let string of strings){
      for(let i = 0; i < string.length; ++i){
        for(let x = 0; x < string.length; ++x){
          this.checkRegex(string.substr(i, x+1-i))
        }
      }
    }
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
    if(foundMatches.length == 0){
      this.setState({ result: false })
    }
    else{
      let matches = []
      for (let wordRange of foundMatches){
        for (let range of wordRange){
          matches.push(stringToMatch.substr(range[0], range[1]-range[0]))
        }
      }
      console.log(matches)

      this.setState({
        result: true,
        matches
      })

    }
  }



  onChange(e) {
    this.setState({ [e.target.name]: e.target.value})
  }

  displayMatches(){
    return <ol> {this.state.matches.map((match) =>
        <li>{match}</li>
      )
    } </ol>
  }

  highlightString(str, ranges){
    let words = str.split(" ")
    return <div> <span>{ words.map((word, i) =>
      <span>{this.highlightWithinWord(word, ranges[i])}</span>)}
    </span></div>
  }

  highlightWithinWord(word, hiliRanges){
    let rangesLength = hiliRanges.length - 1
    return <div style={{display: 'inline'}}> { hiliRanges.map((hiliRange, i) =>
        <span>
            <span>
              {i===0 ? word.substr(0, hiliRange[0]):
                       word.substr(hiliRanges[i-1][1], hiliRange[0]-hiliRanges[i-1][1])}
            </span>
            <span className="highlighted">
              {word.substr(hiliRange[0], hiliRange[1]-hiliRange[0])}
            </span>
        </span>
      )
    }{word.substr(hiliRanges[rangesLength][1], word.length-hiliRanges[rangesLength][1])}</div>
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
        {this.state.result && <div><p>Result = {this.state.match}</p></div>}

        <div className="fl w-100 pl7 pr7 pv4  w-30">
          <div className="tc">
            <h2>Matches Found</h2>
          </div>
          <div className="pv3 ba  7b--black bg-lightest-blue">
            <div className="pl4 pr4" style={{wordWrap: 'break-word'}}>
              {this.state.matchRanges.length != 0 && this.highlightString(this.state.stringToMatch, this.state.matchRanges)}
            </div>
          </div>
          <div className="ba b--black bg-lightest-blue">
            <div className="">
              {this.state.match && this.displayMatches()}
            </div>
          </div>
        </div>

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
