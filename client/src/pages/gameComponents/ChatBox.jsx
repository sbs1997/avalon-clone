import React, { useState, useEffect } from 'react'
import { io } from 'socket.io-client'
import Message from './Message'

let socket

function ChatBox({user, game, localPlayer}) {
    const [messages, setMessages] = useState([])
    const [newMessage, setNewMessage] = useState("")
    const [connected, setConnected] = useState(false)

    useEffect(() => {
        socket = io('ws://localhost:5555');
        setConnected(true)
        socket.emit('set-room', `game${game.id}`)
        fetch(`/api/messages/game/${game.id}`)
        .then(r=>r.json())
        .then((serverMessages)=>{
            console.log(serverMessages)
            setMessages(serverMessages)
        })
        return () => {
          socket.off('disconnected', (msg) => {
              console.log(msg);
            });
        }
    }, []);

    useEffect(() => {
        console.log("use effect")
        if (connected){
            // console.log('the thing!')
            socket.on('server-message', (serverMessage)=>{
                addMessage(serverMessage)
            })
            }
            return () => {
            // console.log('clean-up!')
            socket.removeListener('server-message', (msg) => {
                console.log(msg);
            });
            }
    }, [messages, connected])
    
    function sendMessage(playerID, message, room){
        socket.emit('client-message', playerID, message, room)
    }
    
    function addMessage(message){
        setMessages([...messages, message])
    }

    return (
        <div>
            <div className="chat-box">
                {messages.toReversed().map((message)=>{
                {/* {messages.map((message)=>{ */}
                    return <Message 
                        key={messages.indexOf(message)} 
                        message={message}
                        user={user}
                    />
                })}
            </div>
            <form onSubmit={(e)=>{
                e.preventDefault()
                sendMessage(localPlayer.id, newMessage, `game${game.id}`)
                setNewMessage("")
            }}>
                <label>Message:</label>
                <input onChange={(e)=>setNewMessage(e.target.value)} value={newMessage}/>
            </form>
        </div>
    )
}

export default ChatBox