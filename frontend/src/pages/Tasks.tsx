import React from 'react';
import { Link } from '@inertiajs/react';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function Index( props ) {
    const tasks = props.tasks;
  return (
    
      <div>
        <Header />
        <main>
            <div class="container-md mt-3">
                <h1>Tasks</h1>
                <a href="/tasks/create/" class="btn btn-primary">Create task</a>
                <div class="container-md bg-body-tertiary mt-3 mb-3 border rounded-3">
                    <div class="p-3">
                        <form action="" method="get">
                            {/* форма поиска */}
                        </form>
                    </div>
                </div>
                <table class="table table-striped mt-2" data-test="checks">
                    <thead>
                        <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Status</th>
                        <th>Autor</th>
                        <th>Executor</th>
                        <th>Create date</th>
                        <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {tasks && tasks.map(task => (
                        <tr>
                            <td>{ task.id }</td>
                            <td><Link href={`/tasks/${task.id}/`}>{ task.name }</Link></td>
                            <td>{ task.status }</td>
                            <td>{ task.author }</td>
                            <td>{ task.executor }</td>
                            <td>{ task.created_at}</td>
                            <td>
                                <Link href={`/tasks/${task.id}/update/`}>Edit</Link><br />
                                <Link href={`/tasks/${task.id}/delete/`}>Delete</Link>
                            </td>
                        </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            </main>
        <Footer />
      </div>
  );
}
