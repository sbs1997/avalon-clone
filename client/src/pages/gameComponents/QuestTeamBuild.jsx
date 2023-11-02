import React from 'react'

function QuestTeamBuild() {
    return (
        <>
        <h2>Players:</h2>
        {game.players.map((player)=> <p key={game.players.indexOf(player)} className={game.baddies.includes(player.user.id) ? 'baddie' : 'unknown'}>{player.user.username}</p>)}
        </>
    )
}

export default QuestTeamBuild