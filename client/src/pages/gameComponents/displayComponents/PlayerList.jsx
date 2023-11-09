import React from 'react'

function PlayerList({game, clickHandler}) {
    return (
        <div className='player-list'>
            {/* see who the evil people are render */}
            {game.role == 'Evil' || game.role == 'Merlin' || game.role == 'Assassin' ? 
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
                        <p></p>}</div>)
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
                        <p></p>}
                    </div>)})
            }
        </div>
    )
}

export default PlayerList