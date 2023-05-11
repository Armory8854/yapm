{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    nativeBuildInputs = with pkgs; [
      python310Packages.feedparser
      python310Packages.beautifulsoup4
      python310Packages.requests
      python310Packages.flask
      python310Packages.gunicorn
      python310Packages.schedule
      sqlite
    ];
}
