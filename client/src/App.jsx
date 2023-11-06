import React, { useEffect, useState } from 'react'
import './index.css'
import {
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
  Route
} from "react-router-dom";

import SignUp from './pages/SignUp.jsx';
import Nav from './pages/components/Nav.jsx';
import Game from './pages/Game.jsx';
import LogIn from './pages/LogIn.jsx';
import NewGameForm from './pages/NewGameForm.jsx';
import WaitingRoom from './pages/WaitingRoom.jsx';
import MainMenu from './pages/MainMenu.jsx';


function App() {

    const [user, setUser] = useState({})

    const router = createBrowserRouter(
        createRoutesFromElements(
          <Route path ='/' element= {<Nav user={user} setUser={setUser}/>}>
            <Route index element={<MainMenu user={user}/>}/>
            <Route path='game/:gameId' element={<Game user={user}/>}/>
            <Route path='login' element={<LogIn user={user} setUser={setUser}/>}/>
            <Route path='signup' element={<SignUp user={user} setUser={setUser}/>}/>
            <Route path='new-game' element={<NewGameForm user={user}/>}/>
            <Route path='waiting-room/:id' element={<WaitingRoom user={user}/>}/>
          </Route>
        )
      )
    
  return (
    <div className='App'>
        <RouterProvider router={router}/>
    </div>
  )
}

export default App