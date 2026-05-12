import TransactionList from "./components/TransactionList";
import "./App.css";

export default function App() {
  return (
    <div className="app">
      <header>
        <h1>MyFin</h1>
        <p>Personal Finance Tracker</p>
      </header>
      <main>
        <TransactionList />
      </main>
    </div>
  );
}
