import React from 'react'
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SignUp() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate()
  
    const handleInputChange = (event) => {
      const { name, value } = event.target;
  
      if (name === 'username') {
        setUsername(value);
      } else if (name === 'password') {
        setPassword(value);
      }
    };
  
    const handleSignup = () => {
      // form validation
      if (!username || !password) {
        alert('Please enter a username and password.');
        return;
      }
      console.log(JSON.stringify({ username, password }));
      // POST request for a new user account
      fetch('/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      })
        .then((response) => response.json())
        .then((data) => {
        //   if (data.ok) {
        //     // Handle a successful signup, redirect to the login page
        //     navigate('/login');
        //   } else {
        //     // Handle a signup error
        //     alert(data.message);
        //   }
        navigate('/login')
        })
        .catch((error) => {
          console.error('Error:', error);
          // Handle network or other errors
          alert('An error occurred. Please try again.');
        });
    };
  
    return (
      <div id="signup">
        <h2 id="signup-title">Sign Up</h2>
        <form>
          <div>
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              name="username"
              value={username}
              onChange={handleInputChange}
            />
          </div>
          <div>
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              name="password"
              value={password}
              onChange={handleInputChange}
            />
          </div>
          <div>
            <button type="button" onClick={handleSignup}>
              Sign Up
            </button>
          </div>
        </form>
      </div>
    );
  }

export default SignUp