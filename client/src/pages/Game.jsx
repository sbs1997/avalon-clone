import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import ChatBox from './gameComponents/ChatBox'
import { useNavigate } from 'react-router-dom'
import Display from './gameComponents/Display'
import NotJoinedDisplay from './gameComponents/NotJoinedDisplay'
import { io } from 'socket.io-client'
import Controls from './gameComponents/Controls'

let socket

function Game({ user }) {
    let {gameId} = useParams()
    const [game, setGame] = useState({})
    const [localPlayer, setLocalPlayer] = useState({})
    const [connected, setConnected] = useState(false)
    const [questTeam, setQuestTeam] = useState([])
    const navigate = useNavigate()
    // console.log(user)

    const playerChangeHandler = (newPlayers)=>{
        console.log(newPlayers)
        console.log('player change!')
        setGame({...game, players: newPlayers})
    }


    useEffect(()=>{
        // console.log(user)
        if (!user.id){
            navigate('/login')
        }
        socket = io('ws://localhost:5555');
        socket.on('connect', ()=>{
            console.log(socket.id)
            console.log(gameId)
            setConnected(true)
            socket.emit('set-room', gameId, user.id, socket.id)
        })
        socket.on('update-game', (newGame)=>{
            console.log('update-game')
            console.log(newGame)
            setGame(newGame)
            setLocalPlayer(newGame.players.filter((player)=>(player.user.id == user.id))[0])
        })
        socket.on('game-started', ()=>{
            console.log('game-started')
            socket.emit('info-req', gameId, user.id, socket.id)
            setQuestTeam([])
        })
        socket.on('updated-qt',  (newTeam)=>{
            console.log('updated QT')
            setQuestTeam(newTeam)
        })
        socket.on('qt-submitted', ()=>{
            console.log('quest team proposed!')
            socket.emit('info-req', gameId, user.id, socket.id)
        })
        socket.on('all-qt-votes-in', (approval)=>{
            console.log('all qt votes in')
            socket.emit('info-req', gameId, user.id, socket.id)
            if (!approval){
                console.log('Vote Failed')
            }
        })
        socket.on('quest-failed', (failVotes)=>{
            console.log(`quest failed ${failVotes} against!`)
            socket.emit('info-req', gameId, user.id, socket.id)
            setQuestTeam([])
        })
        socket.on('quest-success', ()=>{
            console.log('quest succeeded!')
            socket.emit('info-req', gameId, user.id, socket.id)
            setQuestTeam([])
        })
        socket.on('merlin-assassination', ()=>{
            console.log('try to assasinate merlin')
            socket.emit('info-req', gameId, user.id, socket.id)
        })
        socket.on('game-over', ()=>{
            socket.emit('info-req', gameId, user.id, socket.id)
        })
        return () => {
            console.log('disconnected!!')
            socket.disconnect()
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
        <div>
            {game ? 
                game.role == 'imposter' && game.round > 0?
                    <p>Sorry you're not in this game and it has started</p>
                    :
                    <div className='game-div'>
                        <div className='game-header'>
                            <h1 className='game-title'>{game.title}: {game.phase == "pregame" ? "Pregame Lobby" :
                                game.phase =="team_building" ? "Team Building": 
                                    game.phase=="qt_voting" ? "Quest Team Voting" :
                                        "Questing"}</h1>
                            <h3>{user.username}: {game.role}</h3>
                        </div>
                        {game.role == 'imposter' ? 
                            <NotJoinedDisplay game={game} user={user} socket={socket}/>
                            :
                            <Display game={game} user={user} socket={socket} questTeam={questTeam} setQuestTeam={setQuestTeam}/>}
                        {game && user && socket ?
                            <Controls socket={socket} user={user} game={game} questTeam={questTeam}/>
                            :
                            <></>
                        }
                        {game && user && socket? 
                            <ChatBox socket={socket} user={user} game={game} localPlayer={localPlayer} connected={connected}/>
                            : 
                            <></>}
                    </div>
                :
                <></>
            }
        </div>
    )
}

export default Game