import React, { Component } from 'react';
import Question from './components/question';
import styled from 'styled-components';
import 'whatwg-fetch';

const choices = [
  ["A. $0.75", "B. $1.87", "C. $1.48", "D. $1.09"],
  ["A. $1.03", "B. $2.37", "C. $2.07", "D. $1.05"],
  ["A. $0.82", "B. $2.31", "C. $3.21", "D. $1.47"],
  ["A. $0.71", "B. $1.02", "C. $0.84", "D. $1.51"],
  ["A. $1.32", "B. $1.30", "C. $1.31", "D. $1.33"],
];

function retrieve() {
  return new Promise(resolve => {
    fetch("https://sheltered-brook-80388.herokuapp.com/fetch").then(response => {
      return response.json();
    }).then(json => {
      resolve(json);
    }).catch(err => {
      resolve(err);
    });
  });
}

let Button = styled.div`
  width: 100vw;
  height: 50px;
  background-color: papayawhip;
  position: absolute;
  top:0;
  text-align: center;
  color: palevioletred;
  font-size: 40px;
`

let RedBox = styled.div`
  width: 100vw;
  height: 100vh;
  color: white;
  background-color: red;
  padding: 25% 0;
`

let GreenBox = styled.div`
  width: 100vw;
  height: 100vh;
  color: white;
  background-color: green;
  padding: 25% 0;
`

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {state: "init", question: "Loading...", choices: ["...", "...", "..."]};
  }
  getGameState = () => {
    retrieve().then(res => {
      console.log(res);
      this.setState(res);
    });
  }
  componentWillMount() {
    try {
      setInterval(async () => {
        this.getGameState();
      }, 5000);
    } catch(e) {
      console.log(e);
    }
  }
  render() {
    if(this.state.state == "init") {
      return (
        <div>
          <Question question={this.state.question} choices={this.state.choices}/>
          {/* <Button onClick={this.getGameState}>Refresh Game</Button> */}
        </div>
      );
    }
    else if(this.state.state == "answering") {
      return(
        <div>
          <Question question={(this.state.playerOneBuzzed ? "Player 1" : "Player 2") + ", what is your answer?"} choices={this.state.choices}/>
          {/* <Button onClick={this.getGameState}>Refresh Game</Button> */}
          <h1>
          </h1>
        </div>
      );
    }
    else if(this.state.state == "result") {
      if(this.state.answeredCorrectly == false) {
        return(
          <RedBox>
            <h1>
              {this.state.playerOneBuzzed ? "Player 1" : "Player 2"}, you got it wrong!
            </h1>
          </RedBox>
        );
      }
      else {
        return(
          <GreenBox>
            <h1>
              {this.state.playerOneBuzzed ? "Player 1" : "Player 2"}, you got it right!
            </h1>
          </GreenBox>
        );
      }
    }
  }
}

export default App;
