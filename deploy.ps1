#deploy generator
Write-Host "Deploying generator..."
Invoke-Expression -Command "pipenv run pyinstaller .\src\generator\generator_main.py --noconfirm --name ACR_QR_Generator --add-data 'LICENSE;.' --add-data 'assets/generator.ico;assets' --noconsole --icon assets/generator.ico"

#deploy scanner
Write-Host "Deploying scanner..."
Invoke-Expression -Command "pipenv run pyinstaller .\src\scanner\scanner_main.py --noconfirm --name ACR_QR_Scanner --add-data 'LICENSE;.' --add-data 'assets/scanner.ico;assets' --noconsole --icon assets/scanner.ico"
