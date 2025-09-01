import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { useForm } from '@inertiajs/react';

interface FormData {
    name: string,
}

console.log('Form data before submit:')
export default function Create(props) {
    const error = props.error
  const { data, setData, post, processing, errors } = useForm<FormData>({
    name: '',
  })

  const formData = new FormData();
    formData.append('name', data.name);

  const handleSubmit  = (e: React.FormEvent) => {
    e.preventDefault()
    post('/statuses/create/', {
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  return (
    <div>
        <Header />
        <main>
    <div className="container-md mt-3">
    <h1>Status</h1>
    {error && (
        <ul class="errorlist">
            <li>{error}</li></ul>
        )}
    <form onSubmit={handleSubmit}>
      <label htmlFor="name">Name:</label>
      <input id="name" name="name" value={data.name} onChange={(e) => setData('name', e.target.value)} /><br />
      <button type="submit">Create</button>
    </form>
    </div>
    </main>
        <Footer />
    </div>
  )
}
