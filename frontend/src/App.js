import React from 'react';
import Dashboard from './components/Dashboard';
import PolicyEditor from './components/PolicyEditor';

function App() {
  return (
    <div className="App">
      <h1>Expense Intellect</h1>
      <Dashboard />
      <PolicyEditor />
    </div>
  );
}

export default App;