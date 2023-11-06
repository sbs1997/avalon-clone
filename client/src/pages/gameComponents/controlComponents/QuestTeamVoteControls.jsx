import React from 'react'

function QuestTeamVoteControls({game, socket, user, questTeam}) {
    // debugging stuff
    function handleStart(){
        socket.emit('start-game', game.id)
    }

    function voteYes(){
        socket.emit('quest-team-vote', true, user.id, game.id, socket.id)
    }
    function voteNo(){
        socket.emit('quest-team-vote', false, user.id, game.id, socket.id)
    }

    return (<>
        <div className='approval-controls'>
            <button onClick={voteYes}>Approve the Quest Team!</button>
            <button onClick={voteNo}>Vote against the Quest Team!</button>
            {/* debugging button */}
        </div>
        <h3>Proposed Quest Team:</h3>
        {/* see who the evil people are render */}
        {game.role == 'evil' || game.role == 'merlin' || game.role == 'assassin' ? 
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
        <button onClick={handleStart}>Start Game!</button>

    </>)
    
}

export default QuestTeamVoteControls