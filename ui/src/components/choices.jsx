import React from 'react';
import styled from 'styled-components';

let Choice = styled.div`
    color: white;
    font-size: 30px;
    padding: 20px 0;
`

export default class Choices extends React.Component {
    render() {
        return(
            <div>
                {this.props.choices.map((choice, i) => {
                    return <Choice key={i}>{choice}</Choice>
                })}
            </div>
        );
    }
}