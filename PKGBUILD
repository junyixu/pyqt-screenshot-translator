# Maintainer: Junyi Xu <junyixu0@gmail.com>
pkgname=pyqt-screenshot-translator
pkgver=1.0.0
pkgrel=1
pkgdesc="Screenshot translator with CLI and PyQt6 GUI using Gemini API"
arch=('any')
url="https://github.com/junyixu/pyqt-screenshot-translator"
license=('MIT')
depends=(
    'python'
    'python-pip'
    'python-openai'
    'python-pyqt6'
    'python-pyqt6-webengine'
    'python-markdown'
    'spectacle'
    'kdialog'
)
makedepends=('git')
install=pyqt-screenshot-translator.install
source=("git+https://github.com/junyixu/pyqt-screenshot-translator.git#branch=python-package-structure")
sha256sums=('SKIP')

pkgver() {
    cd "${srcdir}/pyqt-screenshot-translator"
    printf "1.0.0.r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

prepare() {
    cd "${srcdir}/pyqt-screenshot-translator"
}

build() {
    cd "${srcdir}/pyqt-screenshot-translator"
    # No compilation needed for Python package
}

package() {
    cd "${srcdir}/pyqt-screenshot-translator"
    
    # Install Python package
    python -m pip install --no-deps --target="$pkgdir/usr/lib/python3.11/site-packages" .
    
    # Create wrapper scripts
    install -Dm755 <(cat << 'EOF'
#!/bin/bash
cd "/usr/lib/python3.11/site-packages/screenshot_translator"
python3 -m screenshot_translator.cli "$@"
EOF
    ) "$pkgdir/usr/bin/pyqt-screenshot-translator-cli"
    
    install -Dm755 <(cat << 'EOF'
#!/bin/bash
cd "/usr/lib/python3.11/site-packages/screenshot_translator"
python3 -m screenshot_translator.gui "$@"
EOF
    ) "$pkgdir/usr/bin/pyqt-screenshot-translator-gui"
    
    # Install desktop file for GUI version only
    install -Dm644 <(cat << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Screenshot Translator
Comment=Screenshot translator with graphical user interface
Exec=pyqt-screenshot-translator-gui
Icon=pyqt-screenshot-translator
Terminal=false
Categories=Utility;Translation;Qt;
EOF
    ) "$pkgdir/usr/share/applications/pyqt-screenshot-translator.desktop"
    
    # Install documentation
    install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
    install -Dm644 requirements.txt "$pkgdir/usr/share/doc/$pkgname/requirements.txt"
    install -Dm644 requirements_pyqt.txt "$pkgdir/usr/share/doc/$pkgname/requirements_pyqt.txt"
    
    # Install license
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE" 2>/dev/null || true
}