import React from 'react'

function QuestTeamBuildControls({game, questTeam, socket}) {
    // debugging stuff
  function handleStart(){
      socket.emit('start-game', game.id)
  }

  function submitTeam(){
    socket.emit('submit-qt', game.id )
  }

  return (
    <div>
    {/* quest team list */}
    <h2>Current quest team (it's not locked in yet)</h2>
    {questTeam.map((quester)=><p key={quester.id}>{quester.player.user.username}</p>)}

    {game.leader ?
      <button onClick={submitTeam}>Submit Team</button>
      :
      <></>
    }

    {/* debugging button */}
    {game.owner ? 
        <button onClick={handleStart}>Start Game!</button>
        :
        <></>
    }</div>
  )
}

export default QuestTeamBuildControls