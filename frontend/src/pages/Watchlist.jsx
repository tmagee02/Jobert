import { useEffect } from "react";

export default function Watchlist() {
  useEffect(() => {
    document.title = "Watchlist";
  }, []);
  return <h1>Watchlist</h1>;
}
