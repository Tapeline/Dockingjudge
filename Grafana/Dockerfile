FROM grafana/grafana-enterprise

ADD provisioning /etc/grafana/provisioning
ADD dashboards /var/lib/grafana/dashboards
ADD grafana.ini /etc/grafana/grafana.ini

CMD [ "grafana-reporter" ]
