import React from 'react'
import PropTypes from 'prop-types'

const Description = (props) => {
  return (
    <div>
      <div className="fl w-100 tc  pv6  nowrap">
         <h2>Special Characters Supported</h2>

        <div className="fl w-third">&nbsp;</div>
        <div className="fl w-two-thirds tl">
          <h2>*<span>0 or more repetitions of the preceding RE</span></h2>
          <h2>+<span>1 or more repetitions of the preceding RE</span></h2>
          <h2>?<span>0 or 1 repetitions of the preceding RE</span></h2>
          <h2>()<span>Matches RE within parenthesis, and indicates start and end of a group</span></h2>
          <h2>{'{X}'}<span>Matches the preceding RE with exactly X number of repetitions</span></h2>
          <h2>{'{X,}'}<span>Matches the preceding RE with at least X repetitions, or more</span></h2>
          <h2>{'{X,Y}'}<span>Matches the preceding RE with at least X repetitions but no more than Y</span></h2>
          <h2>.<span>Matches any single character</span></h2>
      </div>

      </div>
    </div>

  )
}

export default Description
