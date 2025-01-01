{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "python-project-env";

  buildInputs = with pkgs; [
    python311
    python311Packages.pip
    gcc
    postgresql
    pylint
    ruff
    python311Packages.python-lsp-server
  ];

  shellHook = ''
    if [ ! -d ".venv" ]; then
      virtualenv .venv
    fi
    if [ -f ~/.profile ]; then
      source ~/.profile
    fi
    alias nv='poetry run nvim "$@"'

    export LD_LIBRARY_PATH=$(gcc -print-file-name=libstdc++.so.6 | xargs dirname):$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=$(pg_config --libdir):$LD_LIBRARY_PATH
 
    echo "LD_LIBRARY_PATH wurde gesetzt: $LD_LIBRARY_PATH"

    source .venv/bin/activate
    #pip install --no-cache-dir -r requirements.txt
    poetry install
    echo "Virtuelle Umgebung und Abhängigkeiten wurden eingerichtet!"
  '';
}

