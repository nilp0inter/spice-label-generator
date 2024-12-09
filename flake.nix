{
  description = "A simple Nix flake providing a Python dev environment and run command for the Spice Label Generator";

  inputs.nixpkgs.url = "nixpkgs";

  outputs = { nixpkgs, ... }:
    let
      # Choose your system. Adjust if needed.
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python3;
      pythonDeps = python.withPackages (ps: [
        ps.pillow
        ps.svgwrite
      ]);
    in {
      # A development shell with Python and dependencies
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          pythonDeps
          pkgs.inkscape
          pkgs.imagemagick
        ];
      };

      # Define an app that runs the script directly
      apps.default = {
        type = "app";
        # `program` should be a full path, so we use `python` from our env
        # and pass the script path.
        # Since `nix run` sets $PWD to the source directory, we can
        # directly call label_generator.py.
        program = "${pythonDeps}/bin/python";
        args = [ "./label_generator.py" ];
      };
    };
}
