import React from 'react'

function GoodDisplay({ game, player }) {

    return (
        <div>
            <h1>{game.title}</h1>
            {game.players.map((player)=>{
                console.log(player)
                return <p key={game.players.indexOf(player)}>{player.user.username}</p>
            })}
        </div>
    )
}

export default GoodDisplay