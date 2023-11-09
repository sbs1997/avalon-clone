import React, { useState, useEffect } from 'react'
import Message from './Message'


function ChatBox({user, game, localPlayer, socket, connected}) {
    const [messages, setMessages] = useState([])
    const [newMessage, setNewMessage] = useState("")
    // console.log(user)

    // Fetch the messages in the server
    useEffect(() => {
        socket.emit('message-request', game.id, socket.id)
    }, [game.round]);

    // add an event listener for new messages from the server
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
        <div className='chat-component'>
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
            <form className='message-form' onSubmit={(e)=>{
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