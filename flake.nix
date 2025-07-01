{
  description = "Python development setup with Nix";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
  flake-utils.lib.eachDefaultSystem (
    system:
    let
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.default = pkgs.mkShell {
        packages = with pkgs; [
          python313
          python313Packages.numpy
          python313Packages.pymupdf
          python313Packages.pytesseract
          python313Packages.pytest
          python313Packages.python-dotenv
          python313Packages.requests 
          tesseract
        ];
      };
      devShells.mini = pkgs.mkShell {
        packages = with pkgs; [
          python313
          python313Packages.python-dotenv
          python313Packages.requests 
        ];
      };
    }
  );
}

