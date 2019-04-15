{
  pkgsSrc ? <nixpkgs>,
  pkgs ? import pkgsSrc {}
}:

with pkgs;

stdenv.mkDerivation {
  name = "inv-dev-env";
  buildInputs = [
    gnumake
    python3
    python3Packages.poetry
  ];
}
