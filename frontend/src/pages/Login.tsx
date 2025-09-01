import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useForm } from '@inertiajs/react';

interface FormData {
  username: string;
  password: string;
}


console.log('Form data before submit:')
export default function Loggin(props) {
    const error = props.error
  const { data, setData, post, processing, errors } = useForm<FormData>({
    username: '',
    password: '',
  })

  const formData = new FormData();
    formData.append('username', data.username);
    formData.append('password', data.password);

  const handleSubmit  = (e: React.FormEvent) => {
    e.preventDefault()
    post('/login/', {
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onError: (errors) => {
        console.error('Form submission errors:', errors);
      },
    });
  }

  return (
    <div>
        <Header />
        <main>
    <div className="container-md mt-3">
    <h1>Login</h1>
    {error && (
        <ul class="errorlist">
            <li>{error}</li></ul>
        )}
    <form onSubmit={handleSubmit}>
      <label htmlFor="username">Login:</label>
      <input id="username" name="username" value={data.username} onChange={(e) => setData('username', e.target.value)} /><br />
      <label htmlFor="last_name">Password:</label>
      <input id="last_name" name="password" value={data.password} type="password" onChange={(e) => setData('password', e.target.value)}/><br />
      <button type="submit">login</button>
    </form>
    </div>
    </main>
        <Footer />
    </div>
  )
}
