import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import ChatBox from './gameComponents/ChatBox'
import { useNavigate } from 'react-router-dom'
import Display from './gameComponents/Display'
import NotJoinedDisplay from './gameComponents/NotJoinedDisplay'


function Game({ user }) {
let {gameId} = useParams()
const [game, setGame] = useState()
const [localPlayer, setLocalPlayer] = useState({})
const [phase, setPhase] = useState("notStarted")
const navigate = useNavigate()



useEffect(()=>{
    console.log(user)
    if (!user.id){
        navigate('/login')
    }
    fetch(`/api/games/${gameId}/${user.id}`)
    .then(r=>r.json())
    .then((serverGame)=>{
        setGame(serverGame)
        if (serverGame.role !== "imposter"){
            // console.log('in there!')
            // console.log(user)
            // console.log(serverGame)
            setLocalPlayer(serverGame.players.filter((player)=>(player.user.id == user.id))[0])
        }
    })
},[])


return (
    <div className='game-div'>
    {game ? game.role == 'imposter' && game.round > 0?
    <p>Sorry you're not in this game and it has started</p>
    :
    game.role == 'imposter' ? 
        <NotJoinedDisplay game={game} user={user} setGame={setGame}/>
        :
        <>
        <Display phase={phase} setPhase={setPhase} game={game} setGame={setGame} localPlayer={localPlayer} user={user}/>
        {game && user ? 
            <ChatBox user={user} game={game} localPlayer={localPlayer}/>
            :
            <></>}
        </>
    :
    <></>
    }
    </div>
)
}

export default Game