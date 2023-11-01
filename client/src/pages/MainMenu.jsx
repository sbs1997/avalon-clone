import React, { useEffect, useState } from 'react';
import GameCard from './menuComponents/GameCard';
import { useNavigate } from 'react-router-dom'


function MainMenu({user}) {
  const [games, setGames] = useState([])
  const navigate = useNavigate()

  useEffect(()=>{
    if (!user.id){
      navigate('/login')
    }
    fetch('/api/games')
    .then(r=>r.json())
    .then(serverGames=>{
      setGames(serverGames)
    })
  },[])

  return (
    <>
      <div>{user.username}</div>
      {games.map((game)=>{
        return <GameCard key={game.id} game={game}/>
      })}
  </>
  )
}

export default MainMenu