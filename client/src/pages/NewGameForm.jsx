import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';

function NewGameForm({user}) {
    const [title, setTitle] = useState("")
    const [size, setSize] = useState("")
    const navigate = useNavigate()


    // const handleInputChange = (e)=>{
    //     const { name, value } = e.target

    //     if (name == "title"){
    //         setTitle(value)
    //     }else if (name == "size"){
    //         setSize(value)
    //     }
    // }

    const handleSubmit = (e)=>{
        e.preventDefault()
        console.log('submit!')
        const newGame = {
            "title": title,
            "size": size
        }
        fetch('api/games', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify(newGame)
        })
        .then((r)=>r.json())
        .then((newGame)=>{
            console.log(newGame)
            const newPlayer = {
                userID : user.id,
                gameID : newGame.id,
                owner: true
            }
            console.log(newPlayer)
            fetch('api/players', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(newPlayer)
            })
            .then(navigate(`/game/${newGame.id}`))
        })
    }

    return (
        <div id='new-game-form'>
            <h1>Create a New Game</h1>
            <form onSubmit={handleSubmit}>
                <label className='new-game-labels'>
                    Title:
                    <input type="text" name="title" value={title} onChange={(e)=>setTitle(e.target.value)}/>
                    <br/><br/>
                </label>
                <label className='new-game-labels'>
                    {"Size:   "}
                    <select value={size} onChange={(e)=>setSize(e.target.value)}>
                        <option value="5">5</option>
                        <option value="6">6</option>
                        <option value="7">7</option>
                        <option value="8">8</option>
                        <option value="9">9</option>
                        <option value="10">10</option>
                    </select>
                    <br/> <br/>
                </label>
                <input className='submit-button' type ="submit" value="Submit"/>
            </form>
        </div>
    )
}

export default NewGameForm