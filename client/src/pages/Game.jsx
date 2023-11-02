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
    const [localSocket, setLocalSocket] = useState('')
    const navigate = useNavigate()
    // console.log(user)

    const playerChangeHandler = (newPlayers)=>{
        console.log(newPlayers)
        console.log('player change!')
        setGame({...game, players: newPlayers})
    }


    useEffect(()=>{
        console.log(user)
        if (!user.id){
            navigate('/login')
        }
        socket = io('ws://localhost:5555');
        socket.on('connect', ()=>{
            console.log(socket.id)
            console.log(gameId)
            setConnected(true)
            setLocalSocket(socket.id)
            socket.emit('set-room', gameId, user.id, socket.id)
        })
        socket.on('update-game', (newGame)=>{
            console.log('update-game')
            setGame(newGame)
            setLocalPlayer(newGame.players.filter((player)=>(player.user.id == user.id))[0])
        })
        return () => {
            console.log('thing!')
            socket.disconnect()
            // socket.off('disconnected', (msg) => {
            //     console.log(msg);
            // });
        }
    },[])

    useEffect(()=>{
        console.log('update player change')
        socket.on('player-change', playerChangeHandler)
        return ()=>{
            socket.off('player-change', playerChangeHandler)
        }
    }, [game, connected])


    return (
        <div className='game-div'>
        {game ? game.role == 'imposter' && game.round > 0?
        <p>Sorry you're not in this game and it has started</p>
        :
        game.role == 'imposter' ? 
            <NotJoinedDisplay game={game} user={user} socket={socket}/>
            :
            <>
            <Display phase={phase} setPhase={setPhase} game={game} setGame={setGame} localPlayer={localPlayer} user={user} socket={socket} localSocket={localSocket}/>
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