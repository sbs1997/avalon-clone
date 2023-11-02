import React from 'react'

function LobbyDisplay({game, user, socket}) {
    
    function handleLeave(){
        socket.emit('leave-game', game.id, user.id, socket.id)
    }

    function handleStart(){
        socket.emit('start-game', game.id)
    }
    
    return (
        <>
            <h2>Players:</h2>
            {game.players.map((player)=> <p key={game.players.indexOf(player)}>{player.user.username}</p>)}
            {game.owner ? <button onClick={handleStart}>Start Game!</button>
            :
            <button onClick={handleLeave}>Leave Game</button>}
        </>
    )
}

export default LobbyDisplay