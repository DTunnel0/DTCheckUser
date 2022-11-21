url='https://github.com/DTunnel0/DTCheckUser.git'
checkuser='https://github.com/DTunnel0/DTCheckUser/raw/master/executable/checkuser'
depends=('git' 'python3' 'python3-pip' 'python3-setuptools' 'python3-dev')

cd ~

function install_dependencies() {
    for depend in ${depends[@]}; do
        if ! which $depend &>/dev/null; then
            echo "Installing $depend..."
            sudo apt install $depend -y
        fi
    done
}

function compile_checkuser() {
    if [[ -d DTCheckUser ]]; then
        rm -rf DTCheckUser
    fi

    echo "Compilando checkuser"
    git clone $url
    cd DTCheckUser
    sudo python3 setup.py install
    cd ..
    rm -rf DTCheckUser
}

function install_binary() {
    if ! command -v checkuser &>/dev/null; then
        echo "Instalando binario checkuser"
        sudo wget $checkuser -O /usr/bin/checkuser
        sudo chmod +x /usr/bin/checkuser
    fi
}

function start_checkuser() {
    read -p 'Porta: ' -e -i 5000 port
    checkuser --port $port --start --daemon

    addr=$(curl -s icanhazip.com)

    echo 'URL: http://'$addr':'$port''
    echo 'WS: ws://'$addr':'$port''
    read
}

function initialize_process_install() {
    local mode=$1

    if [[ $mode == 'binary' ]]; then
        install_binary
    elif [[ $mode == 'compile' ]]; then
        install_dependencies
        compile_checkuser
    else
        echo "Modo de instalacao invalido"
        exit 1
    fi

    if command -v checkuser &>/dev/null; then
        echo "checkuser instalado com sucesso"
        start_checkuser
    else
        echo "Falha ao instalar checkuser"
        exit 1
    fi
}

function uninstall_checkuser() {
    echo 'Desinstalando CheckUser...'
    checkuser --stop
    python3 -m pip uninstall checkuser -y &>/dev/null
    rm -rf $(which checkuser)
    echo 'CheckUser desinstalado com sucesso.'
    read
}

function reinstall_checkuser() {
    uninstall_checkuser
    install_checkuser
}

function console_menu() {
    clear
    echo 'CHECKUSER MENU'
    echo '[01] - INSTALAR CHECKUSER (BINARIO)'
    echo '[02] - INSTALAR CHECKUSER (COMPILAR)'
    echo '[03] - DESINSTALAR CHECKUSER'
    echo '[00] - Sair'

    read -p 'Escolha uma opção: ' option

    case $option in
    01 | 1)
        initialize_process_install 'binary'
        console_menu
        ;;
    02 | 2)
        initialize_process_install 'compile'
        console_menu
        ;;
    03 | 3)
        uninstall_checkuser
        console_menu
        ;;
    00 | 0)
        echo 'Saindo...'
        exit 0
        ;;
    *)
        echo 'Opção inválida.'
        read -p 'Pressione enter para continuar...'
        console_menu
        ;;
    esac

}

function main() {
    case $1 in
    install | -i)
        initialize_process_install $2
        ;;
    uninstall)
        uninstall_checkuser
        ;;
    *)
        echo 'Usage: ./install.sh [install|uninstall] [binary|compile]'
        exit 1
        ;;
    esac
}

if [[ $# -eq 0 ]]; then
    console_menu
else
    main $1
fi
