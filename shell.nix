{ pkgs ? import <nixpkgs> {} }:
let
my-python-packages = ps: with ps; [( 
    buildPythonPackage rec {
      pname = "pyopml";
      version = "1.0.0";
      src = fetchPypi{
        inherit pname version;
        sha256 = "sha256-8wQmC7Cd23iCDzc/TPfWdTux7JBTQ+Gc6oY2o8LvUok=";
      };
      doCheck = false;
      propogatedBuildInputs = with pkgs.python310Packages; [
        lxml
      ];
    }
)];
my-python = pkgs.python3.withPackages my-python-packages;
in
  pkgs.mkShell {
    buildInputs = [
      my-lxml
      my-python
    ];

    nativeBuildInputs = with pkgs; [
      python310Packages.feedparser
      python310Packages.beautifulsoup4
      python310Packages.requests
      python310Packages.flask
      python310Packages.gunicorn
      python310Packages.schedule
      python310Packages.gevent
      sqlite
    ];
}
