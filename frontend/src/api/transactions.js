const BASE_URL = "http://localhost:8000";

export async function fetchTransactions(filters = {}) {
  const params = new URLSearchParams();
  if (filters.type) params.append("type", filters.type);
  if (filters.category) params.append("category", filters.category);
  if (filters.start_date) params.append("start_date", filters.start_date);
  if (filters.end_date) params.append("end_date", filters.end_date);

  const res = await fetch(`${BASE_URL}/transactions/?${params}`);
  if (!res.ok) throw new Error("Failed to fetch transactions");
  return res.json();
}

export async function fetchCategories() {
  const res = await fetch(`${BASE_URL}/transactions/categories`);
  if (!res.ok) throw new Error("Failed to fetch categories");
  return res.json();
}

export async function createTransaction(data) {
  const res = await fetch(`${BASE_URL}/transactions/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create transaction");
  return res.json();
}
