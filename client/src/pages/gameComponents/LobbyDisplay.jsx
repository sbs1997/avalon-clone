import React from 'react'

function LobbyDisplay({game, user, localPlayer, setGame}) {
    console.log(game)
    function handleLeave(){
        // console.log(localPlayer)
        fetch(`/api/players/${localPlayer.id}`, {
            method: "DELETE",
        })
        .then(()=>{
            console.log(game)
            console.log(user)
            fetch(`/api/games/${game.id}/${user.id}`)
            .then(r=>r.json())
            .then((serverGame)=>{
                setGame(serverGame)
            })
        })
    }

    return (
        <>
            <h2>Players:</h2>
            {game.players.map((player)=> <p key={game.players.indexOf(player)}>{player.user.username}</p>)}
            <button onClick={handleLeave}>Leave Game</button>
        </>
    )
}

export default LobbyDisplay