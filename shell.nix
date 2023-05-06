{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    nativeBuildInputs = with pkgs; [
      python310Packages.feedparser
      python310Packages.configparser
      python310Packages.beautifulsoup4
      python310Packages.requests
      python310Packages.pydub
      python310Packages.flask
      python310Packages.gunicorn
      sqlite
    ];
}
