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
        <div className='game-display'>
            <h2>Players:</h2>
            {game.players.map((player)=>{return(
                <div className='player-line' 
                    onClick={()=>clickHandler(player.id, game.round)}
                    key={game.players.indexOf(player)}>
                        <p>{player.user.username}</p>
            </div>)})}
            <button onClick={handleJoin}>Join Game</button>
        </div>
    )
}

export default NotJoinedDisplay