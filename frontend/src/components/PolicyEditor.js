import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PolicyEditor = () => {
  const [policies, setPolicies] = useState([]);
  const [newPolicy, setNewPolicy] = useState({ name: '', rules: [] });
  const [newRule, setNewRule] = useState({ type: 'amount_max', value: 0 });

  useEffect(() => {
    axios.get('http://localhost:8000/expenses/policies/')
      .then(res => setPolicies(res.data))
      .catch(err => console.error(err));
  }, []);

  const addRule = () => {
    setNewPolicy({ ...newPolicy, rules: [...newPolicy.rules, newRule] });
    setNewRule({ type: 'amount_max', value: 0 });
  };

  const createPolicy = () => {
    axios.post('http://localhost:8000/expenses/policies/', newPolicy)
      .then(res => setPolicies([...policies, res.data]))
      .catch(err => console.error(err));
  };

  return (
    <div>
      <h2>Policy Manager (No-Code Builder)</h2>
      <input
        type="text"
        placeholder="Policy Name"
        value={newPolicy.name}
        onChange={e => setNewPolicy({ ...newPolicy, name: e.target.value })}
      />
      <select value={newRule.type} onChange={e => setNewRule({ ...newRule, type: e.target.value })}>
        <option value="amount_max">Max Amount</option>
        {/* Add more types */}
      </select>
      <input
        type="number"
        placeholder="Value"
        value={newRule.value}
        onChange={e => setNewRule({ ...newRule, value: parseFloat(e.target.value) })}
      />
      <button onClick={addRule}>Add Rule</button>
      <button onClick={createPolicy}>Create Policy</button>
      <ul>
        {policies.map(p => (
          <li key={p.id}>{p.name}: {JSON.stringify(p.rules)}</li>
        ))}
      </ul>
    </div>
  );
};

export default PolicyEditor;