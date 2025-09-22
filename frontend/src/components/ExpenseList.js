import React from 'react';
import Table from 'react-bootstrap/Table';

const ExpenseList = ({ expenses }) => (
  <Table striped bordered hover>
    <thead>
      <tr>
        <th>Date</th>
        <th>Vendor</th>
        <th>Category</th>
        <th>Amount</th>
        <th>Status</th>
        <th>Flagged</th>
      </tr>
    </thead>
    <tbody>
      {expenses.map(exp => (
        <tr key={exp.id}>
          <td>{exp.date}</td>
          <td>{exp.vendor}</td>
          <td>{exp.category}</td>
          <td>${exp.amount}</td>
          <td>{exp.status}</td>
          <td>{exp.flagged ? 'Yes' : 'No'}</td>
        </tr>
      ))}
    </tbody>
  </Table>
);

export default ExpenseList;