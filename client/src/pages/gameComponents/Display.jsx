import React from 'react'
import LobbyDisplay from './LobbyDisplay'
import QuestTeamBuild from './QuestTeamBuild'

function Display({ game, user, socket }) {
    // console.log(game)
    return (
        <div className='game-display'>
            {game ?
                <><h1>{game.title}</h1>
                {(game.phase == "pregame" )? 
                    <LobbyDisplay game={game} user={user} socket={socket} />
                    :
                    game.phase == "team_building" ? 
                        <QuestTeamBuild game={game} user={user} socket={socket} />
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