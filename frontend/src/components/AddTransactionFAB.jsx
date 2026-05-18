import { useEffect, useRef, useState } from "react";
import AddTransactionForm from "./AddTransactionForm";

export default function AddTransactionFAB({ onSuccess }) {
  const [open, setOpen] = useState(false);
  const containerRef = useRef(null);

  useEffect(() => {
    if (!open) return;
    function handleClickOutside(e) {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  return (
    <div className="fab-container" ref={containerRef}>
      {open && (
        <div className="fab-popover">
          <AddTransactionForm
            onSuccess={() => {
              setOpen(false);
              onSuccess();
            }}
            onCancel={() => setOpen(false)}
          />
        </div>
      )}
      <button
        className={`fab-button${open ? " fab-button--active" : ""}`}
        onClick={() => setOpen((prev) => !prev)}
        aria-label="Add transaction"
        aria-expanded={open}
      >
        {open ? "×" : "+"}
      </button>
    </div>
  );
}
