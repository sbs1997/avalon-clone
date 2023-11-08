import { useState } from "react"
import React from 'react'

function Scoreboard({game}) {
    console.log(game)
    console.log(game.rounds)
    const [roundNums] = useState([1, 2, 3, 4, 5])
    // {game.rounds.map((round)=>{
    //     setRoundsLeft(roundsLeft-1)
    //     return <p key={round.id}>Round {round.number}: {round.winner}</p>
    // })}
    return (
        <div className="scoreboard">
            {roundNums.map((num)=>{
                return (
                    <div className="score-column" key={num}>
                        <p>Round {num}</p>
                        {game.round>num-1 ? <p>{game.rounds[num-1].winner} </p> : <p> </p>}
                    </div>
                )
            })}
        </div>
    )
}

export default Scoreboard