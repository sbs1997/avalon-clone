import React from 'react'
import { Outlet, NavLink, Link } from 'react-router-dom'


function Nav(user, setUser) {
  function handleLogout(){
    fetch('api/logout', {method: 'DELETE'})
    setUser({})
  }

  return (
    <>
        <NavLink to='/login' onClick={handleLogout}>Log Out</NavLink>
        <NavLink to="/">Main Menu</NavLink>
        <Outlet/>
    </>
  )
}

export default Nav