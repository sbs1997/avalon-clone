import React from 'react'
import { useNavigate } from 'react-router-dom'

function GameCard({game}) {
    const navigate = useNavigate()
    const {title, size, id} = game
    // handleClick = 
    return (
        <div className='game-card' onClick={()=>navigate(`/game/${id}`)}>
            <h2>{title}</h2>
            <p>{size} players</p>
        </div>
    )
}

export default GameCard