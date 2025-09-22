import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import ExpenseList from './ExpenseList';

ChartJS.register(ArcElement, Tooltip, Legend);

const Dashboard = () => {
  const [expenses, setExpenses] = useState([]);
  const [chartData, setChartData] = useState({});

  useEffect(() => {
    axios.get('http://localhost:8000/expenses/')  // CORS: Add middleware in FastAPI for prod
      .then(res => {
        setExpenses(res.data);
        // Aggregate for pie chart
        const categories = {};
        res.data.forEach(exp => {
          categories[exp.category] = (categories[exp.category] || 0) + exp.amount;
        });
        setChartData({
          labels: Object.keys(categories),
          datasets: [{ data: Object.values(categories), backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'] }]
        });
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h2>Spending by Category</h2>
      <Pie data={chartData} />
      <ExpenseList expenses={expenses} />
    </div>
  );
};

export default Dashboard;