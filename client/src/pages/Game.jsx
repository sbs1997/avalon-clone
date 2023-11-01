import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import ChatBox from './gameComponents/ChatBox'
import { useNavigate } from 'react-router-dom'
import Display from './gameComponents/Display'
import NotJoinedDisplay from './gameComponents/NotJoinedDisplay'
import { io } from 'socket.io-client'


let socket

function Game({ user }) {
    let {gameId} = useParams()
    const [game, setGame] = useState()
    const [localPlayer, setLocalPlayer] = useState({})
    const [phase, setPhase] = useState("notStarted")
    const [connected, setConnected] = useState(false)
    const navigate = useNavigate()



    useEffect(()=>{
        console.log(user)
        if (!user.id){
            navigate('/login')
        }
        // fetch(`/api/games/${gameId}/${user.id}`)
        // .then(r=>r.json())
        // .then((serverGame)=>{
        //     setGame(serverGame)
        //     if (serverGame.role !== "imposter"){
        //         // console.log('in there!')
        //         // console.log(user)
        //         // console.log(serverGame)
        //         setLocalPlayer(serverGame.players.filter((player)=>(player.user.id == user.id))[0])
        //     }
        //     socket = io('ws://localhost:5555');
        //     setConnected(true)
        //     socket.emit('set-room', serverGame.id, user.id)
        // })
        socket = io('ws://localhost:5555');
        setConnected(true)
        socket.emit('set-room', gameId, user.id)
        socket.on('update-game', (newGame)=>{
            setGame(newGame)
        })
        return () => {
            socket.off('disconnected', (msg) => {
                console.log(msg);
            });
        }
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
            {game && user && socket? 
                <ChatBox socket={socket} user={user} game={game} localPlayer={localPlayer} connected={connected}/>
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