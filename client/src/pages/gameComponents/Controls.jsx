import React from 'react'
import QuestTeamBuildControls from './controlComponents/QuestTeamBuildControls'
import QuestTeamVoteControls from './controlComponents/QuestTeamVoteControls'

function Controls({game, socket, user, questTeam}) {
    return (
        <div className='controls'>
            {game.phase == 'team_building' ?
                <QuestTeamBuildControls game={game} socket={socket} user={user} questTeam={questTeam}/>
                :
                game.phase == 'qt-voting' ?
                    <QuestTeamVoteControls game={game} socket={socket} user={user} questTeam={questTeam}/>
                    :
                    <></>
            }
        </div>
    )
}

export default Controls