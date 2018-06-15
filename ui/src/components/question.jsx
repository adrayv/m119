import React from 'react';
import styled from 'styled-components';
import Choices from './choices';

let Q = styled.div`
    background-color: palevioletred;
    width: 100vw;
    height: 100vh;
    text-align: center;
    color: white;
    padding: 15% 0;
    font-size: 40px;
`

export default class Question extends React.Component {
  constructor(props) {
    super(props);
  }
    render() {
        console.log(this.props);
        return(
            <Q>
                {this.props.question}
                <Choices choices={this.props.choices}/>
            </Q>
        );
    }
}