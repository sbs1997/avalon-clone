import React, { useEffect } from 'react'

function NotJoinedDisplay({game, user, socket}) {
    
    function handleJoin(){
        console.log(socket.id)
        console.log(game.id)
        const newPlayer = {
            userID: user.id,
            gameID: game.id,
            socketID: socket.id
        }
        socket.emit('join-game', newPlayer)
    }

    return (
        <>
            <h2>Players:</h2>
            {game.players.map((player)=> <p key={game.players.indexOf(player)}>{player.user.username}</p>)}
            <button onClick={handleJoin}>Join Game</button>
        </>
    )
}

export default NotJoinedDisplay