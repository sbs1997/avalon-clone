import React from 'react'

function GameInfo({game}) {
    return (
        <p className='info'>{`Round ${game.round}
Quest size: ${game.rounds[game.round-1].quest_size}
Number of Failed Quest Votes: ${game.rounds[game.round-1].team_votes_failed}/5
${game.rounds[game.round-1].last_votes_for ? `Last vote: ${game.rounds[game.round-1].last_votes_for} approve - ${game.size-game.rounds[game.round-1].last_votes_for} reject` : ''}`}</p>
    )
}

export default GameInfo