import React from 'react'
import { Outlet, NavLink, Link } from 'react-router-dom'


function Nav(user, setUser) {
    console.log(user)
    console.log(user.id)
    function handleLogout(){
        fetch('api/logout', {method: 'DELETE'})
        setUser({})
    }

    return (
        <>
            <h1 className='big-title'>AVALON</h1>
            <div className='nav-bar'>
                <NavLink className='nav-bar-item' to="/">Main Menu</NavLink>
                <NavLink className='nav-bar-item' to='/login' onClick={handleLogout}>{user["user"].id ? "Log Out": "Login"}</NavLink>
                {user['user'].id ? <p className='nav-bar-item'>Logged in as: {user['user'].username}</p> : <></>}
            </div>
            <Outlet/>
        </>

    )
}

export default Nav