{
  description = "Shell for running dev tools";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    inputs@{
      self,
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (system: {
      devShells.default =
        let
          pkgs = import nixpkgs {
            inherit system;
          };
        in
        with pkgs;
        mkShell {
          buildInputs = [
            nix-output-monitor
            nixfmt-rfc-style
            zola
            python3
            python3Packages.requests
            python3Packages.python-slugify
          ];
        };
    });
}
