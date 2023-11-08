import React, {useEffect, useState} from 'react'
import GameInfo from '../../components/GameInfo'

function QuestTeamVoteDisplay({game, socket, questTeam}){
    const [voteValue, setVoteValue] = useState("Not Cast")
    const [voters, setVoters] = useState([])

    useEffect(()=>{
        socket.on('quest-vote-cast', (newVoters)=>{
            setVoters(newVoters)
            console.log(newVoters)
        })
        socket.on('quest-vote-reciept', (vote)=>{
            if(vote.voted_for){
                setVoteValue("Approve")
            }
            else{
                setVoteValue("Reject")
            }
        })
        return(()=>{
            socket.off('quest-vote-cast', (newVoters)=>{
                setVoters(newVoters)
                // console.log(newVoters)
            })
            socket.off('quest-vote-reciept', (vote)=>{
                if(vote.votedFor){
                    setVoteValue("Approve")
                }
                else{
                    setVoteValue("Reject")
                }
            })
        })
    }, [])

    return (
        <>
            <div className='player-list'>
                {game.role == 'Evil' || game.role == 'Merlin' || game.role == 'Assassin' ? 
                    game.players.map((player)=> {
                        return (<div className='player-line'
                                key={game.players.indexOf(player)}>
                            <p className={game.baddies.includes(player.user.id) ? 
                                'baddie' 
                                : 
                                'unknown'} 
                                >{player.user.username}</p>
                            {player.leader ? 
                                <p> (leader)</p> 
                                : 
                                <></>}
                            {voters.includes(player.user.id) ?
                                <p>☑</p>: <p>☐</p>}
                        </div>)
                    })
                :
                    // normall people render
                    game.players.map((player)=>{
                        return (<div className='player-line' 
                            key={game.players.indexOf(player)}>
                                <p>{player.user.username}</p>
                                {player.leader ? 
                                    <p> (leader)</p> 
                                    : 
                                    <></>}
                            {voters.includes(player.user.id) ?
                                <p>☑</p>: <p>☐</p>}
                        </div>)
                    })
                }
            </div>
            <GameInfo game={game}/>
            <p className='vote-reciept'>Your vote: {voteValue}</p>
        </>
    )
}

export default QuestTeamVoteDisplay