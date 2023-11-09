import React, {useState, useEffect} from 'react'
import PlayerList from './PlayerList'
import GameInfo from '../../components/GameInfo'

function QuestTeamBuildDisplay({game, socket, setQuestTeam}) {

    // const updateQT = (newTeam)=>{
    //     console.log('updated QT')
    //     setQuestTeam(newTeam)
    // }

    // const notUpdateQT = () => {
    //     console.log("didn't update qt")
    // }

    // useEffect(()=>{
    //     socket.on('updated-qt', updateQT)
    //     socket.on('not-updated-qt', notUpdateQT)
    //     return ()=>{
    //         console.log('turned updated-qt off')
    //         socket.off('updated-qt', updateQT)}
    //         socket.off('not-updated-qt', notUpdateQT)
    //         // socket.off('not-updated-qt', notUpdateQT)
    // }, [])



    
    function clickHandler(player_id, round_num){
        if (game.leader){
                console.log('update-qt pls')
                socket.emit('update-qt', player_id, round_num, game.id)
        }
    }


    return (
        <>
            <PlayerList game={game} clickHandler={clickHandler}/>
            <GameInfo game={game} />
        </>
    )
}

export default QuestTeamBuildDisplay