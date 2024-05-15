#systemctl daemon-reload
#systemctl enable deposit_calculator_service.service
#systemctl start deposit_calculator_service.service
waitress-serve --host 0.0.0.0 --port 9999 deposit_calculator_app:app


