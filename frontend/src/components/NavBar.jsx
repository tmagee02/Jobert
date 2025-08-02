function NavBar() {
  return (
    <header id="nav-bar" className="bg-red-500 px-10">
      <div
        id="nav-content"
        className="w-full flex justify-between items-center"
      >
        <div id="nav-brand">Caria</div>
        <div id="nav-links" className="flex">
          <div>Jobs</div>
          <div>Bookmarked</div>
          <div>About</div>
        </div>
        <div id="nav-user">
          <div>Login</div>
          <div>Sign Up</div>
        </div>
      </div>
    </header>
  );
}

export default NavBar;
