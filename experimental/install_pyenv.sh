# PYENV_INSTALLER='https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer'
# PYTHON_VERSION='3.8'

# if [[ ! -d ~/.pyenv ]]; then
#     curl -L "${PYENV_INSTALLER}" -o ~/pyenv-installer.sh
#     chmod +x ~/pyenv-installer.sh
#     ~/pyenv-installer.sh
#     rm ~/.pyenv-installer.sh
# fi
# export PATH="${HOME}/.pyenv/bin:${PATH}"
# function pyenv() {
#     "${HOME}/.pyenv/bin/pyenv" "$@"
# }
# eval "$(pyenv init --path)"
# eval "$(pyenv init -)"
# eval "$(pyenv virtualenv-init -)"
# if [[ ! -d ~/.pyenv/versions/"${PYTHON_VERSION}" ]]; then
#     # export LDFLAGS="-L/opt/homebrew/lib"
#     # export CPPFLAGS="-I/opt/homebrew/include"
#     pyenv install "${PYTHON_VERSION}"
# fi
# if [[ ! -d ~/.pyenv/versions/"${CONFIG}" ]]; then
#     pyenv virtualenv "${PYTHON_VERSION}" "${CONFIG}"
# fi
