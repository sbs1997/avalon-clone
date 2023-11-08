import React from 'react'

function QuestTeamVoteControls({game, socket, user, questTeam}) {


    function voteYes(){
        socket.emit('quest-team-vote', true, user.id, game.id, socket.id)
    }
    function voteNo(){
        socket.emit('quest-team-vote', false, user.id, game.id, socket.id)
    }

    return (<>
        <div className='approval-controls'>
            <button onClick={voteYes}>Approve!</button>
            <button onClick={voteNo}>Reject!</button>
        </div>
        <h3>Proposed Quest Team:</h3>
        {/* see who the evil people are render */}
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

    </>)
    
}

export default QuestTeamVoteControls