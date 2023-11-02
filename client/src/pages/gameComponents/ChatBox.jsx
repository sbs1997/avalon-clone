import React, { useState, useEffect } from 'react'
// import { io } from 'socket.io-client'
import Message from './Message'


function ChatBox({user, game, localPlayer, socket, connected}) {
    const [messages, setMessages] = useState([])
    const [newMessage, setNewMessage] = useState("")
    // console.log(user)

    useEffect(() => {
        // fetch(`/api/messages/game/${game.id}`)
        // .then(r=>r.json())
        // .then((serverMessages)=>{
        //     setMessages(serverMessages)
        // })
        // socket.on('messages-fetched', (serverMessages)=>{
        //     console.log(serverMessages)
        //     setMessages(serverMessages)
        // })
        // socket.emit('message-request', game.id)
        socket.emit('message-request', game.id)
    }, []);

    useEffect(() => {
        // console.log("use effect")
        if (connected){
            // console.log('the thing!')
            socket.on('server-message', (serverMessage)=>{
                addMessage(serverMessage)
            })
            }
            socket.on('messages-fetched', (serverMessages)=>{
                setMessages(serverMessages)
            })

            return () => {
            // console.log('clean-up!')
            socket.removeListener('server-message', (msg) => {
                console.log(msg);
            });
            }
    }, [messages, connected, localPlayer])
    
    function sendMessage(playerID, message, room){
        // console.log(localPlayer)
        // console.log(playerID)
        socket.emit('client-message', playerID, message, room)
    }
    
    function addMessage(message){
        setMessages([...messages, message])
    }

    return (
        <div>
            <div className="chat-box">
                {messages.toReversed().map((message)=>{
                    // console.log(message)
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