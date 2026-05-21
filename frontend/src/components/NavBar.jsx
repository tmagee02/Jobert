import { Link } from "react-router-dom";

export default function NavBar() {
    return (
        <header
            id="nav-bar"
            className="bg-red-500/100 h-12 sticky top-0 z-50 backdrop-blur-xs"
        >
            <div
                id="nav-content"
                className="bg-orange-300/100 h-full flex justify-between items-center w-250 mx-auto gap-8"
            >
                <div id="nav-brand" className="bg-purple-500">
                    <Link to="/">Caria</Link>
                </div>
                <div
                    id="nav-links"
                    className="bg-blue-300 w-100 flex justify-between"
                >
                    <div className="text-pink-500">
                        <Link to="/jobs">Jobs</Link>
                    </div>
                    <div className="text-pink-500">
                        <Link to="/watchlist">Watchlist</Link>
                    </div>
                    <div className="">
                        <Link to="/about">About</Link>
                    </div>
                </div>
                <div
                    id="nav-user"
                    className="bg-pink-700 w-40 flex justify-between"
                >
                    <div>Login</div>
                    <div>Sign Up</div>
                </div>
            </div>
        </header>
    );
}
