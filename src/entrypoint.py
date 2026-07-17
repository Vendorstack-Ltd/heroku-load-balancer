"""
Provide implementation of the command line interface.
"""
import click

from src.heroku import (
    GetHerokuPipelineProductionApplicationsUrls,
    HerokuApi,
)
from src.nginx import CreationNginxLoadBalancerConfigFile


@click.group()
def cli():
    """
    Command line interface root function.
    """
    pass


@click.command()
@click.option(
    '--nginx-port',
    type=int,
    required=True,
    help='The port to the Nginx on.',
)
@click.option(
    '--heroku-api-key',
    type=str,
    required=False,
    default='',
    help='The account\'s Heroku API key. No longer required; kept for backwards compatibility.',
)
@click.option(
    '--pipeline-identifier',
    type=str,
    required=False,
    default='',
    help='Pipeline identifier to fetch applications for balancing. No longer required; kept for backwards compatibility.',
)
def create_load_balancer(nginx_port, heroku_api_key, pipeline_identifier):
    """
    Create the Nginx load balancer config file.

    The backend is now a fixed upstream configured directly in the Nginx template
    (see src/nginx.py), so the Heroku pipeline lookup is no longer needed. We still
    attempt it for backwards compatibility, but any failure is silenced so the
    Nginx config is always written and the server can start.
    """
    pipeline_production_applications_urls = []

    if heroku_api_key and pipeline_identifier:
        try:
            heroku_api = HerokuApi(
                key=heroku_api_key,
            )

            get_heroku_pipeline_production_applications_urls = GetHerokuPipelineProductionApplicationsUrls(
                heroku_api=heroku_api,
            )

            pipeline_production_applications_urls = get_heroku_pipeline_production_applications_urls.by_pipeline_identifier(
                identifier=pipeline_identifier,
            )
        except Exception as error:  # noqa: BLE001 - never let the Heroku lookup block Nginx setup
            click.echo(f'Skipping Heroku pipeline lookup (not needed anymore): {error}')
            pipeline_production_applications_urls = []

    CreationNginxLoadBalancerConfigFile(port=nginx_port).with_urls(urls=pipeline_production_applications_urls)


if __name__ == '__main__':
    cli.add_command(create_load_balancer)
    cli()
