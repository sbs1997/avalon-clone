import React from 'react'
import LobbyDisplay from './LobbyDisplay'

function Display({ phase, game, user, localPlayer, setGame, setPhase}) {
    console.log(game)
    return (
        <div className='game-display'>
            {game ?
                <><h1>{game.title}</h1>
                {(phase == "notStarted" )? 
                    <LobbyDisplay game={game} user={user} localPlayer={localPlayer} setGame={setGame}/>
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