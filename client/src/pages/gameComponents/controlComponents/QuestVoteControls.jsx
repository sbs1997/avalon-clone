import React, {useEffect, useState} from 'react'

function QuestVoteControls({game, socket, user, questTeam}) {
    const [filteredTeam, setFilteredTeam]= useState(questTeam.filter((quester=>quester.player.user.id == user.id)))
    const [voteValue, setVoteValue] = useState("Not Cast")

    useEffect(()=>{
        socket.on('quest-vote-reciept', (vote)=>{
            if(vote.voted_for){
                setVoteValue("Pass")
            }
            else{
                setVoteValue("Fail")
            }
        })
        return (()=>{
            socket.off('quest-vote-reciept', (vote)=>{
                if(vote.votedFor){
                    setVoteValue("Pass")
                }
                else{
                    setVoteValue("Fail")
                }
            })
        })
    }, [])

    function voteYes(){
        socket.emit('quest-vote', true, user.id, game.id, socket.id)
    }
    function voteNo(){
        socket.emit('quest-vote', false, user.id, game.id, socket.id)
    }


    return (
        <>
            {filteredTeam.length>0 ? 
                <>
                    <div className='approval-controls'>
                        <button onClick={voteYes}>Pass!</button>
                        <button onClick={voteNo}>Fail!</button>
                    </div>
                    <p>Your vote: {voteValue}</p>
                </>
                :
                <div>Not on the quest</div>}
        </>
    )
}

export default QuestVoteControls