# You need to copy the content of this file to your shell rc file (e.g. `~/.bashrc` `~/.zshrc`)

# Alias for TUIFIManager with cd functionality on exit (Ctrl+E)
alias tuifi='function _tuifi(){
  # Run tuifi
  tuifi

  # Check if path exists in this virtual file system (stored in RAM) and cd...
  if [ -e /dev/shm/tuifi_last_path.txt ]; then
    cd "$(</dev/shm/tuifi_last_path.txt)"
    # Comment the line below (and the if-statement) if you want to always cd regardless of ctrl+e
    rm /dev/shm/tuifi_last_path.txt
  fi
}; _tuifi'
