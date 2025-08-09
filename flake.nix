{
  description = "Python development setup with Nix";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    rust-overlay = {
      url = "github:oxalica/rust-overlay";
      inputs = {
        nixpkgs.follows = "nixpkgs";
      };
    };
  };

  outputs = { nixpkgs, flake-utils, rust-overlay, ... }:
  flake-utils.lib.eachDefaultSystem (
    system:
    let
      overlays = [ (import rust-overlay) ];
      pkgs = import nixpkgs { inherit system overlays; };
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
      devShells.mensa-api = pkgs.mkShell {
        buildInputs = with pkgs; [
          rust-bin.stable.latest.default
          gdb
        ];
      };
    }
  );
}

