FROM ubuntu:22.04
LABEL maintainer="Ivan Praulov praulov2@gmail.com"
WORKDIR /deposit_calculator
COPY deposit_calculator.py deposit_calculator.py
COPY deposit_calculator_app.py deposit_calculator_app.py
# COPY deposit_calculator_service.service /etc/systemd/system/deposit_calculator_service.service
COPY setup.sh setup.sh
RUN apt update
# RUN apt install -y systemctl
RUN apt install -y python3-flask python3-waitress python3-dateutil
EXPOSE 9999
CMD ["/bin/bash", "setup.sh"]