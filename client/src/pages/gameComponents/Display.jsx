import React from 'react'
import LobbyDisplay from './LobbyDisplay'

function Display({ phase, game, user, socket, localPlayer, setGame, setPhase}) {
    // console.log(game)
    return (
        <div className='game-display'>
            {game ?
                <><h1>{game.title}</h1>
                {(phase == "notStarted" )? 
                    <LobbyDisplay game={game} user={user} socket={socket} />
                    :
                    <></>
                }
                </>
                :
                <></>
            }
        </div>
    )
}

export default Display