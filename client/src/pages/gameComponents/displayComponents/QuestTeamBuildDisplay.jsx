import React, {useState, useEffect} from 'react'

function QuestTeamBuildDisplay({game, socket, questTeam, setQuestTeam}) {

    const [qtUpdateFailAlert, setQtUpdateFailAlert] = useState(false)

    // useEffect(()=>{
    //     setTimeout(setQtUpdateFailAlert(false), 1500)
    // }, [qtUpdateFailAlert])
    // console.log(game)

    const updateQT = (newTeam)=>{
        console.log('updated QT')
        setQuestTeam(newTeam)
    }

    const notUpdateQT = () => {
        console.log(message)
        console.log("didn't update qt")
        setQtUpdateFailAlert(true)
    }

    useEffect(()=>{
        socket.on('updated-qt', updateQT)
        socket.on('not-updated-qt', notUpdateQT)
        return ()=>{
            console.log('turned updated-qt off')
            socket.off('updated-qt', updateQT)}
            // socket.off('not-updated-qt', notUpdateQT)
    }, [])

    
    function clickHandler(player_id, round_num){
        if (game.leader){
                console.log('update-qt pls')
                socket.emit('update-qt', player_id, round_num, game.id)
        }


    }
    return (
        <>
            {/* see who the evil people are render */}
            {game.role == 'evil' || game.role == 'merlin' || game.role == 'assassin' ? 
                game.players.map((player)=> {
                return (<div className='player-line'
                        onClick={()=>clickHandler(player.id, game.round)}
                        key={game.players.indexOf(player)}>
                    <p className={game.baddies.includes(player.user.id) ? 
                        'baddie' 
                        : 
                        'unknown'} 
                        >{player.user.username}</p>
                    {player.leader ? 
                        <p> (leader)</p> 
                        : 
                        <></>}</div>)
                    })
            :
                // normall people render
                game.players.map((player)=>{
                return (<div className='player-line' 
                    onClick={()=>clickHandler(player.id, game.round)}
                    key={game.players.indexOf(player)}>
                        <p>{player.user.username}</p>
                        {player.leader ? 
                            <p> (leader)</p> 
                            : 
                            <></>}
                    </div>)})
            }
            <p>{qtUpdateFailAlert ? `cannot add more that ${game.rounds[game.round].quest_size} players this round` : ""}</p>
        </>
    )
}

export default QuestTeamBuildDisplay