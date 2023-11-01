import React from 'react'

function Message({message, user}) {
  console.log(user)
  console.log(message)
  const sender = message.player.user.username
  // console.log(message)
  // console.log(user)
  return (
    <div className='message'>
        <p className={message.player.user.id == user.id ? "my-message" : "their-message"}>{sender}: {" "}</p>
        <p>{message.message}</p>
    </div>
  )
}

export default Message