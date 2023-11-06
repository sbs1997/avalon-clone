import React from 'react'
import LobbyDisplay from './displayComponents/LobbyDisplay'
import QuestTeamBuildDisplay from './displayComponents/QuestTeamBuildDisplay'
import QuestTeamVoteDisplay from './displayComponents/QuestTeamVoteDisplay'

function Display({ game, user, socket, questTeam, setQuestTeam }) {
    // console.log(game)
    return (
        <div className='game-display'>
                {(game.phase == "pregame" )? 
                    <LobbyDisplay game={game} user={user} socket={socket} />
                    :
                    game.phase == "team_building" ? 
                        <QuestTeamBuildDisplay game={game} user={user} socket={socket} questTeam={questTeam} setQuestTeam={setQuestTeam}/>
                        :
                        game.phase == "qt-voting" ?
                            <QuestTeamVoteDisplay game={game} user={user} socket={socket} questTeam={questTeam} />
                            :
                            <></>
                }
        </div> 
    )
}

export default Display