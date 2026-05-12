import { useEffect, useState } from "react";
import { fetchTransactions } from "../api/transactions";
import TransactionFilters from "./TransactionFilters";

const EMPTY_FILTERS = { type: "", category: "", start_date: "", end_date: "" };

function formatDate(iso) {
  return new Date(iso + "T00:00:00").toLocaleDateString();
}

function formatAmount(type, amount) {
  const sign = type === "income" ? "+" : "-";
  return `${sign}€${amount.toFixed(2)}`;
}

export default function TransactionList() {
  const [transactions, setTransactions] = useState([]);
  const [filters, setFilters] = useState(EMPTY_FILTERS);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchTransactions(filters)
      .then(setTransactions)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [filters]);

  return (
    <div className="transaction-list">
      <TransactionFilters filters={filters} onChange={setFilters} />

      {loading && <p className="state-msg">Loading…</p>}
      {error && <p className="state-msg error">{error}</p>}

      {!loading && !error && (
        <>
          <p className="count">{transactions.length} transaction{transactions.length !== 1 ? "s" : ""}</p>
          {transactions.length === 0 ? (
            <p className="state-msg">No transactions found.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Type</th>
                  <th>Category</th>
                  <th>Description</th>
                  <th className="right">Amount</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((t) => (
                  <tr key={t.id} className={t.type}>
                    <td>{formatDate(t.date)}</td>
                    <td><span className={`badge ${t.type}`}>{t.type}</span></td>
                    <td>{t.category}</td>
                    <td className="desc">{t.description ?? "—"}</td>
                    <td className={`right amount ${t.type}`}>{formatAmount(t.type, t.amount)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}
    </div>
  );
}
