import React from 'react'

function QuestTeamBuildControls({game, questTeam, socket}) {

    function submitTeam(){
        socket.emit('submit-qt', game.id )
    }

    return (
        <div>
        {/* quest team list */}
        <h2>Quest Team</h2>
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
        {game.leader ?
        <button onClick={submitTeam}>Submit Team</button>
        :
        <></>
    }</div>
    )
}

export default QuestTeamBuildControls