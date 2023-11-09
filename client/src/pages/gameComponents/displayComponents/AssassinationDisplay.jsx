import React from 'react'
import PlayerList from './PlayerList'

function AssassinationDisplay({game, socket}) {
    
    function clickHandler(playerID, gameRound){
        socket.emit('assassinate', playerID)
    }
    
    function dummyHandler(){
        return
    }

    return (
        <>
            <h3>Good is about to triumph, but evil has one last chance. If the assassin can kill merlin then Evil will steal the victory!</h3>
            {game.role == "Assassin" ? 
                <PlayerList game={game} clickHandler={clickHandler}/>
                : 
                <PlayerList game={game} clickHandler={dummyHandler}/>
            }
        </>
    )
}

export default AssassinationDisplay