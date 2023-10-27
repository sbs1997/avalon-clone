import React from 'react'
import App from './App.jsx'
import './index.css'
import * as ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
  Route
} from "react-router-dom";

import SignUp from './pages/SignUp.jsx';
import Nav from './components/Nav.jsx';
import Game from './pages/Game.jsx';
import LogIn from './pages/LogIn.jsx';
import NewGameForm from './pages/NewGameForm.jsx';
import WaitingRoom from './pages/WaitingRoom.jsx';
import MainMenu from './pages/MainMenu.jsx';


const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path ='/' element= {<Nav/>}>
      <Route index element={<MainMenu/>}/>
      <Route path='game/:id' element={<Game/>}/>
      <Route path='login' element={<LogIn/>}/>
      <Route path='signup' element={<SignUp/>}/>
      <Route path='new-game' element={<NewGameForm/>}/>
      <Route path='waiting-room/:id' element={<WaitingRoom/>}/>
    </Route>
  )
)

ReactDOM.createRoot(document.getElementById('root')).render(
  <RouterProvider router={router}/>
)
