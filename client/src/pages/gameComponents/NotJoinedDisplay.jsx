import React, { useEffect } from 'react'

function NotJoinedDisplay({game, setGame, user, socket, connected}) {
    useEffect(()=>{
        if (connected){
            socket.on('update-players', (newGame)=>{
                setGame(newGame)
            })
        }
    },[])
    function handleJoin(){
        const newPlayer = {
            userID: user.id,
            gameID: game.id,
            owner: false
        }
        fetch(`/api/players`, {
            headers: { "Content-Type": "application/json"},
            method: "POST",
            body: JSON.stringify(newPlayer)
        })
        .then(()=>{
            fetch(`/api/games/${game.id}/${user.id}`)
            .then(r=>r.json())
            .then((serverGame)=>{
                setGame(serverGame)
                // if (serverGame.role !== "imposter"){
                //     setLocalPlayer(serverGame.players.filter((player)=>(player.user.id == user.id))[0])
                // }
            })
        })
    }

    return (
        <>
            <h2>Players:</h2>
            {game.players.map((player)=> <p key={game.players.indexOf(player)}>{player.user.username}</p>)}
            <button onClick={handleJoin}>Join Game</button>
        </>
    )
}

export default NotJoinedDisplay