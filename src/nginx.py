from src.constants import NGINX_LOAD_BALANCER_CONFIG_TEMPLATE


class CreationNginxLoadBalancerConfigFile:
    """
    Implements creation of Nginx load balancer config file transaction.
    """

    def __init__(self, port):
        """
        Constructor.
        """
        self.port = port

    @staticmethod
    def get_host_from_url(url):
        """
        Remove protocol and last slash from the URL.
        """
        return url.replace("https://", "").rstrip("/")

    def with_urls(self, urls=None):
        """
        Create an Nginx configuration that proxies all traffic to
        https://api.getvent.io.
        """

        upstream_server_localhosts_text = "\t\tserver 127.0.0.1:8000;\n"

        upstream_server_configs_text = """
\tserver <
\t\tlisten 8000;

\t\tlocation / <
\t\t\tproxy_pass https://api.getvent.io;

\t\t\tproxy_http_version 1.1;

\t\t\tproxy_ssl_server_name on;
\t\t\tproxy_ssl_name api.getvent.io;

\t\t\tproxy_set_header Host api.getvent.io;
\t\t\tproxy_set_header X-Real-IP $remote_addr;
\t\t\tproxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
\t\t\tproxy_set_header X-Forwarded-Proto $scheme;
\t\t\tproxy_set_header X-Forwarded-Host $host;
\t\t\tproxy_set_header X-Forwarded-Port $server_port;

\t\t\tproxy_set_header Upgrade $http_upgrade;
\t\t\tproxy_set_header Connection "upgrade";

\t\t\tproxy_buffering off;
\t\t>
\t>
"""

        nginx_load_balancer_config_file_ready_to_use = (
            NGINX_LOAD_BALANCER_CONFIG_TEMPLATE.format(
                port=self.port,
                upstream_server_localhosts=upstream_server_localhosts_text,
                upstream_server_configs=upstream_server_configs_text,
            )
        )

        nginx_load_balancer_config_file_ready_to_use = (
            nginx_load_balancer_config_file_ready_to_use
            .replace("<", "{")
            .replace(">", "}")
        )

        with open("nginx.conf", "w") as nginx_config:
            nginx_config.write(nginx_load_balancer_config_file_ready_to_use)