import React from 'react'
import GameInfo from '../../components/GameInfo'

function QuestVoteDisplay({game, questTeam}) {
    return (
        <>
            <h2>Quest Members:</h2>
            <div className='player-list'>
                {game.role == 'Evil' || game.role == 'Merlin' || game.role == 'Assassin' ? 
                    questTeam.map((quester)=> {
                    return (<div className='player-line'
                            key={questTeam.indexOf(quester)}>
                        <p className={game.baddies.includes(quester.player.user.id) ? 
                            'baddie' 
                            : 
                            'unknown'} 
                            >{quester.player.user.username}</p>
                        {quester.player.leader ? 
                            <p> (leader)</p> 
                            : 
                            <></>}</div>)
                    })
                :
                    // normall people render
                    questTeam.map((quester)=> {
                        return (<div className='player-line'
                                key={questTeam.indexOf(quester)}>
                            <p>{quester.player.user.username}</p>
                            {quester.player.leader ? 
                                <p> (leader)</p> 
                                : 
                                <></>}
                        </div>)
                    })
                }
            </div>
            <GameInfo game={game} />
        </>
    )
}

export default QuestVoteDisplay