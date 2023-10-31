import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import ChatBox from './gameComponents/ChatBox'
import { useNavigate } from 'react-router-dom'


function Game({ user }) {
  let {gameId} = useParams()
  const [game, setGame] = useState()
  const [localPlayer, setLocalPlayer] = useState({})
  const navigate = useNavigate()
  

  useEffect(()=>{
    console.log(user)
    if (!user.id){
      navigate('/login')
    }
    // fetch(`/api/games/${gameId}/${user.id}`)
    fetch(`/api/games/${gameId}`)
    .then(r=>r.json())
    .then((serverGame)=>{
      setGame(serverGame)
      if (user){
        setLocalPlayer(serverGame.players.filter((player)=>(player.user.id == user.id))[0])
      }// console.log(serverGame.players.filter((player)=>(player.user.id == user.id)))
    })
  },[])

  // console.log(localPlayer)
  // console.log(localPlayer.id)

  return (
    <div className='game-div'>
      <h1>{game ? game.title : <></>}</h1>
      <h2>Players:</h2>
      {game ? game.players.map((player)=>{
        console.log(player)
          return <p key={game.players.indexOf(player)}>{player.user.username}</p>
        })
        :
        <></>}
      {game && user ? 
        <ChatBox user={user} game={game} localPlayer={localPlayer}/>
        :
        <></>}
    </div>
  )
}

export default Game