import React from 'react'

function LobbyDisplay({game, user, socket}) {
    
    function handleLeave(){
        socket.emit('leave-game', game.id, user.id, socket.id)
    }

    function handleStart(){
        socket.emit('start-game', game.id)
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
            {game.owner ? <button onClick={handleStart}>Start Game!</button>
            :
            <button onClick={handleLeave}>Leave Game</button>}
        </div>
    )
}

export default LobbyDisplay