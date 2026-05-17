import { useState, useRef, useEffect } from "react";

/**
 * SearchBox — filterable dropdown input.
 *
 * Props:
 *   items        – full array of items
 *   value        – currently selected item (object or null)
 *   onChange     – (item) => void
 *   placeholder  – input placeholder
 *   getLabel     – (item) => string   (display text)
 *   filterFn     – (item, query) => bool  (optional custom filter)
 *   maxResults   – cap visible items (default 8)
 */
export default function SearchBox({
  items = [],
  value = null,
  onChange,
  placeholder = "Search…",
  getLabel = (item) => item?.name ?? String(item),
  filterFn,
  maxResults = 8,
}) {
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const wrapperRef = useRef(null);

  // Close on outside click
  useEffect(() => {
    function handleClick(e) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const defaultFilter = (item, q) =>
    getLabel(item).toLowerCase().includes(q.toLowerCase());

  const filtered = (query.trim() === "" ? items : items.filter((item) =>
    (filterFn || defaultFilter)(item, query)
  )).slice(0, maxResults);

  function handleSelect(item) {
    onChange(item);
    setQuery(getLabel(item));
    setOpen(false);
  }

  function handleInputChange(e) {
    setQuery(e.target.value);
    setOpen(true);
    if (e.target.value === "") onChange(null);
  }

  // Sync query text when value changes externally
  useEffect(() => {
    if (value) setQuery(getLabel(value));
    else setQuery("");
  }, [value]);

  return (
    <div className="searchbox" ref={wrapperRef}>
      <div className="input-wrapper">
        <input
          className="input searchbox__input"
          type="text"
          value={query}
          onChange={handleInputChange}
          onFocus={() => setOpen(true)}
          placeholder={placeholder}
          autoComplete="off"
        />
        <span className="input-icon searchbox__icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
        </span>
      </div>

      {open && filtered.length > 0 && (
        <ul className="searchbox__dropdown">
          {filtered.map((item, i) => (
            <li
              key={i}
              className={`searchbox__option ${
                value && getLabel(value) === getLabel(item) ? "searchbox__option--active" : ""
              }`}
              onMouseDown={() => handleSelect(item)}
            >
              {getLabel(item)}
            </li>
          ))}
        </ul>
      )}

      {open && query.trim() !== "" && filtered.length === 0 && (
        <div className="searchbox__dropdown searchbox__empty">
          No results found
        </div>
      )}
    </div>
  );
}
