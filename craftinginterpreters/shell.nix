{ pkgs ? import <nixpkgs> {} }:
  let
    pkgs = import (builtins.fetchTarball {
        url = "https://github.com/NixOS/nixpkgs/archive/582ab1728b9bcd9f32362c845da1df2a1e228ba7.tar.gz";
    }) {};
  in 
  pkgs.mkShell {
    nativeBuildInputs = with pkgs.buildPackages; [ dart ];
}