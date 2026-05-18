import { useState } from "react";
import TransactionList from "./components/TransactionList";
import AddTransactionFAB from "./components/AddTransactionFAB";
import "./App.css";

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="app">
      <header>
        <h1>MyFin</h1>
        <p>Personal Finance Tracker</p>
      </header>
      <main>
        <TransactionList refreshKey={refreshKey} />
      </main>
      <AddTransactionFAB onSuccess={() => setRefreshKey((k) => k + 1)} />
    </div>
  );
}
