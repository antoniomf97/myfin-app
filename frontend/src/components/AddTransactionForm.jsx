import { useEffect, useState } from "react";
import { fetchCategories, createTransaction } from "../api/transactions";

const today = () => new Date().toISOString().slice(0, 10);

const INITIAL = {
  type: "expense",
  category: "",
  newCategory: "",
  description: "",
  amount: "",
  date: today(),
};

export default function AddTransactionForm({ onSuccess, onCancel }) {
  const [formData, setFormData] = useState(INITIAL);
  const [categories, setCategories] = useState([]);
  const [loadingCats, setLoadingCats] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoadingCats(true);
    setFormData((prev) => ({ ...prev, category: "", newCategory: "" }));
    fetchCategories(formData.type)
      .then(setCategories)
      .catch(() => setCategories([]))
      .finally(() => setLoadingCats(false));
  }, [formData.type]);

  function handle(e) {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();

    const resolvedCategory =
      formData.category === "__new__"
        ? formData.newCategory.trim()
        : formData.category;

    if (!resolvedCategory) {
      setError("Please enter a category name.");
      return;
    }
    if (!formData.amount || parseFloat(formData.amount) <= 0) {
      setError("Amount must be greater than 0.");
      return;
    }

    setSubmitting(true);
    setError(null);
    try {
      await createTransaction({
        type: formData.type,
        category: resolvedCategory,
        description: formData.description.trim() || null,
        amount: parseFloat(formData.amount),
        date: formData.date,
      });
      onSuccess();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="add-transaction-form" onSubmit={handleSubmit}>
      {error && <p className="state-msg error">{error}</p>}

      <div className="form-field">
        <label>Type</label>
        <select name="type" value={formData.type} onChange={handle}>
          <option value="income">Income</option>
          <option value="expense">Expense</option>
          <option value="savings">Savings</option>
        </select>
      </div>

      <div className="form-field">
        <label>Category</label>
        <select
          name="category"
          value={formData.category}
          onChange={handle}
          disabled={loadingCats}
          required
        >
          <option value="" disabled>
            {loadingCats ? "Loading…" : "Select category…"}
          </option>
          {categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
          <option value="__new__">Add new…</option>
        </select>
        {formData.category === "__new__" && (
          <input
            type="text"
            name="newCategory"
            placeholder="New category name"
            value={formData.newCategory}
            onChange={handle}
            autoFocus
          />
        )}
      </div>

      <div className="form-field">
        <label>
          Description <span className="optional">(optional)</span>
        </label>
        <input
          type="text"
          name="description"
          value={formData.description}
          onChange={handle}
        />
      </div>

      <div className="form-field">
        <label>Amount</label>
        <input
          type="number"
          name="amount"
          min="0.01"
          step="0.01"
          value={formData.amount}
          onChange={handle}
          required
        />
      </div>

      <div className="form-field">
        <label>Date</label>
        <input
          type="date"
          name="date"
          value={formData.date}
          onChange={handle}
          required
        />
      </div>

      <div className="form-actions">
        <button
          type="button"
          className="btn-cancel"
          onClick={onCancel}
          disabled={submitting}
        >
          Cancel
        </button>
        <button type="submit" className="btn-submit" disabled={submitting}>
          {submitting ? "Saving…" : "Add Transaction"}
        </button>
      </div>
    </form>
  );
}
