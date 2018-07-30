import React from 'react'

class MatchesDisplay extends React.Component {

  displayMatches(){
    return <ol> {this.props.matches.map((match) =>
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
    if(rangesLength === -1){
      return <div style={{display: 'inline'}}><span> {word}</span></div>
    }
    else {
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
  }


  render () {
    const { matchRanges, stringToMatch, match, matches} = this.props
    const isZero = matches.length === 0

    return(
      <div className="fl w-100 pl7 pr7 pv4  w-30">
        <div className="tc">
          <h2>Matches Found</h2>
        </div>
        <div className="pv3 ba  7b--black bg-lightest-blue">
          <div className="pl4 pr4" style={{wordWrap: 'break-word'}}>
            {!isZero ? this.highlightString(stringToMatch, matchRanges):
              <div>No Matches were Found
            </div>
          }
          </div>
        </div>
        <div className="ba b--black bg-lightest-blue">
          <div className="">
            {!isZero && this.displayMatches()}
          </div>
        </div>
      </div>
    )
  }
}

export default MatchesDisplay;
