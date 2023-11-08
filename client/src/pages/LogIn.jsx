import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'


function LogIn({user, setUser}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate()


  const handleLogin = async () => {
    if (!username || !password) {
      setError('Please fill in both username and password fields.');
      return;
    }

    try {
      const response = await fetch('api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const userR = await response.json();
        setUser(userR)
        console.log('Logged in as:', userR.username);
        navigate('/')

      } else {
        setError('Login failed');
      }
    } catch (error) {
      setError('Error: ' + error.message);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form>
        <div>
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => {
              setUsername(e.target.value)
              // console.log(username)
            }}
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="button" onClick={handleLogin}>
          Login
        </button>
        <button type="button" onClick={()=>navigate('/signup')}>
          Sign Up
        </button>
      </form>
    </div>
  );
};

export default LogIn


