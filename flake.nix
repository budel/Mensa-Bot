{
  description = "Construct development shell from requirements.txt";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, pyproject-nix, flake-utils, ... }:
  flake-utils.lib.eachDefaultSystem (system:
  let
    project = pyproject-nix.lib.project.loadRequirementsTxt { projectRoot = ./.; };
    pkgs = nixpkgs.legacyPackages.${system};
    python = pkgs.python3;
    pythonEnv = pkgs.python3.withPackages (project.renderers.withPackages { inherit python; });
  in {
    devShells.default = pkgs.mkShell {
      packages = [ pythonEnv pkgs.tesseract];
    };
  });
}

