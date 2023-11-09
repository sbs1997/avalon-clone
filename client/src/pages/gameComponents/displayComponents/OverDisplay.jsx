import React, { useEffect, useState } from 'react'

function OverDisplay({game}) {

    const goodRoles = ["Merlin", "Good"]
    const evilRoles = ["Assassin", "Evil"]

    const [winners, setWinners] = useState([])
    useEffect(()=>{
        if (game.winner == "Good"){
            setWinners(goodRoles)
        }else{
            setWinners(evilRoles)
        }
    }, [])

    return (
        <>
            <h1 className='game-over-header'>{winners.includes(game.role)? "VICTORY" : "DEFEAT"}</h1>
            {game.players.map((player)=> {
                return (<div className='player-line'
                        key={game.players.indexOf(player)}>
                    <p className={game.baddies.includes(player.user.id) ? 
                        'baddie' 
                        : 
                        'unknown'} 
                        >{player.user.username} ({player.role})</p>
                </div>)
            })}
        </>
    )
}

export default OverDisplay