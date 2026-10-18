import { useState } from "react";
import { countries } from "../data/countries";

export default function CountrySelect({ value, onChange }) {
  const [search, setSearch] = useState("");
  const matches = countries.filter(({ name }) => name.toLowerCase().includes(search.trim().toLowerCase()));
  return (
    <div className="signup-country-picker">
      <label className="field" htmlFor="signup-country-search">
        <span>Country</span>
        <input id="signup-country-search" type="search" placeholder="Search countries…"
          autoComplete="off" value={search} aria-controls="signup-country"
          onChange={(event) => { setSearch(event.target.value); onChange(""); }} />
      </label>
      <select id="signup-country" className="signup-country-list" aria-label="Select your country"
        required value={value} onChange={(event) => onChange(event.target.value)}>
        <option value="" disabled>{matches.length ? "Select your country" : "No countries found"}</option>
        {matches.map(({ code, name }) => <option key={code} value={code}>{name}</option>)}
      </select>
      <small role="status">{value ? `Selected: ${countries.find((country) => country.code === value)?.name}` : `${matches.length} countries and territories · A–Z`}</small>
    </div>
  );
}
