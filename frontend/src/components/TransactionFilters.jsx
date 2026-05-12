export default function TransactionFilters({ filters, onChange }) {
  function handle(e) {
    onChange({ ...filters, [e.target.name]: e.target.value });
  }

  function reset() {
    onChange({ type: "", category: "", start_date: "", end_date: "" });
  }

  return (
    <div className="filters">
      <select name="type" value={filters.type} onChange={handle}>
        <option value="">All types</option>
        <option value="income">Income</option>
        <option value="expense">Expense</option>
      </select>

      <input
        name="category"
        placeholder="Category"
        value={filters.category}
        onChange={handle}
      />

      <input
        type="date"
        name="start_date"
        value={filters.start_date}
        onChange={handle}
      />

      <input
        type="date"
        name="end_date"
        value={filters.end_date}
        onChange={handle}
      />

      <button onClick={reset}>Clear</button>
    </div>
  );
}
