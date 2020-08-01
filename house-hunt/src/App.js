import React from 'react';
import ReactDOM from 'react-dom'
import './App.css';

var players = require("./names.json")
var round_info = require("./round_info.json")
var data = require("./data.json")

var scores = {}

function Item(props) {
    return (
        <div>
            <img src={props.pic} alt={props.word} width="300" height="300"/>
            <p>{props.word}</p>
            <input type="checkbox" className="checkbox" name={props.playerId}/>
        </div>
    );
}

function Category(props) {
    const player_objs = []
    const player_ids = Object.keys(players)
    for(const id of player_ids) {
        const cur_player = data["round"+props.round][id]  // player objs not necessarily ordered
        if(cur_player === undefined) {  // player did not have any objs for this round 
            player_objs.push(<td className="none">None</td>)
            continue
        }
        let cur_obj = null
        for(const el of cur_player) {
            if(el["obj_num"] === props.cat) 
                cur_obj = el
        }
        if(cur_obj === null) {  // player did not get obj for this category
            player_objs.push(<td className="none">None</td>)
        }
        else {
            const pic = cur_obj["pic"]
            const word = cur_obj["word"]
            player_objs.push(<td><Item pic={pic} word={word} playerId={id}/></td>)
        }   
    }
    return (
        <tr className="text">
            <td id="category">{round_info[props.round]["cats"][props.cat - 1]}</td> 
            {player_objs}
        </tr>
    );
}

// 3 rounds, each round has 5 categories
function Round(props) {
    return (
        <table>
            <thead>
                <tr className="table-heading, text">
                    <th id="round_num">ROUND {props.num}: <span id="letter">{round_info[props.num]["letter"]}</span></th>
                    {getPlayerNames()}
                </tr>
            </thead>
            <tbody>
                <Category round={props.num} cat={1}/>
                <Category round={props.num} cat={2}/>
                <Category round={props.num} cat={3}/>
                <Category round={props.num} cat={4}/>
                <Category round={props.num} cat={5}/>
            </tbody>
        </table>
    );
}

function Scoreboard() {
    return (
        <table>
            <tbody>
                <tr className="text">
                    {getScores()}
                </tr>
            </tbody>
        </table>
    );
}

function App() {
  return (
      <div>
        <h1 id="header" className="text">House Hunt</h1>
        <Round num={1}/>
        <br></br>
        <Round num={2}/>
        <br></br>
        <Round num={3}/>
        <br></br>
        <div id="button-div"><button type="button" className="text" id="button" onClick={handleScore}>Score</button></div>
        <br></br>
        <div id="scoreboard-holder"></div>
        <br></br>
      </div>
  );
}

function getPlayerNames() {
    const names = []
    const player_names = Object.values(players)
    for(const name of player_names) 
        names.push(<th id="player-name">{name}</th>)
    return names
}

function getScores() {
    const score_data = []
    const player_ids = Object.keys(scores)
    for(const id of player_ids)
        score_data.push(<td>{players[id]}: <span id="score">{scores[id]}</span></td>)
    return score_data
}

function setUpScores() {
    const ids = Object.keys(players)
    for(const id of ids) 
        scores[id] = 0
}

function calcScores() {
    var checkboxes = document.getElementsByClassName("checkbox")
    for(const c of checkboxes) {
        if(c.checked) {
            const id = c.getAttribute("name")
            scores[id] += 1
        }
    }
}

function handleScore() {
    setUpScores()
    calcScores()
    ReactDOM.render(
        <Scoreboard />,
        document.getElementById("scoreboard-holder")
    )
}

export default App;
