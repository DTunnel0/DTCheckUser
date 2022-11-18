url='https://github.com/DTunnel0/DTCheckUser'
checkuser='https://github.com/DTunnel0/DTCheckUser/raw/master/executable/checkuser'

cd ~

function install_checkuser() {
    if [ -x "$(command -v checkuser)" ]; then
        echo 'CheckUser ja esta instalado.'
        read
        return
    fi

    echo 'Instalando CheckUser...'
    wget $checkuser -O checkuser
    chmod +x checkuser
    sudo mv checkuser /usr/bin/checkuser

    clear
    read -p 'Porta: ' -e -i 5000 port
    checkuser --port $port --start --daemon

    echo 'CheckUser instalado com sucesso.'
    echo 'Execute: checkuser --help'
    echo 'URL: http://'$(curl -s icanhazip.com)':'$port
    read
}

function uninstall_checkuser() {
    echo 'Desinstalando CheckUser...'
    checkuser --stop
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
    echo '[01] - Instalar CheckUser'
    echo '[02] - Desinstalar CheckUser'
    echo '[03] - Reinstalar CheckUser'
    echo '[00] - Sair'

    read -p 'Escolha uma opção: ' option

    case $option in
    01 | 1)
        install_checkuser
        console_menu
        ;;
    02 | 2)
        uninstall_checkuser
        console_menu
        ;;
    03 | 3)
        reinstall_checkuser
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
    install)
        install_checkuser
        ;;
    uninstall)
        uninstall_checkuser
        ;;
    reinstall)
        reinstall_checkuser
        ;;
    *)
        echo 'Usage: ./install.sh [install|uninstall|reinstall]'
        exit 1
        ;;
    esac
}

if [[ $# -eq 0 ]]; then
    console_menu
else
    main $1
fi
