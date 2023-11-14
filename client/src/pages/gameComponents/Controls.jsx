import React from 'react'
import QuestTeamBuildControls from './controlComponents/QuestTeamBuildControls'
import QuestTeamVoteControls from './controlComponents/QuestTeamVoteControls'
import QuestVoteControls from './controlComponents/QuestVoteControls'

function Controls({game, socket, user, questTeam}) {
    // debugging stuff
    // function handleStart(){
    //     socket.emit('start-game', game.id)
    // }
    return (
        <div className='controls'>
            {game.phase == 'team_building' ?
                <QuestTeamBuildControls game={game} socket={socket} user={user} questTeam={questTeam}/>
                :
                game.phase == 'qt_voting' ?
                    <QuestTeamVoteControls game={game} socket={socket} user={user} questTeam={questTeam}/>
                    :
                    game.phase == 'quest_voting' ?
                        <QuestVoteControls game={game} socket={socket} user={user} questTeam={questTeam}/>
                        :
                        <></>
            }
            {/* <button onClick={handleStart}>Start Game!</button> */}
        </div>
    )
}

export default Controls