import React from 'react'
import LobbyDisplay from './displayComponents/LobbyDisplay'
import QuestTeamBuildDisplay from './displayComponents/QuestTeamBuildDisplay'
import QuestTeamVoteDisplay from './displayComponents/QuestTeamVoteDisplay'
import QuestVoteDisplay from './displayComponents/QuestVoteDisplay'
import Scoreboard from './displayComponents/Scoreboard'
import OverDisplay from './displayComponents/OverDisplay'
import AssassinationDisplay from './displayComponents/AssassinationDisplay'

function Display({ game, user, socket, questTeam, setQuestTeam }) {
    // console.log(game)
    return (
        <div className='game-display'>
   
            {(game.phase == "pregame" )? 
                <LobbyDisplay game={game} user={user} socket={socket} />
                :
                <>
                    <Scoreboard game={game}/>
                    {game.phase == "team_building" ? 
                        <QuestTeamBuildDisplay game={game} user={user} socket={socket} questTeam={questTeam} setQuestTeam={setQuestTeam}/>
                        :
                        game.phase == "qt_voting" ?
                            <QuestTeamVoteDisplay game={game} user={user} socket={socket} questTeam={questTeam} />
                            :
                            game.phase == "quest_voting" ?
                                <QuestVoteDisplay game={game} user={user} socket={socket} questTeam={questTeam} />
                                :
                                game.phase == "merlin_assassination" ?
                                    <AssassinationDisplay game={game} socket={socket}/>
                                    :
                                    game.phase == "over" ?
                                        <OverDisplay game={game} />
                                        :
                                        <></>
                    }
                </>
            }
        </div> 
    )
}

export default Display